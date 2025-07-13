import asyncio
import asyncssh
import json
from datetime import datetime

class SSHClient:
    def __init__(self):
        self.connection = None
        self.process = None
        self.websocket = None
        self._output_task = None
        
    async def connect(self, host, username, password=None, key_path=None, port=22):
        # Clean up any existing connection first
        await self.disconnect()
        
        try:
            print(f"Attempting SSH connection to {username}@{host}:{port}")
            
            # Add connection timeout and retry logic
            connect_timeout = 10
            if key_path:
                self.connection = await asyncio.wait_for(
                    asyncssh.connect(
                        host, port=port, username=username, 
                        client_keys=[key_path], known_hosts=None,
                        connect_timeout=connect_timeout
                    ), timeout=15
                )
            else:
                self.connection = await asyncio.wait_for(
                    asyncssh.connect(
                        host, port=port, username=username, 
                        password=password, known_hosts=None,
                        connect_timeout=connect_timeout
                    ), timeout=15
                )
            
            print("SSH connection established, creating process...")
            # Start interactive shell with proper terminal
            self.process = await self.connection.create_process(term_type='xterm-256color')
            print("SSH process created successfully")
            await self.send_output(f"Connected to {username}@{host}:{port}")
            return True
        except asyncio.TimeoutError:
            error_msg = f"SSH Connection timeout to {host}:{port}"
            print(error_msg)
            await self.send_output(error_msg, "error")
            return False
        except Exception as e:
            error_msg = f"SSH Connection failed: {str(e)}"
            print(error_msg)
            await self.send_output(error_msg, "error")
            return False
    
    async def send_command(self, command):
        if not self.process:
            await self.send_output("Not connected to SSH", "error")
            return
            
        try:
            print(f"Executing command: {command}")
            
            # Send raw data directly to SSH process
            if isinstance(command, str) and len(command) == 1:
                # Single character - send as-is (for xterm.js raw input)
                self.process.stdin.write(command)
            else:
                # Multi-character command - send with newline
                self.process.stdin.write(command)
            
            # Start continuous output reading if not already running
            if not hasattr(self, '_output_task') or self._output_task is None or self._output_task.done():
                self._output_task = asyncio.create_task(self._read_output_continuously())
                
        except Exception as e:
            error_msg = f"Command execution failed: {str(e)}"
            print(error_msg)
            await self.send_output(error_msg, "error")
    
    async def _read_output_continuously(self):
        """Continuously read and forward terminal output"""
        if not self.process:
            return
            
        try:
            while True:
                # Read raw terminal data
                data = await self.process.stdout.read(1024)
                if not data:
                    break
                    
                # Send raw data to xterm.js (it handles ANSI codes)
                await self.send_output(data)
                
        except Exception as e:
            print(f"Output reading stopped: {e}")
                
        except Exception as e:
            error_msg = f"Command execution failed: {str(e)}"
            print(error_msg)
            await self.send_output(error_msg, "error")
    
    async def send_interrupt(self):
        """Send Ctrl+C interrupt signal"""
        if self.process:
            try:
                self.process.stdin.write('\x03')
                await self.send_output("^C", "interrupt")
            except Exception as e:
                await self.send_output(f"Failed to send interrupt: {str(e)}", "error")
    
    async def send_output(self, output, output_type="output"):
        if self.websocket and output:
            response = {
                "type": "cli_output",
                "timestamp": datetime.now().isoformat(),
                "payload": {
                    "output": output,
                    "output_type": output_type
                }
            }
            await self.websocket.send_text(json.dumps(response))
    
    def set_websocket(self, ws):
        self.websocket = ws
    
    async def disconnect(self):
        try:
            if self.process:
                print("Closing SSH process...")
                self.process.terminate()
                await asyncio.sleep(0.5)
                if self.process.returncode is None:
                    self.process.kill()
            if self.connection:
                print("Closing SSH connection...")
                self.connection.close()
                await self.connection.wait_closed()
        except Exception as e:
            print(f"Error during disconnect: {e}")
        finally:
            self.connection = None
            self.process = None
            print("SSH client disconnected")
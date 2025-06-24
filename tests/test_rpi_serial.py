import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'rpi', 'src'))

from pico_serial_interface import PicoSerialInterface

class TestPicoSerialInterface(unittest.TestCase):
    
    @patch('serial.Serial')
    def setUp(self, mock_serial):
        self.mock_serial = mock_serial
        self.interface = PicoSerialInterface(baudrate=115200)
    
    def test_initialization(self):
        self.assertEqual(self.interface.baudrate, 115200)
        self.assertIsNone(self.interface.serial_connection)
    
    @patch('serial.tools.list_ports.comports')
    def test_find_pico_port(self, mock_comports):
        # Mock a Pico device
        mock_port = Mock()
        mock_port.device = 'COM3'
        mock_port.description = 'USB Serial Device'
        mock_port.vid = 0x2E8A  # Raspberry Pi vendor ID
        mock_comports.return_value = [mock_port]
        
        port = self.interface._find_pico_port()
        self.assertEqual(port, 'COM3')
    
    @patch('serial.tools.list_ports.comports')
    def test_find_pico_port_not_found(self, mock_comports):
        mock_comports.return_value = []
        port = self.interface._find_pico_port()
        self.assertIsNone(port)
    
    def test_parse_pico_message_valid_json(self):
        test_message = 'INFO: { "type": "system_status", "status": "ready" }'
        result = self.interface._parse_pico_message(test_message)
        expected = {
            'identifier': 'INFO',
            'type': 'system_status',
            'status': 'ready'
        }
        self.assertEqual(result, expected)
    
    def test_parse_pico_message_invalid_format(self):
        test_message = 'Invalid message format'
        result = self.interface._parse_pico_message(test_message)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
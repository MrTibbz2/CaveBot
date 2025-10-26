from core import cavemap, cavesense, primedrive
import time


def maze():
    print("Maze started.")
    



def check_status():
    cavemap_ok = bool(cavemap.client.clients)
    cavesense_ok = cavesense.cavesense is not None
    primedrive_ok = primedrive.prime is not None and primedrive.prime.hub.connected
    
    print("\n=== System Status ===")
    print(f"CaveMap:    {'✓ Connected' if cavemap_ok else '✗ Disconnected'}")
    print(f"CaveSense:  {'✓ Ready' if cavesense_ok else '✗ Not Ready'}")
    print(f"PrimeDrive: {'✓ Ready' if primedrive_ok else '✗ Not Ready'}")
    print("=====================\n")
    
    return cavemap_ok and cavesense_ok and primedrive_ok


def wait_for_ready():
    while not check_status():
        print("Waiting for all systems to be ready...")
        time.sleep(1)
    print("All systems ready.\n")


def cli():
    while True:
        cmd = input("CaveCore> ").strip().lower()
        
        if cmd == "run":
            wait_for_ready()
            print("Starting maze...")
            maze()
            print("Maze complete.\n")
        elif cmd == "status":
            check_status()
        elif cmd == "exit":
            print("Shutting down...")
            break
        else:
            print("Commands: run, status, exit")


def main():
    print("CAVECORE INITIALISING.")
    cavemap.init()
    cavesense.init(cavemap)
    primedrive.init()
    
    print("\nWaiting for initial connections...")
    time.sleep(1)
    
    cli()

if __name__ == "__main__":
    main()



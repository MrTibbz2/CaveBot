# Copyright (c) 2025 Archie Bradby
# All rights reserved.

from primeCommands import Prime

def main():
    hub_name = "NSE_Pybricks"  # Change to your hub's name if needed
    prime = Prime(hub_name)

    print("SPIKE Prime Command Line Control")
    print("Commands:")
    print("  forward <duration_ms>")
    print("  backward <duration_ms>")
    print("  left")
    print("  right")
    print("  stop")
    print("  party")
    print("  turnto <angle>")
    print("  quit")
    print("Example: forward 1000\n")

    while True:
        try:
            cmd = input("Enter command: ").strip().lower()
            if not cmd:
                continue
            if cmd == "quit":
                print("Exiting.")
                break

            parts = cmd.split()
            match parts:
                case ["forward", duration]:
                    prime.moveForward(duration)
                case ["backward", duration]:
                    prime.moveBackwards(duration)
                case ["left"]:
                    prime.turnLeft()
                case ["right"]:
                    prime.turnRight()
                case ["stop"]:
                    prime.stop()
                case ["party"]:
                    prime.partyTime()
                case ["turnto", angle]:
                    prime.turnTo(angle)
                case _:
                    print("Unknown or malformed command.")
        except KeyboardInterrupt:
            print("\nExiting.")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
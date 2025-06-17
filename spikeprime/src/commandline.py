from primeCommands import Prime

def main():
    hub_name = "NSE_Pybricks"  # Change to your hub's name
    prime = Prime(hub_name)

    print("SPIKE Prime Command Line Control")
    print("Commands:")
    print("  forward <distance_cm>")
    print("  backward <distance_cm>")
    print("  left <angle_deg> <factor>")
    print("  right <angle_deg> <factor>")
    print("  stop <speed> <duration>")
    print("  party")
    print("  quit")
    print("Example: forward 30")
    print("")

    while True:
        try:
            cmd = input("Enter command: ").strip().lower()
            if not cmd:
                continue
            if cmd == "quit":
                print("Exiting.")
                break

            parts = cmd.split()
            if parts[0] == "forward" and len(parts) == 2:
                prime.moveForward(parts[1])
            elif parts[0] == "backward" and len(parts) == 2:
                prime.moveBackwards(parts[1])
            elif parts[0] == "left" and len(parts) == 3:
                prime.turnLeft(parts[1], parts[2])
            elif parts[0] == "right" and len(parts) == 3:
                prime.turnRight(parts[1], parts[2])
            elif parts[0] == "stop" and len(parts) == 3:
                prime.stop(parts[1], parts[2])
            elif parts[0] == "party":
                prime.partyTime()
            else:
                print("Unknown or malformed command.")
        except KeyboardInterrupt:
            print("\nExiting.")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
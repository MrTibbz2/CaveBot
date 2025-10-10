from core import cavemap, cavesense, primedrive


def main():
    print("CAVECORE INITIALISING.")
    cavesense.init()
    primedrive.init()
    cavemap.init()

if __name__ == "__main__":
    main()



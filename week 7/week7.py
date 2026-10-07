"""
Name search program.

Loads names from names.txt, then repeatedly prompts the user for a name.
- If the name is in the file, a message is displayed.
- If the name is not in the file, it is written to nofound.txt and a
  message is displayed.

Enter a blank line (or 'quit') to stop.
"""

INPUT_FILE = "names.txt"
OUTPUT_FILE = "nofound.txt"


def load_names(filename):
    """Read the names file and return a list of names (one per line)."""
    try:
        with open(filename, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: could not find '{filename}'. "
              "Make sure it is in the same folder as this script.")
        return None


def main():
    names = load_names(INPUT_FILE)
    if names is None:
        return

    print(f"Loaded {len(names)} names from {INPUT_FILE}.")

    # Case-insensitive lookup
    lookup = {name.lower() for name in names}

    # Opened once in write mode so each run starts with a fresh nofound.txt
    with open(OUTPUT_FILE, "w") as out:
        while True:
            name = input("\nEnter a name to search for (blank to quit): ").strip()

            if name == "" or name.lower() == "quit":
                print("Goodbye!")
                break

            if name.lower() in lookup:
                print(f"{name} was found in the file.")
            else:
                out.write(name + "\n")
                out.flush()
                print(f"{name} was NOT found. It has been written to {OUTPUT_FILE}.")


if __name__ == "__main__":
    main()
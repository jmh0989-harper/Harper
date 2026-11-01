"""
Regular Expression Assignment
-----------------------------
Menu-driven program. Each problem's solution lives in its own if/elif block.
For every problem you can either:
  * type your own text, or
  * just press Enter to run the assignment's built-in test strings.
"""

import re


def get_inputs(prompt, samples):
    """Ask the user for a string. Blank input -> return the assignment's test strings."""
    user_text = input(f"{prompt}\n(Press Enter to use the assignment's test strings) > ")
    if user_text == "":
        return samples
    return [user_text]


def main():
    while True:
        print("\n" + "=" * 60)
        print("REGULAR EXPRESSION ASSIGNMENT")
        print("=" * 60)
        print(" 1. Only a-z, A-Z, 0-9 characters")
        print(" 2. 'a' followed by zero or more 'b's")
        print(" 3. 'a' followed by one or more 'b's")
        print(" 4. Lowercase letters joined by an underscore")
        print(" 5. Match a word at the beginning of a string")
        print(" 6. Match a word containing 'z'")
        print(" 7. Remove leading zeros from an IP address")
        print(" 8. Search for literal strings within a string")
        print(" 9. Literal string search + location")
        print("10. Swap whitespace and underscores")
        print("11. Extract year, month, date from a URL")
        print("12. Find all words starting with 'a' or 'e'")
        print("13. Replace space, comma, or dot with a colon")
        print("14. Find all words starting with 'a' or 'e' (repeat problem)")
        print("15. Remove multiple spaces from a string")
        print(" 0. Quit")

        choice = input("\nChoose a problem number: ").strip()

        # ------------------------------------------------------------------
        # Problem 1
        # ------------------------------------------------------------------
        if choice == "1":
            print("\n--- Problem 1: Only a-z, A-Z and 0-9 ---")
            tests = ["ABCDEFabcdef123450", "*&%@#!}{"]
            for text in get_inputs("Enter a string to check:", tests):
                if re.fullmatch(r"[a-zA-Z0-9]+", text):
                    print(f"'{text}' -> Accepted (only letters and digits)")
                else:
                    print(f"'{text}' -> Not accepted (contains other characters)")

        # ------------------------------------------------------------------
        # Problem 2
        # ------------------------------------------------------------------
        elif choice == "2":
            print("\n--- Problem 2: 'a' followed by zero or more 'b's ---")
            tests = ["ab", "abc", "a", "ab", "abb"]
            for text in get_inputs("Enter a string to check:", tests):
                if re.search(r"ab*", text):
                    print(f"'{text}' -> Match found")
                else:
                    print(f"'{text}' -> Not matched")

        # ------------------------------------------------------------------
        # Problem 3
        # ------------------------------------------------------------------
        elif choice == "3":
            print("\n--- Problem 3: 'a' followed by one or more 'b's ---")
            tests = ["ab", "abc", "a", "ab", "abb"]
            for text in get_inputs("Enter a string to check:", tests):
                if re.search(r"ab+", text):
                    print(f"'{text}' -> Match found")
                else:
                    print(f"'{text}' -> Not matched")

        # ------------------------------------------------------------------
        # Problem 4
        # ------------------------------------------------------------------
        elif choice == "4":
            print("\n--- Problem 4: Lowercase letters joined by an underscore ---")
            tests = ["aab_cbbbc", "aab_Abbbc", "Aaab_abbbc"]
            for text in get_inputs("Enter a string to check:", tests):
                if re.search(r"^[a-z]+_[a-z]+$", text):
                    print(f"'{text}' -> Found a match")
                else:
                    print(f"'{text}' -> Not matched")

        # ------------------------------------------------------------------
        # Problem 5
        # ------------------------------------------------------------------
        elif choice == "5":
            print("\n--- Problem 5: Match a word at the beginning of a string ---")
            tests = [
                "The quick brown fox jumps over the lazy dog.",
                " The quick brown fox jumps over the lazy dog.",
            ]
            for text in get_inputs("Enter a string to check:", tests):
                match = re.match(r"\w+", text)
                if match:
                    print(f"'{text}' -> Found a word at the beginning: '{match.group()}'")
                else:
                    print(f"'{text}' -> No word at the beginning")

        # ------------------------------------------------------------------
        # Problem 6
        # ------------------------------------------------------------------
        elif choice == "6":
            print("\n--- Problem 6: Match a word containing 'z' ---")
            tests = [
                "The quick brown fox jumps over the lazy dog.",
                "Python Exercises.",
            ]
            for text in get_inputs("Enter a string to check:", tests):
                matches = re.findall(r"\b\w*z\w*\b", text)
                if matches:
                    print(f"'{text}' -> Found word(s) containing 'z': {matches}")
                else:
                    print(f"'{text}' -> No word containing 'z'")

        # ------------------------------------------------------------------
        # Problem 7
        # ------------------------------------------------------------------
        elif choice == "7":
            print("\n--- Problem 7: Remove leading zeros from an IP address ---")
            tests = ["216.08.094.196"]
            for text in get_inputs("Enter an IP address:", tests):
                result = re.sub(r"\b0+(\d)", r"\1", text)
                print(f"Original: {text}")
                print(f"Cleaned:  {result}")

        # ------------------------------------------------------------------
        # Problem 8
        # ------------------------------------------------------------------
        elif choice == "8":
            print("\n--- Problem 8: Search for literal strings within a string ---")
            default_text = "The quick brown fox jumps over the lazy dog."
            default_words = ["fox", "dog", "horse"]

            text = input(f"Enter the text to search in\n(Press Enter for '{default_text}') > ")
            if text == "":
                text = default_text

            words_in = input(
                f"Enter words to search for, separated by commas\n(Press Enter for {default_words}) > "
            )
            if words_in.strip() == "":
                words = default_words
            else:
                words = [w.strip() for w in words_in.split(",") if w.strip()]

            print(f"\nSearching in: '{text}'")
            for word in words:
                if re.search(re.escape(word), text):
                    print(f"'{word}' -> Found!")
                else:
                    print(f"'{word}' -> Not found!")

        # ------------------------------------------------------------------
        # Problem 9
        # ------------------------------------------------------------------
        elif choice == "9":
            print("\n--- Problem 9: Literal string search with location ---")
            default_text = "The quick brown fox jumps over the lazy dog."
            default_word = "fox"

            text = input(f"Enter the text to search in\n(Press Enter for '{default_text}') > ")
            if text == "":
                text = default_text

            word = input(f"Enter the word to search for\n(Press Enter for '{default_word}') > ")
            if word == "":
                word = default_word

            match = re.search(re.escape(word), text)
            if match:
                print(
                    f"Found '{word}' in the original string "
                    f"from index {match.start()} to {match.end()}"
                )
            else:
                print(f"'{word}' was not found in the string.")

        # ------------------------------------------------------------------
        # Problem 10
        # ------------------------------------------------------------------
        elif choice == "10":
            print("\n--- Problem 10: Swap whitespace and underscores ---")
            tests = ["Regular Expressions", "Code_Examples"]
            for text in get_inputs("Enter a string:", tests):
                result = re.sub(r"[ _]", lambda m: "_" if m.group() == " " else " ", text)
                print(f"'{text}' -> '{result}'")

        # ------------------------------------------------------------------
        # Problem 11
        # ------------------------------------------------------------------
        elif choice == "11":
            print("\n--- Problem 11: Extract year, month and date from a URL ---")
            tests = [
                "https://www.washingtonpost.com/news/football-insider/wp/2016/09/02/"
                "odell-beckhams-fame-rests-on-one-stupid-little-ball-josh-norman-tells-author/"
            ]
            for url in get_inputs("Enter a URL:", tests):
                found = re.findall(r"/(\d{4})/(\d{1,2})/(\d{1,2})/", url)
                if found:
                    year, month, day = found[0]
                    print(f"URL: {url}")
                    print(f"Year: {year}  Month: {month}  Date: {day}")
                else:
                    print(f"No year/month/date found in: {url}")

        # ------------------------------------------------------------------
        # Problem 12
        # ------------------------------------------------------------------
        elif choice == "12":
            print("\n--- Problem 12: Words starting with 'a' or 'e' ---")
            tests = [
                "The following example creates an ArrayList with a capacity of 50 elements. "
                "Four elements are then added to the ArrayList and the ArrayList is trimmed accordingly."
            ]
            for text in get_inputs("Enter a string:", tests):
                words = re.findall(r"\b[aeAE]\w*", text)
                print(f"Words starting with 'a' or 'e': {words}")

        # ------------------------------------------------------------------
        # Problem 13
        # ------------------------------------------------------------------
        elif choice == "13":
            print("\n--- Problem 13: Replace space, comma, or dot with a colon ---")
            tests = ["Python Exercises, PHP exercises."]
            for text in get_inputs("Enter a string:", tests):
                result = re.sub(r"[ ,.]", ":", text)
                print(f"Original: {text}")
                print(f"Result:   {result}")

        # ------------------------------------------------------------------
        # Problem 14 (same prompt as Problem 12 in the assignment)
        # ------------------------------------------------------------------
        elif choice == "14":
            print("\n--- Problem 14: Words starting with 'a' or 'e' (repeat problem) ---")
            tests = [
                "The following example creates an ArrayList with a capacity of 50 elements. "
                "Four elements are then added to the ArrayList and the ArrayList is trimmed accordingly."
            ]
            for text in get_inputs("Enter a string:", tests):
                # Different approach from #12: case-insensitive flag with finditer
                words = [m.group() for m in re.finditer(r"\b[ae]\w*", text, re.IGNORECASE)]
                print(f"Words starting with 'a' or 'e': {words}")

        # ------------------------------------------------------------------
        # Problem 15
        # ------------------------------------------------------------------
        elif choice == "15":
            print("\n--- Problem 15: Remove multiple spaces from a string ---")
            tests = ["Python      Exercises"]
            for text in get_inputs("Enter a string:", tests):
                result = re.sub(r" +", " ", text)
                print(f"Original: '{text}'")
                print(f"Result:   '{result}'")

        # ------------------------------------------------------------------
        # Quit / invalid
        # ------------------------------------------------------------------
        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number from 0 to 15.")


if __name__ == "__main__":
    main()
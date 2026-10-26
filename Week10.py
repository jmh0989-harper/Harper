"""
Regular Expression Assignment - all 15 questions.
Each question's solution lives inside its own if statement.
Run the file to execute every question, or pass question numbers, e.g.:
    python regex_assignment.py 3 7 11
"""
import re
import sys

# Pick which questions to run (default: all 15)
if len(sys.argv) > 1:
    to_run = [int(a) for a in sys.argv[1:]]
else:
    to_run = list(range(1, 16))

for q in to_run:

    # ------------------------------------------------------------------
    if q == 1:
        print("Question 1: only a-z, A-Z, 0-9")
        pattern = re.compile(r'^[a-zA-Z0-9]+$')
        for s in ["ABCDEFabcdef123450", "*&%@#!}{"]:
            print(f"  {s!r}: {'Accepted' if pattern.match(s) else 'Not accepted'}")

    # ------------------------------------------------------------------
    if q == 2:
        print("Question 2: an 'a' followed by zero or more b's")
        for s in ["ab", "abc", "a", "ab", "abb"]:
            print(f"  {s!r}: {'Found a match!' if re.search(r'ab*', s) else 'Not matched!'}")

    # ------------------------------------------------------------------
    if q == 3:
        print("Question 3: an 'a' followed by one or more b's")
        for s in ["ab", "abc", "a", "ab", "abb"]:
            print(f"  {s!r}: {'Found a match!' if re.search(r'ab+', s) else 'Not matched!'}")

    # ------------------------------------------------------------------
    if q == 4:
        print("Question 4: lowercase letters joined by an underscore")
        for s in ["aab_cbbbc", "aab_Abbbc", "Aaab_abbbc"]:
            print(f"  {s!r}: {'Found a match!' if re.search(r'^[a-z]+_[a-z]+$', s) else 'Not matched!'}")

    # ------------------------------------------------------------------
    if q == 5:
        print("Question 5: a word at the beginning of a string")
        for s in ["The quick brown fox jumps over the lazy dog.",
                  " The quick brown fox jumps over the lazy dog."]:
            m = re.match(r'^\w+', s)
            print(f"  {s!r}: {'Found a match: ' + m.group() if m else 'Not matched!'}")

    # ------------------------------------------------------------------
    if q == 6:
        print("Question 6: a word containing 'z'")
        for s in ["The quick brown fox jumps over the lazy dog.", "Python Exercises."]:
            m = re.findall(r'\b\w*z\w*\b', s)
            print(f"  {s!r}: {('Found: ' + ', '.join(m)) if m else 'Not matched!'}")

    # ------------------------------------------------------------------
    if q == 7:
        print("Question 7: remove leading zeros from an IP address")
        ip = "216.08.094.196"
        result = re.sub(r'\b0+(?=\d)', '', ip)
        print(f"  Original: {ip}")
        print(f"  Cleaned : {result}")

    # ------------------------------------------------------------------
    if q == 8:
        print("Question 8: search for literal strings")
        text = 'The quick brown fox jumps over the lazy dog.'
        for word in ['fox', 'dog', 'horse']:
            print(f"  Searching for {word!r}: "
                  f"{'Matched!' if re.search(re.escape(word), text) else 'Not Matched!'}")

    # ------------------------------------------------------------------
    if q == 9:
        print("Question 9: literal string and its location")
        text = 'The quick brown fox jumps over the lazy dog.'
        m = re.search(re.escape('fox'), text)
        if m:
            print(f"  Found 'fox' at start={m.start()}, end={m.end()}")

    # ------------------------------------------------------------------
    if q == 10:
        print("Question 10: swap whitespace and underscore")
        for s in ["Regular Expressions", "Code_Examples"]:
            swapped = re.sub(r'[ _]', lambda m: '_' if m.group() == ' ' else ' ', s)
            print(f"  {s!r} -> {swapped!r}")

    # ------------------------------------------------------------------
    if q == 11:
        print("Question 11: year, month, day from a URL")
        url = ("https://www.washingtonpost.com/news/football-insider/wp/2016/09/02/"
               "odell-beckhams-fame-rests-on-one-stupid-little-ball-josh-norman-tells-author/")
        m = re.search(r'/(\d{4})/(\d{1,2})/(\d{1,2})/', url)
        if m:
            print(f"  Year: {m.group(1)}, Month: {m.group(2)}, Day: {m.group(3)}")

    # ------------------------------------------------------------------
    if q == 12:
        print("Question 12: words starting with 'a' or 'e'")
        text = ("The following example creates an ArrayList with a capacity of 50 "
                "elements. Four elements are then added to the ArrayList and the "
                "ArrayList is trimmed accordingly.")
        print(" ", re.findall(r'\b[aAeE]\w*', text))

    # ------------------------------------------------------------------
    if q == 13:
        print("Question 13: replace space, comma, or dot with a colon")
        text = 'Python Exercises, PHP exercises.'
        print(" ", re.sub(r'[ ,.]', ':', text))

    # ------------------------------------------------------------------
    if q == 14:
        # Same wording as Question 12 in the assignment.
        print("Question 14: words starting with 'a' or 'e'")
        text = ("The following example creates an ArrayList with a capacity of 50 "
                "elements. Four elements are then added to the ArrayList and the "
                "ArrayList is trimmed accordingly.")
        print(" ", re.findall(r'\b[aAeE]\w*', text))

    # ------------------------------------------------------------------
    if q == 15:
        print("Question 15: remove multiple spaces")
        text = 'Python      Exercises'
        print(" ", re.sub(r' +', ' ', text))

    print()
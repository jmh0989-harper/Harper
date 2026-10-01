#!/usr/bin/env python3
"""Run-length encoding (RLE) encoder/decoder with escape-sequence support.

This program asks the user for a string and either encodes it or decodes it:

* If the string begins with the marker ``##00`` it is treated as already
  RLE-encoded and is decoded.
* Otherwise the string is run-length encoded.

Encoded format
--------------
* A run of a single character is written as the character alone (no count).
  A run of two or more is written as the character followed by its count,
  e.g. ``AAABCC`` -> ``A3BC2``.
* ``#`` is the escape symbol. A digit that is part of the *data* is written
  as ``#`` followed by the digit, so it is not confused with a count.
  Example: ``5`` -> ``#5`` and ``555`` -> ``#53``.
* A literal ``#`` character is written as ``##``.
  Example: ``###`` -> ``##3``.
* Every encoded string begins with the marker ``##00`` so it can be
  recognised as already encoded.

Because digits and ``#`` can be escaped, any input string can be encoded.
For example ``AAA111#`` encodes to ``##00A3#13##``.

Documentation follows PEP 257 (docstring conventions) with Google-style
sections for arguments, return values and exceptions.

Author: (your name here)
"""

MARKER = "##00"
ESCAPE = "#"
DIGITS = "0123456789"


def is_encoded(text):
    """Determine whether a string is already in RLE format.

    A string is considered encoded if it begins with the ``##00`` marker.

    Args:
        text (str): The string to examine.

    Returns:
        bool: True if the string starts with the encoding marker,
            otherwise False.

    Raises:
        TypeError: If ``text`` is not a string.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return text.startswith(MARKER)


def encode_rle(text):
    """Encode a string using run-length encoding.

    Runs of a single character have no count. Digits and ``#`` characters
    in the data are escaped with ``#`` (a literal ``#`` becomes ``##``).
    The result always begins with the ``##00`` marker.

    Args:
        text (str): The string to encode. May contain any characters.

    Returns:
        str: The encoded string, e.g. ``"AAABCC"`` -> ``"##00A3BC2"``.

    Raises:
        TypeError: If ``text`` is not a string.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    pieces = [MARKER]
    i = 0
    while i < len(text):
        char = text[i]
        run = 1
        while i + run < len(text) and text[i + run] == char:
            run += 1

        if char == ESCAPE or char in DIGITS:
            pieces.append(ESCAPE + char)
        else:
            pieces.append(char)
        if run > 1:
            pieces.append(str(run))

        i += run
    return "".join(pieces)


def decode_rle(encoded):
    """Decode an RLE string produced by :func:`encode_rle`.

    Args:
        encoded (str): A string beginning with the ``##00`` marker.

    Returns:
        str: The original, decoded string.

    Raises:
        TypeError: If ``encoded`` is not a string.
        ValueError: If the marker is missing or the encoding is malformed
            (a count with no character, a dangling or invalid escape, or a
            count below 2 / with leading zeros).
    """
    if not isinstance(encoded, str):
        raise TypeError("encoded must be a string")
    if not is_encoded(encoded):
        raise ValueError("encoded string must begin with " + MARKER)

    body = encoded[len(MARKER):]
    result = []
    i = 0
    while i < len(body):
        char = body[i]

        if char == ESCAPE:
            if i + 1 >= len(body):
                raise ValueError("dangling escape symbol at end of string")
            char = body[i + 1]
            if char != ESCAPE and char not in DIGITS:
                raise ValueError(
                    "invalid escape sequence '#%s' at position %d"
                    % (char, len(MARKER) + i)
                )
            i += 2
        elif char in DIGITS:
            raise ValueError(
                "count with no character at position %d" % (len(MARKER) + i)
            )
        else:
            i += 1

        start = i
        while i < len(body) and body[i] in DIGITS:
            i += 1
        count_text = body[start:i]

        if count_text:
            if count_text[0] == "0":
                raise ValueError("counts may not have leading zeros")
            count = int(count_text)
            if count < 2:
                raise ValueError("counts must be 2 or greater")
        else:
            count = 1

        result.append(char * count)
    return "".join(result)


def process_string(text):
    """Encode or decode a string depending on its current format.

    Args:
        text (str): A non-empty string.

    Returns:
        tuple[str, str]: ``(action, result)`` where ``action`` is
            ``"decoded"`` or ``"encoded"``.

    Raises:
        TypeError: If ``text`` is not a string.
        ValueError: If ``text`` is empty, or is marked as encoded but is
            malformed.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if text == "":
        raise ValueError("input string must not be empty")

    if is_encoded(text):
        return "decoded", decode_rle(text)
    return "encoded", encode_rle(text)


def get_input():
    """Prompt the user for a non-empty string.

    Returns:
        str: The string entered by the user.
    """
    while True:
        text = input("Enter a string (or ##00... to decode): ")
        if text:
            return text
        print("Input must not be empty. Please try again.")


def main():
    """Run the program: read a string, then encode or decode it."""
    print("Run-Length Encoder / Decoder")
    try:
        action, result = process_string(get_input())
    except ValueError as error:
        print("Error: %s" % error)
        return
    print("Result (%s): %s" % (action, result))


if __name__ == "__main__":
    main()
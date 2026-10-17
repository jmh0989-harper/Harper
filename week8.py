#!/usr/bin/env python3
"""
Northwind Customer Lookup
=========================

A console interface for browsing and searching customer data stored in a
text file named "Northwind_Customers" (the ".txt" extension is optional).

Features
--------
1. Display company name, contact name, and phone for all customers,
   sorted by company name.
2. Display contact name, company name, and phone for all customers,
   sorted by contact name.
3. Search by company name (full or partial) and show labeled records.
4. Search by contact name (full or partial) and show labeled records.

Assumed file format
-------------------
* One customer per line, fields separated by a tab, comma, semicolon, or
  pipe (the delimiter is detected automatically).
* An optional header row. If a header row with the standard Northwind
  column names is present, columns are located by name. Otherwise the
  standard Northwind column order is assumed:

  CustomerID, CompanyName, ContactName, ContactTitle, Address, City,
  Region, PostalCode, Country, Phone, Fax

Only CompanyName, ContactName, and Phone are required.

Design notes
------------
* No global variables (apart from constants): data is passed to functions
  as parameters and results are returned.
* Sorting and searching are each implemented once and reused for both the
  company and contact versions.
"""

import csv
import os
import sys

# ---------------------------------------------------------------------------
# Constants (read-only configuration)
# ---------------------------------------------------------------------------
DEFAULT_FILENAME = "Northwind_Customers"

STANDARD_COLUMNS = [
    "CustomerID", "CompanyName", "ContactName", "ContactTitle", "Address",
    "City", "Region", "PostalCode", "Country", "Phone", "Fax",
]
REQUIRED_FIELDS = ("CompanyName", "ContactName", "Phone")
VALID_SORT_FIELDS = ("CompanyName", "ContactName")

FIELD_LABELS = {
    "CompanyName": "Company Name",
    "ContactName": "Contact Name",
    "Phone": "Phone",
}


# ---------------------------------------------------------------------------
# Data loading and validation
# ---------------------------------------------------------------------------
def normalize_column_name(name):
    """
    Normalize a column header so it can be matched to a standard name.

    Args:
        name (str): Raw header text, e.g. "Company Name" or "company_name".

    Returns:
        str: Lower-case text with spaces, underscores, and hyphens removed.

    Raises:
        TypeError: If name is not a string.
    """
    if not isinstance(name, str):
        raise TypeError("name must be a string.")
    return name.strip().lower().replace(" ", "").replace("_", "").replace("-", "")


def resolve_filename(filename):
    """
    Locate the data file, trying the name as given and then with ".txt".

    Args:
        filename (str): Base file name or path.

    Returns:
        str: Path to an existing file.

    Raises:
        TypeError: If filename is not a string.
        ValueError: If filename is empty.
        FileNotFoundError: If no matching file exists.
    """
    if not isinstance(filename, str):
        raise TypeError("filename must be a string.")
    if not filename.strip():
        raise ValueError("filename must not be empty.")

    for candidate in (filename, filename + ".txt"):
        if os.path.isfile(candidate):
            return candidate
    raise FileNotFoundError(
        f"Could not find '{filename}' or '{filename}.txt' in the current folder."
    )


def read_file_lines(path):
    """
    Read all non-blank lines from a text file.

    UTF-8 (with or without BOM) is tried first, then Latin-1 as a fallback.

    Args:
        path (str): Path to an existing text file.

    Returns:
        list[str]: Non-blank lines with line endings removed.

    Raises:
        TypeError: If path is not a string.
        OSError: If the file cannot be read.
    """
    if not isinstance(path, str):
        raise TypeError("path must be a string.")

    for encoding in ("utf-8-sig", "latin-1"):
        try:
            with open(path, "r", encoding=encoding, newline="") as handle:
                return [ln.rstrip("\r\n") for ln in handle if ln.strip()]
        except UnicodeDecodeError:
            continue
    return []  # pragma: no cover (latin-1 never fails to decode)


def detect_delimiter(lines):
    """
    Guess the field delimiter from a sample of lines.

    Args:
        lines (list[str]): Lines of the data file.

    Returns:
        str: One of tab, comma, semicolon, or pipe.

    Raises:
        TypeError: If lines is not a list.
        ValueError: If lines is empty.
    """
    if not isinstance(lines, list):
        raise TypeError("lines must be a list.")
    if not lines:
        raise ValueError("The data file is empty.")

    sample = "\n".join(lines[:20])
    try:
        return csv.Sniffer().sniff(sample, delimiters="\t,;|").delimiter
    except csv.Error:
        # Fall back to whichever candidate appears most in the first line.
        return max("\t,;|", key=lambda d: lines[0].count(d))


def build_column_map(first_row):
    """
    Decide which column holds each field.

    If the first row looks like a header (contains CompanyName and
    ContactName), columns are mapped by name; otherwise the standard
    Northwind order is assumed.

    Args:
        first_row (list[str]): Parsed first row of the file.

    Returns:
        tuple[dict, bool]: (mapping of field name -> column index,
        True if the first row was a header and should be skipped).

    Raises:
        TypeError: If first_row is not a list.
        ValueError: If a required column cannot be found.
    """
    if not isinstance(first_row, list):
        raise TypeError("first_row must be a list.")

    normalized = [normalize_column_name(cell) for cell in first_row]
    standard = {normalize_column_name(c): c for c in STANDARD_COLUMNS}

    is_header = "companyname" in normalized and "contactname" in normalized
    if is_header:
        mapping = {
            standard[name]: index
            for index, name in enumerate(normalized)
            if name in standard
        }
    else:
        mapping = {name: index for index, name in enumerate(STANDARD_COLUMNS)}

    missing = [f for f in REQUIRED_FIELDS if f not in mapping]
    if missing:
        raise ValueError("Missing required column(s): " + ", ".join(missing))
    return mapping, is_header


def parse_customers(lines):
    """
    Convert raw text lines into a list of customer records.

    Rows that are too short or lack a company name are skipped.

    Args:
        lines (list[str]): Raw lines from the data file.

    Returns:
        list[dict]: Records with keys CompanyName, ContactName, and Phone.

    Raises:
        TypeError: If lines is not a list.
        ValueError: If the file is empty or has no valid records.
    """
    if not isinstance(lines, list):
        raise TypeError("lines must be a list.")
    if not lines:
        raise ValueError("The data file is empty.")

    delimiter = detect_delimiter(lines)
    rows = list(csv.reader(lines, delimiter=delimiter))
    mapping, has_header = build_column_map(rows[0])

    customers = []
    for row in rows[1:] if has_header else rows:
        record = {}
        for field in REQUIRED_FIELDS:
            index = mapping[field]
            record[field] = row[index].strip() if index < len(row) else ""
        if record["CompanyName"]:
            customers.append(record)

    if not customers:
        raise ValueError("No valid customer records were found in the file.")
    return customers


def load_customers(filename=DEFAULT_FILENAME):
    """
    Load customer records from the data file.

    Args:
        filename (str): Base name or path of the data file.

    Returns:
        list[dict]: Customer records (CompanyName, ContactName, Phone).

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is empty or malformed.
        OSError: If the file cannot be read.
    """
    path = resolve_filename(filename)
    return parse_customers(read_file_lines(path))


# ---------------------------------------------------------------------------
# Sorting and searching (shared by company and contact features)
# ---------------------------------------------------------------------------
def validate_customers(customers):
    """
    Verify that customers is a list of record dictionaries.

    Args:
        customers (list[dict]): Customer records to check.

    Raises:
        TypeError: If customers is not a list of dictionaries.
    """
    if not isinstance(customers, list):
        raise TypeError("customers must be a list.")
    if not all(isinstance(record, dict) for record in customers):
        raise TypeError("Every customer record must be a dictionary.")


def validate_field(field):
    """
    Verify that field is a supported sort/search field.

    Args:
        field (str): Field name to check.

    Raises:
        ValueError: If field is not "CompanyName" or "ContactName".
    """
    if field not in VALID_SORT_FIELDS:
        raise ValueError(f"field must be one of {VALID_SORT_FIELDS}, got {field!r}.")


def sort_customers(customers, field):
    """
    Return customers sorted (case-insensitively) by the given field.

    Args:
        customers (list[dict]): Customer records.
        field (str): "CompanyName" or "ContactName".

    Returns:
        list[dict]: A new, sorted list. The original list is unchanged.

    Raises:
        TypeError: If customers is not a list of dictionaries.
        ValueError: If field is not a supported field.
    """
    validate_customers(customers)
    validate_field(field)
    return sorted(customers, key=lambda rec: rec.get(field, "").casefold())


def search_customers(customers, field, term):
    """
    Find records whose field contains the search text (case-insensitive).

    Args:
        customers (list[dict]): Customer records.
        field (str): "CompanyName" or "ContactName".
        term (str): Full or partial text to look for.

    Returns:
        list[dict]: Matching records, sorted by the searched field.

    Raises:
        TypeError: If customers is not a list of dictionaries, or term is
            not a string.
        ValueError: If field is unsupported or term is blank.
    """
    validate_customers(customers)
    validate_field(field)
    if not isinstance(term, str):
        raise TypeError("term must be a string.")
    term = term.strip().casefold()
    if not term:
        raise ValueError("Search text must not be blank.")

    matches = [rec for rec in customers if term in rec.get(field, "").casefold()]
    return sort_customers(matches, field)


# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------
def display_columns(customers, fields):
    """
    Print records as an aligned table with a header row.

    Args:
        customers (list[dict]): Records to show.
        fields (tuple[str]): Field names, in display order.

    Raises:
        TypeError: If customers is not a list of dictionaries.
        ValueError: If fields is empty or names an unknown field.
    """
    validate_customers(customers)
    if not fields or any(f not in FIELD_LABELS for f in fields):
        raise ValueError("fields must be a non-empty subset of the known fields.")

    headers = [FIELD_LABELS[f] for f in fields]
    widths = [
        max([len(h)] + [len(rec.get(f, "")) for rec in customers])
        for h, f in zip(headers, fields)
    ]
    line = "  ".join(h.ljust(w) for h, w in zip(headers, widths))
    print(line)
    print("  ".join("-" * w for w in widths))
    for rec in customers:
        print("  ".join(rec.get(f, "").ljust(w) for f, w in zip(fields, widths)))
    print(f"\n{len(customers)} record(s).")


def display_labeled(customers, fields):
    """
    Print each record with every field labeled, one field per line.

    Args:
        customers (list[dict]): Records to show.
        fields (tuple[str]): Field names, in display order.

    Raises:
        TypeError: If customers is not a list of dictionaries.
        ValueError: If fields is empty or names an unknown field.
    """
    validate_customers(customers)
    if not fields or any(f not in FIELD_LABELS for f in fields):
        raise ValueError("fields must be a non-empty subset of the known fields.")

    label_width = max(len(FIELD_LABELS[f]) for f in fields)
    for number, rec in enumerate(customers, start=1):
        print(f"Record {number}")
        for f in fields:
            print(f"  {FIELD_LABELS[f].ljust(label_width)} : {rec.get(f, '')}")
        print()
    print(f"{len(customers)} record(s) found.")


# ---------------------------------------------------------------------------
# Menu actions (one function per type of processing)
# ---------------------------------------------------------------------------
def show_sorted_by_company(customers):
    """
    Display company name, contact name, and phone sorted by company name.

    Args:
        customers (list[dict]): Customer records.
    """
    display_columns(
        sort_customers(customers, "CompanyName"),
        ("CompanyName", "ContactName", "Phone"),
    )


def show_sorted_by_contact(customers):
    """
    Display contact name, company name, and phone sorted by contact name.

    Args:
        customers (list[dict]): Customer records.
    """
    display_columns(
        sort_customers(customers, "ContactName"),
        ("ContactName", "CompanyName", "Phone"),
    )


def search_and_display(customers, field, prompt):
    """
    Prompt for search text, search the given field, and show labeled results.

    Args:
        customers (list[dict]): Customer records.
        field (str): "CompanyName" or "ContactName".
        prompt (str): Text shown when asking for the search term.
    """
    term = input(prompt).strip()
    if not term:
        print("Search text must not be blank.")
        return

    results = search_customers(customers, field, term)
    if not results:
        print(f"No records found matching '{term}'.")
        return

    if field == "CompanyName":
        order = ("CompanyName", "ContactName", "Phone")
    else:
        order = ("ContactName", "CompanyName", "Phone")
    print()
    display_labeled(results, order)


def search_by_company(customers):
    """
    Search for full or partial company names and display matches.

    Args:
        customers (list[dict]): Customer records.
    """
    search_and_display(customers, "CompanyName", "Enter company name (or part of it): ")


def search_by_contact(customers):
    """
    Search for full or partial contact names and display matches.

    Args:
        customers (list[dict]): Customer records.
    """
    search_and_display(customers, "ContactName", "Enter contact name (or part of it): ")


# ---------------------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------------------
def display_menu():
    """Print the main menu."""
    print("\n=== Northwind Customers ===")
    print("1. List customers sorted by company name")
    print("2. List customers sorted by contact name")
    print("3. Search by company name")
    print("4. Search by contact name")
    print("5. Exit")


def get_menu_choice(valid_choices):
    """
    Prompt until the user enters a valid menu choice.

    Args:
        valid_choices (tuple[str]): Acceptable inputs.

    Returns:
        str: The validated choice.

    Raises:
        ValueError: If valid_choices is empty.
    """
    if not valid_choices:
        raise ValueError("valid_choices must not be empty.")
    while True:
        choice = input("\nChoose an option: ").strip()
        if choice in valid_choices:
            return choice
        print(f"Invalid choice. Please enter one of: {', '.join(valid_choices)}.")


def run_menu(customers):
    """
    Run the interactive menu loop until the user exits.

    Args:
        customers (list[dict]): Customer records.
    """
    actions = {
        "1": show_sorted_by_company,
        "2": show_sorted_by_contact,
        "3": search_by_company,
        "4": search_by_contact,
    }
    while True:
        display_menu()
        choice = get_menu_choice(("1", "2", "3", "4", "5"))
        if choice == "5":
            print("Goodbye!")
            return
        print()
        actions[choice](customers)


def main(argv=None):
    """
    Program entry point: load the data file and start the menu.

    Args:
        argv (list[str] | None): Command-line arguments. An optional first
            argument overrides the data file name.

    Returns:
        int: Exit status (0 for success, 1 for an error).
    """
    argv = sys.argv[1:] if argv is None else argv
    filename = argv[0] if argv else DEFAULT_FILENAME

    try:
        customers = load_customers(filename)
    except (FileNotFoundError, ValueError, OSError) as error:
        print(f"Error: {error}")
        return 1

    print(f"Loaded {len(customers)} customers.")
    try:
        run_menu(customers)
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""Northwind table manager.

A console program that works with the Northwind SQLite database created
from ``database.sql``.  The program:

1. Lists every table in the database (names are kept in a list).
2. Lets the user pick a table and displays all of its records with column
   names and row numbers.
3. Lets the user (I)nsert, (U)pdate, or (D)elete records in that table.

If the database file does not exist yet, it is built automatically from the
SQL script.

Usage::

    python northwind_manager.py [--db northwind.db] [--sql database.sql]

Design notes:
    * No global variables are used.  Every function receives what it needs
      as parameters and returns its results.
    * Table and column names come only from the database's own catalog and
      are validated against it before being placed in an SQL statement.
      All user-entered *values* are passed as bound parameters.
"""

import argparse
import os
import sqlite3
import sys

# --------------------------------------------------------------------------
# Database setup
# --------------------------------------------------------------------------


def create_database(sql_path, db_path):
    """Build a new SQLite database file from an SQL script.

    Args:
        sql_path (str): Path to the SQL script (e.g. ``database.sql``).
        db_path (str): Path of the database file to create.

    Returns:
        bool: True if the database was created, False otherwise.

    Raises:
        TypeError: If either argument is not a string.
    """
    if not isinstance(sql_path, str) or not isinstance(db_path, str):
        raise TypeError("sql_path and db_path must be strings.")
    if not os.path.isfile(sql_path):
        print(f"Error: SQL script '{sql_path}' was not found.")
        return False
    try:
        with open(sql_path, "r", encoding="utf-8") as script_file:
            script = script_file.read()
        conn = sqlite3.connect(db_path)
        try:
            conn.executescript(script)
            conn.commit()
        finally:
            conn.close()
        return True
    except (OSError, sqlite3.Error) as err:
        print(f"Error: could not create the database: {err}")
        if os.path.exists(db_path):
            os.remove(db_path)  # do not leave a half-built database behind
        return False


def connect_database(db_path):
    """Open a connection to the database with foreign keys enforced.

    Args:
        db_path (str): Path to an existing SQLite database file.

    Returns:
        sqlite3.Connection | None: An open connection, or None on failure.
    """
    if not isinstance(db_path, str) or not os.path.isfile(db_path):
        print(f"Error: database file '{db_path}' does not exist.")
        return None
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    except sqlite3.Error as err:
        print(f"Error: could not open the database: {err}")
        return None


# --------------------------------------------------------------------------
# Metadata and reading
# --------------------------------------------------------------------------


def quote_identifier(name):
    """Quote an SQL identifier (table or column name) safely.

    Args:
        name (str): The identifier to quote.

    Returns:
        str: The identifier wrapped in double quotes.

    Raises:
        ValueError: If ``name`` is not a non-empty string.
    """
    if not isinstance(name, str) or not name:
        raise ValueError("Identifier must be a non-empty string.")
    return '"' + name.replace('"', '""') + '"'


def get_table_names(conn):
    """Return the names of all user tables in the database.

    Args:
        conn (sqlite3.Connection): An open database connection.

    Returns:
        list[str]: Table names sorted alphabetically.
    """
    cursor = conn.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type = 'table' AND name NOT LIKE 'sqlite_%' "
        "ORDER BY name"
    )
    table_names = []  # the list that stores the table names
    for (name,) in cursor.fetchall():
        table_names.append(name)
    return table_names


def get_columns(conn, table_name, table_names):
    """Return column metadata for a table.

    Args:
        conn (sqlite3.Connection): An open database connection.
        table_name (str): Table to describe.
        table_names (list[str]): Valid table names (used for validation).

    Returns:
        list[dict]: One dict per column with the keys ``name``, ``type``,
        ``not_null``, ``default``, and ``pk`` (position in primary key,
        0 if not part of it).

    Raises:
        ValueError: If ``table_name`` is not in ``table_names``.
    """
    if table_name not in table_names:
        raise ValueError(f"Unknown table: {table_name!r}")
    cursor = conn.execute(f"PRAGMA table_info({quote_identifier(table_name)})")
    columns = []
    for _cid, name, col_type, not_null, default, pk in cursor.fetchall():
        columns.append({
            "name": name,
            "type": (col_type or "").upper(),
            "not_null": bool(not_null),
            "default": default,
            "pk": pk,
        })
    return columns


def get_records(conn, table_name, table_names):
    """Fetch every record of a table together with its SQLite rowid.

    The rowid is used internally to identify a record for update/delete;
    it is not shown to the user.

    Args:
        conn (sqlite3.Connection): An open database connection.
        table_name (str): Table to read.
        table_names (list[str]): Valid table names (used for validation).

    Returns:
        list[tuple]: Each tuple is ``(rowid, value1, value2, ...)``.

    Raises:
        ValueError: If ``table_name`` is not in ``table_names``.
    """
    if table_name not in table_names:
        raise ValueError(f"Unknown table: {table_name!r}")
    cursor = conn.execute(f"SELECT rowid, * FROM {quote_identifier(table_name)}")
    return cursor.fetchall()


# --------------------------------------------------------------------------
# Display
# --------------------------------------------------------------------------


def display_records(table_name, columns, records, max_width=28):
    """Print records in an aligned table with column names and row numbers.

    Args:
        table_name (str): Name of the table (used in the heading).
        columns (list[dict]): Column metadata from :func:`get_columns`.
        records (list[tuple]): Records from :func:`get_records`
            (the first element of each tuple, the rowid, is not displayed).
        max_width (int): Longest cell text shown before it is shortened.

    Returns:
        None
    """
    headers = ["Row"] + [col["name"] for col in columns]
    rows = []
    for number, record in enumerate(records, start=1):
        cells = [str(number)]
        for value in record[1:]:
            text = "NULL" if value is None else str(value).replace("\n", " ")
            if len(text) > max_width:
                text = text[:max_width - 3] + "..."
            cells.append(text)
        rows.append(cells)

    widths = [len(h) for h in headers]
    for cells in rows:
        for i, cell in enumerate(cells):
            widths[i] = max(widths[i], len(cell))

    print(f"\n=== {table_name} ({len(records)} records) ===")
    print(" | ".join(h.ljust(widths[i]) for i, h in enumerate(headers)))
    print("-+-".join("-" * w for w in widths))
    for cells in rows:
        print(" | ".join(c.ljust(widths[i]) for i, c in enumerate(cells)))
    if not rows:
        print("(no records)")
    print()


def display_columns(columns):
    """Print a numbered list of a table's columns.

    Args:
        columns (list[dict]): Column metadata from :func:`get_columns`.

    Returns:
        None
    """
    for number, col in enumerate(columns, start=1):
        flags = []
        if col["pk"]:
            flags.append("primary key")
        if col["not_null"]:
            flags.append("required")
        extra = f" ({', '.join(flags)})" if flags else ""
        print(f"  {number}. {col['name']} [{col['type'] or 'TEXT'}]{extra}")


# --------------------------------------------------------------------------
# Input helpers and validation
# --------------------------------------------------------------------------


def prompt_menu_choice(prompt, valid_choices):
    """Ask for a single-letter/word choice until a valid one is entered.

    Args:
        prompt (str): Text shown to the user.
        valid_choices (list[str]): Accepted answers (case-insensitive).

    Returns:
        str: The chosen answer in upper case.

    Raises:
        ValueError: If ``valid_choices`` is empty.
    """
    if not valid_choices:
        raise ValueError("valid_choices must not be empty.")
    allowed = [choice.upper() for choice in valid_choices]
    while True:
        answer = input(prompt).strip().upper()
        if answer in allowed:
            return answer
        print(f"Invalid choice. Please enter one of: {', '.join(allowed)}")


def prompt_number_in_range(prompt, low, high, allow_cancel=True):
    """Ask for an integer between ``low`` and ``high`` (inclusive).

    Args:
        prompt (str): Text shown to the user.
        low (int): Smallest accepted value.
        high (int): Largest accepted value.
        allow_cancel (bool): If True, entering ``0`` or leaving the input
            blank cancels and returns None.

    Returns:
        int | None: The number entered, or None if the user cancelled.

    Raises:
        ValueError: If ``low`` is greater than ``high``.
    """
    if low > high:
        raise ValueError("low must not be greater than high.")
    while True:
        text = input(prompt).strip()
        if allow_cancel and text in ("", "0"):
            return None
        try:
            number = int(text)
        except ValueError:
            print("Please enter a whole number.")
            continue
        if low <= number <= high:
            return number
        print(f"Please enter a number from {low} to {high}.")


def convert_value(text, column):
    """Validate and convert user text to the type of a column.

    Args:
        text (str): The text the user typed.
        column (dict): Column metadata from :func:`get_columns`.

    Returns:
        tuple: ``(ok, value, message)``.  ``ok`` is True when the text is
        acceptable; ``value`` is the converted value (None means SQL NULL);
        ``message`` explains the problem when ``ok`` is False.
    """
    text = text.strip()
    col_type = column["type"]

    if text == "":
        if column["not_null"] and column["default"] is None:
            return False, None, f"'{column['name']}' is required."
        return True, None, ""

    if "INT" in col_type:
        try:
            return True, int(text), ""
        except ValueError:
            return False, None, "Enter a whole number."
    if any(key in col_type for key in ("REAL", "FLOA", "DOUB", "DEC", "NUM", "MONEY")):
        try:
            return True, float(text), ""
        except ValueError:
            return False, None, "Enter a number."
    return True, text, ""


def prompt_for_value(column, blank_hint=""):
    """Ask the user for one field value until it is valid.

    Args:
        column (dict): Column metadata from :func:`get_columns`.
        blank_hint (str): Extra text explaining what a blank entry does.

    Returns:
        object: The validated value (None means SQL NULL).
    """
    label = f"{column['name']} [{column['type'] or 'TEXT'}]"
    if column["not_null"] and column["default"] is None:
        label += " (required)"
    else:
        label += " (blank = NULL)" if not blank_hint else f" ({blank_hint})"
    while True:
        ok, value, message = convert_value(input(f"  {label}: "), column)
        if ok:
            return value
        print(f"  Invalid: {message}")


def is_auto_key(column, columns):
    """Tell whether a column is a single integer primary key SQLite fills in.

    Args:
        column (dict): The column to test.
        columns (list[dict]): All columns of the table.

    Returns:
        bool: True if the column is the table's only primary-key column and
        its type is exactly INTEGER (so SQLite assigns a value if omitted).
    """
    pk_columns = [c for c in columns if c["pk"]]
    return len(pk_columns) == 1 and column["pk"] and column["type"] == "INTEGER"


# --------------------------------------------------------------------------
# Insert / Update / Delete
# --------------------------------------------------------------------------


def insert_record(conn, table_name, table_names):
    """Prompt for field values and insert a new record.

    Args:
        conn (sqlite3.Connection): An open database connection.
        table_name (str): Table to insert into.
        table_names (list[str]): Valid table names (used for validation).

    Returns:
        bool: True if a record was inserted, False otherwise.
    """
    try:
        columns = get_columns(conn, table_name, table_names)
    except ValueError as err:
        print(f"Error: {err}")
        return False

    print("\nInsert a new record (press Ctrl+C to cancel).")
    names, values = [], []
    try:
        for column in columns:
            if is_auto_key(column, columns):
                optional_key = dict(column, not_null=False)  # blank is allowed
                value = prompt_for_value(optional_key, "blank = assign automatically")
                if value is None:
                    continue  # let SQLite pick the next key
            else:
                value = prompt_for_value(column)
            names.append(quote_identifier(column["name"]))
            values.append(value)
    except KeyboardInterrupt:
        print("\nInsert cancelled.")
        return False

    if not names:
        print("Nothing to insert.")
        return False

    sql = (
        f"INSERT INTO {quote_identifier(table_name)} ({', '.join(names)}) "
        f"VALUES ({', '.join('?' for _ in values)})"
    )
    try:
        conn.execute(sql, values)
        conn.commit()
    except sqlite3.Error as err:
        conn.rollback()
        print(f"Insert failed: {err}")
        return False
    print("Record inserted.")
    return True


def update_record(conn, table_name, table_names, records, columns):
    """Let the user pick a row and a field, then update that value.

    Args:
        conn (sqlite3.Connection): An open database connection.
        table_name (str): Table to update.
        table_names (list[str]): Valid table names (used for validation).
        records (list[tuple]): Records currently shown, rowid first.
        columns (list[dict]): Column metadata for the table.

    Returns:
        bool: True if a record was updated, False otherwise.
    """
    if table_name not in table_names:
        print(f"Error: unknown table {table_name!r}.")
        return False
    if not records:
        print("There are no records to update.")
        return False

    row_number = prompt_number_in_range(
        f"Row number to update (1-{len(records)}, 0 to cancel): ", 1, len(records)
    )
    if row_number is None:
        print("Update cancelled.")
        return False

    print("\nFields:")
    display_columns(columns)
    field_number = prompt_number_in_range(
        f"Field number to update (1-{len(columns)}, 0 to cancel): ", 1, len(columns)
    )
    if field_number is None:
        print("Update cancelled.")
        return False

    column = columns[field_number - 1]
    current = records[row_number - 1][field_number]  # +1 offset for the rowid
    print(f"Current value of {column['name']}: {current!r}")
    try:
        new_value = prompt_for_value(column)
    except KeyboardInterrupt:
        print("\nUpdate cancelled.")
        return False

    rowid = records[row_number - 1][0]
    sql = (
        f"UPDATE {quote_identifier(table_name)} "
        f"SET {quote_identifier(column['name'])} = ? WHERE rowid = ?"
    )
    try:
        conn.execute(sql, (new_value, rowid))
        conn.commit()
    except sqlite3.Error as err:
        conn.rollback()
        print(f"Update failed: {err}")
        return False
    print("Record updated.")
    return True


def delete_record(conn, table_name, table_names, records):
    """Let the user pick a row and delete it after confirmation.

    Args:
        conn (sqlite3.Connection): An open database connection.
        table_name (str): Table to delete from.
        table_names (list[str]): Valid table names (used for validation).
        records (list[tuple]): Records currently shown, rowid first.

    Returns:
        bool: True if a record was deleted, False otherwise.
    """
    if table_name not in table_names:
        print(f"Error: unknown table {table_name!r}.")
        return False
    if not records:
        print("There are no records to delete.")
        return False

    row_number = prompt_number_in_range(
        f"Row number to delete (1-{len(records)}, 0 to cancel): ", 1, len(records)
    )
    if row_number is None:
        print("Delete cancelled.")
        return False

    record = records[row_number - 1]
    print(f"Record to delete: {record[1:]}")
    if prompt_menu_choice("Are you sure? (Y/N): ", ["Y", "N"]) != "Y":
        print("Delete cancelled.")
        return False

    try:
        conn.execute(
            f"DELETE FROM {quote_identifier(table_name)} WHERE rowid = ?", (record[0],)
        )
        conn.commit()
    except sqlite3.Error as err:
        conn.rollback()
        print(f"Delete failed (the record may be used by another table): {err}")
        return False
    print("Record deleted.")
    return True


# --------------------------------------------------------------------------
# Menus
# --------------------------------------------------------------------------


def select_table(table_names):
    """Show the numbered list of tables and let the user choose one.

    Args:
        table_names (list[str]): Names of the tables to choose from.

    Returns:
        str | None: The chosen table name, or None if the user quits.
    """
    print("\nTables in the Northwind database:")
    for number, name in enumerate(table_names, start=1):
        print(f"  {number}. {name}")
    choice = prompt_number_in_range(
        f"Select a table (1-{len(table_names)}, 0 to quit): ", 1, len(table_names)
    )
    return None if choice is None else table_names[choice - 1]


def work_with_table(conn, table_name, table_names):
    """Show a table and handle Insert / Update / Delete until the user leaves.

    Args:
        conn (sqlite3.Connection): An open database connection.
        table_name (str): The selected table.
        table_names (list[str]): Valid table names (used for validation).

    Returns:
        None
    """
    while True:
        columns = get_columns(conn, table_name, table_names)
        records = get_records(conn, table_name, table_names)
        display_records(table_name, columns, records)

        action = prompt_menu_choice(
            "(I)nsert, (U)pdate, (D)elete, (B)ack to table list: ",
            ["I", "U", "D", "B"],
        )
        if action == "I":
            insert_record(conn, table_name, table_names)
        elif action == "U":
            update_record(conn, table_name, table_names, records, columns)
        elif action == "D":
            delete_record(conn, table_name, table_names, records)
        else:
            return


def parse_arguments(argv):
    """Parse command-line arguments.

    Args:
        argv (list[str]): Arguments excluding the program name.

    Returns:
        argparse.Namespace: Object with ``db`` and ``sql`` attributes.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Browse and edit the Northwind database.")
    parser.add_argument("--db", default=os.path.join(here, "northwind.db"),
                        help="SQLite database file (created if missing)")
    parser.add_argument("--sql", default=os.path.join(here, "database.sql"),
                        help="SQL script used to build the database")
    return parser.parse_args(argv)


def main(argv):
    """Program entry point.

    Args:
        argv (list[str]): Command-line arguments excluding the program name.

    Returns:
        int: Exit status (0 for success, 1 for a startup error).
    """
    args = parse_arguments(argv)

    if not os.path.isfile(args.db):
        print(f"Database '{args.db}' not found; building it from '{args.sql}'...")
        if not create_database(args.sql, args.db):
            return 1

    conn = connect_database(args.db)
    if conn is None:
        return 1

    try:
        table_names = get_table_names(conn)
        if not table_names:
            print("The database contains no tables.")
            return 1
        while True:
            table_name = select_table(table_names)
            if table_name is None:
                print("Goodbye!")
                return 0
            work_with_table(conn, table_name, table_names)
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
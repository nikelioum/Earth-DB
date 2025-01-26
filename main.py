import os
from create_db import DatabaseManager
from create_tables import TableManager
from operation_tables import TableOperations
from query_tables import QueryTables

def print_help():
    print("""
Available commands:
  CREATE DATABASE <name> - Creates a new database.
  DELETE DATABASE <name> - Deletes a database.
  LIST DATABASES         - Lists all existing databases.
  USE DATABASE <name>    - Selects a database to work with.
  EXIT DATABASE          - Exits the currently selected database.
  CREATE TABLE <name>    - Creates a new table in the selected database.
                           Specify columns and types as 'column_name:type', separated by commas.
                           Supported types: integer, string, float, boolean.
  DROP TABLE <name>      - Deletes a table from the selected database.
  LIST TABLES            - Lists all tables in the selected database.
  INSERT INTO <name>     - Inserts data into a table in the selected database.
                           Example: INSERT INTO users
                                    Enter values: 1, John, 25.5, true
  DELETE FROM <name>     - Deletes rows from a table in the selected database.
                           Example: DELETE FROM users
                                    Enter condition (or press Enter to delete all rows): id = 1
  UPDATE <name>          - Updates rows in a table in the selected database.
                           Example: UPDATE users
                                    Enter updates: name="John", age=30
                                    Enter condition (or press Enter to update all rows): id=1
  SELECT FROM <name>     - Queries data from a table in the selected database.
                           Example: SELECT FROM users
                                    Enter condition (or press Enter for no condition): id=1
  EXIT                   - Exits the CLI.
    """)

def main():
    db_manager = DatabaseManager()
    table_manager = TableManager()
    table_operations = TableOperations()
    query_tables = QueryTables()
    selected_db = None

    print("Welcome to EarthDB CLI!")
    print("Type 'help' for available commands.")

    while True:
        command = input(f"earthdb ({selected_db if selected_db else 'no database selected'})> ").strip()

        if command.lower() == "exit":
            print("Exiting EarthDB CLI. Goodbye!")
            break
        elif command.lower() == "help":
            print_help()
        elif command.startswith("CREATE DATABASE"):
            try:
                _, _, db_name = command.split(" ", 2)
                print(db_manager.create_database(db_name))
            except ValueError:
                print("Error: Invalid syntax. Usage: CREATE DATABASE <name>")
        elif command.startswith("DELETE DATABASE"):
            try:
                _, _, db_name = command.split(" ", 2)
                print(db_manager.delete_database(db_name))
            except ValueError:
                print("Error: Invalid syntax. Usage: DELETE DATABASE <name>")
        elif command.lower() == "list databases":
            print("Available databases:")
            print(db_manager.list_databases())
        elif command.startswith("USE DATABASE"):
            try:
                _, _, db_name = command.split(" ", 2)
                if os.path.exists(f"earthdb_data/{db_name}.json"):
                    selected_db = db_name
                    print(f"Now using database '{selected_db}'.")
                else:
                    print(f"Error: Database '{db_name}' does not exist!")
            except ValueError:
                print("Error: Invalid syntax. Usage: USE DATABASE <name>")
        elif command.lower() == "exit database":
            if selected_db:
                print(f"Exited from database '{selected_db}'.")
                selected_db = None
            else:
                print("Error: No database is currently selected.")
        elif command.startswith("CREATE TABLE"):
            if not selected_db:
                print("Error: No database selected. Use 'USE DATABASE <name>' first.")
            else:
                try:
                    _, _, table_name = command.split(" ", 2)
                    print("Enter columns and types in the format 'column_name:type', separated by commas.")
                    print("Supported types: integer, string, float, boolean.")
                    columns_with_types = input("Columns: ").strip().split(",")
                    print(table_manager.create_table(selected_db, table_name, columns_with_types))
                except ValueError:
                    print("Error: Invalid syntax. Usage: CREATE TABLE <name>")
        elif command.startswith("DROP TABLE"):
            if not selected_db:
                print("Error: No database selected. Use 'USE DATABASE <name>' first.")
            else:
                try:
                    _, _, table_name = command.split(" ", 2)
                    print(table_manager.drop_table(selected_db, table_name))
                except ValueError:
                    print("Error: Invalid syntax. Usage: DROP TABLE <name>")
        elif command.startswith("LIST TABLES"):
            if not selected_db:
                print("Error: No database selected. Use 'USE DATABASE <name>' first.")
            else:
                print("Tables in database:")
                print(table_manager.list_tables(selected_db))
        elif command.startswith("INSERT INTO"):
            if not selected_db:
                print("Error: No database selected. Use 'USE DATABASE <name>' first.")
            else:
                try:
                    _, _, table_name = command.split(" ", 2)
                    print("Enter values for the table columns, separated by commas.")
                    values = input("Values: ").strip().split(",")
                    print(table_operations.insert_into_table(selected_db, table_name, values))
                except ValueError:
                    print("Error: Invalid syntax. Usage: INSERT INTO <name>")
        elif command.startswith("UPDATE"):
            if not selected_db:
                print("Error: No database selected. Use 'USE DATABASE <name>' first.")
            else:
                try:
                    _, table_name = command.split(" ", 1)
                    print("Enter updates in the format 'column=value', separated by commas:")
                    updates = input("Updates: ").strip()
                    print("Enter condition (or press Enter to update all rows):")
                    condition = input("Condition: ").strip()
                    condition = condition if condition else None
                    print(table_operations.update_table(selected_db, table_name, updates, condition))
                except ValueError:
                    print("Error: Invalid syntax. Usage: UPDATE <table>")
        elif command.startswith("DELETE FROM"):
            if not selected_db:
                print("Error: No database selected. Use 'USE DATABASE <name>' first.")
            else:
                try:
                    _, _, table_name = command.split(" ", 2)
                    print("Enter condition (or press Enter to delete all rows):")
                    condition = input("Condition: ").strip()
                    condition = condition if condition else None
                    print(table_operations.delete_from_table(selected_db, table_name, condition))
                except ValueError:
                    print("Error: Invalid syntax. Usage: DELETE FROM <name>")
        elif command.startswith("SELECT FROM"):
            if not selected_db:
                print("Error: No database selected. Use 'USE DATABASE <name>' first.")
            else:
                try:
                    _, _, table_name = command.split(" ", 2)
                    print("Enter columns to select (comma-separated or * for all):")
                    columns = input("Columns: ").strip()
                    columns = columns if columns else "*"
                    print("Enter condition (or press Enter for no condition):")
                    condition = input("Condition: ").strip()
                    condition = condition if condition else None
                    print("Enter column to sort by (or press Enter for no sorting):")
                    order_by = input("Order by: ").strip()
                    order_by = order_by if order_by else None
                    if order_by:
                        print("Enter sort order (asc/desc):")
                        sort_order = input("Sort order: ").strip().lower()
                    else:
                        sort_order = "asc"
                    print(
                        query_tables.select_from_table(
                            selected_db, table_name, columns, condition, order_by, sort_order
                        )
                    )
                except ValueError:
                    print("Error: Invalid syntax. Usage: SELECT FROM <name>")
        else:
            print("Error: Unknown command. Type 'help' for available commands.")

if __name__ == "__main__":
    main()

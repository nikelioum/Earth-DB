import os
import json
import operator
from query_tables import QueryTables  # Import QueryTables for condition parsing and evaluation

class TableOperations:
    def __init__(self, db_path="earthdb_data"):
        self.db_path = db_path

    def load_database(self, db_name):
        """Load the JSON file of the specified database."""
        db_file = os.path.join(self.db_path, f"{db_name}.json")
        if not os.path.exists(db_file):
            raise Exception(f"Error: Database '{db_name}' does not exist!")
        with open(db_file, "r") as f:
            return json.load(f), db_file

    def save_database(self, db_data, db_file):
        """Save changes to the database JSON file."""
        with open(db_file, "w") as f:
            json.dump(db_data, f, indent=4)

    def insert_into_table(self, db_name, table_name, data):
        """Insert data into a specified table."""
        db_data, db_file = self.load_database(db_name)
        if table_name not in db_data["tables"]:
            return f"Error: Table '{table_name}' does not exist in database '{db_name}'!"

        table = db_data["tables"][table_name]
        columns = table["columns"]

        # Validate the input data
        if len(data) != len(columns):
            return f"Error: Mismatch in column count. Table '{table_name}' expects {len(columns)} columns."

        row = {}
        for (column_name, column_type), value in zip(columns.items(), data):
            # Type validation
            try:
                if column_type == "integer":
                    row[column_name] = int(value)
                elif column_type == "float":
                    row[column_name] = float(value)
                elif column_type == "boolean":
                    row[column_name] = value.lower() in ["true", "1"]
                elif column_type == "string":
                    row[column_name] = str(value)
                else:
                    return f"Error: Unsupported column type '{column_type}'."
            except ValueError:
                return f"Error: Invalid value '{value}' for column '{column_name}' (expected {column_type})."

        # Add the row to the table
        table["rows"].append(row)
        self.save_database(db_data, db_file)
        return f"Data inserted successfully into table '{table_name}'."

    def delete_from_table(self, db_name, table_name, condition=None):
        """Deletes rows from a specified table based on a condition."""
        db_data, db_file = self.load_database(db_name)
        if table_name not in db_data["tables"]:
            return f"Error: Table '{table_name}' does not exist in database '{db_name}'!"

        table = db_data["tables"][table_name]
        rows = table["rows"]
        columns = table["columns"]

        if not rows:
            return f"No data found in table '{table_name}' to delete."

        # If no condition is provided, clear all rows
        if not condition:
            table["rows"] = []
            self.save_database(db_data, db_file)
            return f"All rows deleted from table '{table_name}'."

        # Parse and apply the condition
        key, op, value = QueryTables().parse_condition(condition)
        if key not in columns:
            return f"Error: Column '{key}' does not exist in table '{table_name}'."
        col_type = columns[key]

        # Filter rows to keep only those that don't match the condition
        original_row_count = len(rows)
        table["rows"] = [
            row for row in rows
            if not QueryTables().evaluate_condition(row, key, op, value, col_type)
        ]

        deleted_row_count = original_row_count - len(table["rows"])
        self.save_database(db_data, db_file)
        return f"{deleted_row_count} row(s) deleted from table '{table_name}'."

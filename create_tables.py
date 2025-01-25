import os
import json

class TableManager:
    SUPPORTED_TYPES = ["integer", "string", "float", "boolean"]  # Allowed data types

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

    def create_table(self, db_name, table_name, columns_with_types):
        """Create a new table in the specified database."""
        db_data, db_file = self.load_database(db_name)
        if table_name in db_data["tables"]:
            return f"Error: Table '{table_name}' already exists in database '{db_name}'!"

        # Parse and validate columns and types
        columns = {}
        for column_def in columns_with_types:
            try:
                column_name, column_type = column_def.split(":")
                column_name = column_name.strip()
                column_type = column_type.strip().lower()
                if column_type not in self.SUPPORTED_TYPES:
                    return f"Error: Unsupported data type '{column_type}'. Supported types are: {', '.join(self.SUPPORTED_TYPES)}"
                columns[column_name] = column_type
            except ValueError:
                return f"Error: Invalid column definition '{column_def}'. Use format 'column_name:type'."

        # Create table metadata
        db_data["tables"][table_name] = {
            "columns": columns,
            "rows": []
        }
        self.save_database(db_data, db_file)
        return f"Table '{table_name}' created successfully in database '{db_name}'."

    def drop_table(self, db_name, table_name):
        """Drop a table from the specified database."""
        db_data, db_file = self.load_database(db_name)
        if table_name not in db_data["tables"]:
            return f"Error: Table '{table_name}' does not exist in database '{db_name}'!"
        del db_data["tables"][table_name]
        self.save_database(db_data, db_file)
        return f"Table '{table_name}' dropped successfully from database '{db_name}'."

    def list_tables(self, db_name):
        """List all tables in the specified database."""
        db_data, _ = self.load_database(db_name)
        tables = db_data["tables"]
        if not tables:
            return f"No tables found in database '{db_name}'."
        return "\n".join(tables.keys())

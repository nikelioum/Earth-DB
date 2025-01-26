import os
import json
import csv

class ExportFunctionality:
    def __init__(self, db_path="earthdb_data", export_path="exports"):
        self.db_path = db_path
        self.export_path = export_path

        # Ensure the export folder exists
        if not os.path.exists(self.export_path):
            os.makedirs(self.export_path)

    def load_database(self, db_name):
        """Load the JSON file of the specified database."""
        db_file = os.path.join(self.db_path, f"{db_name}.json")
        if not os.path.exists(db_file):
            raise Exception(f"Error: Database '{db_name}' does not exist!")
        with open(db_file, "r") as f:
            return json.load(f), db_file

    def export_table_to_csv(self, db_name, table_name, output_file):
        """Export a specific table to a CSV file."""
        db_data, _ = self.load_database(db_name)
        if table_name not in db_data["tables"]:
            return f"Error: Table '{table_name}' does not exist in database '{db_name}'!"

        table = db_data["tables"][table_name]
        rows = table["rows"]
        columns = list(table["columns"].keys())

        if not rows:
            return f"Error: Table '{table_name}' is empty!"

        # Ensure the output file is in the exports folder
        output_path = os.path.join(self.export_path, output_file)

        # Write to CSV
        with open(output_path, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)

        return f"Table '{table_name}' exported successfully to '{output_path}'."

    def export_table_to_json(self, db_name, table_name, output_file):
        """Export a specific table to a JSON file."""
        db_data, _ = self.load_database(db_name)
        if table_name not in db_data["tables"]:
            return f"Error: Table '{table_name}' does not exist in database '{db_name}'!"

        table = db_data["tables"][table_name]

        # Ensure the output file is in the exports folder
        output_path = os.path.join(self.export_path, output_file)

        # Write to JSON
        with open(output_path, "w") as jsonfile:
            json.dump(table, jsonfile, indent=4)

        return f"Table '{table_name}' exported successfully to '{output_path}'."

    def export_database_to_json(self, db_name, output_file):
        """Export the entire database to a JSON file."""
        db_data, _ = self.load_database(db_name)

        # Ensure the output file is in the exports folder
        output_path = os.path.join(self.export_path, output_file)

        # Write to JSON
        with open(output_path, "w") as jsonfile:
            json.dump(db_data, jsonfile, indent=4)

        return f"Database '{db_name}' exported successfully to '{output_path}'."

    def import_table_from_json(self, db_name, table_name, input_file):
        """Import a table from a JSON file."""
        db_data, db_file = self.load_database(db_name)

        # Load JSON data
        with open(input_file, "r") as jsonfile:
            table_data = json.load(jsonfile)

        if "rows" not in table_data or "columns" not in table_data:
            return "Error: Invalid JSON file format for table import."

        db_data["tables"][table_name] = table_data
        
        # Save database
        with open(db_file, "w") as f:
            json.dump(db_data, f, indent=4)

        return f"Table '{table_name}' imported successfully from '{input_file}'."

    def import_table_from_csv(self, db_name, table_name, input_file):
        """Import a table from a CSV file."""
        db_data, db_file = self.load_database(db_name)

        # Read CSV data
        with open(input_file, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            rows = [row for row in reader]

        if not rows:
            return "Error: CSV file is empty."

        columns = {col: "string" for col in rows[0].keys()}  # Assume all columns are strings for simplicity

        db_data["tables"][table_name] = {
            "columns": columns,
            "rows": rows
        }

        # Save database
        with open(db_file, "w") as f:
            json.dump(db_data, f, indent=4)

        return f"Table '{table_name}' imported successfully from '{input_file}'."

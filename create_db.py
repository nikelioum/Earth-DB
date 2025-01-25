import os
import json

class DatabaseManager:
    def __init__(self, storage_path="earthdb_data"):
        self.storage_path = storage_path
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)

    def create_database(self, db_name):
        """Creates a new database (JSON file)."""
        db_file = os.path.join(self.storage_path, f"{db_name}.json")
        if os.path.exists(db_file):
            return f"Error: Database '{db_name}' already exists!"
        with open(db_file, "w") as f:
            json.dump({"tables": {}}, f) 
        return f"Database '{db_name}' created successfully."

    def delete_database(self, db_name):
        """Deletes a database (JSON file)."""
        db_file = os.path.join(self.storage_path, f"{db_name}.json")
        if not os.path.exists(db_file):
            return f"Error: Database '{db_name}' does not exist!"
        os.remove(db_file)
        return f"Database '{db_name}' deleted successfully."

    def list_databases(self):
        """Lists all databases (JSON files)."""
        databases = [
            file.replace(".json", "") for file in os.listdir(self.storage_path) if file.endswith(".json")
        ]
        if not databases:
            return "No databases found."
        return "\n".join(databases)

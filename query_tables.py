import os
import json
import operator

class QueryTables:
    def __init__(self, db_path="earthdb_data"):
        self.db_path = db_path

    def load_database(self, db_name):
        """Load the JSON file of the specified database."""
        db_file = os.path.join(self.db_path, f"{db_name}.json")
        if not os.path.exists(db_file):
            raise Exception(f"Error: Database '{db_name}' does not exist!")
        with open(db_file, "r") as f:
            return json.load(f)

    def parse_condition(self, condition):
        """Parse a condition string into components for evaluation."""
        operators = {
            "=": operator.eq,
            "!=": operator.ne,
            "<": operator.lt,
            "<=": operator.le,
            ">": operator.gt,
            ">=": operator.ge,
        }
        for op in operators:
            if op in condition:
                left, right = condition.split(op, 1)
                return left.strip(), operators[op], right.strip()
        raise ValueError("Invalid condition format. Supported operators: =, !=, <, <=, >, >=")

    def evaluate_condition(self, row, key, op, value, col_type):
        """Evaluate a single condition on a row."""
        # Convert value to the appropriate type
        if col_type == "integer":
            value = int(value)
        elif col_type == "float":
            value = float(value)
        elif col_type == "boolean":
            value = value.lower() in ["true", "1"]
        elif col_type == "string":
            value = str(value)

        return op(row[key], value)

    def select_from_table(
        self, db_name, table_name, columns="*", condition=None, order_by=None, sort_order="asc"
    ):
        """Query data from a table with support for conditions, sorting, and column selection."""
        db_data = self.load_database(db_name)
        if table_name not in db_data["tables"]:
            return f"Error: Table '{table_name}' does not exist in database '{db_name}'!"

        table = db_data["tables"][table_name]
        rows = table["rows"]
        all_columns = table["columns"]

        if not rows:
            return f"No data found in table '{table_name}'."

        # Filter columns if specific columns are requested
        if columns != "*":
            columns = [col.strip() for col in columns.split(",")]
            for col in columns:
                if col not in all_columns:
                    return f"Error: Column '{col}' does not exist in table '{table_name}'."
        else:
            columns = all_columns.keys()

        # Apply condition
        if condition:
            key, op, value = self.parse_condition(condition)
            if key not in all_columns:
                return f"Error: Column '{key}' does not exist in table '{table_name}'."
            col_type = all_columns[key]
            rows = [row for row in rows if self.evaluate_condition(row, key, op, value, col_type)]

        # Sort rows
        if order_by:
            if order_by not in all_columns:
                return f"Error: Column '{order_by}' does not exist in table '{table_name}'."
            rows = sorted(
                rows,
                key=lambda row: row[order_by],
                reverse=(sort_order.lower() == "desc"),
            )

        # Format output
        output = [", ".join(columns)]
        for row in rows:
            output.append(", ".join(str(row[col]) for col in columns))
        return "\n".join(output)

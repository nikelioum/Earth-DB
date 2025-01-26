import os
import json
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from create_db import DatabaseManager
from create_tables import TableManager
from operation_tables import TableOperations
from query_tables import QueryTables


class EarthDBGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("EarthDB - Complete GUI")
        self.root.geometry("1000x700")

        # Managers
        self.db_manager = DatabaseManager()
        self.table_manager = TableManager()
        self.table_operations = TableOperations()
        self.query_tables = QueryTables()

        # Paths
        self.db_path = "earthdb_data"

        # Selected database and table
        self.selected_db = None
        self.selected_table = None

        # GUI Layout
        self.create_gui()

    def create_gui(self):
        # Top Frame: Database Selection
        frame_top = tk.Frame(self.root)
        frame_top.pack(fill="x", pady=5)

        tk.Label(frame_top, text="Selected Database:").pack(side="left", padx=5)
        self.selected_db_label = tk.Label(frame_top, text="No database selected", fg="blue")
        self.selected_db_label.pack(side="left", padx=5)
        tk.Button(frame_top, text="Change Database", command=self.select_database).pack(side="left", padx=5)

        # Left Panel: Operations
        frame_left = tk.Frame(self.root)
        frame_left.pack(side="left", fill="y", padx=10, pady=10)

        tk.Button(frame_left, text="Create Database", command=self.create_database).pack(fill="x", pady=5)
        tk.Button(frame_left, text="Delete Database", command=self.delete_database).pack(fill="x", pady=5)
        tk.Button(frame_left, text="List Databases", command=self.populate_databases).pack(fill="x", pady=5)

        tk.Button(frame_left, text="Create Table", command=self.create_table).pack(fill="x", pady=5)
        tk.Button(frame_left, text="Drop Table", command=self.drop_table).pack(fill="x", pady=5)
        tk.Button(frame_left, text="List Tables", command=self.populate_tables).pack(fill="x", pady=5)

        tk.Button(frame_left, text="Insert Data", command=self.insert_data).pack(fill="x", pady=5)
        tk.Button(frame_left, text="Query Data", command=self.query_data).pack(fill="x", pady=5)
        tk.Button(frame_left, text="Delete Record", command=self.delete_record).pack(fill="x", pady=5)  # New Button

        # Right Panel: Output
        frame_right = tk.Frame(self.root)
        frame_right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Databases Treeview
        self.db_tree = ttk.Treeview(frame_right, columns=("Databases"), show="headings", height=5)
        self.db_tree.heading("Databases", text="Databases")
        self.db_tree.pack(fill="x", padx=5)
        self.db_tree.bind("<<TreeviewSelect>>", self.on_database_select)

        # Tables Treeview
        self.table_tree = ttk.Treeview(frame_right, columns=("Tables"), show="headings", height=5)
        self.table_tree.heading("Tables", text="Tables")
        self.table_tree.pack(fill="x", padx=5)
        self.table_tree.bind("<<TreeviewSelect>>", self.on_table_select)

        # Table Data Treeview
        self.data_tree = ttk.Treeview(frame_right, show="headings")
        self.data_tree.pack(fill="both", expand=True, padx=5)

        # Populate Databases
        self.populate_databases()

    def populate_databases(self):
        """Populate the database list in the Treeview."""
        databases = [
            db.replace(".json", "") for db in os.listdir(self.db_path) if db.endswith(".json")
        ]
        self.db_tree.delete(*self.db_tree.get_children())  # Clear existing data
        for db in databases:
            self.db_tree.insert("", "end", values=(db,))

    def on_database_select(self, event):
        """Handle database selection and populate tables."""
        selected_item = self.db_tree.focus()
        self.selected_db = self.db_tree.item(selected_item, "values")[0]  # Extract database name
        self.selected_db_label.config(text=self.selected_db)
        self.populate_tables()

    def populate_tables(self):
        """Populate the table list for the selected database."""
        if not self.selected_db:
            return
        db_file = os.path.join(self.db_path, f"{self.selected_db}.json")
        try:
            with open(db_file, "r") as f:
                db_data = json.load(f)
            tables = list(db_data["tables"].keys())
            self.table_tree.delete(*self.table_tree.get_children())  # Clear existing data
            for table in tables:
                self.table_tree.insert("", "end", values=(table,))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tables: {str(e)}")

    def on_table_select(self, event):
        """Handle table selection and display data."""
        selected_item = self.table_tree.focus()
        self.selected_table = self.table_tree.item(selected_item, "values")[0]  # Extract table name
        self.populate_table_data()

    def populate_table_data(self):
        """Populate the data for the selected table."""
        if not self.selected_db or not self.selected_table:
            return
        db_file = os.path.join(self.db_path, f"{self.selected_db}.json")
        try:
            with open(db_file, "r") as f:
                db_data = json.load(f)
            table_data = db_data["tables"][self.selected_table]
            rows = table_data["rows"]
            columns = list(table_data["columns"].keys())

            # Clear existing data
            self.data_tree.delete(*self.data_tree.get_children())
            self.data_tree["columns"] = columns
            self.data_tree["show"] = "headings"

            # Set column headings
            for col in columns:
                self.data_tree.heading(col, text=col)
                self.data_tree.column(col, width=100, anchor="center")

            # Insert rows
            for row in rows:
                self.data_tree.insert("", "end", values=[row[col] for col in columns])

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load table data: {str(e)}")

    def select_database(self):
        """Allow the user to manually select a database."""
        db_name = simpledialog.askstring("Select Database", "Enter database name:")
        if db_name and db_name in self.db_manager.list_databases():
            self.selected_db = db_name
            self.selected_db_label.config(text=db_name)
            self.populate_tables()
        else:
            messagebox.showerror("Error", f"Database '{db_name}' does not exist.")

    def create_database(self):
        db_name = simpledialog.askstring("Create Database", "Enter new database name:")
        if db_name:
            result = self.db_manager.create_database(db_name)
            self.populate_databases()
            messagebox.showinfo("Success", result)

    def delete_database(self):
        db_name = simpledialog.askstring("Delete Database", "Enter database name to delete:")
        if db_name:
            result = self.db_manager.delete_database(db_name)
            self.populate_databases()
            messagebox.showinfo("Success", result)

    def create_table(self):
        if not self.selected_db:
            messagebox.showerror("Error", "No database selected.")
            return
        table_name = simpledialog.askstring("Create Table", "Enter table name:")
        if table_name:
            columns = simpledialog.askstring("Create Table", "Enter columns (e.g., id:integer, name:string):")
            if columns:
                result = self.table_manager.create_table(self.selected_db, table_name, columns.split(","))
                self.populate_tables()
                messagebox.showinfo("Success", result)

    def drop_table(self):
        if not self.selected_db:
            messagebox.showerror("Error", "No database selected.")
            return
        table_name = simpledialog.askstring("Drop Table", "Enter table name:")
        if table_name:
            result = self.table_manager.drop_table(self.selected_db, table_name)
            self.populate_tables()
            messagebox.showinfo("Success", result)

    def insert_data(self):
        if not self.selected_db:
            messagebox.showerror("Error", "No database selected.")
            return
        table_name = simpledialog.askstring("Insert Data", "Enter table name:")
        if table_name:
            values = simpledialog.askstring("Insert Data", "Enter values (comma-separated):")
            if values:
                result = self.table_operations.insert_into_table(self.selected_db, table_name, values.split(","))
                self.populate_table_data()
                messagebox.showinfo("Success", result)

    def query_data(self):
        if not self.selected_db:
            messagebox.showerror("Error", "No database selected.")
            return
        table_name = simpledialog.askstring("Query Data", "Enter table name:")
        if table_name:
            columns = simpledialog.askstring("Query Data", "Enter columns (* for all):")
            condition = simpledialog.askstring("Query Data", "Enter condition (or leave blank):")
            result = self.query_tables.select_from_table(self.selected_db, table_name, columns or "*", condition or None)
            if result:
                self.populate_table_data()
                messagebox.showinfo("Success", "Query executed successfully.")
            else:
                messagebox.showinfo("Info", "No results found.")

    def delete_record(self):
        """Delete a record from the selected table."""
        if not self.selected_db:
            messagebox.showerror("Error", "No database selected.")
            return
        if not self.selected_table:
            messagebox.showerror("Error", "No table selected.")
            return
        condition = simpledialog.askstring("Delete Record", "Enter condition to match records to delete:")
        if condition:
            result = self.table_operations.delete_from_table(self.selected_db, self.selected_table, condition)
            self.populate_table_data()
            messagebox.showinfo("Success", result)


if __name__ == "__main__":
    root = tk.Tk()
    app = EarthDBGUI(root)
    root.mainloop()

# EarthDB CLI - Documentation

Welcome to **EarthDB CLI**, a command-line tool for managing and querying databases. This documentation will guide you through its features, commands, and usage.

---

## **Features**
- Create and delete databases.
- Create and drop tables with specified column types.
- Insert data into tables with type validation.
- Query tables with support for conditions, sorting, and column-specific selection.
- Delete data from tables with or without conditions.
- Update data in tables with specified conditions.
- Export tables or databases to JSON/CSV.
- Import tables from JSON/CSV files.
- Easy-to-use interface for managing your custom database.

---

## **Getting Started**

### Prerequisites
- Python 3.6 or later
- A terminal or command prompt to run the CLI

### Running the CLI
To start the CLI, navigate to the project directory and run:
```bash
python main.py
```
You will be greeted with the welcome message and the available commands.

---

## **Available Commands**

### 1. **CREATE DATABASE <name>**
Creates a new database.

**Usage:**
```bash
CREATE DATABASE mydb
```
**Output:**
```
Database 'mydb' created successfully.
```

---

### 2. **DELETE DATABASE <name>**
Deletes an existing database.

**Usage:**
```bash
DELETE DATABASE mydb
```
**Output:**
```
Database 'mydb' deleted successfully.
```

---

### 3. **LIST DATABASES**
Lists all existing databases.

**Usage:**
```bash
LIST DATABASES
```
**Output:**
```
Available databases:
 - mydb
 - testdb
```

---

### 4. **USE DATABASE <name>**
Selects a database to work with.

**Usage:**
```bash
USE DATABASE mydb
```
**Output:**
```
Now using database 'mydb'.
```

---

### 5. **EXIT DATABASE**
Exits the currently selected database.

**Usage:**
```bash
EXIT DATABASE
```
**Output:**
```
Exited from database 'mydb'.
```

---

### 6. **CREATE TABLE <name>**
Creates a new table in the selected database. Specify column names and types.

**Supported Types:**
- `integer`
- `string`
- `float`
- `boolean`

**Usage:**
```bash
CREATE TABLE users
Enter columns and types in the format 'column_name:type', separated by commas.
Columns: id:integer, name:string, age:float, is_active:boolean
```
**Output:**
```
Table 'users' created successfully in database 'mydb'.
```

---

### 7. **DROP TABLE <name>**
Deletes a table from the selected database.

**Usage:**
```bash
DROP TABLE users
```
**Output:**
```
Table 'users' dropped successfully from database 'mydb'.
```

---

### 8. **LIST TABLES**
Lists all tables in the selected database.

**Usage:**
```bash
LIST TABLES
```
**Output:**
```
Tables in database:
 - users
```

---

### 9. **INSERT INTO <name>**
Inserts data into a table in the selected database. Ensure the values match the table schema.

**Usage:**
```bash
INSERT INTO users
Enter values for the table columns, separated by commas.
Values: 1, John Doe, 25.5, true
```
**Output:**
```
Data inserted successfully into table 'users'.
```

---

### 10. **DELETE FROM <name>**
Deletes rows from a table in the selected database. You can specify a condition to delete specific rows or leave it blank to delete all rows.

**Usage:**
```bash
DELETE FROM users
Enter condition (or press Enter to delete all rows):
Condition: id = 1
```
**Output:**
```
1 row(s) deleted from table 'users'.
```

**Delete All Rows:**
```bash
DELETE FROM users
Enter condition (or press Enter to delete all rows):
Condition:
```
**Output:**
```
All rows deleted from table 'users'.
```

---

### 11. **UPDATE <name>**
Updates rows in a table in the selected database. You can specify which columns to update and the condition to match rows.

**Usage:**
```bash
UPDATE users
Enter updates in the format 'column=value', separated by commas:
Updates: name="John Doe", age=30
Enter condition (or press Enter to update all rows):
Condition: id = 1
```
**Output:**
```
1 row(s) updated in table 'users'.
```

**Update All Rows:**
```bash
UPDATE users
Enter updates in the format 'column=value', separated by commas:
Updates: is_active=false
Enter condition (or press Enter to update all rows):
Condition:
```
**Output:**
```
3 row(s) updated in table 'users'.
```

---

### 12. **SELECT FROM <name>**
Queries data from a table in the selected database. Supports conditions, sorting, and column-specific selection.

**Usage:**
```bash
SELECT FROM users
Enter columns to select (comma-separated or * for all):
Columns: id, name
Enter condition (or press Enter for no condition):
Condition: age > 20 AND is_active=true
Enter column to sort by (or press Enter for no sorting):
Order by: age
Enter sort order (asc/desc):
Sort order: desc
```
**Output:**
```
id, name
1, John Doe
```

---

### 13. **EXPORT TABLE <name> TO <format>**
Exports a table to a file in the specified format (JSON or CSV).

**Usage:**
```bash
EXPORT TABLE users TO csv
Enter output file name (with extension): users_backup.csv
```
**Output:**
```
Table 'users' exported successfully to 'users_backup.csv'.
```

**Export to JSON:**
```bash
EXPORT TABLE users TO json
Enter output file name (with extension): users_backup.json
```
**Output:**
```
Table 'users' exported successfully to 'users_backup.json'.
```

---

### 14. **EXPORT DATABASE <name> TO JSON**
Exports the entire database to a JSON file.

**Usage:**
```bash
EXPORT DATABASE testdb TO json
Enter output file name (with extension): testdb_backup.json
```
**Output:**
```
Database 'testdb' exported successfully to 'testdb_backup.json'.
```

---

### 15. **IMPORT TABLE <name> FROM <file>**
Imports a table from a JSON or CSV file.

**Usage:**
```bash
IMPORT TABLE users FROM users_backup.json
```
**Output:**
```
Table 'users' imported successfully from 'users_backup.json'.
```

**Import from CSV:**
```bash
IMPORT TABLE users FROM users_backup.csv
```
**Output:**
```
Table 'users' imported successfully from 'users_backup.csv'.
```

---

## **Example Workflow**
Here’s an example demonstrating the CLI’s functionality:

```bash
$ python main.py
Welcome to EarthDB CLI!
Made by LIAROPOULOS DIMITRIS
Type 'help' for available commands.

earthdb> CREATE DATABASE testdb
Database 'testdb' created successfully.

earthdb> USE DATABASE testdb
Now using database 'testdb'.

earthdb (testdb)> CREATE TABLE users
Enter columns and types in the format 'column_name:type', separated by commas.
Columns: id:integer, name:string, age:float, is_active:boolean
Table 'users' created successfully in database 'testdb'.

earthdb (testdb)> INSERT INTO users
Enter values for the table columns, separated by commas.
Values: 1, John Doe, 25.5, true
Data inserted successfully into table 'users'.

earthdb (testdb)> UPDATE users
Enter updates in the format 'column=value', separated by commas:
Updates: name="Dimitris", age=30
Enter condition (or press Enter to update all rows):
Condition: id = 1
1 row(s) updated in table 'users'.

earthdb (testdb)> DELETE FROM users
Enter condition (or press Enter to delete all rows):
Condition: id = 1
1 row(s) deleted from table 'users'.

earthdb (testdb)> EXPORT TABLE users TO csv
Enter output file name (with extension): users_backup.csv
Table 'users' exported successfully to 'users_backup.csv'.

earthdb (testdb)> EXIT
Exiting EarthDB CLI. Goodbye!
```

---

## **Additional Notes**
1. Ensure that column names and types are consistent when inserting, updating, or querying data.
2. Conditions in `SELECT`, `DELETE`, and `UPDATE` support logical operators like `AND` and `OR`.
3. Sorting allows you to order results by any column in ascending or descending order.
4. Exported files (JSON/CSV) can be re-imported into the database.

---

Enjoy using EarthDB CLI! Feel free to extend or modify it for your use case.


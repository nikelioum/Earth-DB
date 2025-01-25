# EarthDB CLI - Documentation

Welcome to **EarthDB CLI**, a command-line tool for managing and querying databases. This documentation will guide you through its features, commands, and usage.

---

## **Features**
- Create and delete databases.
- Create and drop tables with specified column types.
- Insert data into tables with type validation.
- Query tables with support for conditions, sorting, and column-specific selection.
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

### 10. **SELECT FROM <name>**
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

earthdb (testdb)> SELECT FROM users
Enter columns to select (comma-separated or * for all):
Columns: *
Enter condition (or press Enter for no condition):
Condition: age > 20
Enter column to sort by (or press Enter for no sorting):
Order by: age
Enter sort order (asc/desc):
Sort order: asc
id, name, age, is_active
1, John Doe, 25.5, true

earthdb (testdb)> EXIT
Exiting EarthDB CLI. Goodbye!
```

---

## **Additional Notes**
1. Ensure that column names and types are consistent when inserting or querying data.
2. Conditions in `SELECT` support logical operators like `AND` and `OR`.
3. Sorting allows you to order results by any column in ascending or descending order.

---

Enjoy using EarthDB CLI! Feel free to extend or modify it for your use case.


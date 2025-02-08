# database.py
"""
This module handles the database connection and initialization.
It connects to the MySQL server, creates the necessary databases and tables,
and returns a connection and cursor for further operations.
"""

import mysql.connector

def get_db_connection(database=None):
    """Returns a MySQL connection. If 'database' is provided, connects to that database."""
    config = {
        "host": "localhost",
        "user": "root",
        "password": "Dev230107"
    }
    if database:
        config["database"] = database
    return mysql.connector.connect(**config)

def initialize_databases_and_tables():
    """
    Initializes the databases and tables.
    First, it ensures that a database named 'books' exists.
    Then, it creates/uses the 'book_store' database and creates the required tables:
      - signup
      - Available_Books
      - Sell_rec
      - Staff_details
      - staff_login
    Returns a tuple of (db_connection, cursor).
    """
    # Connect without specifying a database to check/create the 'books' database.
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SHOW DATABASES LIKE 'books'")
    result = cursor.fetchone()
    if not result:
        print("Database 'books' does not exist. Creating it now...")
        cursor.execute("CREATE DATABASE books")
    else:
        print("Database 'books' already exists.")
    db.close()

    # Connect to the 'books' database.
    db = get_db_connection(database="books")
    cursor = db.cursor()
    if db.is_connected():
        print("Successfully connected to the 'books' database.")

    # Create/use the 'book_store' database.
    cursor.execute("CREATE DATABASE IF NOT EXISTS book_store")
    cursor.execute("USE book_store")

    # Create tables if they do not exist.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS signup(
            username VARCHAR(20) PRIMARY KEY,
            password VARCHAR(20)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Available_Books(
            BookName VARCHAR(30) PRIMARY KEY,
            Genre VARCHAR(20),
            Quantity INT,
            Author VARCHAR(20),
            Publication VARCHAR(30),
            Price INT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Sell_rec(
            Customer_Id INTEGER PRIMARY KEY,
            CustomerName VARCHAR(20),
            PhoneNumber INT,
            BookName VARCHAR(30),
            Quantity INT,
            Price INT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Staff_details(
            Staff_id INT PRIMARY KEY,
            Name VARCHAR(30),
            Gender VARCHAR(10),
            Age INT,
            PhoneNumber INT,
            Address VARCHAR(40)
        )
    """)
    # Create a separate table for staff login.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS staff_login(
            username VARCHAR(20) PRIMARY KEY,
            password VARCHAR(20)
        )
    """)
    db.commit()
    return db, cursor


# auth.py
"""
This module contains authentication functions for customers and staff.
Functions include signup and login for each type of user.
"""

import mysql.connector

def customer_signup(cursor, db):
    """
    Registers a new customer by inserting into the 'signup' table.
    Uses robust input validation.
    """
    while True:
        temp = input("USERNAME: ").strip()
        if not temp:
            print("Username cannot be blank. Try again.")
        else:
            username = temp
            break
    while True:
        temp = input("PASSWORD: ").strip()
        if not temp:
            print("Password cannot be blank. Try again.")
        else:
            password = temp
            break
    try:
        cursor.execute("INSERT INTO signup (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        print("Signup successful!")
    except mysql.connector.IntegrityError:
        print("Signup failed. Username may already exist.")
    except Exception as e:
        print("An error occurred during signup:", e)

def customer_login(cursor):
    """
    Authenticates a customer from the 'signup' table.
    Returns the username if login is successful; otherwise, returns None.
    """
    while True:
        temp = input("USERNAME: ").strip()
        if not temp:
            print("Username cannot be blank. Try again.")
        else:
            username = temp
            break
    try:
        cursor.execute("SELECT username FROM signup WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user:
            while True:
                temp = input("PASSWORD: ").strip()
                if not temp:
                    print("Password cannot be blank. Try again.")
                else:
                    password = temp
                    break
            cursor.execute("SELECT password FROM signup WHERE username = %s AND password = %s", (username, password))
            auth = cursor.fetchone()
            if auth:
                print("Login successful!")
                return username
            else:
                print("Invalid password.")
                return None
        else:
            print("Invalid username.")
            return None
    except Exception as e:
        print("An error occurred during login:", e)
        return None

def staff_signup(cursor, db):
    """
    Registers a new staff member in the 'staff_login' table.
    Uses robust input validation.
    """
    print("=== Staff Signup ===")
    while True:
        temp = input("Enter STAFF username: ").strip()
        if not temp:
            print("Username cannot be blank. Please try again.")
        else:
            username = temp
            break
    while True:
        temp = input("Enter STAFF password: ").strip()
        if not temp:
            print("Password cannot be blank. Please try again.")
        else:
            password = temp
            break
    try:
        cursor.execute("INSERT INTO staff_login (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        print("Staff signup successful!")
    except mysql.connector.IntegrityError:
        print("Staff signup failed. Username may already exist.")
    except Exception as e:
        print("An error occurred during staff signup:", e)

def staff_login(cursor):
    """
    Authenticates a staff member from the 'staff_login' table.
    Returns the username if login is successful; otherwise, returns None.
    """
    print("=== Staff Login ===")
    while True:
        temp = input("Enter STAFF username: ").strip()
        if not temp:
            print("Username cannot be blank. Try again.")
        else:
            username = temp
            break
    while True:
        temp = input("Enter STAFF password: ").strip()
        if not temp:
            print("Password cannot be blank. Try again.")
        else:
            password = temp
            break
    try:
        cursor.execute("SELECT username FROM staff_login WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        if result:
            print("Staff login successful!")
            return username
        else:
            print("Invalid STAFF username or password.")
            return None
    except Exception as e:
        print("An error occurred during staff login:", e)
        return None

# staff_management.py
"""
This module contains functions for managing staff details:
- Adding a new staff entry.
- Removing an existing staff member.
- Displaying all staff details.
"""

def staff_add(cursor, db):
    """
    Adds a new staff entry to the Staff_details table.
    Determines a new Staff_id by counting existing records.
    """
    try:
        cursor.execute("SELECT * FROM Staff_details")
        rows = cursor.fetchall()
        staff_id = len(rows) + 1
    except Exception as e:
        print("Error retrieving staff details:", e)
        return

    while True:
        fname = input("Enter Fullname: ").strip()
        if not fname:
            print("Fullname cannot be blank. Try again.")
        else:
            break
    while True:
        gender = input("Gender (M/F/O): ").strip()
        if not gender:
            print("Gender cannot be blank. Try again.")
        elif gender not in ["M", "F", "O"]:
            print("Invalid gender. Please enter M, F, or O.")
        else:
            break
    while True:
        temp = input("Age: ").strip()
        if not temp:
            print("Age cannot be blank. Try again.")
        else:
            try:
                age = int(temp)
                break
            except ValueError:
                print("Please enter a valid integer for age.")
    while True:
        temp = input("Staff phone no.: ").strip()
        if not temp:
            print("Phone number cannot be blank. Try again.")
        else:
            try:
                phon = int(temp)
                break
            except ValueError:
                print("Please enter a valid integer for phone number.")
    while True:
        add = input("Address: ").strip()
        if not add:
            print("Address cannot be blank. Try again.")
        else:
            break
    try:
        query = """
            INSERT INTO Staff_details (Staff_id, Name, Gender, Age, PhoneNumber, Address)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (staff_id, fname, gender, age, phon, add))
        db.commit()
        print("Staff successfully added!")
    except Exception as e:
        print("Error adding staff:", e)

def staff_remove(cursor, db):
    """
    Removes a staff entry from the Staff_details table.
    """
    while True:
        nm = input("Enter staff name to remove: ").strip()
        if not nm:
            print("Staff name cannot be blank. Try again.")
        else:
            break
    try:
        # Check if the staff member exists.
        cursor.execute("SELECT Name FROM Staff_details WHERE Name = %s", (nm,))
        result = cursor.fetchone()
        if result:
            cursor.execute("DELETE FROM Staff_details WHERE Name = %s", (nm,))
            db.commit()
            print("Staff successfully removed!")
        else:
            print("Staff does not exist!")
    except Exception as e:
        print("Error removing staff:", e)

def staff_details(cursor):
    """
    Displays all existing staff details.
    """
    try:
        cursor.execute("SELECT * FROM Staff_details")
        result = cursor.fetchall()
        if result:
            print("Existing staff details:")
            for row in result:
                print(row)
        else:
            print("No staff exists!")
    except Exception as e:
        print("Error fetching staff details:", e)

# sales.py
"""
This module contains functions for sales operations:
- Viewing or resetting the sell history.
- Calculating and displaying the total income.
"""

def sell_history(cursor, db):
    """
    Provides an option to view or reset the sell history.
    """
    print("1: View Sell history details")
    print("2: Reset Sell history")
    while True:
        temp = input("Enter your choice: ").strip()
        if not temp:
            print("Choice cannot be blank. Try again.")
        else:
            try:
                choice = int(temp)
                break
            except ValueError:
                print("Please enter a valid integer.")
    if choice == 1:
        try:
            cursor.execute("SELECT * FROM Sell_rec")
            records = cursor.fetchall()
            if records:
                for record in records:
                    print(record)
            else:
                print("No sell records found.")
        except Exception as e:
            print("Error fetching sell history:", e)
    elif choice == 2:
        confirm = input("Are you sure you want to reset sell history? (Y/N): ").strip().upper()
        if confirm == "Y":
            try:
                cursor.execute("DELETE FROM Sell_rec")
                db.commit()
                print("Sell history reset successfully.")
            except Exception as e:
                print("Error resetting sell history:", e)
        else:
            print("Sell history reset cancelled.")
    else:
        print("Invalid choice.")

def income_total(cursor):
    """
    Calculates and displays the total income from sales.
    """
    try:
        cursor.execute("SELECT SUM(Price) FROM Sell_rec")
        result = cursor.fetchone()
        total_income = result[0] if result[0] is not None else 0
        print("Total Income: {} Rs.".format(total_income))
    except Exception as e:
        print("Error calculating income:", e)

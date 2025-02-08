# main.py
"""
This is the entry point for the bookstore management system.
It handles role selection (staff or customer), calls the appropriate
authentication functions, and then enters the main menu loop.
It also plays background music while the program runs.
"""

import pygame

from database import initialize_databases_and_tables
from auth import customer_signup, customer_login, staff_signup, staff_login
from book_management import add_books, buy_book, search_by_name, search_by_genre, search_by_author, available_books
from staff_management import staff_add, staff_remove, staff_details
from sales import sell_history, income_total

def play_background_music():
    """
    Plays background music in a loop using pygame.
    Ensure that 'background.mp3' is in the same directory.
    """
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("chill_tunes.mp3")
        pygame.mixer.music.play(-1)  # Loop indefinitely
        print("Background music playing...")
    except Exception as e:
        print("Could not play background music:", e)

def main():
    # Start background music (non-blocking).
    play_background_music()

    # Initialize the database and tables.
    db, cursor = initialize_databases_and_tables()

    # Role selection.
    current_user_role = None
    current_username = None
    login_bool = False

    while True:
        print("\nPlease select your role:")
        print("1. Staff")
        print("2. Customer")
        role_choice = input("Enter choice (1/2): ").strip()
        if role_choice == '1':
            current_user_role = 'staff'
            break
        elif role_choice == '2':
            current_user_role = 'customer'
            break
        else:
            print("Invalid choice. Please try again.")

    # Staff or Customer signup/login.
    if current_user_role == 'staff':
        print("\n1: Staff Signup\n2: Staff Login")
        while True:
            temp = input("Enter your choice (1 for Signup, 2 for Login): ").strip()
            if not temp:
                print("Choice cannot be blank. Try again.")
                continue
            try:
                choice = int(temp)
                if choice not in [1, 2]:
                    print("Invalid choice. Please enter 1 or 2.")
                    continue
                break
            except ValueError:
                print("Please enter a valid integer (1 or 2).")
        if choice == 1:
            staff_signup(cursor, db)
            # After signup, proceed to login.
            username = staff_login(cursor)
            if username:
                current_username = username
                login_bool = True
        elif choice == 2:
            username = staff_login(cursor)
            if username:
                current_username = username
                login_bool = True
    else:
        print("\n1: Signup\n2: Login")
        while True:
            temp = input("Enter your choice (1 for Signup, 2 for Login): ").strip()
            if not temp:
                print("Choice cannot be blank. Try again.")
                continue
            try:
                choice = int(temp)
                if choice not in [1, 2]:
                    print("Invalid choice. Please enter 1 or 2.")
                    continue
                break
            except ValueError:
                print("Please enter a valid integer (1 or 2).")
        if choice == 1:
            customer_signup(cursor, db)
            username = customer_login(cursor)
            if username:
                current_username = username
                login_bool = True
        elif choice == 2:
            username = customer_login(cursor)
            if username:
                current_username = username
                login_bool = True

    # Main menu loop.
    while login_bool:
        if current_user_role == 'staff':
            print("""
================= STAFF MENU (EXCLUSIVE) =================
1:  Add Books            
2:  Staff Details (Add/Remove/View)
3:  Sell Record (View/Reset)
4:  Available Books (View as table)
5:  Total Income
6:  Buy Books            
7:  Search Books
8:  Exit
==========================================================
            """)
            while True:
                temp = input("Enter your choice: ").strip()
                if not temp:
                    print("Choice cannot be blank. Try again.")
                    continue
                try:
                    choice = int(temp)
                    break
                except ValueError:
                    print("Please enter a valid integer choice.")
            if choice == 1:
                add_books(cursor, db)
            elif choice == 2:
                print("1: New staff entry")
                print("2: Remove staff")
                print("3: Existing staff details")
                while True:
                    temp = input("Enter your choice: ").strip()
                    if not temp:
                        print("Choice cannot be blank. Try again.")
                        continue
                    try:
                        sub_choice = int(temp)
                        break
                    except ValueError:
                        print("Please enter a valid integer.")
                if sub_choice == 1:
                    staff_add(cursor, db)
                elif sub_choice == 2:
                    staff_remove(cursor, db)
                elif sub_choice == 3:
                    staff_details(cursor)
                else:
                    print("Invalid choice.")
            elif choice == 3:
                sell_history(cursor, db)
            elif choice == 4:
                available_books(cursor)
            elif choice == 5:
                income_total(cursor)
            elif choice == 6:
                buy_book(cursor, db, current_user_role, current_username)
            elif choice == 7:
                print("1: Search by name")
                print("2: Search by genre")
                print("3: Search by author")
                while True:
                    temp = input("Enter your choice: ").strip()
                    if not temp:
                        print("Choice cannot be blank. Try again.")
                        continue
                    try:
                        search_choice = int(temp)
                        break
                    except ValueError:
                        print("Please enter a valid integer.")
                if search_choice == 1:
                    search_by_name(cursor)
                elif search_choice == 2:
                    search_by_genre(cursor)
                elif search_choice == 3:
                    search_by_author(cursor)
                else:
                    print("Invalid choice.")
            elif choice == 8:
                print("Exiting... Goodbye!")
                login_bool = False
            else:
                print("Invalid choice. Please try again.")
        else:  # Customer menu.
            print("""
================= CUSTOMER MENU (EXCLUSIVE) =================
1:  Buy Books            
2:  Search Books         
3:  Available Books      
4:  Exit
=============================================================
            """)
            while True:
                temp = input("Enter your choice: ").strip()
                if not temp:
                    print("Choice cannot be blank. Try again.")
                    continue
                try:
                    customer_choice = int(temp)
                    break
                except ValueError:
                    print("Please enter a valid integer choice.")
            if customer_choice == 1:
                buy_book(cursor, db, current_user_role, current_username)
            elif customer_choice == 2:
                print("1: Search by name")
                print("2: Search by genre")
                print("3: Search by author")
                while True:
                    temp = input("Enter your choice: ").strip()
                    if not temp:
                        print("Choice cannot be blank. Try again.")
                        continue
                    try:
                        search_choice = int(temp)
                        break
                    except ValueError:
                        print("Please enter a valid integer.")
                if search_choice == 1:
                    search_by_name(cursor)
                elif search_choice == 2:
                    search_by_genre(cursor)
                elif search_choice == 3:
                    search_by_author(cursor)
                else:
                    print("Invalid choice.")
            elif customer_choice == 3:
                available_books(cursor)
            elif customer_choice == 4:
                print("Exiting... Goodbye!")
                login_bool = False
            else:
                print("Invalid choice. Please try again.")

    # Cleanup: stop background music and close the database connection.
    pygame.mixer.music.stop()
    cursor.close()
    db.close()

if __name__ == '__main__':
    main()

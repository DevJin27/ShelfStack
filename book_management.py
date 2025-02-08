# book_management.py
"""
This module contains functions for managing books:
- Adding new books or updating existing ones.
- Buying books.
- Searching books by name, genre, or author.
- Displaying available books in a table format using pandas.
"""

import pandas as pd

def add_books(cursor, db):
    """
    Adds a new book or updates the quantity of an existing book
    in the Available_Books table.
    """
    print("All information prompted are mandatory to be filled")
    while True:
        temp = input("Enter Book Name: ").strip()
        if not temp:
            print("Book name cannot be blank. Try again.")
        else:
            book = temp
            break
    while True:
        temp = input("Genre: ").strip()
        if not temp:
            print("Genre cannot be blank. Try again.")
        else:
            genre = temp
            break
    while True:
        temp = input("Enter quantity: ").strip()
        if not temp:
            print("Quantity cannot be blank. Try again.")
        else:
            try:
                quantity = int(temp)
                break
            except ValueError:
                print("Please enter a valid integer for quantity.")
    while True:
        temp = input("Enter author name: ").strip()
        if not temp:
            print("Author name cannot be blank. Try again.")
        else:
            author = temp
            break
    while True:
        temp = input("Enter publication house: ").strip()
        if not temp:
            print("Publication house cannot be blank. Try again.")
        else:
            publication = temp
            break
    while True:
        temp = input("Enter the price: ").strip()
        if not temp:
            print("Price cannot be blank. Try again.")
        else:
            try:
                price = int(temp)
                break
            except ValueError:
                print("Please enter a valid integer for price.")
    try:
        cursor.execute("SELECT * FROM Available_Books WHERE BookName = %s", (book,))
        row = cursor.fetchone()
        if row is not None:
            # Update quantity if the book exists.
            cursor.execute(
                "UPDATE Available_Books SET Quantity = Quantity + %s WHERE BookName = %s",
                (quantity, book)
            )
            print("Successfully updated book quantity!")
        else:
            # Insert new book.
            cursor.execute(
                "INSERT INTO Available_Books (BookName, Genre, Quantity, Author, Publication, Price) VALUES (%s, %s, %s, %s, %s, %s)",
                (book, genre, quantity, author, publication, price)
            )
            print("Successfully added new book!")
        db.commit()
    except Exception as e:
        print("An error occurred while adding/updating the book:", e)

def buy_book(cursor, db, current_user_role, current_username):
    """
    Allows a user to purchase a book.
    Displays available books (using pandas), validates the purchase,
    updates the Sell_rec and Available_Books tables.
    """
    print("AVAILABLE BOOKS...")
    try:
        cursor.execute("SELECT * FROM Available_Books")
        books = cursor.fetchall()
        if not books:
            print("No books available.")
            return
        df = pd.DataFrame(books, columns=["BookName", "Genre", "Quantity", "Author", "Publication", "Price"])
        print(df)
    except Exception as e:
        print("Error fetching available books:", e)
        return

    # Determine a new customer ID based on the number of sell records.
    try:
        cursor.execute("SELECT * FROM Sell_rec")
        sell_records = cursor.fetchall()
        cusid = len(sell_records) + 1
    except Exception as e:
        print("Error fetching sell records:", e)
        return

    # Determine customer name.
    if current_user_role == 'customer' and current_username:
        cusname = current_username
    else:
        while True:
            temp = input("Enter customer name: ").strip()
            if not temp:
                print("Customer name cannot be blank. Try again.")
            else:
                cusname = temp
                break

    phno = 0  # Default phone number.
    price = 0 # Default price (could be updated as needed).

    while True:
        temp = input("Enter Book Name to purchase: ").strip()
        if not temp:
            print("Book name cannot be blank. Try again.")
        else:
            book = temp
            break
    while True:
        temp = input("Enter quantity: ").strip()
        if not temp:
            print("Quantity cannot be blank. Try again.")
        else:
            try:
                n = int(temp)
                break
            except ValueError:
                print("Please enter a valid integer for quantity.")

    try:
        cursor.execute("SELECT Quantity FROM Available_Books WHERE BookName = %s", (book,))
        result = cursor.fetchone()
        if result:
            available_quantity = result[0]
            if available_quantity < n:
                print(f"Only {available_quantity} books are available. Cannot purchase {n}.")
                return
            else:
                cursor.execute("SELECT BookName FROM Available_Books WHERE BookName = %s", (book,))
                log = cursor.fetchone()
                if log:
                    cursor.execute(
                        "INSERT INTO Sell_rec (Customer_Id, CustomerName, PhoneNumber, BookName, Quantity, Price) VALUES (%s, %s, %s, %s, %s, %s)",
                        (cusid, cusname, phno, book, n, price)
                    )
                    cursor.execute(
                        "UPDATE Available_Books SET Quantity = Quantity - %s WHERE BookName = %s",
                        (n, book)
                    )
                    db.commit()
                    print("Thank you for shopping!")
                else:
                    print("Book is not available!")
        else:
            print("Book is not available!")
    except Exception as e:
        print("An error occurred during purchase:", e)

def search_by_name(cursor):
    """
    Searches for a book by its name.
    """
    while True:
        book = input("Enter Book to search: ").strip()
        if not book:
            print("Book name cannot be blank. Try again.")
        else:
            break
    try:
        cursor.execute("SELECT BookName FROM Available_Books WHERE BookName = %s", (book,))
        result = cursor.fetchone()
        if result:
            print("Book is in stock!")
        else:
            print("Book is not in stock!")
    except Exception as e:
        print("Error during search:", e)

def search_by_genre(cursor):
    """
    Searches for books by genre.
    """
    while True:
        genre = input("Enter genre to search: ").strip()
        if not genre:
            print("Genre cannot be blank. Try again.")
        else:
            break
    try:
        cursor.execute("SELECT * FROM Available_Books WHERE Genre = %s", (genre,))
        results = cursor.fetchall()
        if results:
            print("Books found:")
            for row in results:
                print(row)
        else:
            print("Books of such genre are not available!")
    except Exception as e:
        print("Error during genre search:", e)

def search_by_author(cursor):
    """
    Searches for books by author.
    """
    while True:
        author = input("Enter author to search: ").strip()
        if not author:
            print("Author name cannot be blank. Try again.")
        else:
            break
    try:
        cursor.execute("SELECT * FROM Available_Books WHERE Author = %s", (author,))
        results = cursor.fetchall()
        if results:
            print("Books by this author:")
            for row in results:
                print(row)
        else:
            print("Books by this author are not available!")
    except Exception as e:
        print("Error during author search:", e)

def available_books(cursor):
    """
    Displays all available books as a table using pandas.
    """
    try:
        cursor.execute("SELECT * FROM Available_Books ORDER BY BookName")
        books = cursor.fetchall()
        if books:
            df = pd.DataFrame(books, columns=["BookName", "Genre", "Quantity", "Author", "Publication", "Price"])
            print(df)
        else:
            print("No available books found.")
    except Exception as e:
        print("Error fetching available books:", e)

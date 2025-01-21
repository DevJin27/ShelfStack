import mysql.connector
import pandas as pd  # ADDED for table display

# =============== ADDED: Global Variables for Role & Username ===============
current_user_role = None       # Will store whether user is 'staff' or 'customer'
current_username = None        # Will store the logged-in username

# =============== ADDED: Staff Tables (Separate from Existing Signup) ===============
def create_staff_table(mycursor):
    """
    Creates a separate table for staff login credentials, if not already present.
    """
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS staff_login(
            username VARCHAR(20) PRIMARY KEY,
            password VARCHAR(20)
        )
    """)

# =============== ADDED: Staff Signup/Login Functions ===============
def staff_signup(mycursor, mydb):
    """
    Registers a new staff member by inserting into staff_login table.
    Handles duplicate usernames.
    """
    print("=== Staff Signup ===")
    # username = input("Enter STAFF username: ").strip()
    # pw = input("Enter STAFF password: ").strip()
    # ADDED: robust input handling for username
    while True:
        temp = input("Enter STAFF username: ")
        temp = temp.strip()
        if not temp:
            print("Username cannot be blank. Please try again.")
            continue
        username = temp
        break

    while True:
        temp = input("Enter STAFF password: ")
        temp = temp.strip()
        if not temp:
            print("Password cannot be blank. Please try again.")
            continue
        pw = temp
        break

    try:
        mycursor.execute(
            "INSERT INTO staff_login (username, password) VALUES (%s, %s)",
            (username, pw)
        )
        mydb.commit()
        print("Staff signup successful!")
    except mysql.connector.IntegrityError:
        print("Staff signup failed. Username may already exist.")
    except Exception as e:
        print("An error occurred during staff signup:", e)

def staff_login(mycursor):
    """
    Authenticates a staff member from staff_login table.
    Returns True if login is successful, False otherwise.
    Also sets global username if successful.
    """
    global current_username

    print("=== Staff Login ===")
    # username = input("Enter STAFF username: ").strip()
    # pw = input("Enter STAFF password: ").strip()
    # ADDED: robust input handling
    while True:
        temp = input("Enter STAFF username: ")
        temp = temp.strip()
        if not temp:
            print("Username cannot be blank. Try again.")
            continue
        username = temp
        break

    while True:
        temp = input("Enter STAFF password: ")
        temp = temp.strip()
        if not temp:
            print("Password cannot be blank. Try again.")
            continue
        pw = temp
        break

    try:
        mycursor.execute(
            "SELECT username FROM staff_login WHERE username = %s AND password = %s",
            (username, pw)
        )
        result = mycursor.fetchone()
        if result:
            print("Staff login successful!")
            current_username = username
            return True
        else:
            print("Invalid STAFF username or password.")
            return False
    except Exception as e:
        print("An error occurred during staff login:", e)
        return False

# ==================== ORIGINAL CODE STARTS HERE ====================

login_bool = False

def signup(mycursor, mydb):
    # username = input("USERNAME: ").strip()
    # pw = input("PASSWORD: ").strip()
    # ADDED robust input handling
    while True:
        temp = input("USERNAME: ")
        temp = temp.strip()
        if not temp:
            print("Username cannot be blank. Try again.")
            continue
        username = temp
        break

    while True:
        temp = input("PASSWORD: ")
        temp = temp.strip()
        if not temp:
            print("Password cannot be blank. Try again.")
            continue
        pw = temp
        break

    try:
        mycursor.execute("INSERT INTO signup (username, password) VALUES (%s, %s)", (username, pw))
        mydb.commit()
        print("SIGNUP SUCCESSFUL")
    except mysql.connector.IntegrityError:
        print("Signup failed. Username may already exist.")
    except Exception as e:
        print("An error occurred:", e)

def login(mycursor):
    global login_bool, current_username

    # username = input("USERNAME: ").strip()
    # ADDED robust input handling
    while True:
        temp = input("USERNAME: ")
        temp = temp.strip()
        if not temp:
            print("Username cannot be blank. Try again.")
            continue
        username = temp
        break

    try:
        mycursor.execute("SELECT username FROM signup WHERE username = %s", (username,))
        user = mycursor.fetchone()

        if user:
            print("VALID USERNAME!!!!!!")
            # pw = input("PASSWORD: ").strip()
            while True:
                temp = input("PASSWORD: ")
                temp = temp.strip()
                if not temp:
                    print("Password cannot be blank. Try again.")
                    continue
                pw = temp
                break

            mycursor.execute("SELECT password FROM signup WHERE username = %s AND password = %s", (username, pw))
            auth = mycursor.fetchone()

            if auth:
                print("+++++++++++++++++++++++\n+++LOGIN SUCCESSFULL+++\n+++++++++++++++++++++++")
                login_bool = True
                current_username = username
            else:
                print("INVALID PASSWORD")
        else:
            print("INVALID USERNAME")
    except Exception as e:
        print("An error occurred:", e)

def add_books(mycursor, mydb):
    print("All information prompted are mandatory to be filled")

    try:
        # book = input("Enter Book Name: ").strip()
        # genre = input("Genre: ").strip()
        # quantity = int(input("Enter quantity: "))
        # author = input("Enter author name: ").strip()
        # publication = input("Enter publication house: ").strip()
        # price = int(input("Enter the price: "))

        while True:
            temp = input("Enter Book Name: ")
            temp = temp.strip()
            if not temp:
                print("Book name cannot be blank. Try again.")
                continue
            book = temp
            break

        while True:
            temp = input("Genre: ")
            temp = temp.strip()
            if not temp:
                print("Genre cannot be blank. Try again.")
                continue
            genre = temp
            break

        while True:
            temp = input("Enter quantity: ")
            temp = temp.strip()
            if not temp:
                print("Quantity cannot be blank. Try again.")
                continue
            try:
                quantity = int(temp)
                break
            except ValueError:
                print("Please enter a valid integer for quantity.")

        while True:
            temp = input("Enter author name: ")
            temp = temp.strip()
            if not temp:
                print("Author name cannot be blank. Try again.")
                continue
            author = temp
            break

        while True:
            temp = input("Enter publication house: ")
            temp = temp.strip()
            if not temp:
                print("Publication house cannot be blank. Try again.")
                continue
            publication = temp
            break

        while True:
            temp = input("Enter the price: ")
            temp = temp.strip()
            if not temp:
                print("Price cannot be blank. Try again.")
                continue
            try:
                price = int(temp)
                break
            except ValueError:
                print("Please enter a valid integer for price.")

        # Check if the book exists
        mycursor.execute("SELECT * FROM Available_Books WHERE bookname = %s", (book,))
        row = mycursor.fetchone()

        if row is not None:
            # Update quantity if book exists
            mycursor.execute(
                "UPDATE Available_Books SET quantity = quantity + %s WHERE bookname = %s",
                (quantity, book),
            )
            print("+++++++++++++++++++++++SUCCESSFULLY ADDED++++++++++++++++++++++++")
        else:
            # Insert new book
            mycursor.execute(
                "INSERT INTO Available_Books (bookname, genre, quantity, author, publication, price) VALUES (%s, %s, %s, %s, %s, %s)",
                (book, genre, quantity, author, publication, price),
            )
            print("++++++++++++++++++++++++SUCCESSFULLY ADDED++++++++++++++++++++++++")
        mydb.commit()
    except ValueError:
        print("Invalid input. Please enter numeric values where required.")
    except Exception as e:
        print("An error occurred:", e)

def buy_book(mycursor, mydb):
    """
    Updated to:
    1) Print available books as a table (pandas).
    2) Only ask for Book Name and Quantity.
    3) Use fetchall() to avoid 'Unread result found' error.
    """
    print("AVAILABLE BOOKS...")

    mycursor.execute("SELECT * FROM Available_Books")
    books = mycursor.fetchall()

    df = pd.DataFrame(books, columns=["BookName", "Genre", "Quantity", "Author", "Publication", "Price"])
    print(df)

    mycursor.execute("SELECT * FROM Sell_rec")
    sell_records = mycursor.fetchall()
    no_of_rows = len(sell_records)
    cusid = no_of_rows + 1

    # If user is 'customer' and we have a valid username, we can use that as customer name
    if current_user_role == 'customer' and current_username:
        cusname = current_username
    else:
        while True:
            temp = input("Enter customer name: ")
            temp = temp.strip()
            if not temp:
                print("Customer name cannot be blank. Try again.")
                continue
            cusname = temp
            break

    phno = 0  # default value
    price = 0  # default value

    # book = input("Enter Book Name: ").strip()
    # n = int(input("Enter quantity: "))
    while True:
        temp = input("Enter Book Name: ")
        temp = temp.strip()
        if not temp:
            print("Book name cannot be blank. Try again.")
            continue
        book = temp
        break

    while True:
        temp = input("Enter quantity: ")
        temp = temp.strip()
        if not temp:
            print("Quantity cannot be blank. Try again.")
            continue
        try:
            n = int(temp)
            break
        except ValueError:
            print("Please enter a valid integer for quantity.")

    # Fetch the available quantity of the book
    mycursor.execute("SELECT quantity FROM available_books WHERE bookname = %s", (book,))
    lk = mycursor.fetchone()

    if lk:
        available_quantity = lk[0]
        if available_quantity < n:
            print(f"{n} Books are not available!!!!")
        else:
            mycursor.execute("SELECT bookname FROM available_books WHERE bookname = %s", (book,))
            log = mycursor.fetchone()

            if log:
                mycursor.execute(
                    "INSERT INTO Sell_rec (Customer_Id, CustomerName, PhoneNumber, BookName, Quantity, Price) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (cusid, cusname, phno, book, n, price)
                )
                mycursor.execute(
                    "UPDATE Available_Books SET quantity = quantity - %s WHERE BookName = %s", (n, book)
                )
                mydb.commit()

                print("++++++++++++++++++++++++THANK YOU FOR SHOPPING++++++++++++++++++++++++")
            else:
                print("BOOK IS NOT AVAILABLE!!!!!!!")
    else:
        print("BOOK IS NOT AVAILABLE!!!!!!!")

def search_bn(mycursor):
    while True:
        o = input("Enter Book to search: ")
        o = o.strip()
        if not o:
            print("Book name cannot be blank. Try again.")
            continue
        break

    mycursor.execute(
        "select bookname from available_books where bookname='{}'".format(o))
    tree = mycursor.fetchone()

    if tree != None:
        print("""++++++++++++++++++++++BOOK IS IN STOCK++++++++++++++++++++++""")
    else:
        print("BOOK IS NOT IN STOCK!!!!!!!")

def search_bg(mycursor):
    while True:
        g = input("Enter genre to search: ")
        g = g.strip()
        if not g:
            print("Genre cannot be blank. Try again.")
            continue
        break

    mycursor.execute(
        "select genre from available_books where genre='{}'".format(g))
    poll = mycursor.fetchall()

    if poll is not None and len(poll) > 0:
        print("""++++++++++++++++++++++BOOK IS IN STOCK++++++++++++++++++++++""")
        mycursor.execute(
            "select * from available_books where genre='{}'".format(g))

        for y in mycursor:
            print(y)
    else:
        print("BOOKS OF SUCH GENRE ARE NOT AVAILABLE!!!!!!!!!")

def search_ba(mycursor):
    while True:
        au = input("Enter author to search: ")
        au = au.strip()
        if not au:
            print("Author name cannot be blank. Try again.")
            continue
        break

    mycursor.execute(
        "select author from available_books where author='{}'".format(au))
    home = mycursor.fetchall()

    if home is not None and len(home) > 0:
        print("""++++++++++++++++++++
++BOOK IS IN STOCK++
++++++++++++++++++++""")
        mycursor.execute(
            "select * from available_books where author='{}'".format(au))

        for z in mycursor:
            print(z)
    else:
        print("BOOKS OF THIS AUTHOR ARE NOT AVAILABLE!!!!!!!")

def staff_add(mycursor):
    mycursor.execute("select * from Staff_details")
    rows = mycursor.rowcount
    staff_id = rows + 1

    # fname = input("Enter Fullname:")
    while True:
        temp = input("Enter Fullname: ")
        temp = temp.strip()
        if not temp:
            print("Fullname cannot be blank. Try again.")
            continue
        fname = temp
        break

    # gender = input("Gender(M/F/O):")
    while True:
        temp = input("Gender(M/F/O): ")
        temp = temp.strip()
        if not temp:
            print("Gender cannot be blank. Try again.")
            continue
        if temp not in ["M","F","O"]:
            print("Invalid gender. Please enter M, F, or O.")
            continue
        gender = temp
        break

    # age = int(input("Age:"))
    while True:
        temp = input("Age: ")
        temp = temp.strip()
        if not temp:
            print("Age cannot be blank. Try again.")
            continue
        try:
            age = int(temp)
            break
        except ValueError:
            print("Please enter a valid integer for age.")

    # phon = int(input("Staff phone no.:"))
    while True:
        temp = input("Staff phone no.: ")
        temp = temp.strip()
        if not temp:
            print("Staff phone number cannot be blank. Try again.")
            continue
        try:
            phon = int(temp)
            break
        except ValueError:
            print("Please enter a valid integer for phone number.")

    # add = input("Address:")
    while True:
        temp = input("Address: ")
        temp = temp.strip()
        if not temp:
            print("Address cannot be blank. Try again.")
            continue
        add = temp
        break

    mycursor.execute(
        "insert into Staff_details values({},'{}','{}',{},{},'{}')".format(staff_id, fname, gender, age, phon, add))
    print("""++++++++++++++++++++++++++++++STAFF IS SUCCESSFULLY ADDED++++++++++++++++++++++++++++++""")

def staff_rem(mycursor):
    # nm = str(input("Enter staff name to remove:"))
    while True:
        temp = input("Enter staff name to remove: ")
        temp = temp.strip()
        if not temp:
            print("Staff name cannot be blank. Try again.")
            continue
        nm = temp
        break

    mycursor.execute("select name from staff_details where name='{}'".format(nm))
    toy = mycursor.fetchone()
    if toy is not None:
        mycursor.execute("delete from staff_details where name='{}'".format(nm))
        print("""+++++++++++++++++++++++++++++++++++STAFF IS SUCCESSFULLY REMOVED+++++++++++++++++++++++++++++++++++""")
    else:
        print("STAFF DOESNOT EXIST!!!!!!")

def staff_det(mycursor):
    mycursor.execute("select * from Staff_details")
    row = mycursor.fetchone()
    if row is not None:
        print("EXISTING STAFF DETAILS...")
        print(row)
        for t in mycursor:
            print(t)
    else:
        print("NO STAFF EXISTS!!!!!!!")

def sell_history(mycursor):
    print("1:Sell history details")
    print("2:Reset Sell history")

    while True:
        temp = input("Enter your choice: ")
        temp = temp.strip()
        if not temp:
            print("Choice cannot be blank. Try again.")
            continue
        try:
            ty = int(temp)
            break
        except ValueError:
            print("Please enter a valid integer (1 or 2).")

    if ty == 1:
        mycursor.execute("select * from sell_rec")
        for u in mycursor:
            print(u)

    if ty == 2:
        bb = input("Are you sure(Y/N):")
        if bb == "Y":
            mycursor.execute("delete from sell_rec")
            mydb.commit()
        elif bb == "N":
            pass

def available_books(mycursor):
    """
    Updated to display available books as a table using pandas.
    """
    mycursor.execute("select * from available_books order by bookname")
    books = mycursor.fetchall()
    df = pd.DataFrame(books, columns=["BookName", "Genre", "Quantity", "Author", "Publication", "Price"])
    print(df)

def income_total(mycursor):
    mycursor.execute("select sum(price) from sell_rec")
    for x in mycursor:
        print(*x,"Rs.")

# =============== DATABASE CONNECTION & SETUP ===============

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Dev230107"
)

mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES LIKE 'books'")
result = mycursor.fetchone()

if not result:
    print("Database 'books' does not exist. Creating it now...")
    mycursor.execute("CREATE DATABASE books")
else:
    print("Database 'books' already exists.")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Dev230107",
    database="books"
)

if mydb.is_connected():
    print("Successfully connected")
mycursor = mydb.cursor()

# Create and use book_store database
mycursor.execute("create database if not exists book_store")
mycursor.execute("use book_store")

# Original tables
mycursor.execute("create table if not exists signup(username varchar (20) primary key,password varchar(20))")
mycursor.execute("create table if not exists Available_Books(BookName varchar(30) primary key,Genre varchar(20),Quantity int,Author varchar(20),Publication varchar(30),Price int)")
mycursor.execute("create table if not exists Sell_rec(Customer_Id integer primary key, CustomerName varchar(20),PhoneNumber int , BookName varchar(30),Quantity int(100),Price int(4))")
mycursor.execute("create table if not exists Staff_details(Staff_id int primary key,Name varchar(30), Gender varchar(10),Age int(3), PhoneNumber int , Address varchar(40))")

# Separate table for staff login
create_staff_table(mycursor)

mydb.commit()
mycursor = mydb.cursor()

# ==================== ROLE SELECTION ====================
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

# ==================== STAFF SIGNUP/LOGIN ====================
if current_user_role == 'staff':
    print("\n1: Staff Signup\n2: Staff Login")
    while True:
        temp = input("STAFF SIGNUP/LOGIN(1,2): ")
        temp = temp.strip()
        if not temp:
            print("Choice cannot be blank. Try again.")
            continue
        try:
            ch = int(temp)
            if ch not in [1, 2]:
                print("Invalid choice. Please enter 1 or 2.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter an integer (1 or 2).")

    if ch == 1:
        staff_signup(mycursor, mydb)
        if staff_login(mycursor):
            login_bool = True
        else:
            login_bool = False
    elif ch == 2:
        if staff_login(mycursor):
            login_bool = True
        else:
            login_bool = False

# ==================== CUSTOMER SIGNUP/LOGIN ====================
else:
    print("\n1: Signup\n2: Login")
    while True:
        temp = input("SIGNUP/LOGIN(1,2): ")
        temp = temp.strip()
        if not temp:
            print("Choice cannot be blank. Try again.")
            continue
        try:
            ch = int(temp)
            if ch not in [1, 2]:
                print("Invalid choice. Please enter 1 for SIGNUP or 2 for LOGIN.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter an integer (1 or 2).")

    if ch == 1:
        signup(mycursor, mydb)
        login(mycursor)
    elif ch == 2:
        login(mycursor)

# ==================== MAIN MENU LOOP ====================
while login_bool:
    # STAFF-ONLY FUNCTIONS
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
            temp = input("Enter your choice: ")
            temp = temp.strip()
            if not temp:
                print("Choice cannot be blank. Try again.")
                continue
            try:
                choice = int(temp)
                break
            except ValueError:
                print("Please enter a valid integer choice.")

        if choice == 1:
            add_books(mycursor, mydb)
        elif choice == 2:
            print("1: New staff entry")
            print("2: Remove staff")
            print("3: Existing staff details")
            while True:
                temp = input("Enter your choice: ")
                temp = temp.strip()
                if not temp:
                    print("Choice cannot be blank. Try again.")
                    continue
                try:
                    ch2 = int(temp)
                    break
                except ValueError:
                    print("Please enter a valid integer.")

            if ch2 == 1:
                staff_add(mycursor)
                mydb.commit()
            elif ch2 == 2:
                staff_rem(mycursor)
            elif ch2 == 3:
                staff_det(mycursor)
                mydb.commit()

        elif choice == 3:
            sell_history(mycursor)
        elif choice == 4:
            available_books(mycursor)
        elif choice == 5:
            income_total(mycursor)
        elif choice == 6:
            buy_book(mycursor, mydb)
        elif choice == 7:
            print("""1:Search by name
2:Search by genre
3:Search by author""")
            while True:
                temp = input("Enter choice: ")
                temp = temp.strip()
                if not temp:
                    print("Choice cannot be blank. Try again.")
                    continue
                try:
                    l = int(temp)
                    break
                except ValueError:
                    print("Please enter a valid integer.")

            if l == 1:
                search_bn(mycursor)
            elif l == 2:
                search_bg(mycursor)
            elif l == 3:
                search_ba(mycursor)
            mydb.commit()
        elif choice == 8:
            login_bool = False
        else:
            print("Invalid choice.")

    # CUSTOMER-ONLY FUNCTIONS
    else:
        print("""
================= CUSTOMER MENU (EXCLUSIVE) =================
1:  Buy Books            
2:  Search Books         
3:  Available Books      
4:  Exit
=============================================================
        """)
        while True:
            temp = input("Enter your choice: ")
            temp = temp.strip()
            if not temp:
                print("Choice cannot be blank. Try again.")
                continue
            try:
                a = int(temp)
                break
            except ValueError:
                print("Please enter a valid integer choice.")

        if a == 1:
            buy_book(mycursor, mydb)
        elif a == 2:
            print("""1:Search by name
2:Search by genre
3:Search by author""")
            while True:
                temp = input("Enter choice: ")
                temp = temp.strip()
                if not temp:
                    print("Choice cannot be blank. Try again.")
                    continue
                try:
                    l = int(temp)
                    break
                except ValueError:
                    print("Please enter a valid integer.")

            if l == 1:
                search_bn(mycursor)
            elif l == 2:
                search_bg(mycursor)
            elif l == 3:
                search_ba(mycursor)
            mydb.commit()

        elif a == 3:
            available_books(mycursor)
        elif a == 4:
            login_bool = False

# End of Script

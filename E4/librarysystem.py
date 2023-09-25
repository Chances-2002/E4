import pymysql.cursors

# 连接数据库
mydb = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',  # name
    passwd='123456',  # password
    db='library',
    charset='utf8'
)

# 创建游标
cursor = mydb.cursor()

# Function to add a new book to the Books table
def add_book():
  title = input("Enter the book title: ")
  author = input("Enter the author: ")
  isbn = input("Enter the ISBN: ")
  status = input("Enter the status: ")

  # Execute the SQL INSERT statement
  add_book_query = "INSERT INTO Books (Title, Author, ISBN, Status) VALUES (%s, %s, %s, %s)"
  book_data = (title, author, isbn, status)
  cursor.execute(add_book_query, book_data)
  mydb.commit()
  print("Book added successfully.")

# Function to find a book's detail based on BookID
def find_book_by_id():
  book_id = input("Enter the BookID: ")

  # Execute the SQL SELECT statement with JOIN to retrieve book details and reservation information
  book_query = '''SELECT Books.*, Users.Name, Users.Email, Reservations.ReservationDate
                  FROM Books
                  LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                  LEFT JOIN Users ON Reservations.UserID = Users.UserID
                  WHERE Books.BookID = %s'''
  cursor.execute(book_query, (book_id,))
  result = cursor.fetchone()

  print(result)  # Print the result tuple to inspect its contents

  if result:
    print("BookID:", result[0])
    print("Title:", result[1])
    print("Author:", result[2])
    print("ISBN:", result[3])
    print("Status:", result[4])

    if result[5]:
      print("Reservation Information:")
      print("Reservation Date:", result[7])
      print("Reserved by:", result[5], "(", result[6], ")")
    else:
      print("Not reserved.")

  else:
    print("Book not found.")

# Function to find a book's reservation status based on BookID, Title, UserID, or ReservationID
def find_reservation_status():
    search_text = input("Enter BookID, Title, UserID, or ReservationID: ")

    # Determine the search type based on the first two letters of the input
    if search_text[:2] == "LB":
        search_type = "Books.BookID"
        search_value = int(search_text[2:])
    elif search_text[:2] == "LU":
        search_type = "Users.UserID"
        search_value = int(search_text[2:])
    elif search_text[:2] == "LR":
        search_type = "Reservations.ReservationID"
        search_value = int(search_text[2:])
    else:
        search_type = "Books.Title"
        search_value = search_text

    # Execute the SQL SELECT statement with JOIN to retrieve reservation status based on the search type
    reservation_query = f'''SELECT Books.BookID, Books.Title, Books.Status, Users.UserID, Users.Name, Users.Email, Reservations.ReservationID, Reservations.ReservationDate
                           FROM Books
                           LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                           LEFT JOIN Users ON Reservations.UserID = Users.UserID
                           WHERE {search_type} = %s'''

    try:
        cursor.execute(reservation_query, (search_value,))
        result = cursor.fetchone()

        if result:
            print("Reservation Information:")
            print("BookID:", result[0])
            print("Title:", result[1])
            print("Status:", result[2])
            print("UserID:", result[3])
            print("User Name:", result[4])
            print("User Email:", result[5])
            print("ReservationID:", result[6])
            print("Reservation Date:", result[7])
        else:
            print("No reservation found for the given search.")
    except pymysql.Error as e:
        print("An error occurred while fetching the reservation:", str(e))

# Function to find all the books in the database
def find_all_books():
  # Execute the SQL SELECT statement with JOIN to retrieve all book details and reservation information
  all_books_query = '''SELECT Books.*, Users.UserID, Users.Name, Users.Email, Reservations.ReservationID, Reservations.ReservationDate
                       FROM Books
                       LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                       LEFT JOIN Users ON Reservations.UserID = Users.UserID'''

  cursor.execute(all_books_query)
  results = cursor.fetchall()
  print(results)

  if results:
    for result in results:
      print("BookID:", result[0])
      print("Title:", result[1])
      print("Author:", result[2])
      print("ISBN:", result[3])
      print("Status:", result[4])

      if result[5]:
        print("Reservation Information:")
        print("Reservation Date:", result[9])
        print("Reserved by:", result[6], "(", result[7], ")")
      else:
       print("Not reserved.")
  else:
    print("No books found in the database.")

# Function to modify/update book details based on its BookID
def update_book_details():
  book_id = input("Enter the BookID: ")
  new_title = input("Enter the new title (leave blank to skip): ")
  new_author = input("Enter the new author (leave blank to skip): ")
  new_isbn = input("Enter the new ISBN (leave blank to skip): ")
  new_status = input("Enter the new status (leave blank to skip): ")

  # Build the SQL UPDATE statement based on the provided input
  update_query = "UPDATE Books SET"
  update_data = []

  if new_title:
    update_query += " Title = %s,"
    update_data.append(new_title)
  if new_author:
    update_query += " Author = %s,"
    update_data.append(new_author)
  if new_isbn:
    update_query += " ISBN = %s,"
    update_data.append(new_isbn)
  if new_status:
    update_query += " Status = %s,"
    update_data.append(new_status)

  # Remove the trailing comma and add the WHERE clause
  update_query = update_query.rstrip(",") + " WHERE BookID = %s"
  update_data.append(book_id)

  # Execute the SQL UPDATE statement
  cursor.execute(update_query, update_data)
  mydb.commit()
  print("Book details updated successfully.")

# Function to delete a book based on its BookID
def delete_book():
  book_id = input("Enter the BookID: ")

  # Execute the SQL DELETE statement to delete the book and its reservation (if any)
  delete_query = "DELETE Books, Reservations FROM Books LEFT JOIN Reservations ON Books.BookID = Reservations.BookID WHERE Books.BookID = %s"
  cursor.execute(delete_query, (book_id,))
  mydb.commit()
  print("Book deleted successfully.")

# Main program loop
while True:
  print("\n--- Library Database Menu ---")
  print("1. Add a new book to the database")
  print("2. Find a book's detail based on BookID")
  print("3. Find a book's reservation status")
  print("4. Find all the books in the database")
  print("5. Modify/update book details based on BookID")
  print("6. Delete a book based on BookID")
  print("7. Exit")
  choice = input("Enter your choice (1-7): ")

  if choice == "1":
    add_book()
  elif choice == "2":
    find_book_by_id()
  elif choice == "3":
    find_reservation_status()
  elif choice == "4":
    find_all_books()
  elif choice == "5":
    update_book_details()
  elif choice == "6":
    delete_book()
  elif choice == "7":
    break
  else:
    print("Invalid choice. Please try again.")

# Close the cursor and database connection
cursor.close()
mydb.close()
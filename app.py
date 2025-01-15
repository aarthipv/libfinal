from flask import Flask, render_template, request, redirect, session, flash
from flask_mysqldb import MySQL
from datetime import datetime
import bcrypt

app = Flask(__name__)
app.secret_key = "supersecretkey"

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'library_db'

mysql = MySQL(app)

# Home Route
@app.route('/')
def home():
    return render_template('home.html')

# Librarian Login
@app.route('/librarian_login', methods=['GET', 'POST'])
def librarian_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM librarians WHERE email = %s", [email])
        librarian = cur.fetchone()
        cur.close()

        if librarian and librarian[2] == password:
            session['librarian_id'] = librarian[0]
            # flash('Logged in successfully!', 'success')
            return redirect('/librarian_dashboard')
        else:
            flash('Invalid credentials!', 'danger')
    return render_template('librarian_login.html')

# Librarian Dashboard
@app.route('/librarian_dashboard')
def librarian_dashboard():
    if 'librarian_id' in session:
        return render_template('librarian_dashboard.html')
    return redirect('/librarian_login')

# Add Book
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if 'librarian_id' in session:  # Make sure the user is logged in
        if request.method == 'POST':
            title = request.form['title']
            author = request.form['author']
            isbn = request.form['isbn']
            available = request.form['available'] if request.form['available'] else 1  # Default available to 1 if not specified

            cur = mysql.connection.cursor()
            
            # Check if the ISBN is already in the database
            cur.execute("SELECT * FROM books WHERE isbn = %s", [isbn])
            existing_book = cur.fetchone()

            if existing_book:
                flash('A book with this ISBN already exists.', 'danger')
            else:
                try:
                    cur.execute("""
                        INSERT INTO books (title, author, isbn, available) 
                        VALUES (%s, %s, %s, %s)
                    """, (title, author, isbn, available))
                    mysql.connection.commit()
                    # flash('Book added successfully!', 'success')
                except Exception as e:
                    mysql.connection.rollback()
                    flash(f'Error adding book: {e}', 'danger')

            cur.close()
            return redirect('/librarian_dashboard')  # Redirect to dashboard or any appropriate page after adding

        return render_template('add_book.html')  # Render the add book form

    return redirect('/librarian_login')  # Redirect to login if not logged in

# Remove Book
@app.route('/remove_book', methods=['GET', 'POST'])
def remove_book():
    if 'librarian_id' in session:
        if request.method == 'POST':
            book_id = request.form['book_id']

            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM books WHERE book_id = %s", [book_id])
            mysql.connection.commit()
            cur.close()
            # flash('Book removed successfully!', 'success')
            return redirect('/librarian_dashboard')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM books")
        books = cur.fetchall()
        cur.close()
        return render_template('remove_book.html', books=books)
    return redirect('/librarian_login')

# Manage Users (Librarian)
@app.route('/manage_users', methods=['GET'])
def manage_users():
    # Check if the user is logged in and is a librarian
    if 'librarian_id' in session: 
        cur = mysql.connection.cursor()

        # Query to get the users and their borrowed books
        cur.execute("""
            SELECT u.user_id, u.name, u.email, bb.book_id, b.title, b.author, bb.due_date
            FROM users u
            LEFT JOIN borrowed_books bb ON u.user_id = bb.user_id AND bb.status = 'borrowed'
            LEFT JOIN books b ON bb.book_id = b.book_id
        """)
        users_data = cur.fetchall()
        cur.close()

        # Debug: print the raw data from the database
        print("Users Data:", users_data)

        # Organize the borrowed books by user
        users = []
        for user in users_data:
            user_id = user[0]
            # Check if the user already exists in the list
            existing_user = next((u for u in users if u['user_id'] == user_id), None)
            if not existing_user:
                existing_user = {
                    'user_id': user[0],
                    'name': user[1],
                    'email': user[2],
                    'borrowed_books': []
                }
                users.append(existing_user)

            if user[3]:  # If the user has borrowed a book
                borrowed_book = {
                    'title': user[4],
                    'author': user[5],
                    'due_date': user[6]
                }
                existing_user['borrowed_books'].append(borrowed_book)

        # Debug: print the organized data for users
        print("Organized Users Data:", users)

        return render_template('manage_users.html', users=users)

    return redirect('/librarian_login')
@app.route('/list_books', methods=['GET'])
def list_books():
    if 'librarian_id' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM books")
        books = cur.fetchall()
        cur.close()
        return render_template('list_books.html', books=books)
    return redirect('/librarian_login')

# User Login
@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", [email])
        user = cur.fetchone()
        cur.close()

        if user and user[3] == password:
            session['user_id'] = user[0]
            # flash('Logged in successfully!', 'success')
            return redirect('/user_dashboard')
        else:
            flash('Invalid credentials!', 'danger')
    return render_template('user_login.html')

# User Dashboard
@app.route('/user_dashboard')
def user_dashboard():
    if 'user_id' in session:
        return render_template('user_dashboard.html')
    return redirect('/user_login')

# Borrow Book
@app.route('/borrow_book', methods=['GET', 'POST'])
def borrow_book():
    if 'user_id' in session:
        if request.method == 'POST':
            book_id = request.form['book_id']
            user_id = session['user_id']
            due_date = request.form['due_date']

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO borrowed_books (user_id, book_id, due_date) VALUES (%s, %s, %s)", 
                        (user_id, book_id, due_date))
            cur.execute("UPDATE books SET available = available - 1 WHERE book_id = %s", [book_id])
            mysql.connection.commit()
            cur.close()
            # flash('Book borrowed successfully!', 'success')
            return redirect('/user_dashboard')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM books WHERE available > 0")
        books = cur.fetchall()
        cur.close()
        return render_template('borrow_book.html', books=books)
    return redirect('/user_login')

# Search Book
@app.route('/search_book', methods=['GET', 'POST'])
def search_book():
    if 'user_id' in session:
        if request.method == 'POST':
            search_query = request.form['search_query']
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM books WHERE title LIKE %s OR author LIKE %s", ('%' + search_query + '%', '%' + search_query + '%'))
            books = cur.fetchall()
            cur.close()
            return render_template('search_book.html', books=books)
        return render_template('search_book.html')
    return redirect('/user_login')

# Overdue Books

@app.route('/overdue_books', methods=['GET'])
def overdue_books():
    if 'user_id' in session:
        user_id = session['user_id']
        cur = mysql.connection.cursor()

        # Query for overdue books (borrowed books with a past due date and not returned)
        cur.execute("""
            SELECT b.book_id, b.title, b.author, bb.due_date
            FROM borrowed_books bb
            JOIN books b ON bb.book_id = b.book_id
            WHERE bb.user_id = %s
            AND bb.return_date IS NULL
            AND bb.due_date < %s
        """, (user_id, datetime.now().date()))
        overdue_books = cur.fetchall()

        # Query for borrowed books (not returned yet)
        cur.execute("""
            SELECT b.book_id, b.title, b.author, bb.due_date
            FROM borrowed_books bb
            JOIN books b ON bb.book_id = b.book_id
            WHERE bb.user_id = %s
            AND bb.return_date IS NULL
        """, (user_id,))
        borrowed_books = cur.fetchall()

        cur.close()
        return render_template('overdue_books.html', overdue_books=overdue_books, borrowed_books=borrowed_books)
    
    return redirect('/user_login')

# Register (User)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", 
                    (name, email, hashed_password))
        mysql.connection.commit()
        cur.close()
        # flash('Registration successful! Please log in.', 'success')
        return redirect('/user_login')

    return render_template('register.html')

@app.route('/return_book', methods=['GET', 'POST'])
def return_book():
    if 'user_id' in session:
        if request.method == 'POST':
            borrow_id = request.form['borrow_id']
            book_id = request.form['book_id']

            cur = mysql.connection.cursor()

            # First, check if the book is indeed borrowed by the current user
            cur.execute("""
                SELECT * FROM borrowed_books 
                WHERE borrow_id = %s AND book_id = %s AND user_id = %s AND status = 'borrowed'
            """, (borrow_id, book_id, session['user_id']))
            borrowed_book = cur.fetchone()

            if borrowed_book:
                # Update the borrowed_books table to mark the book as returned
                cur.execute("""
                    UPDATE borrowed_books 
                    SET return_date = CURDATE(), status = 'returned' 
                    WHERE borrow_id = %s
                """, [borrow_id])

                # Update the books table to increment the availability
                cur.execute("""
                    UPDATE books 
                    SET available = available + 1 
                    WHERE book_id = %s
                """, [book_id])

                mysql.connection.commit()
                # flash('Book returned successfully!', 'success')
            else:
                flash('Invalid book return request or book is already returned.', 'danger')

            cur.close()
            return redirect('/user_dashboard')

        # GET request: Show borrowed books that are not yet returned
        user_id = session['user_id']
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT bb.borrow_id, bb.book_id, b.title, b.author 
            FROM borrowed_books bb
            JOIN books b ON bb.book_id = b.book_id
            WHERE bb.user_id = %s AND bb.status = 'borrowed'
        """, [user_id])
        borrowed_books = cur.fetchall()
        cur.close()
        return render_template('return_book.html', borrowed_books=borrowed_books)

    return redirect('/user_login')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    # flash('Logged out successfully!', 'info')
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)

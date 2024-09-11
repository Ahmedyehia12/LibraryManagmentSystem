from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from prometheus_client import start_http_server, Counter
#hi there
import json
#trying commit


# Create a metric to track the number of requests
REQUEST_COUNTER = Counter('http_requests_total', 'Total number of HTTP requests')

app = Flask(__name__)
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

library_url = 'data/library.json'
users_url = 'data/users.json'

class library: # Where all common functions between users and admins are stored
    def __init__(self):
        pass
    
    def getInventory(self):
        try:
            with open(library_url, 'r') as file:  # Open the file in read mode
                data = json.load(file) # Load the json data from the file
                return data # Return the data
        except FileNotFoundError: # If the file is not found
            return "File Not Found!" # Return an empty dictionary
    
    def getUsers(self):
        try:
            with open(users_url, 'r') as file:  # Open the file in read mode
                data = json.load(file) # Load the json data from the file
                return data # Return the data
        except FileNotFoundError: # If the file is not found
            return "File Not Found!" # Return an empty dictionary
        

    def saveUser(self, User):
        try:
            with open(users_url, 'w') as file: # Open the file in write mode
                json.dump(User, file) # Write the data to the file
        except FileNotFoundError: # If the file is not found
            return FileNotFoundError # Return the error
        

    def getBooks(self,keyword):
        inventory = self.getInventory() # Get the inventory
        result = [] # Create an empty list to store the search results
        for book in inventory['books']:  # Iterate through the books in the inventory
            if keyword.lower() in book['title'].lower() or keyword.lower() in book['author'].lower() or keyword == book['isbn']:
                result.append(book) # If the keyword is found in the title, author or isbn, add the book to the result list
        return result
    def generateISBN(self):
        inventory = self.getInventory()
        isbn = 0
        for book in inventory['books']:
            current_isbn = book['isbn']
            #convert to integer
            current_isbn = int(current_isbn)
            isbn = max(isbn, current_isbn)
        return isbn + 1

    def getBook(self,isbn):
        inventory = self.getInventory() # Get the inventory
        for book in inventory['books']: # Iterate through the books in the inventory
            if book['isbn'] == isbn: # If the isbn matches
                return book # Return the book@app.route('/') # Home route
    def index():
        books = library().getInventory()
        return render_template('index.html', books=books['books']) # Render the index.html template with the books
    
    @app.route('/searchBooks') # Request parameter : keyword
    @login_required
    def search():
        keyword = request.form['keyword'] # Get the keyword from the form
        books = library().getBooks(keyword) # Get the books that match the keyword
        return jsonify(books) # Return the books as a json response
    
    @app.route('/search') # Request parameter : isbn
    @login_required
    def searchBook():
        isbn = request.form['isbn'] # Get the isbn from the form
        book = library().getBook(isbn) # Get the book with the given isbn
        return jsonify(book) # Return the book as a json response



class Admin_User(UserMixin, library): # Admin Privileges
    def __init__(self, username):
        self.id = username

    @login_required
    def addBook(self, title , author, genre, date): # Function to add a book to the inventory
        inventory = library().getInventory() # Get the inventory
        isbn = library().generateISBN() # Generate a new isbn
        if library().getBook(isbn): # If the book already exists
            return False # Return False
        inventory['books'].append({ # Append the new book to the inventory
            "title" : title, # Title of the book
            "author" : author,
            "isbn" : isbn,
            "genre": genre,
            "date_of_publish": date,
            "status" : "Available"
        })
        self.saveInventory(inventory) # Save the inventory
        return True # Return True
    
    def saveInventory(self, Inventory):
        try:
            with open(library_url , 'w') as file: # Open the file in write mode
                json.dump(Inventory ,    file) # Write the data to the file
        except FileNotFoundError: # If the file is not found
            return FileNotFoundError # Return the error
    
    @login_required
    def removeBook(self, isbn): # Function to remove a book from the inventory
        inventory = library().getInventory() # Get the inventory
        inventory['books'] = [book for book in inventory['books'] if book['isbn'] != isbn] # Remove the book with the given isbn
        self.saveInventory(inventory) # Save the inventory  

    @login_required
    def addAnotherAdmin(self, username, password): # Function to add another admin
        users = library().getUsers() # Get the users
        users[username] = {"password": password, "role": "Admin"} # Add the new admin to the users
        library().saveUser(users) # Save the users
    
        

class User(UserMixin, library): # Normal User Privileges
    def __init__(self, username):
        self.id = username  

    @login_manager.user_loader
    def load_user(username):
        users_db = library().getUsers()
        if username in users_db.keys():
            user = users_db[username]
            return User(user)
        return None

    @login_required
    def borrowBook(self, isbn): # Function to borrow a book
        inventory = library().getInventory() # Get the inventory
        for book in inventory['books']: # Iterate through the books in the inventory
            if book['isbn'] == isbn and book['status'] == 'Available': # If the isbn matches and the book is available
                book['status'] = 'Borrowed' # Change the status to borrowed
                Admin_User(None).saveInventory(inventory) # Save the inventory
                return True # Return True
        return False # Return False
    
    @login_required
    def returnBorrowedBook(isbn):
        inventory = library().getInventory() # Get the inventory
        for book in inventory['books']: # Iterate through the books in the inventory
            if book['isbn'] == isbn: # If the isbn matches
                book['status'] = 'Available' # Change the status to available
                Admin_User(None).saveInventory(inventory) # Save the inventory
                return True # Return True
        return False


@app.route('/admin_home') # Home route
@login_required
def index():
    if current_user.id['role'] == 'User':
        flash('You do not have permission to access the admin page')
        return redirect(url_for('index_user'))
    books = library().getInventory()
    return render_template('index.html', books=books['books']) # Render the index.html template with the books
# Home route


@app.route('/home')
@login_required
def index_user():
    if current_user.id['role'] == 'Admin':
        flash('You do not have permission to access the user page')
        return redirect(url_for('index'))
    books = library().getInventory()
    return render_template('index_user.html', books=books['books']) # Render the index.html template with the books

@app.route('/add_book', methods=['POST']) # Request method : POST
def add_book(): # Function to add a book
    if current_user.id['role'] == 'User':
        flash('You do not have permission to add a book')
        return redirect(url_for('index_user'))
    title = request.form['title'] # Get the title from the form
    author = request.form['author'] # Get the author from the form
    genre = request.form['genre'] # Get the genre of the book
    date = request.form['date_of_publish'] # get the date of publish
    Admin_User(None).addBook(title , author , genre, date) # Add the book to the inventory
    return redirect(url_for('index')) # Redirect to the index page

@app.route('/remove_book/<isbn>', methods=["GET", "POST"]) # Request parameter : isbn
def remove_book(isbn): # Function to remove a book
    if current_user.id['role'] == 'User':
        flash('You do not have permission to remove a book')
        return redirect(url_for('index_user'))
    Admin_User(None).removeBook(isbn) # Remove the book from the inventory
    return redirect(url_for('index')) # Redirect to the index page

@app.route('/borrow_book/<isbn>', methods=["POST"]) # Request parameter : isbn
def borrow_book(isbn): # Function to borrow a book
    if current_user.id['role'] == 'Admin':
        flash('You do not have permission to borrow a book')
        return redirect(url_for('index'))
    if User(None).borrowBook(isbn): # If the book is borrowed successfully
        return redirect(url_for('index_user')) # Redirect to the index page
    flash("An Unexpected Error Occured D:")
    return redirect(url_for('index_user')) # Redirect to the index page

@app.route('/return_book/<isbn>', methods=["POST"]) # Request parameter : isbn
def return_book(isbn): # Function to return a borrowed book
    if current_user.id['role'] == 'Admin':
        flash('You do not have permission to return a book')
        return redirect(url_for('index'))
    if User.returnBorrowedBook(isbn): # If the book is returned successfully
        return redirect(url_for('index_user')) # Redirect to the index page
    flash("An Unexpected Error Occured D:")
    return redirect(url_for('index_user')) # Redirect to the index page


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users_db = library().getUsers()
        if username in users_db and users_db[username]['password'] == password:
            role = users_db[username]['role']
            if role == "Admin":
                user = Admin_User(username)
                login_user(user)
                return redirect(url_for('index'))
            else:
                user = User(username)
                login_user(user)
                return redirect(url_for("index_user"))

            
        flash('Invalid credentials')
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])   
def logout():
    logout_user()
    session.clear()  # Optional: clear the session
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # newest_user_id = users_db[list(users_db.keys())[-1]]
        users_db = library().getUsers()
        if username not in users_db.keys():
            users_db[username] = {"password": password, "role": "User", "id":200}
            library().saveUser(users_db)
            flash('Signup successful! You can now log in.')
            return redirect(url_for('login'))
        flash('Username already exists')
    return render_template('signup.html')


# the root route should direct to the login page
@app.route('/' , methods=['GET', 'POST'])
def root():
    REQUEST_COUNTER.inc()  # Increment the counter
    return redirect(url_for('login'))



@app.route('/add_admin', methods=['GET', 'POST'])
def add_admin():
    if current_user.id['role'] == 'User':
        flash('You do not have permission to add an admin')
        return redirect(url_for('index_user'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        Admin_User(None).addAnotherAdmin(username, password)
        return redirect(url_for('index'))
    return render_template('add_admin.html')



if __name__ == '__main__':
    start_http_server(8000)
    app.run(host="0.0.0.0", port=5000)
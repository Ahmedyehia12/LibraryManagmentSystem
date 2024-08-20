from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class library: # Where all common functions between users and admins are stored
    def __init__(self):
        pass
    
    def getInventory(self):
        try:
            with open('library.json', 'r') as file:  # Open the file in read mode
                data = json.load(file) # Load the json data from the file
                return data # Return the data
        except FileNotFoundError: # If the file is not found
            return "File Not Found!" # Return an empty dictionary
    
    def getUsers(self):
        try:
            with open('users.json', 'r') as file:  # Open the file in read mode
                data = json.load(file) # Load the json data from the file
                return data # Return the data
        except FileNotFoundError: # If the file is not found
            return "File Not Found!" # Return an empty dictionary
        

    def saveUser(self, User):
        try:
            with open('users.json', 'w') as file: # Open the file in write mode
                json.dump(User, file) # Write the data to the file
        except FileNotFoundError: # If the file is not found
            return FileNotFoundError # Return the error
        

    def getBooks(self,keyword):
        inventory = self.getInventory() # Get the inventory
        result = [] # Create an empty list to store the search results
        for book in inventory:  # Iterate through the books in the inventory
            if keyword.lower() in book['title'].lower() or keyword.lower() in book['author'].lower() or keyword == book['isbn']:
                result.append(book) # If the keyword is found in the title, author or isbn, add the book to the result list
        return result

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
    def addBook(self, title , author , isbn, genre, date): # Function to add a book to the inventory
        inventory = library().getInventory() # Get the inventory
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
            with open('library.json' , 'w') as file: # Open the file in write mode
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
    books = library().getInventory()
    return render_template('index.html', books=books['books']) # Render the index.html template with the books
# Home route


@app.route('/home')
@login_required
def index_user():
    books = library().getInventory()
    return render_template('index_user.html', books=books['books']) # Render the index.html template with the books

@app.route('/add_book', methods=['POST']) # Request method : POST
def add_book(): # Function to add a book
    if library().getBook(request.form['isbn']): # If the book already exists
        flash("Book already exists!")
        return redirect(url_for('index')) # Redirect to the index page
    title = request.form['title'] # Get the title from the form
    author = request.form['author'] # Get the author from the form
    isbn = request.form['isbn'] # Get the isbn from the form
    genre = request.form['genre'] # Get the genre of the book
    date = request.form['date_of_publish'] # get the date of publish
    Admin_User(None).addBook(title , author , isbn, genre, date) # Add the book to the inventory
    return redirect(url_for('index')) # Redirect to the index page

@app.route('/remove_book/<isbn>', methods=["GET", "POST"]) # Request parameter : isbn
def remove_book(isbn): # Function to remove a book
    Admin_User(None).removeBook(isbn) # Remove the book from the inventory
    return redirect(url_for('index')) # Redirect to the index page

@app.route('/borrow_book/<isbn>', methods=["POST"]) # Request parameter : isbn
def borrow_book(isbn): # Function to borrow a book
    if User(None).borrowBook(isbn): # If the book is borrowed successfully
        return redirect(url_for('index_user')) # Redirect to the index page
    flash("An Unexpected Error Occured D:")
    return redirect(url_for('index_user')) # Redirect to the index page

@app.route('/return_book/<isbn>', methods=["POST"]) # Request parameter : isbn
def return_book(isbn): # Function to return a borrowed book
    if User.returnBorrowedBook(isbn): # If the book is returned successfully
        return redirect(url_for('index_user')) # Redirect to the index page
    flash("An Unexpected Error Occured D:")
    return redirect(url_for('index_user')) # Redirect to the index page

users_db = library().getUsers()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
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
        if username not in users_db.keys():
            users_db[username] = {"password": password, "role": "User", "id":200}
            library().saveUser(users_db)
            flash('Signup successful! You can now log in.')
            return redirect(url_for('login'))
        flash('Username already exists')
    return render_template('signup.html')

@app.route('/add_admin', methods=['GET', 'POST'])
def add_admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        Admin_User(None).addAnotherAdmin(username, password)
        return redirect(url_for('index'))
    return render_template('add_admin.html')



if __name__ == '__main__':
    app.run(debug=True)

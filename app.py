from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Inventory management functions
def getInventory():
    try:
        with open('library.json', 'r') as file:  # Open the file in read mode
            data = json.load(file) # Load the json data from the file
            return data # Return the data
    except FileNotFoundError: # If the file is not found
        return {"books":[] } # Return an empty dictionary
    
def saveInventory(Inventory):
    try:
        with open('library.json' , 'w') as file: # Open the file in write mode
            json.dump(Inventory ,    file) # Write the data to the file
    except FileNotFoundError: # If the file is not found
        return FileNotFoundError # Return the error

def addBook(title , author , isbn): # Function to add a book to the inventory
    inventory = getInventory() # Get the inventory
    inventory['books'].append({ # Append the new book to the inventory
        "title" : title, # Title of the book
        "author" : author,  
        "isbn" : isbn, 
        "status" : "Available"
    })
    saveInventory(inventory) # Save the inventory

def removeBook(isbn): # Function to remove a book from the inventory
    inventory = getInventory() # Get the inventory
    inventory['books'] = [book for book in inventory['books'] if book['isbn'] != isbn] # Remove the book with the given isbn
    saveInventory(inventory) # Save the inventory

def getBooks(keyword):
    inventory = getInventory() # Get the inventory
    result = [] # Create an empty list to store the search results
    for book in inventory:  # Iterate through the books in the inventory
        if keyword.lower() in book['title'].lower() or keyword.lower() in book['author'].lower() or keyword == book['isbn']:
            result.append(book) # If the keyword is found in the title, author or isbn, add the book to the result list
    return result

def getBook(isbn):
    inventory = getInventory() # Get the inventory
    for book in inventory['books']: # Iterate through the books in the inventory
        if book['isbn'] == isbn: # If the isbn matches
            return book # Return the book
        
def borrowBook(isbn): # Function to borrow a book
    inventory = getInventory() # Get the inventory
    for book in inventory['books']: # Iterate through the books in the inventory
        if book['isbn'] == isbn and book['status'] == 'Available': # If the isbn matches and the book is available
            book['status'] = 'Borrowed' # Change the status to borrowed
            saveInventory(inventory) # Save the inventory
            return True # Return True
    return False # Return False

def returnBorrowedBook(isbn):
    inventory = getInventory() # Get the inventory
    for book in inventory['books']: # Iterate through the books in the inventory
        if book['isbn'] == isbn: # If the isbn matches
            book['status'] = 'Available' # Change the status to available
            saveInventory(inventory) # Save the inventory
            return True # Return True
    return False


def load_users_db():
    with open('users_db.json', 'r') as f:
        return json.load(f)
    
def save_users_db(users_db):
    with open('users_db.json', 'w') as f:
        json.dump(users_db, f)


# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class
class User(UserMixin):
    def __init__(self, username, role):
        self.id = username
        self.role = role

@login_manager.user_loader
def load_user(username):
    users_db = load_users_db()
    if username in users_db:
        user = users_db[username]
        return User(username, user['role'])
    return None

# Inventory management functions (unchanged)
# ...

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    users_db = load_users_db()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users_db and users_db[username]['password'] == password:
            user = User(username, users_db[username]['role'])
            login_user(user) # this will log the user in, you can access the logged in user with current_user this is a flask_login function
            return redirect(url_for('index'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    users_db = load_users_db()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        if username not in users_db:
            users_db[username] = {"password": password, "role": role}
            save_users_db(users_db)
            flash('Signup successful! You can now log in.')
            return redirect(url_for('login'))
        flash('Username already exists')
    return render_template('signup.html')

# Access control for book management
@app.route('/add_book', methods=['POST'])
@login_required
def add_book():
    if current_user.role != 'admin':
        flash('Only admins can add books.')
        return redirect(url_for('index'))
    # Add book logic...
    addBook(request.form['title'], request.form['author'], request.form['isbn'])
    return redirect(url_for('index'))

@app.route('/remove_book/<isbn>')
@login_required
def remove_book(isbn):
    if current_user.role != 'admin':
        flash('Only admins can remove books.')
        return redirect(url_for('index'))
    # Remove book logic...
    removeBook(isbn)
    return redirect(url_for('index'))


# Access control for borrowing and returning books
@app.route('/borrow_book/<isbn>')
@login_required
def borrow_book(isbn):
    if current_user.role != 'user':
        flash('Only users can borrow books.')
        return redirect(url_for('index'))
    # Borrow book logic...
    borrowBook(isbn)
    return redirect(url_for('index'))

@app.route('/return_book/<isbn>')
@login_required
def return_book(isbn):
    if current_user.role != 'user':
        flash('Only users can return books.')
        return redirect(url_for('index'))
    # Return book logic...
    returnBorrowedBook(isbn)
    return redirect(url_for('index'))

# Home route with access control
@app.route('/')
@login_required
def index():
    books = getInventory()
    return render_template('index.html', books=books['books'], user_role=current_user.role)

if __name__ == '__main__':
    app.run(debug=True)

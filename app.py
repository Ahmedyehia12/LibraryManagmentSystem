from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)



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

@app.route('/') # Home route
def index():
    books = getInventory()
    return render_template('index.html', books=books['books']) # Render the index.html template with the books

@app.route('/add_book', methods=['POST']) # Request method : POST
def add_book(): # Function to add a book
    if getBook(request.form['isbn']): # If the book already exists
        return redirect(url_for('index')) # Redirect to the index page
    title = request.form['title'] # Get the title from the form
    author = request.form['author'] # Get the author from the form
    isbn = request.form['isbn'] # Get the isbn from the form
    addBook(title , author , isbn) # Add the book to the inventory
    return redirect(url_for('index')) # Redirect to the index page

@app.route('/remove_book/<isbn>') # Request parameter : isbn
def remove_book(isbn): # Function to remove a book
    removeBook(isbn) # Remove the book from the inventory
    return redirect(url_for('index')) # Redirect to the index page  

@app.route('/searchBooks') # Request parameter : keyword
def search():
    keyword = request.form['keyword'] # Get the keyword from the form
    books = getBooks(keyword) # Get the books that match the keyword
    return jsonify(books) # Return the books as a json response

@app.route('/search') # Request parameter : isbn
def searchBook():
    isbn = request.form['isbn'] # Get the isbn from the form
    book = getBook(isbn) # Get the book with the given isbn
    return jsonify(book) # Return the book as a json response


@app.route('/borrow_book/<isbn>') # Request parameter : isbn
def borrow_book(isbn): # Function to borrow a book
    if borrowBook(isbn): # If the book is borrowed successfully
        return redirect(url_for('index')) # Redirect to the index page
    return redirect(url_for('index')) # Redirect to the index page

@app.route('/return_book/<isbn>') # Request parameter : isbn
def return_book(isbn): # Function to return a borrowed book
    if returnBorrowedBook(isbn): # If the book is returned successfully
        return redirect(url_for('index')) # Redirect to the index page
    return redirect(url_for('index')) 

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)



def getInventory():
    try:
        with open('library.json', 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return {"books":[] }
    
def saveInventory(Inventory):
    try:
        with open('library.json' , 'w') as file:
            json.dump(Inventory , file)
    except FileNotFoundError:
        return FileNotFoundError

def addBook(title , author , isbn):
    inventory = getInventory()
    inventory['books'].append({
        "title" : title,
        "author" : author,
        "isbn" : isbn,
        "status" : "Available"
    })
    saveInventory(inventory)

def removeBook(isbn):
    inventory = getInventory()
    inventory['books'] = [book for book in inventory['books'] if book['isbn'] != isbn]
    saveInventory(inventory)

def getBooks(keyword):
    inventory = getInventory()
    result = []
    for book in inventory:
        if keyword.lower() in book['title'].lower() or keyword.lower() in book['author'].lower() or keyword == book['isbn']:
            result.append(book)
    return result

def getBook(isbn):
    inventory = getInventory()
    for book in inventory['books']:
        if book['isbn'] == isbn:
            return book
        
def borrowBook(isbn):
    inventory = getInventory()
    for book in inventory['books']:
        if book['isbn'] == isbn and book['status'] == 'Available':
            book['status'] = 'Borrowed'
            saveInventory(inventory)
            return True
    return False

def returnBorrowedBook(isbn):
    inventory = getInventory()
    for book in inventory['books']:
        if book['isbn'] == isbn:
            book['status'] = 'Available'
            saveInventory(inventory)
            return True
    return False

@app.route('/')
def index():
    books = getInventory()
    return render_template('index.html', books=books['books'])

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    isbn = request.form['isbn']
    addBook(title , author , isbn)
    return redirect(url_for('index'))

@app.route('/remove_book/<isbn>') # Request parameter : isbn
def remove_book(isbn):
    removeBook(isbn)
    return redirect(url_for('index'))

@app.route('/searchBooks') # Request parameter : keyword
def search():
    keyword = request.form['keyword']
    books = getBooks(keyword)
    return jsonify(books)

@app.route('search') # Request parameter : isbn
def searchBook():
    isbn = request.form['isbn']
    book = getBook(isbn)
    return jsonify(book)


@app.route('/borrow_book/<isbn>') # Request parameter : isbn
def borrow_book(isbn):
    if borrowBook(isbn):
        return "Borrowed"
    return "Not Available"

@app.route('/return_book/<isbn>') # Request parameter : isbn
def return_book(isbn):
    if returnBorrowedBook(isbn):
        return "Returned"
    return "Not Borrowed"

if __name__ == '__main__':
    app.run(debug=True)

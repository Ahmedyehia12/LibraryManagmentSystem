from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

# Load the inventory from the JSON file
def load_inventory():
    if os.path.exists('library.json'):
        with open('library.json', 'r') as file:
            return json.load(file) # Return the inventory if the file exists
    return {"books": []} # Return an empty inventory if the file does not exist

# Save the inventory to the JSON file
def save_inventory(inventory): 
    with open('library.json', 'w') as file: # Open the file in write mode
        json.dump(inventory, file, indent=4) # Write the inventory to the file using json.dump

# Add a book to the inventory
def add_book(title, author, isbn):
    inventory = load_inventory() # Load the inventory
    inventory['books'].append({
        "title": title,
        "author": author,
        "isbn": isbn   #ISBN is the unique identifier for the book
    })
    save_inventory(inventory)

# Remove a book from the inventory
def remove_book(isbn):
    inventory = load_inventory()
    inventory['books'] = [book for book in inventory['books'] if book['isbn'] != isbn]
    save_inventory(inventory)


@app.route('/')
def index():
    inventory = load_inventory()
    return render_template('index.html', books=inventory['books'])

@app.route('/add_book', methods=['POST'])
def handle_add_book():
    title = request.form['title']
    author = request.form['author']
    isbn = request.form['isbn']
    add_book(title, author, isbn)
    return redirect(url_for('index'))

@app.route('/remove_book/<isbn>', methods=['GET'])
def handle_remove_book(isbn):
    remove_book(isbn)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

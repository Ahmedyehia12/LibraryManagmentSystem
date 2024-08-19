from flask import Flask, render_template, request, redirect, url_for, flash
import json
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Global data structures to hold library inventory and borrowed books
library_inventory = {}
borrowed_books = {}
borrowed_history = []

# Function to load data from JSON file
def load_from_json():
    global library_inventory, borrowed_books, borrowed_history
    try:
        with open('library_data.json', 'r') as file:
            data = json.load(file)
            library_inventory = data.get('inventory', {})
            borrowed_books = data.get('borrowed', {})
            borrowed_history = data.get('history', [])
    except FileNotFoundError:
        library_inventory = {}
        borrowed_books = {}
        borrowed_history = []

# Function to save data to JSON file
def save_to_json():
    with open('library_data.json', 'w') as file:
        json.dump({'inventory': library_inventory, 'borrowed': borrowed_books, 'history': borrowed_history}, file)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'add_book' in request.form:
            title = request.form['title']
            author = request.form['author']
            isbn = request.form['isbn']
            if isbn in library_inventory:
                flash('Book with this ISBN already exists.', 'error')
            else:
                library_inventory[isbn] = {'title': title, 'author': author}
                save_to_json()
                flash('Book added successfully!', 'success')
        elif 'remove_book' in request.form:
            isbn = request.form['isbn']
            if isbn in library_inventory:
                del library_inventory[isbn]
                save_to_json()
                flash('Book removed successfully!', 'success')
            else:
                flash('Book not found.', 'error')
        elif 'borrow_book' in request.form:
            isbn = request.form['isbn']
            if isbn in library_inventory and isbn not in borrowed_books:
                return_deadline = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
                borrowed_books[isbn] = {'return_deadline': return_deadline}
                borrowed_history.append({
                    'isbn': isbn,
                    'borrow_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'return_deadline': return_deadline
                })
                save_to_json()
                flash(f'Book borrowed successfully! Please return by {return_deadline}.', 'success')
            else:
                flash('Book is either not available or already borrowed.', 'error')
        elif 'return_book' in request.form:
            isbn = request.form['isbn']
            if isbn in borrowed_books:
                del borrowed_books[isbn]
                save_to_json()
                flash('Book returned successfully!', 'success')
            else:
                flash('This book is not borrowed.', 'error')
        elif 'search_book' in request.form:
            keyword = request.form['keyword']
            results = []
            for isbn, book in library_inventory.items():
                if (keyword.lower() in book['title'].lower() or
                    keyword.lower() in book['author'].lower() or
                    keyword == isbn):
                    results.append((isbn, book))
            return render_template('index.html', library_inventory=library_inventory, borrowed_books=borrowed_books, search_results=results)
        elif 'refresh' in request.form:
            return redirect(url_for('index'))
        elif 'track_borrowed_books' in request.form:
            return render_template('return_book.html', track_data=[
                {
                    'isbn': isbn,
                    'title': library_inventory.get(isbn, {}).get('title', 'Unknown'),
                    'author': library_inventory.get(isbn, {}).get('author', 'Unknown'),
                    'return_deadline': info['return_deadline'],
                    'remaining_days': (datetime.strptime(info['return_deadline'], '%Y-%m-%d %H:%M:%S') - datetime.now()).days,
                    'is_overdue': (datetime.now() > datetime.strptime(info['return_deadline'], '%Y-%m-%d %H:%M:%S'))
                }
                for isbn, info in borrowed_books.items()
            ])
    return render_template('index.html', library_inventory=library_inventory, borrowed_books=borrowed_books)

@app.route('/return_book', methods=['POST'])
def return_book():
    isbn = request.form['isbn']
    if isbn in borrowed_books:
        del borrowed_books[isbn]
        save_to_json()
        flash('Book returned successfully!', 'success')
    else:
        flash('This book is not borrowed.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    load_from_json()  # Load existing data from JSON
    app.run(debug=True)

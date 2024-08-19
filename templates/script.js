document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('book-form');
    const tableBody = document.querySelector('#view-books tbody');
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-query');
    const isbnSearchForm = document.getElementById('isbn-search-form');
    const isbnSearchInput = document.getElementById('isbn-query');
    
    // Array to hold book data for search functionality
    let books = [];
    
    form.addEventListener('submit', (event) => {
        event.preventDefault();
        
        const title = document.getElementById('title').value;
        const author = document.getElementById('author').value;
        const year = document.getElementById('year').value;
        const genre = document.getElementById('genre').value;
        const isbn = document.getElementById('isbn').value; // Get ISBN
        
        const book = { title, author, year, genre, isbn, borrowed: false };
        books.push(book);
        
        addBookToTable(book);
        
        form.reset();
    });

    function addBookToTable(book) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${book.title}</td>
            <td>${book.author}</td>
            <td>${book.year}</td>
            <td>${book.genre}</td>
            <td>${book.isbn}</td> <!-- New ISBN column -->
            <td>${book.borrowed ? 'Borrowed' : 'In-Stock'}</td>
            <td><button class="borrow-return-btn">${book.borrowed ? 'Return' : 'Borrow'}</button></td>
            <td><button class="delete-btn">Delete</button></td>
        `;
        
        tableBody.appendChild(row);
    }

    function filterBooks(query) {
        tableBody.innerHTML = ''; // Clear existing table rows

        const lowercasedQuery = query.toLowerCase();

        const filteredBooks = books.filter(book => 
            book.title.toLowerCase().includes(lowercasedQuery) ||
            book.author.toLowerCase().includes(lowercasedQuery) ||
            book.genre.toLowerCase().includes(lowercasedQuery)
        );

        filteredBooks.forEach(book => addBookToTable(book));
    }

    function filterBooksByISBN(isbn) {
        tableBody.innerHTML = ''; // Clear existing table rows

        const lowercasedIsbn = isbn.toLowerCase();

        const filteredBooks = books.filter(book => 
            book.isbn.toLowerCase().includes(lowercasedIsbn)
        );

        filteredBooks.forEach(book => addBookToTable(book));
    }

    searchForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const query = searchInput.value.trim(); // Get the search query
        filterBooks(query);
    });

    isbnSearchForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const isbn = isbnSearchInput.value.trim(); // Get the ISBN search query
        filterBooksByISBN(isbn);
    });

    // Delegate event listener to handle delete and borrow/return buttons
    tableBody.addEventListener('click', (event) => {
        if (event.target.classList.contains('delete-btn')) {
            const row = event.target.closest('tr');
            const title = row.children[0].textContent;
            const author = row.children[1].textContent;
            
            // Remove book from array
            books = books.filter(book => !(book.title === title && book.author === author));
            
            // Remove row from table
            row.remove();
        } else if (event.target.classList.contains('borrow-return-btn')) {
            const row = event.target.closest('tr');
            const title = row.children[0].textContent;
            const author = row.children[1].textContent;
            const book = books.find(book => book.title === title && book.author === author);
            
            if (book) {
                book.borrowed = !book.borrowed;
                event.target.textContent = book.borrowed ? 'Return' : 'Borrow';
                row.children[5].textContent = book.borrowed ? 'Borrowed' : 'In-Stock'; // Update status column
            }
        }
    });
});


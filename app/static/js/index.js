// JavaScript for Filtering Books by ISBN
document.getElementById('isbn-search-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const isbn = document.getElementById('isbn-search').value.trim();
    const books = document.querySelectorAll('#book-list tbody tr');

    books.forEach(book => {
        if (book.getAttribute('data-isbn') === isbn || isbn === '') {
            book.style.display = '';
        } else {
            book.style.display = 'none';
        }
    });
});

// JavaScript for Filtering Books by Keyword
document.getElementById('keyword-search-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const keyword = document.getElementById('keyword-search').value.trim().toLowerCase();
    const books = document.querySelectorAll('#book-list tbody tr');

    books.forEach(book => {
        const title = book.getAttribute('data-title').toLowerCase();
        const author = book.getAttribute('data-author').toLowerCase();
        const isbn = book.getAttribute('data-isbn').toLowerCase();
        const genre = book.getAttribute('data-genre').toLowerCase();

        if (title.includes(keyword) || author.includes(keyword) || isbn.includes(keyword) || genre.includes(keyword)) {
            book.style.display = '';
        } else {
            book.style.display = 'none';
        }
    });
});

// JavaScript for Logout Confirmation
function confirmLogout() {
    if (confirm('Are you sure you want to log out?')) {
        document.getElementById('logout-form').submit();
    }
}

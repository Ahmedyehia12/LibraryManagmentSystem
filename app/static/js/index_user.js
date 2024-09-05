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

// JavaScript for Borrow and Return Actions
document.addEventListener('DOMContentLoaded', function() {
    const actionButtons = document.querySelectorAll('.action-btn');

    actionButtons.forEach(button => {
        button.addEventListener('click', function() {
            const isbn = button.getAttribute('data-isbn');
            const status = button.getAttribute('data-status');
            const newStatus = status === 'Available' ? 'Borrowed' : 'Available';
            const url = status === 'Available' ? `/borrow_book/${isbn}` : `/return_book/${isbn}`;

            fetch(url, { method: 'POST' })
                .then(response => {
                    if (response.ok) {
                        // Update the button and book status on success
                        button.textContent = newStatus === 'Available' ? 'Borrow' : 'Return';
                        button.setAttribute('data-status', newStatus);
                        const row = button.closest('tr');
                        row.querySelector('td:nth-child(6)').textContent = newStatus;
                    } else {
                        alert('An error occurred while updating the book status.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        });
    });
});

// JavaScript for Logout Confirmation
function confirmLogout() {
    if (confirm('Are you sure you want to log out?')) {
        document.getElementById('logout-form').submit();
    }
}

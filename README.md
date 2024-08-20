# Library Management System

## Overview

The Library Management System is a web application built with Flask that facilitates managing a library's book inventory and user interactions. The system supports user and admin roles, allowing for a range of functionalities from basic book browsing to full inventory management.

## Features

### User Authentication
- **Sign Up**: New users can create an account.
- **Login**: Existing users can log in to access their personalized features.
- **Logout**: Users can log out, clearing their session.

### Book Management (Admin Only)
- **Add Books**: Administrators can add new books to the library.
- **Remove Books**: Administrators can remove books from the inventory.
- **Search Books**: Both users and admins can search for books by title, author, or ISBN.

### Book Borrowing and Returning
- **Borrow Books**: Users can borrow available books.
- **Return Books**: Users can return books they have borrowed.

### User Roles
- **Admin**: Full access to book management features and user management.
- **User**: Access to book browsing and borrowing features.

## Code Structure

### Main Application (`app.py`)

- **Flask Setup**: Initializes the Flask app and sets up user session management.
- **Routes**:
  - `/` - Displays the login page.
  - `/signup` - Allows new users to register.
  - `/admin_home` - Admin dashboard for managing books.
  - `/home` - User dashboard for browsing and borrowing books.
  - `/add_book` - Endpoint for adding new books (Admin only).
  - `/remove_book/<isbn>` - Endpoint for removing books (Admin only).
  - `/borrow_book/<isbn>` - Endpoint for borrowing books (User only).
  - `/return_book/<isbn>` - Endpoint for returning borrowed books (User only).

- **Classes**:
  - `library`: Contains methods for interacting with the inventory and user data.
  - `Admin_User`: Inherits from `UserMixin` and `library`, adds methods for managing book inventory.
  - `User`: Inherits from `UserMixin` and `library`, adds methods for borrowing and returning books.

### Files
- **`library.json`**: Stores the library's book inventory.
- **`users.json`**: Stores user information including credentials and roles.
- **HTML Templates**:
  - `index.html`: Display for admins and users to view books.
  - `index_user.html`: User-specific view for book interactions.
  - `login.html`: Login page for authentication.
  - `signup.html`: Registration page for new users.

## Installation

1. **Clone the Repository**
    ```bash
    git clone https://github.com/Ahmedyehia12/LibraryManagmentSystem/tree/users
    cd <repository-directory>
    ```

2. **Install Dependencies**
    Ensure you have Python and pip installed, then run:
    ```bash
    pip install -r requirements.txt
    ```

3. **Setup Configuration**
    Ensure that `library.json` and `users.json` files exist in the root directory of your project. These files should be formatted as valid JSON.

4. **Run the Application**
    ```bash
    python app.py
    ```

5. **Access the Application**
    Open your web browser and navigate to `http://localhost:5000` to start using the application.

## Usage

### User Roles and Actions

- **Admin**:
  - **Log In**: Access `/` and log in with admin credentials.
  - **Manage Books**: Admin has acess to manage the inventory (add and remove books)
  
- **User**:
  - **Log In**: Access `/` and log in with user credentials.
  - **Browse Books**: Navigate to `/home` to view and search for books.
  - **Borrow Books**: User can borrow a book from the inventory and it will automatically be marked as "Borrowed"
  - **Return Books**: User can return a borrowed book to the inventory and it will automatically be marked as "Available"
### Common Routes

- **`/signup`**: Create a new user account. Requires username and password.
- **`/login`**: Log in with existing credentials.
- **`/logout`**: End the current session and log out.

## Code Overview

### Library Class
- **`getInventory()`**: Reads the inventory data from `library.json`.
- **`getUsers()`**: Reads user data from `users.json`.
- **`saveUser(User)`**: Writes user data to `users.json`.
- **`getBooks(keyword)`**: Searches for books based on title, author, or ISBN.
- **`getBook(isbn)`**: Retrieves a book by its ISBN.

### Admin_User Class
- **`addBook(title, author, isbn, genre, date)`**: Adds a new book to the inventory.
- **`removeBook(isbn)`**: Removes a book from the inventory.
- **`saveInventory(Inventory)`**: Saves the updated inventory to `library.json`.

### User Class
- **`borrowBook(isbn)`**: Marks a book as borrowed.
- **`returnBorrowedBook(isbn)`**: Marks a book as available.

This project is done via the colaborative work of:
- [**Marwan Mohammed**](https://github.com/MarwanMohammed2500)
- [**Ahmed Yahia**](https://github.com/Ahmedyehia12)
- [**Safia Adel**](https://github.com/safiaadel)
- [**Sama Hatem**](https://github.com/samahatem387)

And is part of a greater DevOps Project!

# Images from the website:
### Login Page:
![image](https://github.com/user-attachments/assets/4ad8d953-4989-4cb7-8f46-52fa3cdbfe44)

### Signup Page:
![image](https://github.com/user-attachments/assets/6692d936-c91b-4a34-99e0-8681daca2476)

### Admin Home Page:
![image](https://github.com/user-attachments/assets/0dc1eced-4048-4000-9eda-3481a55806e9)
![image](https://github.com/user-attachments/assets/b02ea470-a1e8-40fa-93b7-3441c6f5fcd6)

### User Home Page:
![image](https://github.com/user-attachments/assets/993f3f7c-db64-4887-8166-747edf901ad7)


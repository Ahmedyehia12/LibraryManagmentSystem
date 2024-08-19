<h1>Library Management System</h1>

A simple Library Management System designed to manage and display book information. This system includes features for viewing and adding books, using basic HTML, CSS, and JavaScript.

<b>Table of Contents</b>
<ul>
  <li>Overview</li>
  <li>Features</li>
  <li>File Structure</li>
  <li>Usage</li>
  <li>Dependencies</li>
</ul>

<h2>Overview:</h2>
The Library Management System is a web-based application allowing users to view and add books to a library. It consists of two main HTML pages:
<ul>
  <li>index.html: The main page that displays a form for adding books and a table for viewing the books currently in the library.</li>
  <li>view-books.html: A separate page dedicated to viewing books with an additional "Status" column.</li>
</ul>
The application uses CSS for styling and JavaScript to handle the dynamic addition of books.

<h2>Features</h2>
<li>
  View Books: Displays a table of books with columns for Title, Author, Year, and Genre.
  Add New Book: Provides a form to enter and submit book details, which are then dynamically added to the table.
  Responsive Design: Adapts to different screen sizes using responsive CSS styling.
</li>

<h2>File Structure</h2>
The project directory contains the following files:

```
/library-management-system
│
├── index.html        # Main page with form and book table
├── view-books.html   # Page for viewing books with an additional status column
├── styles.css        # CSS file for styling the application
└── script.js         # JavaScript file for handling form submission and book addition
```

<h3>index.html:</h3>
The main HTML file for the application. It includes:
<ul>
  <li>Header: Contains the site title and navigation links.</li>
  <li>Main Content:</li>
  <ul>
    <li>A section to view books with a table.</li>
    <li>A section to add new books via a form.</li>
  </ul>
  <li>Footer: Displays the copyright information.</li>
</ul>
<h3>view-books.html:</h3>
An HTML file similar to index.html but intended solely for viewing books. It features:
<ul>
  <li>Header: Same as index.html.</li>
  <li>Main Content:</li>
  <ul>
    <li>A section to view books with a table including a "Status" column.</li>
  </ul>
  <li>Footer: Same as index.html.</li>
</ul>
<h3>styles.css</h3>
CSS file for styling the application. Key styles include:
<ul>
  <li>Global Styles: Font settings, margins, and padding.</li>
  <li>Header and Navigation: Background color, text color, and layout.</li>
  <li>Tables: Borders, padding, and alignment.</li>
  <li>Forms: Input field and button styling.</li>
  <li>Footer: Text alignment and background color.</li>
</ul>

<h3>script.js</h3>
JavaScript file that handles:
<ul>
  <li>Form Submission: Prevents the default form submission behavior, extracts values from the form fields, and adds a new row to the table in index.html.</li>
</ul>

<h2>Usage</h2>
<ul>
  <li>Open the application:</li>
    <ul>
        <li>Open index.html in a web browser to access the main page.</li>
        <li>Navigate to view-books.html to view the list of books.</li>
    </ul>
  <li>Add a New Book:</li>
    <ul>
      <li>Fill out the form on index.html with the book’s title, author, year, and genre.</li>
      <li>Click the "Add Book" button to submit the form and add the book to the table.</li>
    </ul>
  <li>View Books:</li>
    <ul>
  <li>Visit view-books.html to see the table of books with an extra "Status" column.</li>
</ul>

<h2>Dependencies</h2>
<li>
  None: The project does not have any external dependencies.
</li>

<h2>Images from the website</h2>
<h4>Home Page:</h4>

![homepage](https://github.com/user-attachments/assets/376d46e1-2867-4be4-b92c-0b66c50a9ce9)


<h4>View Book Page:</h4>

![View_Book](https://github.com/user-attachments/assets/481d9dfd-13e5-45ce-830c-324ff6f2bffc)

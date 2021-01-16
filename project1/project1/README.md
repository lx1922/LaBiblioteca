# Project 1

## Requirements

1. **Registration**: The first page or the index page that shows up after the `flask run` command is the signup or registration page which takes the user's desired username, password and email.

2. **Login**: After registration, the website takes the user to a page with some welcome message and a login link which takes user to a login form. Also on the signup page there's a same login link if the user has already registerred.

3. **Logout**: After Login every subsequent page has a logout link on the top left of the page which the user can use to logout and this takes them back to the login page.

4. **Import**: A separate import.py file is there in the project1 folder which has the script to import all the 5000 books into the SQL table.

5. **Search**: The login page takes the user to a search bar (if the login info is correct) where they can enter the desired info to search for. On pressing enter key it shows all the results matching the given search item. The user can then click on the book they need.

6. **Book Page**: On clicking on the book link from the search bar, the user will be taken to the book's page with details about it like the Author, ISBN, Title, rating count, average rating and reviews left by other users.

7. **Review Submission**: On the books page, there is also a form where user can enter thier own reviews and ratings.

8. **Goodreads Review Data**: The average rating and the ratings count on the book page is the goodreads review data.

9. **API access**: The users can visit the route `/api/<isbn>` on the website to get the JSON data about any particular book (if available).


### La Biblioteca: Shrey Vakil through edX

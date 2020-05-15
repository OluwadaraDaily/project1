# Project 1

Web Programming with Python and JavaScript

When you get to the landing page you see a 'Get Started' button that links to the Login page If you do not have an account a 'Register' button is also on the login page that links to the register page. 

On the register page, you choose a Username and Password and if it meets the requirements, then, it redirects the user to the home page.

If the person has an account already, when the person logs in through the Login page and the credentials supplied match that in the database, then the user is redirected to the home page. 

The Home page has a large search bar that would enable the user to search for the book to review using the book title, author or ISBN number of the book. 

When the user searches using a particular parameter that is similar to what is on the database, it return a list of books that are similar to the search parameter on the results page.

If the parameter inputed does not look like any book title, author or ISBN an error page is displayed and then the user can cycle back to the home page to try again.  

The user will have to click on the book title to get to the individual book page. On the individual book page, the book details are displayed as well as reviews on that particular book by other users marked by their usernames. 

Here, also, the user can add his or her own reviews and rating the book out of five. 

When the user writes their review and rate the book successfully, a success page is displayed and then the user can cycle back to the home page of the website.

--------------------------------------------------------------------------------------------

404.html - This page contains an error message that shows up when someone is trying to get data from the website through the API but puts in an incorrect ISBN number

book.html - This is the page that shows each individual book after they have been selected after been searched for

error.html - This is a reusable error template page that is shown whenever a user does something that is not acceptable on the website like searching with the wrong characters and so on. 

home.html - This is the homepage where the search bar is located so that users can search for books to review. 

index.html - This is the landing page of the site

layout.html - This page includes the navbar and other links that is used on every page like the Bootstrap CDN

login.html - This is the login page

register.html - This is the registration page

results.html - This is the page that lists all the corresponding result from the user's search action from the home page. 

success.html - This is a reusable success page that indicates when a user successfully posts a review for instance. 

application.py - This is the main back end file where connections are made to the database also requests are handled properly. 

books.csv - Contains pre-loaded data of books, their author, the year of publish, ISBN number to be added to the database. 

import.py - This is a script used to read into books.csv and load the data present there to the database at once. 

requirements.txt - Contains all the packages installed to make this website function as it does. 

static folder - Includes CSS and image files used in the HTML files

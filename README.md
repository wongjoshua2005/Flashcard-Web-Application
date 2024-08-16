# Flashcard-Web-Application
## Description: 
Charming Flashcards is a web application that uses Flask, Python, Bootstrap, SQLite3, HTML/CSS, and JavaScript. 
The purpose of this program is to make users not be distracted by other websites and make a loud beep.
The loud beep encourages the user to return to the site and keep studying.
In addition, the web application has a simple and user-friendly interface in dark mode
to make your eyes more relaxed when studying. This application is mostly aimed at people
who are distracted and want to make as much progress in their academics as possible. This program
CAN be run on a phone or tablet, but I did not implement PWA because I did not know it even existed
when I was developing this project. ;-;

## Features:
The application has the following features:
1. Create an account to log into every time to study using Python's bcrypt hashing to prevent brute force (I know. 10/10 feature. :/)
2. Create a set and manage your collection of sets
4. Create flashcards and modify them to your liking
6. The Pomodoro timer to keep track of your study route
7. An alarm comes with JavaScript detection for when the user exists outside of the page (when the Pomodoro timer runs)

The features are just the basics of what I can make during the remainder of my summer. If the project does become popular in the future,
I will continue to add more features.

## Reflection:
A major problem I had throughout making the web application was to store the Flask application in a class to use OOP. I thought that not using OOP would have been 
more beneficial, but I wanted to use the knowledge I learned during my first year of computer science. Unfortunately, I regret making that decision because
the Flask framework does not like to be turned into a class, and sometimes making workarounds is too much to sacrifice for little benefits. I do believe that
web applications made with Flask would be better off with a procedural paradigm. 

This project taught me **a lot** about the difference between classroom assignments and making my programs from scratch.
My computer science courses never taught me to make projects on my own, and I learned how to do so from CS50x. A problem I had faced throughout
college was going through tutorial hell. I think this is the first step in the right direction to just start making projects and be confident. :)

## Files:
1. The **.venv** and **_pycache_** folders manage all third-party pip installations and Python versions for bcrypt password encryption, flask framework, and sqlite3.
2. The **flask_session** folder handles all session details to save when the user logs back into the web application.
3. The **static** folder keeps all CSS and JavaScript files necessary for dealing with the Pomodoro timer, alarm, and the background styles of the web application.
4. The **templates** folder is where all the HTML information and routes are stored when a user wants to visit different areas of the web application. The HTML files interact with Jinja and the Flask framework
5. The **app.py** is where all the functionality necessary for retrieving user's information and handling their data are stored. In addition, this allows the HTML file to render to the server without revealing sensitive information
6. The **user_database.db** is an SQLite3 database that stores the user's information, sets, and all flashcards they add to their set.

## TODO

Due to the nature of bad decisions by trying to wrap Flask into a class, the program is going to run through the good old command line. 
To get started, make sure you have git downloaded into the terminal to clone this repository and try it out for yourself.
After you have git installed, you want to install any IDE that can use the command line that is similar to Linux.
The purpose of having an IDE installed is to run this command: **python3 app.py** to run a local server to access the site.
Congrats! You have your flashcard application! Make sure you study hard and earn those As that you deserve. ;)

## Pictures of The Program
![Screenshot of the sets page where the user can add new collections to their account.](![Screenshot 2024-08-15 9 05 51 PM](https://github.com/user-attachments/assets/3bfc8975-47f6-453b-a7f7-066238aa208e))

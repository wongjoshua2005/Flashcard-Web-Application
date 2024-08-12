# Flashcard-Web-Application
#### Description: 
Charming Flashcards is a web application that uses Flask, Python, Bootstrap, SQLite3, HTML/CSS, and JavaScript. 
The purpose of this program is to make users not be distracted by other websites and make a loud beep. 
In addition, the web application has a simple and user-friendly interface in dark mode
to make your eyes more relaxed when studying.

#### Features:
The application has the following features:
1. Create an account to log into every time to study
2. Create a set and manage sets
3. Add flashcards to a specific set
4. Update flashcard information when necessary
5. Delete flashcards that are no longer in use
6. Pomodoro timer to keep track of study route
7. An alarm that forces the user to study and not be distracted





A major problem I had throughout making the web application was to store the Flask application in a class to use OOP. I thought that not using OOP would have been 
more beneficial, but I wanted to use the knowledge I learned during my first year of computer science. Unfortunately, I regret making that decision because
the Flask framework does not like to be turned into a class, and sometimes making workarounds is too much to sacrifice for little benefits. I do believe that
web applications made with Flask would be better off with a procedural paradigm. This project taught me **a lot** about the difference between classroom
assignments and making my programs from scratch. My college never taught me any ways to learn to make projects on my own, and I learned how to do so from CS50x.



#### Files:
1. The **.venv** and **_pycache_** folders manage all third-party pip installations and Python versions for bcrypt password encryption, flask framework, and sqlite3.
2. The **flask_session** folder handles all session details to save when the user logs back into the web application.
3. The **static** folder keeps all CSS and JavaScript files necessary for dealing with the Pomodoro timer, alarm, and the background styles of the web application.
4. The **templates** folder is where all the HTML information and routes are stored when a user wants to visit different areas of the web application. The HTML files interact with Jinja and the Flask framework
5. The **app.py** is where all the functionality necessary for retrieving user's information and handling their data are stored. In addition, this allows the HTML file to render to the server without revealing sensitive information
6. The **user_database.db** is an SQLite3 database that stores the user's information, sets, and all flashcards they add to their set.


TODO

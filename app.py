"""
Joshua Wong
Summer 2024
app.py
"""

# To retrieve the password encryption, Flask framework, and SQLite modifications
from flask import (
    Flask, render_template, request, redirect, session, url_for, g
)
import bcrypt
from flask_session import Session
import sqlite3

def get_db(db_name):
    """
    The get_db() function handles starting a new connection for the
    database and returning that connection back to the user to
    execute queries.

    Args:
        db_name (str): The name of the database to start a connection.
    Returns:
        Connection: The database object that is connected.
    """
    
    # Searches for the database connection to ensure none are open
    db = getattr(g, '_database', None)

    # Checks if there are no database connections to establish new
    # connection
    if db is None:
        db = g._database = sqlite3.connect(db_name)

    return db

def retrieve_cursor(database):
    """
    The retrieve_cursor() function handles automatically adding
    a cursor to the database and converting into a dictionary
    to retrieve information efficiently.

    Args:
        database: The name of the database to add a cursor.
    Returns:
        Cursor: To allow the database to execute queries. 
    """

    database.row_factory = sqlite3.Row
    db_cursor = database.cursor()

    return db_cursor

class MainApp(Flask):
    """
    The MainApp class represents the implementation of the Flask framework
    to handle backend, routes for the HTML pages, and Jinja implementations. 
    In addition, MainApp is useful for providing most SQLite functionality
    and access to multiple libraries to do password encryption and sessions.
    """

    def __init__(self):
        """
        The constructor for the class will help initialize the Flask framework
        and setting up all the routes necessary for the HTML page
        interactivity.
        """

        # Creates the Flask app initialization
        super().__init__(__name__)

        # Store the name of the database for this application
        self.__DATABASE = "user_database.db"

        # Set up the session configuration for the user to stay logged in
        self.config["SESSION_PERMANENT"] = False
        self.config["SESSION_TYPE"] = "filesystem"
        Session(self)

        # Runs all routes necessary for interacting with the website
        self.__run_routes()

    def __run_routes(self):
        """
        The __run_routes() method runs inside the constructor used for starting
        the application. The method allows all routes to be registered and 
        running for interactivity with the HTML forms. In addition, the 
        method will allow adding properties to databases and giving errors.
        """

        def __send_error(error_code):
            """
            The __send_error() method reduces the amount of code required
            to send an error message to the error route and saves code lines.
            In addition, the method improves readability and does not need
            to write the messages themselves.

            Args:
                error_code: The code you want to display to the user when
                entering into the error page.
            Returns:
                Error route: Redirects the user to the error page for making
                a mistake in their inputs.
            """

            error_msg = None

            # Sets a pre-defined message to display to the user when reaches
            # error page
            match error_code:
                case 404:
                    error_msg = "404: INVALID INPUT(S)!!! :/"
                case 401:
                    error_msg = "401: INVALID GIVEN INPUT! CHECK AGAIN! ;-;"
                case 409:
                    error_msg = """409: CONFLICT WITH GIVEN 
                    INPUT! CHECK AGAIN! ;-;"""

            return redirect(url_for("error", message=error_msg, 
                                    code=error_code))

        def __search_user(db_cursor, user_name, set_session_id):
            """
            The __search_users() method enters into the SQLite database
            to retrieve all the users that is currently stored in the database
            to find a specific username.
            Useful for verifying information when registering or logging into
            accounts.

            Args:
                db_cursor: The cursor that is connected to the database
                to make queries.
                user_name (str): The user name to check in the database to 
                ensure it exists.
                set_session_id (bool): To determine if the user wants to 
                set the session id to that user when entering into website.
            Returns:
                bool: Confirms if the user exists in the database.        
            """

            # Searches through database to find the user
            search_user = db_cursor.execute(
                "SELECT * FROM user_info WHERE user_name = ?", (user_name,)
            )

            # Stores the result of the search into the result variable to
            # return 
            result = search_user.fetchone()

            # Saves user's id when needed to search in sets if need_id is True
            if set_session_id:
                return result["user_id"]

            return True if result else False

        def __search_set(db_cursor, set_name):
            """
            The __search_set() method enters into the SQLite database
            to search for a specific set name for that specific user.
            Just like the annoying to implement __search_user(), this does
            exact same except has a different way to search. Why have separate
            methods? I could do f-string, but I do not want to risk
            getting an SQL injection attack.

            Args:
                db_cursor: The cursor that is connected to the database
                to make queries.
                set_name (str): The name of the set that the user wants to
                verify exist in the database.
            Returns:
                bool: Confirms if the set exists in the database.        
            """

            # Retrieve the set data from the database
            set_data = db_cursor.execute(
                """SELECT * FROM collection WHERE set_title = ? 
                AND user_id = ?""", (set_name, session["user_id"])
            )
                    
            verify = set_data.fetchone()

            return True if verify else False

        def __search_flashcard(db_cursor, card_name):
            """
            The __search_flashcard() method enters into the SQLite database
            to search for a specific flashcard name for that specific user
            within their set. Pretty self explanatory.

            Args:
                db_cursor: The cursor that is connected to the database
                to make queries.
                card_name (str): The name of the flashcard
                  that the user wants to verify exist in their specific set.
            Returns:
                bool: Confirms the flashcard exists in the database or not.        
            """

            # Retrieve flashcard data from the specific set to verify existence
            verify_term = db_cursor.execute(
                """SELECT * FROM flashcard WHERE term = ? 
                AND user_id = ? AND set_name = ?""",
                (card_name, session["user_id"], session["set"])
            )

            card_result = verify_term.fetchone()

            return True if card_result else False

        def __find_hash(db_cursor, username):
            """
            The __find_hash() method retrieves the hash necessary from the
            specific user usually to verify if the password hashes match
            to log the user into the site.

            Args:
                db_cursor: The cursor that is connected to the database
                to make queries.
                username (str): The user that wants to enter into the site.
            Returns:
                hash_result: The data necessary to use bcrypt's check hash
                method.
            """

            # Searches for the hash information from specific user
            hash_data = db_cursor.execute("""
                SELECT hash FROM user_info WHERE user_name = ?
            """, (username, ))

            hash_result = hash_data.fetchone()

            return hash_result

        @self.route("/", methods=["GET", "POST"])
        def register():
            """
            The register() method sets the route to the default sign up
            page when you first enter into the website. This page only exists
            for people who are new to the application and wants to sign up.

            Returns:
                HTML Render: Renders the register.html template for the user
                to register for an account.

                Error: Can return an error if the user does something wrong
                during the registration process.
            """

            # To prevent the user from accessing the register page
            # when they are already logged into the site
            if 'user' in session:
                return redirect("/sets")

            # To register the user's information into the database
            if request.method == "POST":

                # To retrieve all user's information to verify for validity
                username = request.form.get("username")
                password = request.form.get("password")
                confirm_pass = request.form.get("confirm_pass")

                # To prevent the user from trying to enter blank inputs
                # and ensure password matches the confirmed password
                if (not username or not password 
                    or not confirm_pass or password != confirm_pass):
                    return __send_error(404)
                
                # Starts a database to query information
                db = get_db(self.__DATABASE)
                db_cursor = retrieve_cursor(db)

                # To give an error to the user when a username already taken
                if __search_user(db_cursor, username, False):
                    return __send_error(409)

                # Encrypts the password for security when entering into 
                # database
                pass_bytes = password.encode("utf-8")
                salt = bcrypt.gensalt()
                hash = bcrypt.hashpw(pass_bytes, salt)

                # To commit all user information into the database to make
                # them officially into the site
                db_cursor.execute(
                    "INSERT INTO user_info (user_name, hash) VALUES (?, ?)", 
                    (username, hash)
                )

                # Allows the user to sign back in when they leave the site
                session["user"] = username
                session["sort_cards"] = False
                session["user_id"] = __search_user(db_cursor, username, True)

                db.commit()
                db.close()

                return redirect("/sets")

            return render_template("register.html")

        @self.route("/login", methods=["GET", "POST"])
        def login():
            """
            The login() method sets the route to the log in
            page when the user clicks on the login button. This page only exists
            for people who are returning users and want to log back into the
            site to continue.

            Returns:
                HTML Render: Renders the login.html template for the user
                to continue studying.

                Error: Can return an error if the user does something wrong
                when trying to log into the site.
            """

            # To process the information received by the post method form
            if request.method == "POST":

                # To retrieve all form inputs that the user given to verify
                user = request.form.get("username")
                password = request.form.get("password")

                # To prevent SQL injection attack and no data
                if not user or not password:
                    return __send_error(404)

                # Starts the database connection to make queries
                db = get_db(self.__DATABASE)
                db_cursor = retrieve_cursor(db)

                # To encourage user to register an account
                if not __search_user(db_cursor, user, False):
                    return __send_error(404)

                # To compare the password from the database and the user's
                # input to determine validity
                encode_pass = password.encode("utf-8")
                pass_hash = __find_hash(db_cursor, user)["hash"]
                result = bcrypt.checkpw(encode_pass, pass_hash)

                # To prevent user from entering into the account using
                # wrong password
                if not result:
                    return __send_error(401)

                # Logs session to the user to confirm everything works
                session["user"] = user
                session["sort_cards"] = False
                session["user_id"] = __search_user(db_cursor, user, True)

                db.commit()
                db.close()

                return redirect("/sets")

            # Closes out any user information logged in if they return back
            session.clear()

            return render_template("login.html")    

        @self.route("/error")
        def error():
            """
            The error() method sets the route to the error page
            whenever a user made a mistake when registering account, logging
            in, creating a set, and modifying flashcards. To indicate that
            a user made a mistake and should prevent making that mistake
            in the future.

            Returns:
                HTML Render: Renders the error.html template for the user
                to tell them what they did wrong and send error code to the
                network.
            """

            # Retrieve the error message and the code given when redirected
            error_reason = request.args.get("message")
            code = request.args.get("code")

            return render_template("error.html", code=error_reason), code   

        @self.route("/sets", methods=["GET", "POST"])
        def user_sets():
            """
            The user_sets() method loads the index.html page that shows 
            the user's collection of sets that they have created and allow them
            to create new sets to study.

            Returns:
                HTML Render: Renders the index.html template for the user
                to choose which set to study or create a set.

                Error: Can return an error if the user does something wrong
                when trying to modify sets.
            """

            # To change the navigation bar options when user logged in
            user_logged = 'user' in session

            # Prevent the user from trying to access sets after not signed in
            if not user_logged:
                session.clear()
                return redirect("/")

            # To retrieve the database to search up and make query commits
            db = get_db(self.__DATABASE)
            db_cursor = retrieve_cursor(db)

            # To run through all sets that the user contained in the database
            set_data = db_cursor.execute(
                "SELECT set_title FROM collection WHERE user_id = ?", 
                (session["user_id"],)
            )

            all_sets = set_data.fetchall()

            # To see if any forms were submitted by the HTML page
            if request.method == "POST":

                # To add set name into the user's database 
                if 'create' in request.form:
                    new_set = request.form.get("create")

                    # To verify if the set title is not in the database
                    if not new_set:
                        return __send_error(404)

                    # Warns user that the set already exist and can modify
                    # that set
                    if __search_set(db_cursor, new_set):
                        return __send_error(409)

                    # To add the new set name into the user's database
                    db_cursor.execute(
                        """INSERT INTO collection (user_id, set_title) 
                        VALUES (?, ?)""", 
                        (session["user_id"], new_set)
                    )

                    db.commit()
                    db.close()

                    return redirect("/sets")

                # To allow the user to rename their set
                if 'rename' in request.form:
                    
                    # To perform an update to the database
                    new_name = request.form.get("rename")
                    old_name = request.form.get("old_name")

                    # Warn user of trying to enter blank inputs
                    if not new_name or not old_name:
                        return __send_error(404)

                    # Warns user of trying to change name of an invalid set
                    if not __search_set(db_cursor, old_name):
                        return __send_error(404)

                    # To permanently change the old set title with new set
                    # title 
                    db_cursor.execute(
                        """UPDATE collection SET set_title = ?
                        WHERE user_id = ? AND set_title = ?""", 
                        (new_name, session["user_id"], old_name)
                    )

                    db.commit()
                    db.close()  

                    return redirect("/sets")

                # To run operation to delete set based on request
                if 'delete' in request.form:
                    user_request = request.form.get("delete")

                    # Warn user of trying to enter blank inputs
                    if not user_request:
                        return __send_error(404)

                    # Warns user of trying to change name of an invalid set
                    if not __search_set(db_cursor, user_request):
                        return __send_error(404)

                    # To permanently delete the set from the database
                    db_cursor.execute(
                        """DELETE FROM flashcard WHERE set_name = ? AND
                        user_id = ?""", 
                        (user_request, session["user_id"])
                    )

                    db_cursor.execute(
                        """DELETE FROM collection WHERE set_title = ? AND
                        user_id = ?""", 
                        (user_request, session["user_id"])
                    )

                    db.commit()
                    db.close()

                    return redirect("/sets")

                # To go into the specific set to start studying
                if 'display_set' in request.form:
                    
                    # To retrieve all user information and the set name to
                    # run the flashcards
                    chosen_card = request.form.get("display_set")
                    session["set"] = chosen_card

                    return redirect("/flashcard")

            return render_template("index.html", logged=user_logged,
                                    name=session["user"], sets=all_sets) 
        
        @self.route("/flashcard", methods=["GET", "POST"])
        def flashcard():
            """
            The flashcard() method handles all of the flashcards from the
            specific set to study. In addition, this is where most
            of the functionality takes place for the user to study and run
            a pomodoro timer to focus on their goals.

            Returns:
                HTML Render: Renders the flashcard.html template for the user
                to run pomodoro timer and study the flashcards.

                Error: Can return an error if the user does something wrong
                when trying to add a new flashcard to the set.           
            """

            # Sets the title and shows specific navigation bars buttons when
            # logged in
            user_logged = 'user' in session

            # Prevent the user from trying to access sets after not signed in
            if not user_logged:
                session.clear()
                return redirect("/")   

            # Creates the database connection to make query commits
            db = get_db(self.__DATABASE)
            db_cursor = retrieve_cursor(db)

            # To display the cards on screen depending on randomly sorted button
            # was pressed or not
            if not session["sort_cards"]:

                # To run through all the terms and definitions in a graph
                # for the user to see how many is in their set
                flashcards = db_cursor.execute(
                    "SELECT term, definition FROM flashcard WHERE set_name = ?",
                    (session["set"],)
                )

            else:

                # Display flashcards in random order
                flashcards = db_cursor.execute(
                    """SELECT term, definition FROM flashcard 
                    WHERE set_name = ? ORDER BY RANDOM()""",
                    (session["set"],) )
                
                session["sort_cards"] = False


            cards_list = flashcards.fetchall()

            # Creates a dummy flashcard if the user does not have any flashcards
            implement_dummy = not cards_list

            # To allow the user to make a new flashcard
            if request.method == "POST":

                # Allows user to create a new flashcard
                if 'create_term' in request.form:

                    # Retrieve form information and prevents any blanks
                    new_term = request.form.get("create_term")
                    new_definition = request.form.get("create_def")

                    if not new_term or not new_definition:
                        return __send_error(404)

                    # Warns user if flashcard already in their set
                    if __search_flashcard(db_cursor, new_term):
                        return __send_error(409)

                    # Insert the new flashcard into that specific set
                    db_cursor.execute(
                    """INSERT INTO flashcard (user_id, set_name, term, 
                    definition) VALUES (?, ?, ?, ?);""", (session["user_id"], 
                                              session["set"],
                                            new_term, new_definition)
                    )

                    db.commit()
                    db.close()

                    return redirect("/flashcard")     

                # Checks when the user wants to replace the term and definition
                # of a specific flashcard
                if 'replace_term' in request.form:

                    # Retrieve form information and prevents any blanks
                    replace_term = request.form.get("replace_term")
                    replace_def = request.form.get("replace_def")
                    old_term = request.form.get("old_term")
                    old_def = request.form.get("old_def")

                    if (not replace_term or not replace_def or not old_term
                        or not old_def):
                        return __send_error(404)

                    # To verify if the old flashcard term exists in the database
                    if not __search_flashcard(db_cursor, old_term):
                        return __send_error(404)

                    # Updates the term and definition of the original flashcard
                    db_cursor.execute("""UPDATE flashcard SET 
                                        term = ?, definition = ?
                                        WHERE set_name = ? AND user_id = ?
                                        AND term = ? AND definition = ?""",
                                        (replace_term, replace_def, 
                                         session["set"], 
                                         session["user_id"], old_term, old_def)
                                        )

                    db.commit()
                    db.close()

                    return redirect("/flashcard")

                # Allows user to delete the flashcard from their set
                if 'del_flashcard' in request.form:

                    # To prevent blanks from being entered as inputs
                    term_request = request.form.get("del_flashcard")

                    if not term_request:
                        return __send_error(404)

                    # To ensure flashcard exists in the set to delete
                    if not __search_flashcard(db_cursor, term_request):
                        return __send_error(404)

                    # Runs query to delete flashcard based on given name
                    db_cursor.execute("""DELETE FROM flashcard 
                                        WHERE term = ? AND set_name = ? AND
                                        user_id = ?
                                        """, (term_request, session["set"],
                                               session["user_id"])
                                        )

                    db.commit()
                    db.close()

                    return redirect("/flashcard")

                # To check if the user wants their flashcards randomly sorted
                if 'random_sort' in request.form:
                    
                    # To make the change when they load into the site and 
                    # not be permanent
                    session["sort_cards"] = True

                    return redirect("/flashcard")

            return render_template("flashcard.html", logged=user_logged,
                                    name=session["set"], cards=cards_list,
                                    empty_list=implement_dummy)

# Runs the server necessary to start using the web application (for now)
if __name__ == "__main__":
    MainApp().run()
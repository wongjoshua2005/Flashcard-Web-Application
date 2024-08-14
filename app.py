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
                user_name = request.form.get("username")
                password = request.form.get("password")
                confirm_pass = request.form.get("confirm_pass")

                # To prevent the user from trying to enter blank inputs
                # and ensure password matches the confirmed password
                if (not user_name or not password 
                    or not confirm_pass or password != confirm_pass):
                    return __send_error(404)
                
                # Starts a database to query information
                db = get_db(self.__DATABASE)
                main_cursor = retrieve_cursor(db)

                # To ensure that the user's input does not exist in the
                # database already
                users_data = main_cursor.execute(
                    "SELECT * FROM user_info WHERE user_name = ?", (user_name,)
                )

                user = users_data.fetchone()

                # To give an error to the user when a username already taken
                if user:
                    return __send_error(409)

                # Encrypts the password for security when entering into 
                # database
                pass_bytes = password.encode("utf-8")
                salt_key = bcrypt.gensalt()
                hash_key = bcrypt.hashpw(pass_bytes, salt_key)

                # To commit all user information into the database to make
                # them officially into the site
                main_cursor.execute(
                    "INSERT INTO user_info (user_name, hash) VALUES (?, ?)", 
                    (user_name, hash_key)
                    )

                db.commit()
                db.close()

                # Allows the user to sign back in when they leave the site
                session["user"] = user_name
                session["sort_cards"] = False

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
                main_cursor = retrieve_cursor(db)

                # To ensure the username is in the database
                user_name = main_cursor.execute(
                    "SELECT * FROM user_info WHERE user_name = ?", (user,)
                )

                verify_user = user_name.fetchone()

                # To encourage user to register an account
                if not verify_user:
                    return __send_error(404)

                # To compare the password from the database and the user's
                # input to determine validity
                encode_pass = password.encode("utf-8")
                pass_hash = verify_user["hash"]
                result = bcrypt.checkpw(encode_pass, pass_hash)

                # To prevent user from entering into the account using
                # wrong password
                if not result:
                    return __send_error(401)

                # Logs session to the user to confirm everything works
                session["user"] = user
                session["sort_cards"] = False

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
            main_cursor = retrieve_cursor(db)

            # To find the user's id based on their session username to make
            # changes to the database information
            id_info = main_cursor.execute(
                "SELECT user_id FROM user_info WHERE user_name = ?", 
                    (session["user"],)
            )

            user_id = id_info.fetchone()

            # To run through all sets that the user contained in the database
            set_title = main_cursor.execute(
                "SELECT card_title FROM card_list WHERE user_id = ?", 
                (user_id["user_id"],)
            )

            sets_names = set_title.fetchall()

            # To see if any forms were submitted by the HTML page
            if request.method == "POST":

                # To add set name into the user's database 
                if 'create' in request.form:

                    card_title = request.form.get("create")

                    # To verify if the set title is not in the database
                    if not card_title:
                        return __send_error(404)

                    # To search in the collection of sets if name already
                    # taken
                    set_data = main_cursor.execute(
                        """SELECT * FROM card_list WHERE card_title = ? 
                        AND user_id = ?""", 
                        (card_title, user_id["user_id"])
                    )

                    card_names = set_data.fetchone()

                    # Warns user that the set already exist and can modify
                    # that set
                    if card_names:
                        return __send_error(409)

                    # To add the new set name into the user's database
                    main_cursor.execute(
                        """INSERT INTO card_list (user_id, card_title) 
                        VALUES (?, ?)""", 
                        (user_id["user_id"], card_title)
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
                    
                    # To check if the set already exists in the user's database
                    list_of_sets = []   
                    for v in sets_names:
                        list_of_sets.append(v["card_title"])


                    # Warns user of trying to change name of an invalid set
                    if old_name not in list_of_sets:
                        return __send_error(404)

                    # To permanently change the old set title with new set
                    # title 
                    main_cursor.execute(
                        """UPDATE card_list SET card_title = ?
                        WHERE user_id = ? AND card_title = ?""", 
                        (new_name, user_id["user_id"], old_name)
                    )

                    db.commit()
                    db.close()  

                    return redirect("/sets")

                if 'delete' in request.form:
                    user_request = request.form.get("delete")

                    # Warn user of trying to enter blank inputs
                    if not user_request:
                        return __send_error(404)

                    # To check if the set already exists in the user's database
                    list_of_sets = []   
                    for v in sets_names:
                        list_of_sets.append(v["card_title"])


                    # Warns user of trying to change name of an invalid set
                    if user_request not in list_of_sets:
                        return __send_error(404)

                    # To run through all sets that the user 
                    # contained in the database
                    set_id = main_cursor.execute(
                        """SELECT id FROM card_list WHERE user_id = ? AND
                        card_title = ?""", 
                        (user_id["user_id"], user_request)
                    )

                    result_id = set_id.fetchone()

                    # To permanently change the old set title with new set
                    # title 
                    main_cursor.execute(
                        """DELETE FROM flashcard WHERE card_set = ? AND
                        user_id = ?""", 
                        (result_id["id"], user_id["user_id"])
                    )

                    main_cursor.execute(
                        """DELETE FROM card_list WHERE id = ? AND
                        user_id = ?""", 
                        (result_id["id"], user_id["user_id"])
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
                    session["id"] = user_id["user_id"]

                    return redirect("/flashcard")

            return render_template("index.html", logged=user_logged,
                                    name=session["user"], flashcards=sets_names) 
        
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
            user_set = session["set"]  

            # Prevent the user from trying to access sets after not signed in
            if not user_logged:
                session.clear()
                return redirect("/")   

            # Creates the database connection to make query commits
            db = get_db(self.__DATABASE)
            main_cursor = retrieve_cursor(db)

            # To look for the specific set id to modify when adding flashcards
            set_data = main_cursor.execute(
                "SELECT id FROM card_list WHERE card_title = ?", (user_set,)
            )

            set_id = set_data.fetchone()

            print(session["sort_cards"])

            if not session["sort_cards"]:
                # To run through all the terms and definitions in a graph
                # for the user to see how many is in their set
                flashcards = main_cursor.execute(
                    "SELECT term, definition FROM flashcard WHERE card_set = ?",
                    (set_id["id"],)
                )
            else:
                flashcards = main_cursor.execute(
                    """SELECT term, definition FROM flashcard 
                    WHERE card_set = ? ORDER BY RANDOM()""",
                    (set_id["id"],) )
                
                session["sort_cards"] = False


            cards_list = flashcards.fetchall()

            # Creates a dummy flashcard if the user does not have any flashcards
            implement_dummy = not cards_list

            # To allow the user to make a new flashcard
            if request.method == "POST":

                if 'term' in request.form:
                    # Retrieve form information and prevents any blanks
                    new_term = request.form.get("term")
                    new_definition = request.form.get("definition")

                    if not new_term or not new_definition:
                        return __send_error(404)
                    
                    # Searches through the flashcards to see if term does not
                    # already exist
                    verify_term = main_cursor.execute(
                    """SELECT * FROM flashcard WHERE term = ? 
                    AND user_id = ? AND card_set = ?""",
                    (new_term, session["id"], int(set_id["id"]))
                    )

                    result = verify_term.fetchone()

                    # To instruct the user on how to properly create a flashcard
                    if result:
                        return __send_error(409)
                    
                    # To run through the set id based on the set_title
                    set_data = main_cursor.execute(
                        "SELECT id FROM card_list WHERE card_title = ?", 
                        (user_set,)
                    )

                    set_id = set_data.fetchone()

                    # Insert the new flashcard into that specific set
                    main_cursor.execute(
                    """INSERT INTO flashcard (user_id, card_set, term, definition) 
                    VALUES (?, ?, ?, ?);""", (session["id"], set_id["id"],
                                            new_term, new_definition)
                    )

                    db.commit()
                    db.close()

                    return redirect("/flashcard")     

                if 'replace_term' in request.form:
                    # Retrieve form information and prevents any blanks
                    replace_term = request.form.get("replace_term")
                    replace_def = request.form.get("replace_def")
                    old_term = request.form.get("old_term")
                    old_def = request.form.get("old_def")

                    if (not replace_term or not replace_def or not old_term
                        or not old_def):
                        return __send_error(404)
                    
                    # Searches through the flashcards to see if term does not
                    # already exist
                    verify_term = main_cursor.execute(
                    """SELECT * FROM flashcard WHERE term = ? 
                    AND user_id = ? AND card_set = ?""",
                    (old_term, session["id"], int(set_id["id"]))
                    )

                    result = verify_term.fetchone()

                    # To instruct the user on how to properly create a flashcard
                    if not result:
                        return __send_error(404)

                    main_cursor.execute("""UPDATE flashcard SET 
                                        term = ?, definition = ?
                                        WHERE card_set = ? AND user_id = ?
                                        AND term = ? AND definition = ?""",
                                        (replace_term, replace_def, set_id["id"]
                                        , session["id"], old_term, old_def)
                                        )

                    db.commit()
                    db.close()

                    return redirect("/flashcard")

                if 'del_flashcard' in request.form:
                    term_request = request.form.get("del_flashcard")

                    # To instruct the user on how to properly create a flashcard
                    if not term_request:
                        return __send_error(404)

                    verify_term = main_cursor.execute(
                    """SELECT * FROM flashcard WHERE term = ? 
                    AND user_id = ? AND card_set = ?""",
                    (term_request, session["id"], int(set_id["id"]))
                    )

                    result = verify_term.fetchone()

                    # To instruct the user on how to properly create a flashcard
                    if not result:
                        return __send_error(404)

                    main_cursor.execute("""DELETE FROM flashcard 
                                        WHERE term = ? AND card_set = ? AND
                                        user_id = ?
                                        """, (term_request, int(set_id["id"]),
                                               session["id"])
                                        )

                    db.commit()
                    db.close()

                    return redirect("/flashcard")

                if 'random_sort' in request.form:
                    session["sort_cards"] = True

                    return redirect("/flashcard")

            return render_template("flashcard.html", logged=user_logged,
                                    name=user_set, cards=cards_list,
                                    empty_list=implement_dummy)

# Runs the server necessary to start using the web application (for now)
if __name__ == "__main__":
    MainApp().run()
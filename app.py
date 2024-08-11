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
        self.__routes()

    def __routes(self):
        """
        The __routes() method runs inside the constructor used for starting
        the application. The method allows all routes to be registered and 
        running for interactivity with the HTML forms.
        """

        @self.route("/", methods=["GET", "POST"])
        def register():
            """
            The register() method sets the route to the default sign up
            page when you first enter into the website. This page only exists
            for people who are new to the application and wants to sign up.

            
            """

            if 'user' in session:
                return redirect("/sets")

            if request.method == "POST":
                user_name = request.form.get("username")
                password = request.form.get("password")
                confirm_pass = request.form.get("confirm_pass")

                if not user_name or not password or not confirm_pass:
                    error_msg = "404...INVALID USERNAME OR PASSWORD >:C"
                    return redirect(url_for("error", 
                                            message=error_msg, code=404))

                if password != confirm_pass:
                    error_msg = "404...Invalid Password Verification!!! :C"
                    return redirect(url_for("error", 
                                            message=error_msg, code=404))
                
                db = get_db(self.__DATABASE)
                main_cursor = retrieve_cursor(db)

                users_data = main_cursor.execute(
                    "SELECT * FROM user_info WHERE user_name = ?", (user_name,)
                )

                user = users_data.fetchone()

                if user:
                    error_msg = "409 Conflict! Username is already taken!!! >:C"
                    return redirect(url_for("error", 
                                            message=error_msg, code=409))

                pass_bytes = password.encode("utf-8")
                salt_key = bcrypt.gensalt()
                hash_key = bcrypt.hashpw(pass_bytes, salt_key)

                main_cursor.execute(
                    "INSERT INTO user_info (user_name, hash) VALUES (?, ?)", 
                    (user_name, hash_key)
                    )

                db.commit()
                db.close()

                session["user"] = user_name

                return redirect("/sets")

            return render_template("register.html")

        @self.route("/login", methods=["GET", "POST"])
        def login():
            if request.method == "POST":
                user = request.form.get("username")
                password = request.form.get("password")

                if not user or not password:
                    error_msg = "404...INVALID USERNAME OR PASSWORD >:C"
                    return redirect(url_for("error", 
                                            message=error_msg, code=404))

                db = get_db(self.__DATABASE)
                main_cursor = retrieve_cursor(db)

                user_name = main_cursor.execute(
                    "SELECT * FROM user_info WHERE user_name = ?", (user,)
                )

                verify_user = user_name.fetchone()

                if not verify_user:
                    error_msg = """404...Username doesn't exist in the database 
                    :CCCC"""
                    return redirect(url_for("error", 
                                            message=error_msg, code=404))

                encode_pass = password.encode("utf-8")

                pass_hash = verify_user["hash"]

                result = bcrypt.checkpw(encode_pass, pass_hash)

                if not result:
                    error_msg = "401...Invalid password!!!"
                    return redirect(url_for("error", 
                                            message=error_msg, code=401))

                session["user"] = user

                db.commit()
                db.close()

                return redirect("/sets")

            # Closes out any user information logged in
            session.clear()

            return render_template("login.html")    

        @self.route("/error")
        def error():
            error_reason = request.args.get("message")
            code = request.args.get("code")
            return render_template("error.html", code=error_reason), code   

        @self.route("/sets", methods=["GET", "POST"])
        def user_sets():
            user_logged = 'user' in session

            db = get_db(self.__DATABASE)
            main_cursor = retrieve_cursor(db)

            id_info = main_cursor.execute(
                "SELECT user_id FROM user_info WHERE user_name = ?", 
                    (session["user"],)
            )

            user_id = id_info.fetchone()

            set_title = main_cursor.execute(
                "SELECT card_title FROM card_list WHERE user_id = ?", 
                (user_id["user_id"],)
            )

            sets_names = set_title.fetchall()

            if request.method == "POST":
                if 'card_name' in request.form:
                    card_title = request.form.get("card_name")

                    if not card_title:
                        error_msg = "404 CARD TITLE SHOULD NEVER BE EMPTY >:C"
                        return redirect(url_for("error", 
                                                message=error_msg, code=404))

                    set_data = main_cursor.execute(
                        "SELECT * FROM card_list WHERE card_title = ?", 
                        (card_title,)
                    )

                    card_names = set_data.fetchone()

                    if card_names:
                        error_msg = """409 Card already exists in your set. 
                        Go back!"""
                        return redirect(url_for("error", 
                                                message=error_msg, code=409))

                    main_cursor.execute(
                        """INSERT INTO card_list (user_id, card_title) 
                        VALUES (?, ?)""", 
                        (user_id["user_id"], card_title)
                    )

                    db.commit()
                    db.close()

                    return redirect("/sets")

                if 'card_title' in request.form:
                    chosen_card = request.form.get("card_title")
                    session["set"] = chosen_card
                    session["id"] = user_id["user_id"]
                    return redirect("/flashcard")

            return render_template("index.html", logged=user_logged,
                                    name=session["user"], flashcards=sets_names) 
        
        @self.route("/flashcard", methods=["GET", "POST"])
        def flashcard():
            user_logged = 'user' in session
            user_set = session["set"]     

            db = get_db(self.__DATABASE)
            main_cursor = retrieve_cursor(db)

            set_data = main_cursor.execute(
                "SELECT id FROM card_list WHERE card_title = ?", (user_set,)
            )

            set_id = set_data.fetchone()

            flashcards = main_cursor.execute(
                "SELECT term, definition FROM flashcard WHERE card_set = ?",
                (set_id["id"],)
            )

            cards_list = flashcards.fetchall()

            implement_dummy = not cards_list

            if request.method == "POST":
                new_term = request.form.get("term")
                new_definition = request.form.get("definition")

                if not new_term or not new_definition:
                    error_msg = "404 FLASHCARD SHOULD NEVER BE EMPTY >:C"
                    return redirect(url_for("error", 
                                            message=error_msg, code=404))
                
                verify_term = main_cursor.execute(
                """SELECT * FROM flashcard WHERE term = ? 
                AND user_id = ? AND card_set = ?""",
                (new_term, session["id"], int(set_id["id"]))
                )

                result = verify_term.fetchone()

                if result:
                    error_msg = """409 Conflict! Flashcard already exists! 
                    Use update button!!!"""
                    return redirect(url_for("error", 
                                            message=error_msg, code=409))
                
                set_data = main_cursor.execute(
                    "SELECT id FROM card_list WHERE card_title = ?", (user_set,)
                )

                set_id = set_data.fetchone()

                main_cursor.execute(
                """INSERT INTO flashcard (user_id, card_set, term, definition) 
                VALUES (?, ?, ?, ?);""", (session["id"], set_id["id"],
                                        new_term, new_definition)
                )

                db.commit()
                db.close()

                return redirect("/flashcard")       

            return render_template("flashcard.html", logged=user_logged,
                                    name=user_set, cards=cards_list,
                                    empty_list=implement_dummy)

if __name__ == "__main__":
    run_instance = MainApp()
    run_instance.run()
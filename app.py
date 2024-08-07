from flask import (
    Flask, render_template, request, redirect, session, g, url_for
)
from flask_session import Session
import sqlite3
import bcrypt

app = Flask(__name__)

DATABASE = "user_database.db"
# Database connection information
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

# Session information
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET", "POST"])
def register():
    if 'user' in session:
        return redirect("/sets")

    if request.method == "POST":
        user_name = request.form.get("username")
        password = request.form.get("password")
        confirm_pass = request.form.get("confirm_pass")

        if not user_name or not password or not confirm_pass:
            error_msg = "404...INVALID USERNAME OR PASSWORD >:C"
            return redirect(url_for("error", message=error_msg, code=404))

        if password != confirm_pass:
            error_msg = "404...Invalid Password Verification!!! :C"
            return redirect(url_for("error", message=error_msg, code=404))
        
        main_db = get_db()
        main_db.row_factory = make_dicts

        main_cursor = main_db.cursor()

        data = main_cursor.execute(
            "SELECT * FROM user_info WHERE user_name = ?", (user_name,)
        )

        user_list = data.fetchone()

        if user_list:
            error_msg = "409 Conflict! Username is already taken!!! >:C"
            return redirect(url_for("error", message=error_msg, code=409))

        pass_bytes = password.encode("utf-8")

        salt_key = bcrypt.gensalt()

        hash_key = bcrypt.hashpw(pass_bytes, salt_key)

        main_cursor.execute(
            "INSERT INTO user_info (user_name, hash) VALUES (?, ?)", 
            (user_name, hash_key)
            )

        main_db.commit()
        main_db.close()

        session["user"] = user_name

        return redirect("/sets")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        user = request.form.get("username")
        password = request.form.get("password")

        if not user or not password:
            error_msg = "404...INVALID USERNAME OR PASSWORD >:C"
            return redirect(url_for("error", message=error_msg, code=404))
        
        main_db = get_db()
        main_db.row_factory = make_dicts

        cursor = main_db.cursor()

        user_data = cursor.execute(
            "SELECT * FROM user_info WHERE user_name = ?", (user,)
        )

        users_list = user_data.fetchone()

        if not users_list:
            error_msg = "404...Username doesn't exist in the database :CCCC"
            return redirect(url_for("error", message=error_msg, code=404))

        encode_pass = password.encode("utf-8")

        verify_pass = users_list["hash"]

        print(verify_pass)

        result = bcrypt.checkpw(encode_pass, verify_pass)

        if not result:
            error_msg = "401...Invalid password!!!"
            return redirect(url_for("error", message=error_msg, code=401))

        session["user"] = user

        main_db.commit()
        main_db.close()

        return redirect("/sets")

    # Closes out any user information logged in
    session.clear()

    return render_template("login.html")

@app.route("/error")
def error():
    error_reason = request.args.get("message")
    code = request.args.get("code")
    return render_template("error.html", code=error_reason), code
    

@app.route("/sets", methods=["GET", "POST"])
def user_sets():
    user_logged = 'user' in session
    main_db = get_db()
    main_db.row_factory = make_dicts
    main_cursor = main_db.cursor()

    retrieve_id = main_cursor.execute(
        "SELECT user_id FROM user_info WHERE user_name = ?", 
            (session["user"],)
    )

    id = retrieve_id.fetchone()

    info = main_cursor.execute(
        "SELECT card_title FROM card_list WHERE user_id = ?", (id["user_id"],)
    )

    all_titles = info.fetchall()

    if request.method == "POST":
        card_title = request.form.get("card_name")

        if not card_title:
            error_msg = "404 CARD TITLE SHOULD NEVER BE EMPTY >:C"
            return redirect(url_for("error", message=error_msg, code=404))

        data = main_cursor.execute(
            "SELECT * FROM card_list WHERE card_title = ?", (card_title,)
        )

        card_names = data.fetchone()

        if card_names:
            error_msg = "409 Card already exists in your set. Go back!"
            return redirect(url_for("error", message=error_msg, code=409))

        main_cursor.execute(
            "INSERT INTO card_list (user_id, card_title) VALUES (?, ?)", 
            (id["user_id"], card_title)
        )

        main_db.commit()
        main_db.close()

        return redirect("/sets")

    return render_template("index.html", logged=user_logged,
                            name=session["user"], flashcards=all_titles)

@app.route("/flashcard", methods=["GET", "POST"])
def enter_flashcard():
    user_logged = 'user' in session
    error_msg = "Not supposed to be here...Go back!!! >:CCCCCCCCC"

    if request.method == "POST":
        title = request.form.get("card_title")

        main_db = get_db()
        main_db.row_factory = make_dicts
        main_cursor = main_db.cursor()        

        set_data = main_cursor.execute(
            "SELECT id FROM card_list WHERE card_title = ?", (title,)
        )

        set_id = set_data.fetchone()
        print(set_id)

        main_cursor.execute(
            """INSERT INTO flashcard (card_id, term, definition) 
            VALUES (?, 'Hello', ':)')""", (set_id["id"],)
        )

        flashcards = main_cursor.execute(
            "SELECT term, definition FROM flashcard WHERE card_id = ?",
              (set_id["id"],)
        )

        cards_list = flashcards.fetchall()

        return render_template("flashcard.html", logged=user_logged,
                                name=title, cards=cards_list)

    return redirect(url_for("error", message=error_msg, code=403))

# Debuggging purposes
if __name__ == "__main__":
    app.run(debug=True)
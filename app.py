from flask import Flask, render_template, request, redirect, session, g, url_for
from flask_session import Session
import sqlite3

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


# Session information
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user_name = request.form.get("username")
        password = request.form.get("password")
        confirm_pass = request.form.get("confirm_pass")

        if not user_name or not password or not confirm_pass:
            error_msg = "404...INVALID USERNAME OR PASSWORD >:C"
            return redirect(url_for("error", message=error_msg))

        if password != confirm_pass:
            error_msg = "404...Invalid Password Verification!!! :C"
            return redirect(url_for("error", message=error_msg))
        
        main_db = get_db().cursor()
        user_list = main_db.execute(
            "SELECT * FROM user_info WHERE user_name = ?", (user_name,)
        )
        
        print(user_list)
        return redirect("/sets")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    # Closes out any user information logged in
    session.clear()

    if request.method == "POST":
        return redirect("/sets")

    return render_template("login.html")

@app.route("/error")
def error():
    error_reason = request.args.get("message")
    return render_template("error.html", code=error_reason)
    

@app.route("/sets")
def user_sets():
    return render_template("index.html")

# Debuggging purposes
if __name__ == "__main__":
    app.run(debug=True)
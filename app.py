from flask import Flask, render_template, request, redirect, session
from flask_session import Session

app = Flask(__name__)

# Session information
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = 'supersecretkey'
Session(app)

@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        session["user_signed"] = True
        return redirect("/sets")

    session["user_signed"] = False
    return render_template("register.html", logged=session.get("user_signed"))

@app.route("/sets")
def user_sets():
    return render_template("index.html", logged=session.get("user_signed"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["user_signed"] = True
        return redirect("/sets")

    return render_template("login.html", logged=session.get("user_signed"))


# Debuggging purposes
if __name__ == "__main__":
    app.run(debug=True)
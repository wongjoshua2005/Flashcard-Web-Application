from flask import Flask, render_template, request, redirect
from flask_session import Session

app = Flask(__name__)

# Session information
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
user_signed = False

@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        global user_signed
        user_signed = True
        return redirect("/home")
    
    user_signed = False
    return render_template("register.html", logged=user_signed)

@app.route("/home")
def home():
    return render_template("index.html", logged=user_signed)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        global user_signed
        user_signed = True
        return redirect("/home")

    user_signed = False
    return render_template("login.html")
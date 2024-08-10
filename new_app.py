"""
Joshua Wong
Summer 2024
app.py
"""

# To retrieve the password encryption, Flask framework, and SQLite modifications
from flask import (
    Flask, render_template, request, redirect, session, url_for
)
import bcrypt
from flask_session import Session
from sql_helper import SQLHelper

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

        self.__app = super().__init__(__name__)

        __DATABASE = "user_database.db"
        self.__db = SQLHelper(__DATABASE)
        self.__main_cursor = self.__db.retrieve_cursor()

        # Set up the session configuration for the user to stay logged in
        self.__app.config["SESSION_PERMANENT"] = False
        self.__app.config["SESSION_TYPE"] = "filesystem"
        Session(self.__app)

        self.__routes()

    def run(self):
        self.app.run()

    def __routes(self):
        
        @self.__app.route("/", methods=["GET", "POST"])
        def register():
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

                users_data = self.__main_cursor.execute(
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

                self.__main_cursor.execute(
                    "INSERT INTO user_info (user_name, hash) VALUES (?, ?)", 
                    (user_name, hash_key)
                    )

                self.__db.commit()
                self.__db.close_connection()

                session["user"] = user_name

                return redirect("/sets")

            return render_template("register.html")

        @self.__app.route("/login", methods=["GET", "POST"])
        def login():
            if request.method == "POST":
                user = request.form.get("username")
                password = request.form.get("password")

                if not user or not password:
                    error_msg = "404...INVALID USERNAME OR PASSWORD >:C"
                    return redirect(url_for("error", 
                                            message=error_msg, code=404))

                user_name = self.__main_cursor.execute(
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

                self.__db.commit()
                self.__db.close()

                return redirect("/sets")

            # Closes out any user information logged in
            session.clear()

            return render_template("login.html")        


if __name__ == "__main__":
    MainApp().run()





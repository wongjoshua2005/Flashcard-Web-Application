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

        # Set up the session configuration for the user to stay logged in
        self.__app.config["SESSION_PERMANENT"] = False
        self.__app.config["SESSION_TYPE"] = "filesystem"
        Session(self.__app)

        





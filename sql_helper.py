import sqlite3
from flask import g

class SQLHelper:
    """
    The SQLHelper class sets up the sqlite3 for any Flask
    app with ease without having to go through massive hurdles of running
    many database objects and taking up memory. The class will contain methods
    such as initializing the database, converting the cursor object to 
    a dictionary, and executing queries.
    """

    def __init__(self, app, database_name):
        """
        The constructor for the class will create a single database that
        can be modified based on the reference. Useful for having one reference
        to do all SQLite tasks.

        Args:
            database_name (String): The name of the database to connect
        """

        self.__app = app

        self.__database = self.__get_db(database_name)


    



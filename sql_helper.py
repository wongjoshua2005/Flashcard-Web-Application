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

    def __init__(self, database_name):
        """
        The constructor for the class will create a single database that
        can be modified based on the reference. Useful for having one reference
        to do all SQLite tasks.

        Args:
            database_name (String): The name of the database to connect
        """
        self.__database = self.__get_db(database_name)

    def __get_db(self, db_name):
        """
        The __get_db() method handles starting a new connection for the
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
    
    def close_connection(self, exception):
        """
        The __close_connection() method allows the database connection
        object to close after making changes to the database.

        Args:
            exception (Exception): The parameter handles any exceptions
            occuring when closing the connection.
        """

        # Searches for the database connection to close it
        db = getattr(g, '_database', None)

        # Closes database if connection exists
        if db is not None:
            db.close()

    def retrieve_cursor(self):
        self.__database.row_factory = sqlite3.Row
        db_cursor = self.__database.cursor()

        return db_cursor


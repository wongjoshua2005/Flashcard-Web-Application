from flask import Flask, render_template, request

class MainApp:

    def __init__(self):
        self.__app = Flask(__name__)
        self.__setup_routes()

    def __setup_routes(self):
        @self.__app.route("/")
        def index():
            return render_template("index.html")

    def run_app(self):
        self.__app.run()

# Runs the flask application
if __name__ == "__main__":
    MainApp().run_app()
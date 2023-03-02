from flask import Flask
from controllers.database_controller import database_controller

app = Flask(__name__)

app.register_blueprint(database_controller)

if __name__ == '__main__':
    app.run(debug=True)
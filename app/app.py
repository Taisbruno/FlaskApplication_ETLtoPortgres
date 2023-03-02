from flask import Flask
from controllers.data_controller import data_controller

app = Flask(__name__)

app.register_blueprint(data_controller)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
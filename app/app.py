from flask import Flask
from controllers.data_controller import data_controller

app = Flask(__name__, template_folder='view')

app.register_blueprint(data_controller)

if __name__ == '__main__': # Iniciando a aplicação Flask
    app.run(host='0.0.0.0', debug=True)
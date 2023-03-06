from flask import Flask
from controllers.data_controller import data_controller

def create_app():
    app = Flask(__name__, template_folder='view')
    app.register_blueprint(data_controller)
    return app

if __name__ == '__main__': # Iniciando a aplicação Flask
    app = create_app()
    app.run(host='0.0.0.0', debug=True)
from flask import Blueprint, render_template, redirect, request, url_for
from services.data_service import DatabaseService
from werkzeug.utils import secure_filename

database_controller = Blueprint('database_controller', __name__)
service = DatabaseService()

@database_controller.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            file = request.files['file']
            if file and service.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(service.get_upload_folder() + filename)
                df = service.manipulate_data(file.filename)
                service.insert_data(df)
                return redirect(url_for('database_controller.download_file'))
        except Exception as e:
            return redirect(url_for('database_controller.show_error', error=str(e)))
    return render_template('index.html')
    
@database_controller.route('/upload', methods=['GET', 'POST'])
def download_file():
    return render_template('sent.html')

@database_controller.errorhandler(Exception)
def handle_error(e):
    return redirect(url_for('database_controller.show_error', error=str(e)))

@database_controller.route('/error')
def show_error():
    error_message = request.args.get('error')
    return render_template('error.html', error_message=error_message)

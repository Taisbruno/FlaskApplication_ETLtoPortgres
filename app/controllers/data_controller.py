from flask import Blueprint, render_template, redirect, request, url_for
from services.data_service import DataService
from werkzeug.utils import secure_filename

data_controller = Blueprint('data_controller', __name__)
service = DataService()

@data_controller.route('/', methods=['GET', 'POST']) # Rota raiz da aplicação para upload de arquivo
def upload_file():
    if request.method == 'POST':
        try:
            file = request.files['file'] # obtém o arquivo enviado pelo usuário
            if file and service.allowed_file(file.filename): # verifica se o tipo de arquivo é permitido
                filename = secure_filename(file.filename)
                file.save(service.get_upload_folder() + filename) # salva o arquivo
                df = service.manipulate_data(file.filename) # manipula os dados do arquivo
                service.insert_data(df) # insere os dados no banco
                return redirect(url_for('data_controller.download_file')) # redireciona para a página de sucesso
        except Exception as e:
            return redirect(url_for('data_controller.show_error', error=str(e))) # redireciona para a página de erro
    return render_template('index.html') # renderiza página de upload
    
@data_controller.route('/upload', methods=['GET', 'POST']) # Rota para a página de sucesso
def download_file():
    return render_template('sent.html')

@data_controller.errorhandler(Exception) # Manipulador de erro para a aplicação
def handle_error(e):
    return redirect(url_for('data_controller.show_error', error=str(e))) # Redireciona para a página de erro

@data_controller.route('/error') # Rota para a página de erro
def show_error():
    error_message = request.args.get('error') # Obtém a mensagem de erro da query string
    return render_template('error.html', error_message=error_message) # Renderiza a página de erro com a mensagem

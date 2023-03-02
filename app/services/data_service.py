import pandas as pd
from repository.database_repository import DbRepository
import os
from dotenv import load_dotenv
from pycpfcnpj import cpfcnpj

load_dotenv()

db_config = {
    'host': os.getenv('DATABASE_HOST'),
    'database': os.getenv('DATABASE_NAME'),
    'user': os.getenv('DATABASE_USER'),
    'password': os.getenv('DATABASE_PASSWORD')
}

class DatabaseService:
    def __init__(self):
        self.db_repo = DbRepository(db_config)
        self.db_repo.connect()

    def manipulate_data(self, filename):
        delimiter = self.get_delimiter(filename)
        try:
            df = pd.read_csv(
                filename, delimiter=delimiter, skiprows=1, header=None, decimal=','
            )
            df.columns = [
                'cpf', 'private', 'incompleto', 'data da ultima compra', 
                'ticket medio', 'ticket da ultima compra', 'loja mais frequente', 'loja da ultima compra'
                ]
            df = df.applymap(lambda x: str(x).replace(',', '.') if isinstance(x, float) else x)
            self.validate_cpf_cnpj(df)
            print(df)
            return df
        except pd.errors.ParserError:
            raise ValueError('Error parsing file')
        except Exception as e:
            raise ValueError(str(e))
    
    def get_delimiter(self, filename):
        if filename.endswith('.csv'):
            return ','
        elif filename.endswith('.txt'):
            return '\s+'
        raise ValueError('Invalid file format. Allowed formats: .csv and .txt')
    
    def validate_cpf_cnpj(self, df):
        for i, row in df.iterrows():
            cpf = row['cpf']
            cnpj = row['loja da ultima compra']
            if not cpfcnpj.validate(cpf):
                raise ValueError(f"Invalid CPF on row {i+1}")
            elif cnpj != 'nan' and not cpfcnpj.validate(cnpj):
                raise ValueError(f"Invalid CNPJ on row {i+1}")
                
    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in {'txt', 'csv'}

    def get_upload_folder(self):
        return './'

    def insert_data(self, df):
        try:
            self.db_repo.connect()
            self.db_repo.drop_table()
            self.db_repo.create_table()  # Criação da tabela no banco de dados
            self.db_repo.insert_data(df)
            self.db_repo.commit()
        except Exception as e:
            raise ValueError(str(e))

    def __del__(self):
        self.db_repo.close()

import pandas as pd
from repository.data_repository import DbRepository
import os
from dotenv import load_dotenv
from pycpfcnpj import cpfcnpj
import logging
from unidecode import unidecode

load_dotenv()

# Configuração para conexão com o banco de dados
db_config = { 
    'host': os.getenv('DATABASE_HOST'),
    'database': os.getenv('DATABASE_NAME'),
    'user': os.getenv('DATABASE_USER'),
    'password': os.getenv('DATABASE_PASSWORD')
}

class DataService:
    def __init__(self):
        self.db_repo = DbRepository(db_config)
        self.db_repo.connect()

        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger()

    def manipulate_data(self, filename): # Método para manipulação dos dados
        delimiter = self.get_delimiter(filename) # Identifica o delimitador do arquivo (CSV ou TXT)
        try:
            df = pd.read_csv( # Carrega o arquivo CSV ou TXT para um dataframe Pandas
                filename, delimiter=delimiter, skiprows=1, header=None, decimal=','
            )
            df.columns = [ # Define os nomes das colunas do dataframe
                'cpf', 'private', 'incompleto', 'data da ultima compra', 
                'ticket medio', 'ticket da ultima compra', 'loja mais frequente', 'loja da ultima compra'
                ]
            df = self.clean_data(df) # Limpeza dos dados
            self.validate_cpf_cnpj(df) # Valida CPFs e CNPJs das linhas do dataframe
            self.logger.debug(df)
            return df
        except pd.errors.ParserError:
            raise ValueError('Error parsing file')
        except Exception as e:
            raise ValueError(str(e))
    
    def get_delimiter(self, filename): # Identifica o delimitador do arquivo
        if filename.endswith('.csv'):
            return ','
        elif filename.endswith('.txt'):
            return '\s+'
        raise ValueError('Invalid file format. Allowed formats: .csv and .txt')
    
    def clean_data(self, df):
        df = df.drop_duplicates(subset=['cpf']) # Remove linhas duplicadas com base na coluna 'cpf'
        df = df.applymap(lambda x: str(x).lower() if isinstance(x, str) else x) # Converte para minúsculas
        df = df.applymap(lambda x: unidecode(str(x)) if isinstance(x, str) else x) # Substitui caracteres especiais
        df[['loja da ultima compra', 'loja mais frequente']] = df[['loja da ultima compra', 'loja mais frequente']].replace('\D', '', regex=True) # Substitui não dígitos por uma string vazia em CNPJs
        df['cpf'] = df['cpf'].apply(lambda x: ''.join(filter(str.isdigit, str(x)))) # Formata a coluna 'cpf' para conter apenas dígitos
        df['data da ultima compra'] = pd.to_datetime(df['data da ultima compra']).dt.strftime('%Y-%m-%d') # Padroniza datas
        df = df.applymap(lambda x: str(x).replace(',', '.') if isinstance(x, float) and not pd.isna(x) else x) # Troca vírgula por ponto em valores do tipo float e não nulo
        df = df.where(pd.notnull(df), None) # Substitui valores nulos por None em todas as colunas
        return df
    
    def validate_cpf_cnpj(self, df):  # Valida CPFs e CNPJs das linhas do dataframe
        for i, row in df.iterrows():
            cpf = str(row['cpf'])
            cnpj1 = str(row['loja da ultima compra'])
            cnpj2 = str(row['loja mais frequente'])
            try:
                if not cpfcnpj.validate(cpf):
                    self.logger.warning(f"Invalid CPF on row {i+1}")
                if (cnpj1 != 'None' and not cpfcnpj.validate(cnpj1)) or (cnpj2 != 'None' and not cpfcnpj.validate(cnpj2)):
                    self.logger.warning(f"Invalid CNPJ on row {i+1}")
            except Exception as e:
                self.logger.warning(f"Error validating row {i+1}: {str(e)}")
                
    def allowed_file(self, filename): # Verifica se o formato do arquivo é permitido
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in {'txt', 'csv'}

    def get_upload_folder(self):
        return './'

    def insert_data(self, df): 
        try:
            self.db_repo.connect()
            self.db_repo.drop_table()
            self.db_repo.create_table()
            self.db_repo.insert_data(df)
            self.db_repo.commit() # Commit da transação
        except Exception as e:
            raise ValueError(str(e))

    def __del__(self): # Fecha a conexão quando o objeto é deletado
        self.db_repo.close()

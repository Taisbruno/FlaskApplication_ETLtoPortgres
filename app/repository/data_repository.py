import psycopg2
import psycopg2.extras

class DbRepository: 
    def __init__(self, db_config): 
        self.db_config = db_config
        self.conn = None
        self.cursor = None

    def connect(self): # Método que estabelece a conexão com o banco de dados
        self.conn = psycopg2.connect(**self.db_config)
        self.cursor = self.conn.cursor()

    def create_table(self): # Método que cria a tabela no banco
        create_table_query = """
            CREATE TABLE IF NOT EXISTS clientes (
                cpf VARCHAR PRIMARY KEY,
                private INT,
                incompleto INT,
                data_ultima_compra DATE,
                ticket_medio FLOAT,
                ticket_ultima_compra FLOAT,
                loja_mais_frequente VARCHAR(14),
                loja_ultima_compra VARCHAR(14)
            );
        """
        self.cursor.execute(create_table_query)

    def insert_data(self, data): # Método que insere os dados no banco
        insert_query = """
            INSERT INTO clientes (
                cpf,
                private,
                incompleto,
                data_ultima_compra,
                ticket_medio,
                ticket_ultima_compra,
                loja_mais_frequente,
                loja_ultima_compra
            ) VALUES %s
        """
        values = [(row['cpf'], row['private'], row['incompleto'], row['data da ultima compra'], row['ticket medio'],
                   row['ticket da ultima compra'], row['loja mais frequente'], row['loja da ultima compra']) for _, row in data.iterrows()]
        psycopg2.extras.execute_values(self.cursor, insert_query, values)

    def drop_table(self): # Método que apaga a tabela do banco, caso a mesma já exista
        drop_table_query = """
            DROP TABLE IF EXISTS clientes;
        """
        self.cursor.execute(drop_table_query)

    def commit(self): # Método que efetua o commit das alterações realizadas
        self.conn.commit()

    def close(self): # Fechamento da conexão com o banco e do cursor utilizado para executar as operações
        self.cursor.close()
        self.conn.close()
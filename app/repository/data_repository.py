import psycopg2

class DbRepository:
    def __init__(self, db_config):
        self.db_config = db_config
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = psycopg2.connect(**self.db_config)
        self.cursor = self.conn.cursor()

    def create_table(self):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS test (
                cpf VARCHAR PRIMARY KEY,
                private INT,
                incompleto INT,
                data_ultima_compra VARCHAR(10),
                ticket_medio FLOAT,
                ticket_ultima_compra FLOAT,
                loja_mais_frequente VARCHAR(18),
                loja_ultima_compra VARCHAR(18)
            );
        """
        self.cursor.execute(create_table_query)

    def insert_data(self, data):
        insert_query = """
            INSERT INTO test (
                cpf,
                private,
                incompleto,
                data_ultima_compra,
                ticket_medio,
                ticket_ultima_compra,
                loja_mais_frequente,
                loja_ultima_compra
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        for _, row in data.iterrows():
            self.cursor.execute(insert_query, (
                row['cpf'],
                row['private'],
                row['incompleto'],
                row['data da ultima compra'],
                row['ticket medio'],
                row['ticket da ultima compra'],
                row['loja mais frequente'],
                row['loja da ultima compra']
            ))

    def drop_table(self):
        drop_table_query = """
            DROP TABLE IF EXISTS test;
        """
        self.cursor.execute(drop_table_query)

    def commit(self):
        self.conn.commit()


    def close(self):
        self.cursor.close()
        self.conn.close()

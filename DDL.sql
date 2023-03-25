-- Tabela que armazena informações de clientes de uma loja

CREATE TABLE IF NOT EXISTS clientes (
    cpf VARCHAR PRIMARY KEY,          -- CPF do cliente (chave primária)
    private INT,                      -- Indica se o cliente é uma pessoa privada ou empresa
    incompleto INT,                   -- Indica se o cadastro do cliente está incompleto
    data_ultima_compra DATE,          -- Data da última compra do cliente no formato AAAA-MM-DD
    ticket_medio FLOAT,               -- Valor médio dos tickets de compra do cliente
    ticket_ultima_compra FLOAT,       -- Valor do ticket da última compra do cliente
    loja_mais_frequente VARCHAR(14),  -- CNPJ da loja onde o cliente mais fez compras
    loja_ultima_compra VARCHAR(14)    -- CNPJ da loja onde o cliente fez a última compra
);
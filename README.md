# Aplicação Flask com ETL para o Postgres

Aplicação Flask que recebe um arquivo no formato .txt ou .csv (a exemplo do base_teste.txt), trata os dados que estão dentro do arquivo e salva-os dentro do banco de dados Postgres. A aplicação também valida os CPF's e CNPJ's contidos no arquivo, alerta caso haja CPF's ou CNPJ's inválidos, mas não impede a inserção do dado no banco.

## Tecnologias utilizadas

- Python
- Pandas
- Flask
- PostgreSQL
- Docker

## Instalação

1. Certifique-se de ter o Docker e o Docker Compose instalados em sua máquina.

## Funcionalidades

- Recebe o upload de um arquivo no formato .txt ou .csv
- Salva o arquivo em questão
- Processa e trata os dados existentes dentro do arquivo
- Insere as informações no banco de dados PostgreSQL

## Como usar

1. Clone este repositório
2. No terminal, navegue até a raiz do projeto e execute o comando: **docker-compose up --build**
3. Aguarde até que os serviços sejam executados e o aplicativo esteja disponível na porta 5000. Você pode acessar a aplicação em seu navegador em http://localhost:5000
4. Faça upload do arquivo base_teste.txt ou base_teste.csv
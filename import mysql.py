import mysql.connector

# Função para conectar ao banco de dados
def conectar():
    conn = mysql.connector.connect(
        host='localhost',    # Endereço do servidor MySQL
        user='root',         # Usuário do MySQL
        password='', # Senha do MySQL
        database='cidades2' # Nome do banco de dados
    )
    return conn

# Testar a conexão
try:
    conn = conectar()
    if conn.is_connected():
        print("Conexão com o banco de dados foi um sucesso!")
    conn.close()  # Fechar a conexão depois do teste
except mysql.connector.Error as err:
    print(f"Erro: {err}")

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cidades (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100),
            estado VARCHAR(100)
        )
    ''')
    conn.commit()
    conn.close()

# Executar a função
criar_tabela()
def inserir_cidade(nome, estado):
    conn = conectar()
    cursor = conn.cursor()
    # Inserir dados na tabela
    cursor.execute('INSERT INTO cidades (nome, estado) VALUES (%s, %s)', (nome, estado))
    conn.commit()
    conn.close()

# Exemplo de inserção de dados
inserir_cidade('Itumbiara', 'GO')
print("Dados inseridos com sucesso!")


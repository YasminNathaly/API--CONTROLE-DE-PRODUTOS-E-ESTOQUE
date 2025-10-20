import psycopg2

def conectar():
    try:
        conexao = psycopg2.connect(
            host="localhost",
            database="estoque_db",   # coloque o nome do seu banco
            user="postgres",          # seu usuário
            password="minhasenha123"  # sua senha
        )
        cursor = conexao.cursor()
        return conexao, cursor
    except Exception as erro:
        print(f"Erro ao conectar ao banco de dados: {erro}")
        return None, None

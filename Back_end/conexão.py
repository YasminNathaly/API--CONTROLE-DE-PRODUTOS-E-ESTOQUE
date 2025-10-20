import psycopg2

def conectar():
    try:
        conexao = psycopg2.connect(
            host="localhost",
            database="nome_do_banco",
            user="seu_usuario",
            password="dev1t@24"   # <- muito importante!
        )
        cursor = conexao.cursor()
        return conexao, cursor
    except Exception as erro:
        print(f"Erro ao conectar ao banco de dados: {erro}")
        return None, None
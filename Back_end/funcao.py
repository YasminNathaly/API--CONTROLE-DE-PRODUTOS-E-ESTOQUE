from conexao import conectar

# Criar tabela de produtos
def criar_tabela():
    conexao, cursor = conectar()
    if conexao:
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS produtos (
                    id SERIAL PRIMARY KEY,
                    nome TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    preco REAL NOT NULL,
                    quantidade INTEGER NOT NULL
                )
            """)
            conexao.commit()
        except Exception as erro:
            print(f"Erro ao criar a tabela: {erro}")
        finally:
            cursor.close()
            conexao.close()

criar_tabela()

# Inserir um produto
def criar_produto(nome, categoria, preco, quantidade):
    conexao, cursor = conectar()
    if conexao:
        try:
            cursor.execute(
                "INSERT INTO produtos (nome, categoria, preco, quantidade) VALUES (%s, %s, %s, %s)",
                (nome, categoria, preco, quantidade)
            )
            conexao.commit()
        except Exception as erro:
            print(f'Erro ao inserir produto: {erro}')
        finally:
            cursor.close()
            conexao.close()

# Listar todos os produtos
def listar_produtos():
    conexao, cursor = conectar()
    if conexao:
        try:
            cursor.execute("SELECT * FROM produtos ORDER BY id")
            return cursor.fetchall()
        except Exception as erro:
            print(f'Erro ao listar produtos: {erro}')
            return []
        finally:
            cursor.close()
            conexao.close()
# Atualizar um produto
def atualizar_produto(id, nome, categoria, preco, quantidade):
    conexao, cursor = conectar()
    if conexao:
        try:
            cursor.execute(
                "UPDATE produtos SET nome=%s, categoria=%s, preco=%s, quantidade=%s WHERE id=%s",
                (nome, categoria, preco, quantidade, id)
            )
            conexao.commit()
        except Exception as erro:
            print(f'Erro ao atualizar produto: {erro}')
        finally:
            cursor.close()
            conexao.close()
# Deletar um produto
def deletar_produto(id):
    conexao, cursor = conectar()
    if conexao:
        try:
            cursor.execute("DELETE FROM produtos WHERE id=%s", (id,))
            conexao.commit()
        except Exception as erro:
            print(f'Erro ao deletar produto: {erro}')
        finally:
            cursor.close()
            conexao.close()
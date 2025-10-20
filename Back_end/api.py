from fastapi import FastAPI
from conexao import conectar

app = FastAPI(title="API de Produtos e Estoque")

# Criar tabela se não existir
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
            print(f"Erro ao criar tabela: {erro}")
        finally:
            cursor.close()
            conexao.close()

criar_tabela()

# Endpoints

@app.get("/produtos")
def listar_produtos():
    conexao, cursor = conectar()
    if conexao:
        try:
            cursor.execute("SELECT * FROM produtos ORDER BY id")
            produtos = cursor.fetchall()
            # Retorna lista de dicionários
            resultado = []
            for p in produtos:
                resultado.append({
                    "id": p[0],
                    "nome": p[1],
                    "categoria": p[2],
                    "preco": p[3],
                    "quantidade": p[4]
                })
            return resultado
        except Exception as erro:
            return {"erro": f"Erro ao listar produtos: {erro}"}
        finally:
            cursor.close()
            conexao.close()
    return {"erro": "Não foi possível conectar ao banco"}

@app.post("/produtos")
def criar_produto(produto: dict):
    conexao, cursor = conectar()
    if conexao:
        try:
            nome = produto.get("nome")
            categoria = produto.get("categoria")
            preco = produto.get("preco")
            quantidade = produto.get("quantidade")

            cursor.execute(
                "INSERT INTO produtos (nome, categoria, preco, quantidade) VALUES (%s, %s, %s, %s) RETURNING id",
                (nome, categoria, preco, quantidade)
            )
            id_criado = cursor.fetchone()[0]
            conexao.commit()
            return {"id": id_criado, "message": "Produto criado com sucesso!"}
        except Exception as erro:
            return {"erro": f"Erro ao criar produto: {erro}"}
        finally:
            cursor.close()
            conexao.close()
    return {"erro": "Não foi possível conectar ao banco"}

@app.put("/produtos/{produto_id}")
def atualizar_produto(produto_id: int, produto: dict):
    conexao, cursor = conectar()
    if conexao:
        try:
            nome = produto.get("nome")
            categoria = produto.get("categoria")
            preco = produto.get("preco")
            quantidade = produto.get("quantidade")

            cursor.execute(
                "UPDATE produtos SET nome=%s, categoria=%s, preco=%s, quantidade=%s WHERE id=%s",
                (nome, categoria, preco, quantidade, produto_id)
            )
            conexao.commit()
            if cursor.rowcount == 0:
                return {"erro": "Produto não encontrado"}
            return {"message": "Produto atualizado com sucesso!"}
        except Exception as erro:
            return {"erro": f"Erro ao atualizar produto: {erro}"}
        finally:
            cursor.close()
            conexao.close()
    return {"erro": "Não foi possível conectar ao banco"}

@app.delete("/produtos/{produto_id}")
def deletar_produto(produto_id: int):
    conexao, cursor = conectar()
    if conexao:
        try:
            cursor.execute("DELETE FROM produtos WHERE id=%s", (produto_id,))
            conexao.commit()
            if cursor.rowcount == 0:
                return {"erro": "Produto não encontrado"}
            return {"message": "Produto deletado com sucesso!"}
        except Exception as erro:
            return {"erro": f"Erro ao deletar produto: {erro}"}
        finally:
            cursor.close()
            conexao.close()
    return {"erro": "Não foi possível conectar ao banco"}

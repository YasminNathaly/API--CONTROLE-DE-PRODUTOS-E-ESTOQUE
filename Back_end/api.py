from fastapi import FastAPI, HTTPException
from typing import Optional

app = FastAPI(title="API Controle de Produtos e Estoque")

# Lista interna de produtos
produtos_db = []
id_counter = 1  # Para gerar IDs únicos


# -------------------- Adicionar Produto --------------------
@app.post("/produtos")
def criar_produto(nome: str, categoria: str = "", preco: float = 0, quantidade: int = 0):
    global id_counter
    try:
        if not nome:
            raise HTTPException(status_code=400, detail="O nome do produto é obrigatório")
        produto = {
            "id": id_counter,
            "nome": nome,
            "categoria": categoria,
            "preco": preco,
            "quantidade": quantidade
        }
        produtos_db.append(produto)
        id_counter += 1
        return {"mensagem": "Produto adicionado com sucesso", "produto": produto}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------- Listar Produtos --------------------
@app.get("/produtos")
def listar_produtos():
    return {"produtos": produtos_db}


# -------------------- Atualizar Produto --------------------
@app.put("/produtos/{id}")
def atualizar_produto(
    id: int,
    nome: Optional[str] = None,
    categoria: Optional[str] = None,
    preco: Optional[float] = None,
    quantidade: Optional[int] = None
):
    produto = next((p for p in produtos_db if p["id"] == id), None)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    if nome is not None:
        produto["nome"] = nome
    if categoria is not None:
        produto["categoria"] = categoria
    if preco is not None:
        produto["preco"] = preco
    if quantidade is not None:
        produto["quantidade"] = quantidade

    return {"mensagem": "Produto atualizado com sucesso", "produto": produto}


# -------------------- Excluir Produto --------------------
@app.delete("/produtos/{id}")
def excluir_produto(id: int):
    global produtos_db
    produto = next((p for p in produtos_db if p["id"] == id), None)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    produtos_db = [p for p in produtos_db if p["id"] != id]
    return {"mensagem": "Produto excluído com sucesso"}


# -------------------- Valor Total do Estoque --------------------
@app.get("/produtos/valor_total")
def valor_total_estoque():
    total = sum(p["preco"] * p["quantidade"] for p in produtos_db)
    return {"valor_total": total}

from fastapi import FastAPI
import funcao

app = FastAPI(title="API Controle de Produtos e Estoque")


# ROTAS DE PRODUTOS

# Adicionar um novo produto
@app.post("/produtos")
def criar_produto(nome: str, categoria: str = "", preco: float = 0, quantidade: int = 0):
    resultado = funcoes.adicionar_produto(nome, categoria, preco, quantidade)
    return resultado

# Listar todos os produtos
@app.get("/produtos")
def listar_produtos():
    produtos = funcoes.listar_produtos()
    return {"produtos": produtos}

# Atualizar produto
@app.put("/produtos/{id}")
def atualizar_produto(
    id: int,
    nome: str = None,
    categoria: str = None,
    preco: float = None,
    quantidade: int = None
):
    resultado = funcoes.atualizar_produto(id, nome, categoria, preco, quantidade)
    return resultado

# Excluir produto
@app.delete("/produtos/{id}")
def excluir_produto(id: int):
    resultado = funcoes.excluir_produto(id)
    return resultado

# Valor total do estoque
@app.get("/produtos/valor_total")
def valor_total_estoque():
    total = funcoes.valor_total_estoque()
    return total

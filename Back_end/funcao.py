from conexao import conectar

def adicionar_produto(nome, categoria, preco, quantidade):
    conn = conectar()
    if not conn:
        return {"erro": "Não foi possível conectar ao banco de dados"}

    cursor = conn.cursor()
    sql = "INSERT INTO produtos (nome, categoria, preco, quantidade) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (nome, categoria, preco, quantidade))
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensagem": "Produto adicionado com sucesso"}


def listar_produtos():
    conn = conectar()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM produtos")
        resultado = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultado

def atualizar_produto(id, nome=None, categoria=None, preco=None, quantidade=None):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        campos = []
        valores = []
        if nome: 
            campos.append("nome=%s")
            valores.append(nome)
        if categoria:
            campos.append("categoria=%s")
            valores.append(categoria)
        if preco is not None:
            campos.append("preco=%s")
            valores.append(preco)
        if quantidade is not None:
            campos.append("quantidade=%s")
            valores.append(quantidade)
        valores.append(id)
        sql = f"UPDATE produtos SET {', '.join(campos)} WHERE id=%s"
        cursor.execute(sql, tuple(valores))
        conn.commit()
        cursor.close()
        conn.close()
        return {"mensagem": "Produto atualizado com sucesso"}

def excluir_produto(id):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produtos WHERE id=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"mensagem": "Produto excluído com sucesso"}

def valor_total_estoque():
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(preco * quantidade) FROM produtos")
        total = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return {"valor_total": total if total else 0}

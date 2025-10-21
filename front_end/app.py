import streamlit as st
import requests

# Rodar o Streamlit:
# python -m streamlit run app.py

API_URL = "http://127.0.0.1:8000"  # Endereço da API
st.set_page_config(page_title="Controle de Produtos", page_icon="📦")
st.title("📦 Sistema de Controle de Produtos e Estoque")

# Menu lateral
menu = st.sidebar.radio("Navegação", ["Catálogo", "Adicionar produto", "Atualizar produto", "Excluir produto"])


# -------------------- Catálogo --------------------
if menu == "Catálogo":
    st.subheader("Todos os produtos 🛒")
    response = requests.get(f"{API_URL}/produtos")  # endpoint da API de produtos
    if response.status_code == 200:
        produtos = response.json().get("produtos", [])
        if produtos:
            for produto in produtos:
                st.write(f"**ID {produto['id']}** - {produto['nome']} | Categoria: {produto['categoria']} | "
                         f"Qtd: {produto['quantidade']} | Preço: R${produto['preco']:.2f}")
        else:
            st.info("Nenhum produto cadastrado")
    else:
        st.error("Erro ao conectar com a API")

# -------------------- Adicionar produto --------------------
elif menu == "Adicionar produto":
    st.subheader("➕ Adicionar Produto")
    nome = st.text_input("Nome do Produto")
    categoria = st.text_input("Categoria")
    quantidade = st.number_input("Quantidade em estoque", min_value=0, step=1)
    preco = st.number_input("Preço do produto", min_value=0.0, step=0.01, format="%.2f")

    if st.button("Salvar produto"):
        dados = {"nome": nome, "categoria": categoria, "quantidade": quantidade, "preco": preco}
        response = requests.post(f"{API_URL}/produtos", json=dados)
        if response.status_code == 200:
            st.success("Produto adicionado com sucesso")
        else:
            st.error("Erro ao adicionar produto")

# -------------------- Atualizar produto --------------------
elif menu == "Atualizar produto":
    st.subheader("🔄 Atualizar Produto")
    id_produto = st.number_input("ID do Produto a atualizar", min_value=1, step=1)
    nova_quantidade = st.number_input("Nova quantidade", min_value=0, step=1)
    novo_preco = st.number_input("Novo preço", min_value=0.0, step=0.01, format="%.2f")

    if st.button("Atualizar"):
        dados = {"quantidade": nova_quantidade, "preco": novo_preco}
        response = requests.put(f"{API_URL}/produtos/{id_produto}", json=dados)
        if response.status_code == 200:
            data = response.json()
            if "erro" in data:
                st.warning(data["erro"])
            else:
                st.success("Produto atualizado com sucesso!")
        else:
            st.error("Erro ao atualizar produto")

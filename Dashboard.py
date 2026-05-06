import streamlit as st
import requests 
import pandas as pd
import plotly.express as px

# Função para formatar números grandes (milhares e milhões) com prefixo opcional
def formata_numero(valor, prefixo=''):
    for unidade in ['','mil']:
        if valor < 1000:
            return f'{prefixo} {valor:.2f} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor:.2f} milhões'


# Título principal do dashboard
st.title('DASHBOARD DE VENDAS :shopping_cart:')

# Fetch dos dados de produtos via API e transformação para DataFrame
url = 'https://labdados.com/produtos'
response = requests.get(url)
dados = pd.DataFrame.from_dict(response.json())

# Cria duas colunas para exibir métricas principais (KPIs)
col1, col2 = st.columns(2)

with col1:
    st.metric('Receita', formata_numero(dados['Preço'].sum(), 'R$'))
with col2:
    st.metric('Quantidade de vendas', formata_numero(dados.shape[0]))

# Exibe a tabela de dados para exploração detalhada
st.dataframe(dados)
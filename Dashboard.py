import streamlit as st
import requests 
import pandas as pd
import plotly.express as px

# Configura o layout da página como "wide" (mais espaço horizontal)
st.set_page_config(layout = 'wide')


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

# Converte a coluna de data para formato datetime (necessário para análise temporal)
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format = '%d/%m/%Y')


## =========================
## Tratamento e agregações
## =========================

# Calcula a receita total por estado
receita_estados = dados.groupby('Local da compra')[['Preço']].sum()

# Junta dados de localização (lat/lon) com a receita e ordena do maior para o menor
receita_estados = dados.drop_duplicates(subset= 'Local da compra')[['Local da compra', 'lat', 'lon']].merge(receita_estados, left_on = 'Local da compra', right_index = True).sort_values('Preço', ascending = False)


# Agrupa a receita por mês (frequência mensal)
receita_mensal = dados.set_index('Data da Compra').groupby(pd.Grouper(freq = 'ME'))[['Preço']].sum().reset_index()

# Cria colunas auxiliares para análise temporal
receita_mensal['Ano'] = receita_mensal['Data da Compra'].dt.year
receita_mensal['Mes'] = receita_mensal['Data da Compra'].dt.month_name()

# Receita por categoria
receita_categorias = dados.groupby('Categoria do Produto')[['Preço']].sum().sort_values('Preço', ascending = False)

# Quantidade de vendas por estado
vendas_estados = pd.DataFrame(dados.groupby('Local da compra')['Preço'].count()).rename(columns={'Preço': 'Quantidade'})

# Adiciona latitude e longitude aos estados
vendas_estados = dados.drop_duplicates(subset = 'Local da compra')[['Local da compra', 'lat', 'lon']].merge(vendas_estados, left_on = 'Local da compra', right_index = True).sort_values('Quantidade', ascending = False)

# Quantidade de vendas por mês
vendas_mensal = pd.DataFrame(dados.set_index('Data da Compra').groupby(pd.Grouper(freq = 'ME'))['Preço'].count()).reset_index().rename(columns={'Preço': 'Quantidade'})

# Colunas auxiliares para análise temporal
vendas_mensal['Ano'] = vendas_mensal['Data da Compra'].dt.year
vendas_mensal['Mes'] = vendas_mensal['Data da Compra'].dt.month_name()

# Quantidade de vendas por categoria
vendas_categorias = pd.DataFrame(dados.groupby('Categoria do Produto')['Preço'].count().sort_values(ascending = False)).rename(columns={'Preço': 'Quantidade'})

# Métricas por vendedor
vendedores = pd.DataFrame(dados.groupby('Vendedor')['Preço'].agg(['sum', 'count']))

## =========================
## Criação dos gráficos
## =========================

fig_mapa_receita = px.scatter_geo(receita_estados,
                                  lat = 'lat',
                                  lon = 'lon',
                                  scope = 'south america',
                                  size = 'Preço',
                                  template = 'seaborn',
                                  hover_name = 'Local da compra',
                                  hover_data = {'lat': False, 'lon': False},
                                  title = 'Receita por estado')

fig_receita_mensal = px.line(receita_mensal,
                             x = 'Mes',
                             y = 'Preço',
                             markers = True,
                             range_y = (0, receita_mensal['Preço'].max()),
                             color = 'Ano',
                             line_dash = 'Ano',
                             title = 'Receita mensal')

fig_receita_mensal.update_layout(yaxis_title = 'Receita')

fig_receita_estados = px.bar(receita_estados.head(),
                             x = 'Local da compra',
                             y = 'Preço',
                             text_auto = True,
                             title = 'Top estados (receita)')

fig_receita_estados.update_layout(yaxis_title = 'Receita')

fig_receita_categorias = px.bar(receita_categorias,
                                text_auto = True,
                                title = 'Top estados (receita)')

fig_receita_categorias.update_layout(yaxis_title = 'Receita')

fig_mapa_vendas = px.scatter_geo(vendas_estados,
                                  lat = 'lat',
                                  lon = 'lon',
                                  scope = 'south america',
                                  #fitbounds = 'locations',
                                  template = 'seaborn',
                                  size = 'Quantidade', 
                                  hover_name = 'Local da compra',
                                  hover_data = {'lat': False, 'lon': False},
                                  title = 'Vendas por estado')

fig_vendas_mensal = px.line(vendas_mensal,
                             x = 'Data da Compra',
                             y = 'Quantidade',
                             markers = True,
                             range_y = (0, vendas_mensal['Quantidade'].max()),
                             color = 'Ano',
                             line_dash = 'Ano',
                             title = 'Quantidade de vendas mensal')

fig_vendas_mensal.update_layout(yaxis_title = 'Quantidade de vendas')

fig_vendas_estados = px.bar(vendas_estados.head(),
                             x = 'Local da compra',
                             y = 'Quantidade',
                             text_auto = True,
                             title = 'Top 5 estados')

fig_vendas_estados.update_layout(yaxis_title = 'Quantidade de vendas')

fig_vendas_categorias = px.bar(vendas_categorias,
                                y = 'Quantidade',
                                text_auto = True,
                                title = 'Vendas por categoria')

fig_vendas_categorias.update_layout(showlegend = False, yaxis_title = 'Quantidade de vendas')


## =========================
## Layout e visualização
## =========================

aba1, aba2, aba3 = st.tabs(['Receita', 'Quantidade de vendas', 'Vendedores'])

with aba1:

    col1, col2 = st.columns(2)

    with col1:
        st.metric('Receita', formata_numero(dados['Preço'].sum(), 'R$'))
        st.plotly_chart(fig_mapa_receita, use_container_width = True)
        st.plotly_chart(fig_receita_estados, use_container_width = True)

    with col2:
        st.metric('Quantidade de vendas', formata_numero(dados.shape[0]))
        st.plotly_chart(fig_receita_mensal, use_container_width = True)
        st.plotly_chart(fig_receita_categorias, use_container_width = True)

with aba2:

    col1, col2 = st.columns(2)

    with col1:
        st.metric('Receita', formata_numero(dados['Preço'].sum(), 'R$'))
        st.plotly_chart(fig_mapa_vendas, use_container_width = True)
        st.plotly_chart(fig_vendas_estados, use_container_width= True)

    with col2:
        st.metric('Quantidade de vendas', formata_numero(dados.shape[0]))
        st.plotly_chart(fig_vendas_mensal, use_container_width = True)
        st.plotly_chart(fig_vendas_categorias, use_container_width= True)

with aba3:

    qtd_vendedores = st.number_input('Quantidade de vendedores', 2, 10, 5)

    col1, col2 = st.columns(2)

    with col1:

        st.metric('Receita', formata_numero(dados['Preço'].sum(), 'R$'))

        fig_receita_vendedores = px.bar(vendedores[['sum']].sort_values('sum', ascending = False).head(qtd_vendedores),
                                        x='sum',
                                        y=vendedores[['sum']].sort_values('sum', ascending=False).head(qtd_vendedores).index,
                                        text_auto=True,
                                        title=f'Top {qtd_vendedores} vendedores (receita)')
        
        st.plotly_chart(fig_receita_vendedores, use_container_width=True)

    with col2:

        st.metric('Quantidade de vendas', formata_numero(dados.shape[0]))
        
        fig_vendas_vendedores = px.bar(vendedores[['count']].sort_values('count', ascending = False).head(qtd_vendedores),
                                        x='count',
                                        y=vendedores[['count']].sort_values('count', ascending=False).head(qtd_vendedores).index,
                                        text_auto=True,
                                        title=f'Top {qtd_vendedores} vendedores (quantidade de vendas)')
        
        st.plotly_chart(fig_vendas_vendedores, use_container_width=True)

# Exibe a tabela de dados para exploração detalhada
#st.dataframe(dados)
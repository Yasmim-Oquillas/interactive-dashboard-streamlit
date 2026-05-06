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

## =========================
## Criação dos gráficos
## =========================

# Mapa geográfico com receita por estado
fig_mapa_receita = px.scatter_geo(receita_estados,
                                  lat = 'lat',
                                  lon = 'lon',
                                  scope = 'south america',
                                  size = 'Preço',
                                  template = 'seaborn',
                                  hover_name = 'Local da compra',
                                  hover_data = {'lat': False, 'lon': False},
                                  title = 'Receita por estado')

# Gráfico de linha com evolução da receita mensal
fig_receita_mensal = px.line(receita_mensal,
                             x = 'Mes',
                             y = 'Preço',
                             markers = True,
                             range_y = (0, receita_mensal['Preço'].max()),
                             color = 'Ano',
                             line_dash = 'Ano',
                             title = 'Receita mensal')

fig_receita_mensal.update_layout(yaxis_title = 'Receita')

## =========================
## Layout e visualização
## =========================

# Cria duas colunas para exibir métricas e gráficos lado a lado
col1, col2 = st.columns(2)

with col1:
    # KPI: Receita total
    st.metric('Receita', formata_numero(dados['Preço'].sum(), 'R$'))

    # Exibe o mapa
    st.plotly_chart(fig_mapa_receita, use_container_width = True)

with col2:
    # KPI: Quantidade de vendas
    st.metric('Quantidade de vendas', formata_numero(dados.shape[0]))
    
    # Exibe o gráfico de linha
    st.plotly_chart(fig_receita_mensal, use_container_width = True)

# Exibe a tabela de dados para exploração detalhada
st.dataframe(dados)
import streamlit as st
import requests 
import pandas as pd
import plotly.express as px

st.title('DASHBOARD DE VENDAS :shopping_cart:')

# Fetch dos dados de produtos via API e transformação para DataFrame
url = 'https://labdados.com/produtos'
response = requests.get(url)
dados = pd.DataFrame.from_dict(response.json())

# Renderiza o DataFrame no dashboard com visualização interativa
st.dataframe(dados)
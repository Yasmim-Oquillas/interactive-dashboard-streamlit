# 📊 Dashboard Interativo de Vendas com Streamlit

Projeto desenvolvido com Python e Streamlit durante os estudos do curso de Streamlit da Alura, com foco na construção de dashboards interativos para análise de dados.

A aplicação consome dados de uma API e permite visualizar métricas, gráficos, filtros dinâmicos e exportação de dados em CSV.

---

# 🚀 Tecnologias utilizadas

- Python
- Streamlit
- Pandas
- Plotly Express
- Requests

---

# 📁 Estrutura do projeto

```bash
DASHBOARD_STREAMLIT/
│
├── Dashboard.py
├── README.md
├── requirements.txt
├── pages/
│   └── Dados_brutos.py
├── .streamlit/
│   └── config.toml
└── venv/
```

---

# 📌 Funcionalidades

- Dashboard interativo de vendas
- Filtros dinâmicos na sidebar
- Visualização de métricas e gráficos
- Página de dados brutos
- Exportação de dados em CSV
- Ranking de vendedores

---

# ▶️ Como executar o projeto

## Clone o repositório

```bash
git clone https://github.com/Yasmim-Oquillas/interactive-dashboard-streamlit.git
```

## Acesse a pasta do projeto

```bash
cd DASHBOARD_STREAMLIT
```

## Crie o ambiente virtual

```bash
python -m venv venv
```

## Ative o ambiente virtual

### Windows (PowerShell)

```bash
.\venv\Scripts\activate
```

## Instale as dependências

```bash
pip install -r requirements.txt
```

## Execute o Streamlit

```bash
streamlit run Dashboard.py
```

---

# 🎨 Personalização

O projeto utiliza um arquivo de configuração do Streamlit para personalização da interface:

```bash
.streamlit/config.toml
```

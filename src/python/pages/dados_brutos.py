import plotly.express as px
import streamlit as st
import requests as req
import pandas as pd

# Leiaute de webapp
st.set_page_config(
    layout='wide',
    page_title='Painel de Vendas - Estudo de API'
)

st.set_page_config(page_title="Dados brutos 📦", page_icon="🔠")

# Título da página
st.title("Dados brutos 📦")
st.markdown("[Link da API](https://labdados.com/produtos)")

# Botão atualizar
if st.button("🔄 Atualizar agora"):
    st.cache_data.clear()
    st.rerun()

# Endereço da API
link_api = 'https://labdados.com/produtos'

try:
    # Realizando requisição
    res = req.get(link_api, verify=False)
    dados = res.json()
    #st.success(f'Status da requisição: {res.status_code}')
except:
    st.error(f'Status da requisição: {res.status_code}')

# Carga de dados
df = pd.DataFrame(dados)
df['Data da Compra'] = pd.to_datetime(df['Data da Compra'], format='%d/%m/%Y')

# Big Numbers
metrica_qtde = len(df)
metrica_qtde_f = f'{format(metrica_qtde, ',.0f')\
                        .replace(',', '.')}'

metrica_valor = df['Preço'].sum()
metrica_valor_f = f'R$ {format(metrica_valor, ',.2f')\
                        .replace(',', '-')\
                            .replace('.', ',')\
                                .replace('-', '.')}'

col_metrica_0, col_metrica_1, col_metrica_2 = st.columns([1,1,2])
with col_metrica_0:
    st.metric(label="Quantidade de vendas", value=metrica_qtde_f)
with col_metrica_1:
    st.metric(label="Receita", value=metrica_valor_f)
with col_metrica_2:
    st.text(' ')

@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# Tabela geral de dados
exp_dados_geral = st.expander("📊 Dados gerais", expanded=True)
with exp_dados_geral:
    aba_geral_1, aba_geral_2 = st.tabs(["Dados Gerais", "Exportação em formato CSV"])
    with aba_geral_1:
        # Dados totais
        st.dataframe(df)
    with aba_geral_2:
        # Exportação de dados
        csv = convert_df_to_csv(df)
        st.download_button(
            label="Baixar CSV",
            data=csv,
            file_name=f'Dados_Vendas.csv',
            mime='text/csv',
            help='Clique para baixar os dados em formato CSV',
        )

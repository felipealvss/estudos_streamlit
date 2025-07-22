import plotly.express as px
import streamlit as st
import requests as req
import pandas as pd

st.set_page_config(layout='wide')

# Título da página
st.markdown("# Painel de vendas 🛒")

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

# Dados de receita por estado
col_tab1, col_tab2, col_tab3 = st.columns([1,1,1])
#col_tab1, col_tab2, col_tab3 = st.tabs(["🗺️ Informação por Coordenadas", "🚩 Receita por Cidade", "🗓️ Receita po Ano-Mês"])

with col_tab1:
    #st.subheader(f'🗺️ Informação por Coordenadas')
    receita_estados_local = df.groupby(['Local da compra', 'lat', 'lon'])['Preço'].sum().reset_index()
    #st.dataframe(receita_estados_local)
    px_map_receita = px.scatter_geo(
        receita_estados_local,
        title='Receita por Estado',
        lat='lat',
        lon='lon',
        scope='south america',
        size='Preço',
        template='seaborn',
        hover_name='Local da compra',
        hover_data={'lat': False, 'lon': False},
    )
    st.plotly_chart(px_map_receita, use_container_width=True)
with col_tab2:
    #st.subheader(f'🚩 Receita por Cidade')
    # Grafico de barras
    receita_estados = df.groupby('Local da compra')['Preço'].sum().sort_values(ascending=True).reset_index()
    #st.dataframe(receita_estados)
    #st.bar_chart(receita_estados)
    px_bar_receita = px.bar(
        receita_estados.head(),
        title="Receita por Cidade",
        x='Preço',
        y='Local da compra',
        hover_name='Local da compra',
        hover_data={'Local da compra': False},
        range_y=(0, receita_estados.max()),
    )
    st.plotly_chart(px_bar_receita, use_container_width=False)
with col_tab3:
    categorias_estados = df.groupby('Categoria do Produto')['Preço'].sum().sort_values(ascending=True).reset_index()
    # Criando o gráfico de pizza
    px_pie_categorias = px.pie(
        categorias_estados,
        title="Receita por Categoria",
        values='Preço',
        names='Categoria do Produto',
        hover_name='Categoria do Produto',
        hover_data={'Categoria do Produto': False}
    )
    st.plotly_chart(px_pie_categorias, use_container_width=False)

# informação de Receita por Ano-Mês
#st.subheader("🗓️ Receita po Ano-Mês")
receita_mensal = df.set_index('Data da Compra').groupby(pd.Grouper(freq='M'))['Preço'].sum().reset_index()
receita_mensal['Ano'] = receita_mensal['Data da Compra'].dt.year
receita_mensal['Mês'] = receita_mensal['Data da Compra'].dt.month_name()
#st.dataframe(receita_mensal)
# Grafico de Linhas
px_line_receita = px.line(
    receita_mensal,
    title="Receita por Mês",
    x='Mês',
    y='Preço',
    orientation='h',
    markers=True,
    range_y=(0, receita_mensal.max()),
    color='Ano',
    line_dash='Ano',
)
# Mudar nome de Preço para Receita
px_line_receita.update_layout(yaxis_title = 'Receita')

st.plotly_chart(px_line_receita, use_container_width=True)

@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# Tabela geral de dados
exp_dados_geral = st.expander("📊 Dados gerais")
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
            file_name='dados_vendas.csv',
            mime='text/csv',
            help='Clique para baixar os dados em formato CSV',
        )

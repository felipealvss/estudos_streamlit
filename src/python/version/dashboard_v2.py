import plotly.express as px
import streamlit as st
import requests as req
import pandas as pd

# Leiaute de webapp
st.set_page_config(
    layout='wide',
    page_title='Painel de Vendas - Estudo de API'
)

# Título da página
st.markdown("# Painel de vendas 🛒")
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

# Estruturas de dados - Parâmetro principal: Preço
receita_estados_local = df.groupby(['Local da compra', 'lat', 'lon'])['Preço'].sum().reset_index()
receita_categorias = df.groupby('Categoria do Produto')['Preço'].sum().sort_values(ascending=False).reset_index()
receita_estados = df.groupby('Local da compra')['Preço'].sum().sort_values(ascending=False).reset_index()
# Estruturas de dados - Parâmetro principal: Quantidade
qtde_estados_local = df.groupby(['Local da compra', 'lat', 'lon']).size().reset_index(name='Contagem')
qtde_categorias = df.groupby('Categoria do Produto').size().sort_values(ascending=False).reset_index(name='Contagem')
qtde_estados = df.groupby('Local da compra').size().sort_values(ascending=False).reset_index(name='Contagem')
# Estruturas de dados - Parâmetro principal: Vendedores
agrupa_vendedores = df.groupby(['Vendedor'])['Preço'].agg(['sum', 'count'])
agrupa_vendedores = agrupa_vendedores.rename(columns={'sum': 'Soma de Vendas', 'count': 'Contagem de Vendas'})

# Abas de gráficos
col_tab1, col_tab2, col_tab3 = st.tabs(["🧮 Abertura por Quantidade", "💰 Abertura por Receita", "👨‍💻👨🏽‍💻 Abertura por Vendedores"])

# Abertura por quantidade
with col_tab1:
    # Colunas de gráficos
    qtde_col1, qtde_col2, qtde_col3 = st.columns([1,1,1])

    with qtde_col1:
        # Gráfico de mapa
        px_qtde_map_receita = px.scatter_geo(
            qtde_estados_local,
            title='Quantidade por Estado',
            lat='lat',
            lon='lon',
            scope='south america',
            size='Contagem',
            template='seaborn',
            hover_name='Local da compra',
            hover_data={'lat': False, 'lon': False},
        )
        st.plotly_chart(px_qtde_map_receita, use_container_width=True, key='px_qtde_map_receita')
    with qtde_col2:    
        # Gráfico de pizza
        px_qtde_pie_categorias = px.pie(
            qtde_categorias,
            title="Quantidade por Categoria",
            values='Contagem',
            names='Categoria do Produto',
            hover_name='Categoria do Produto',
            hover_data={'Categoria do Produto': False}
        )
        st.plotly_chart(px_qtde_pie_categorias, use_container_width=False, key='px_qtde_pie_categorias')
    with qtde_col3:
        # Grafico de barras
        px_qtde_bar_receita = px.bar(
            qtde_estados.head(),
            title="Quantidade por Cidade",
            x='Local da compra',
            y='Contagem',
            hover_name='Local da compra',
            hover_data={'Local da compra': False},
            range_y=(0, receita_estados.max()),
        )
        st.plotly_chart(px_qtde_bar_receita, use_container_width=False, key='px_qtde_bar_receita')
# Abertura por Receita
with col_tab2:
    # Colunas de gráficos
    receita_col1, receita_col2, receita_col3 = st.columns([1,1,1])

    with receita_col1:
        # Gráfico de mapa
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
        st.plotly_chart(px_map_receita, use_container_width=True, key='px_map_receita')
    with receita_col2:    
        # Gráfico de pizza
        px_pie_categorias = px.pie(
            receita_categorias,
            title="Receita por Categoria",
            values='Preço',
            names='Categoria do Produto',
            hover_name='Categoria do Produto',
            hover_data={'Categoria do Produto': False}
        )
        st.plotly_chart(px_pie_categorias, use_container_width=False, key='px_pie_categorias')
    with receita_col3:
        # Grafico de barras
        px_bar_receita = px.bar(
            receita_estados.head(),
            title="Receita por Cidade",
            x='Local da compra',
            y='Preço',
            hover_name='Local da compra',
            hover_data={'Local da compra': False},
            range_y=(0, receita_estados.max()),
        )
        st.plotly_chart(px_bar_receita, use_container_width=False, key='px_bar_receita')
# Abertura por vendedores
with col_tab3:
    # Selecionador de vendedores
    qtde_vendedores = st.number_input("Quantidade de Vendedores", 2, 10, 5)
    # Definir colunas para abertura de Contagem e Soma
    dados_vendedor_col1, dados_vendedor_col2 = st.columns([1,1])
    # Gráfico de barras - Contagem 
    with dados_vendedor_col1:
        px_dados_vendedores1 = px.bar(
            agrupa_vendedores[['Contagem de Vendas']].sort_values('Contagem de Vendas', ascending=True).head(qtde_vendedores),
            title=f'🏆 Top {qtde_vendedores} Vendedores - Quantidade',
            x='Contagem de Vendas',
            y=agrupa_vendedores[['Contagem de Vendas']].sort_values('Contagem de Vendas', ascending=True).head(qtde_vendedores).index,
            text_auto=True,
        )
        px_dados_vendedores1.update_layout(yaxis_title = 'Vendedor')
        st.plotly_chart(px_dados_vendedores1, use_container_width=True, key='px_dados_vendedores1')
    # Grafico de barras - Soma
    with dados_vendedor_col2:
        px_dados_vendedores2 = px.bar(
            agrupa_vendedores[['Soma de Vendas']].sort_values('Soma de Vendas', ascending=True).head(qtde_vendedores),
            title=f'🏆 Top {qtde_vendedores} Vendedores - Valor',
            x='Soma de Vendas',
            y=agrupa_vendedores[['Soma de Vendas']].sort_values('Soma de Vendas', ascending=True).head(qtde_vendedores).index,
            text_auto=True,
        )
        px_dados_vendedores2.update_layout(yaxis_title = 'Vendedor')
        st.plotly_chart(px_dados_vendedores2, use_container_width=True, key='px_dados_vendedores2')

# informação de Receita por Ano-Mês
#st.subheader("🗓️ Receita po Ano-Mês")
receita_mensal = df.set_index('Data da Compra').groupby(pd.Grouper(freq='ME'))['Preço'].sum().reset_index()
receita_mensal['Ano'] = receita_mensal['Data da Compra'].dt.year
receita_mensal['Mês'] = receita_mensal['Data da Compra'].dt.month_name()
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
# Plot de gráfico
st.plotly_chart(px_line_receita, use_container_width=True, key='px_line_receita')

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

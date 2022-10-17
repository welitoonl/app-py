import pandas as pd
import streamlit as st
import altair as alt

st.title('App - Tópicos Avançados')

@st.cache
def load_database():
    return pd.read_feather('tavbase/gs.feather'), \
        pd.read_feather('tavbase/classificacaoz_consumidor.feather'), \
        pd.read_feather('tavbase/clusterizacao_pais.feather'), \
        pd.read_feather('tavbase/regressao_mercado.feather'), \
        pd.read_feather('tavbase/regressao_regiao.feather')

gs, cla_con, clu_pai, reg_mer, reg_reg = load_database()

taberp, tabbi, tabstore = st.tabs(['Sistema Interno', 'Gestão', 'E-Commerce'])

with taberp:
    st.header('Dados do Sistema Interno')
    consumidor = st.selectbox(
        'Selecione o consumidor', 
        gs['Customer ID'].unique()
    )
    gs_con = gs[gs['Customer ID'] == consumidor]
    # st.dataframe(gs_con)
    cla_con_con = cla_con[cla_con['Customer ID'] == consumidor].reset_index() 
    # st.dataframe(cla_con_con)
    st.dataframe(gs_con[['Customer Name', 'Segment']].drop_duplicates())
    cl1, cl2, cl3, cl4 = st.columns(4)
    cl1.metric('Score', round(cla_con_con['score'][0],4), "1")
    cl2.metric('Classe', round(cla_con_con['classe'][0],4), "1")
    cl3.metric('Rank', round(cla_con_con['rank'][0],4), "1")
    cl4.metric('Lucro', round(cla_con_con['lucro'][0],4), "1")
    cl1.metric('Valor Total Comprado', round(gs_con['Sales'].sum(),2), "1")
    cl2.metric('Valor Lucro', round(gs_con['Profit'].sum(),2), "1")
    cl3.metric('Valor Médio Comprado', round(gs_con['Sales'].mean(),2), "1")
    cl4.metric('Quantidade Comprada', round(gs_con['Quantity'].sum(),2), "1")
    with st.expander('Pedidos:'):
        st.dataframe(gs_con[
                ['Order Date','Product Name','Quantity','Sales','Profit']
            ]
        )
    clu_pai_cli = clu_pai[clu_pai['referencia'] == gs_con['Country'].values[0]]
    st.dataframe(clu_pai_cli[
        ['referencia', 'm_entrega', 'm_lucro', 'm_vendas', 'm_qtde',
         'f_vendas', 'f_lucro', 'r_dias']
    ])
    st.dataframe(clu_pai_cli[
        ['cluster', 'clm_entrega', 'clm_lucro', 'clm_vendas', 'clm_qtde',
         'clf_vendas', 'cls_lucro', 'clr_dias']
    ])
with tabbi:
    st.header('Dados do Business Intelligence')
    with st.expander('Mercado'):
        aggm = st.selectbox('Agregador Mercado, ', ['sum', 'mean'])
        st.dataframe(reg_mer.pivot_table(index='Market', columns='ano', 
            values='yhat', aggfunct=aggm, fill_value=0))
    if st.checkbox('Detalhar mercado'):
        mercado = st.selectbox('Mercado', rg_mer['Market'].unique())
        gr_mer = rg_mer[rg_mer['Market'].groupby('ano').mean().reset_index()]
        proj = alt.Chart(gr_mer).mark_line(color='blue').encode(x='ano', y='yhat').reset_index()
        gr_gs = gs[gs['Market'] == mercado].groupby('Year')['Sales'].sum().reset_index
        real = alt.Chart(gr_gs).mark_line(color='red').encode(x= 'Year', y='Sales')
        st.altair_chart(proj + real)
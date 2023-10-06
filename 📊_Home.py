#BIBLIOTECAS
import pandas as pd
import numpy as np
import inflection
import plotly.express as px
import streamlit as st
import folium
from folium.plugins import MarkerCluster
from PIL import Image
from streamlit_folium import folium_static


st.set_page_config(page_title='Home', page_icon='📊', layout='wide')

#---------------------------------------------------------------------------------------------------------
# DEF FUNÇÕES
#---------------------------------------------------------------------------------------------------------
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}
def country_name(country_id):
    return COUNTRIES[country_id]

def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"
    
COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}
def color_name(color_code):
    return COLORS[color_code]

BOOKING = {
0: "yes",
1: "no",
}
def booking(booking_code):
    return BOOKING[booking_code]

ONLINE = {
1: "yes",
0: "no",
}
def online(online_code):
    return ONLINE[online_code]

NOW = {
1: "yes",
0: "no",
}
def now(now_code):
    return NOW[now_code]

def clean_code(df1):
    
    # acerto dos tipos de cuisines
    df1["cuisines"] = df1.loc[:, "cuisines"].astype(str).apply(lambda x: x.split(",")[0])
    
    # acerto dos códigos/nome de country, color, price, booking, online deliver, deliver now
    df1["country_code"] = df1.loc[:, "country_code"].apply(lambda x: country_name(x))
    df1['rating_color'] = df1.loc[:, 'rating_color'].apply(lambda x: color_name(x))
    df1['price_range'] = df1.loc[:, 'price_range'].apply(lambda x: create_price_type(x))
    df1["has_table_booking"] = df1.loc[:, "has_table_booking"].apply(lambda x: booking(x))
    df1["has_online_delivery"] = df1.loc[:, "has_online_delivery"].apply(lambda x: online(x))	
    df1["is_delivering_now"] = df1.loc[:, "is_delivering_now"].apply(lambda x: now(x))
    
    # exlcuir IDs duplicados
    df2 = df1.drop_duplicates(subset=['restaurant_id'], keep='first', inplace=True)
    
    # excluir coluna com apenas um dado igual para todas linhas
    df1 = df1.drop(['switch_to_order_menu'], axis=1)
    
    # excluir linhas 'nan'
    aux = df1['cuisines'] != 'nan'
    df1 = df1.loc[aux, :]
    
    #resetar index e acertar nome de colunas country
    df1 = df1.reset_index(drop=True)
    df1 = df1.rename(columns={'country_code': 'country'})
    
    return df1

def pie_stats(df1, col):
    dfaux1 = df1.loc[:,['restaurant_id', col]].groupby([col]).count().reset_index()
    fig = px.pie(df1, values='restaurant_id', names=col)
    
    return fig

@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

#---------------------------------------------------------------------------------------------------------
#                                     INÍCIO ESTRUTURA LÓGICA
# IMPORTANDO DATASET
# LIMPEZA DATASET
#---------------------------------------------------------------------------------------------------------
df_raw = pd.read_csv('dataset/zomato.csv')
df1 = rename_columns( df_raw )
df1 = clean_code( df1 )
csv = convert_df( df1 )

#---------------------------------------------------------------------------------------------------------                             
# 1.1 VISÃO GERENCIAL//MAIN PAGE
#---------------------------------------------------------------------------------------------------------
#SIDEBAR--------------------------------------------------------------------------------------------------

#image_path = "C:/Users/Thiago/Desktop/DADOS/repos/ftc_programacao_python_PROJETO/logo_pa.png"
image = Image.open('logo_pa.png')
st.sidebar.image(image, width=100)

st.sidebar.markdown('# TáNaMesa')
st.sidebar.markdown('## Filtros para pesquisa')

country_options = st.sidebar.multiselect('Defina países para visualizar restaurantes no mapa',
                                         ['Philippines', 'Brazil', 'Australia', 'United States of America',
                                          'Canada', 'Singapure', 'United Arab Emirates', 'India',
                                          'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
                                          'Sri Lanka', 'Turkey'],
                                         default=['Brazil', 'Australia', 'United States of America', 'England', 'United Arab Emirates'])

st.sidebar.markdown("""____""")
st.sidebar.markdown('### Dados tratados')
st.sidebar.download_button(label = 'Download.csv',
                          data = csv,
                          file_name = 'dadostratados.csv',
                          mime = 'text/csv')

st.sidebar.markdown("""____""")
st.sidebar.markdown('#### desenvolvido por @tfmeneghello')


#LAYOUT--------------------------------------------------------------------------------------------------
st.write("# TáNaMesa!")
st.header("O melhor lugar para encontrar seu novo restaurante favorito.")

with st.container():
    st.write("""#### Conheça os principais indicadores cadastrados em nossa plataforma:""")
    col1, col2, col3, col4, col5 = st.columns([0.15,0.1,0.1,0.2,0.4], gap='small')
    
    with col1:
        rest_uniques = df1['restaurant_id'].nunique()
        col1.metric('Restaurantes', rest_uniques)
    with col2:
        country_uniques = df1['country'].nunique()
        col2.metric('Países', country_uniques)
    with col3:
        city_uniques = df1['city'].nunique()
        col3.metric('Cidades', city_uniques)
    with col4:
        cuisines_uniques = df1['cuisines'].nunique()
        col4.metric('Tipos de Culinária', cuisines_uniques)
    with col5:
        votes_total = df1['votes'].sum()
        votes_total = f'{votes_total:,}'
        votes_total = votes_total.replace(',', '.')
        col5.metric('Avaliações registradas', votes_total)

with st.container():
    col1, col2, col3 = st.columns(3, gap='small')
    with col1:
        st.markdown('##### Restaurantes que estão fazendo entrega')
        fig = pie_stats(df1, col='is_delivering_now')
        st.plotly_chart(fig,use_container_width=True)
    
    with col2:
        st.markdown('##### Restaurantes que aceitam pedido online')
        fig = pie_stats(df1, col='has_online_delivery')
        st.plotly_chart(fig,use_container_width=True)
        
    with col3:
        st.markdown('##### Restaurantes que reservam mesa')
        fig = pie_stats(df1, col='has_table_booking')
        st.plotly_chart(fig,use_container_width=True)

        
linhas_selecionadas = df1['country'].isin(country_options)
df1 = df1.loc[linhas_selecionadas,:]
with st.container():
    st.write("""##### Mapa interativo para busca de restaurantes (utilize o filtro ao lado)""")
    mapa = folium.Map(tiles='OpenStreetMap', zoom_start=1)

    marker_cluster = MarkerCluster().add_to(mapa)

    cols = ['restaurant_name', 'cuisines', 'average_cost_for_two', 'aggregate_rating', 'rating_color','latitude', 'longitude']
    location_marker = df1.loc[:, cols].groupby(['restaurant_name', 'cuisines', 'average_cost_for_two', 'aggregate_rating', 'rating_color']).median().reset_index()

    for index, loc_info in location_marker.iterrows():
        folium.Marker([loc_info['latitude'],
                       loc_info['longitude']],
                      popup=folium.Popup('<b>{}</b><br>culinária: {};<br>valor 2 pessoas: ${};<br>nota média: {}/5.0'.format(loc_info['restaurant_name'],loc_info['cuisines'],loc_info['average_cost_for_two'],loc_info['aggregate_rating']), max_width=150),
                      icon=folium.Icon(color=loc_info['rating_color'], icon="fa-solid fa-utensils", prefix='fa')).add_to(marker_cluster)
    
    folium_static(mapa, width=1024, height=600)


print("estou aqui")
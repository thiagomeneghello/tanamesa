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

st.set_page_config(page_title='Restaurantes & Culinárias', page_icon='🍴', layout='wide')

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

def best_rest(df1, food):    
    ls = (df1['cuisines'] == food)
    cols = ['restaurant_id','aggregate_rating', 'restaurant_name']
    dfaux = df1.loc[ls, cols].sort_values(['aggregate_rating','restaurant_id'], axis=0, ascending=[False, True])
    
    return dfaux

def best_cuisines(df1, op):
    cols = ['aggregate_rating', 'cuisines']
    dfaux = df1.loc[:, cols].groupby(['cuisines']).mean()
    dfaux = dfaux.sort_values(['aggregate_rating'], ascending=op).reset_index()
    dfaux = dfaux.head(ntop)
    fig = px.bar(dfaux, x='cuisines', y='aggregate_rating', text_auto=True)
    
    return fig



#---------------------------------------------------------------------------------------------------------
#                                     INÍCIO ESTRUTURA LÓGICA
# IMPORTANDO DATASET
# LIMPEZA DATASET
#---------------------------------------------------------------------------------------------------------
df_raw = pd.read_csv('dataset/zomato.csv')
df1 = rename_columns( df_raw )
df1 = clean_code( df1 )
df2 = df1.copy()

#---------------------------------------------------------------------------------------------------------                             
# 1.3 VISÃO RESTAURANTES//REST&CUISINES
#---------------------------------------------------------------------------------------------------------
#SIDEBAR--------------------------------------------------------------------------------------------------

#image_path = "C:/Users/Thiago/Desktop/DADOS/repos/ftc_programacao_python_PROJETO/logo_pa.png"
image = Image.open('logo_pa.png')
st.sidebar.image(image, width=100)

st.sidebar.markdown('# TáNaMesa')
st.sidebar.markdown('## Filtros para pesquisa')

country_options = st.sidebar.multiselect('Defina países para visualizar informações',
                                         ['Philippines', 'Brazil', 'Australia', 'United States of America',
                                          'Canada', 'Singapure', 'United Arab Emirates', 'India',
                                          'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
                                          'Sri Lanka', 'Turkey'],
                                         default=['Brazil', 'Australia', 'United States of America', 'England', 'United Arab Emirates'])

st.sidebar.markdown("""____""")
food_options = st.sidebar.multiselect('Defina o tipo de culinária',
                                       ['Italian', 'European', 'Filipino', 'American', 'Korean', 'Pizza',
                                        'Taiwanese', 'Japanese', 'Coffee', 'Chinese', 'Seafood',
                                        'Singaporean', 'Vietnamese', 'Latin American', 'Healthy Food',
                                        'Cafe', 'Fast Food', 'Brazilian', 'Argentine', 'Arabian', 'Bakery',
                                        'Tex-Mex', 'Bar Food', 'International', 'French', 'Steak',
                                        'German', 'Sushi', 'Grill', 'Peruvian', 'North Eastern',
                                        'Ice Cream', 'Burger', 'Mexican', 'Vegetarian', 'Contemporary',
                                        'Desserts', 'Juices', 'Beverages', 'Spanish', 'Thai', 'Indian',
                                        'Mineira', 'BBQ', 'Mongolian', 'Portuguese', 'Greek', 'Asian',
                                        'Author', 'Gourmet Fast Food', 'Lebanese', 'Modern Australian',
                                        'African', 'Coffee and Tea', 'Australian', 'Middle Eastern',
                                        'Malaysian', 'Tapas', 'New American', 'Pub Food', 'Southern',
                                        'Diner', 'Donuts', 'Southwestern', 'Sandwich', 'Irish',
                                        'Mediterranean', 'Cafe Food', 'Korean BBQ', 'Fusion', 'Canadian',
                                        'Breakfast', 'Cajun', 'New Mexican', 'Belgian', 'Cuban', 'Taco',
                                        'Caribbean', 'Polish', 'Deli', 'British', 'California', 'Others',
                                        'Eastern European', 'Creole', 'Ramen', 'Ukrainian', 'Hawaiian',
                                        'Patisserie', 'Yum Cha', 'Pacific Northwest', 'Tea', 'Moroccan',
                                        'Burmese', 'Dim Sum', 'Crepes', 'Fish and Chips', 'Russian',
                                        'Continental', 'South Indian', 'North Indian', 'Salad',
                                        'Finger Food', 'Mandi', 'Turkish', 'Kerala', 'Pakistani',
                                        'Biryani', 'Street Food', 'Nepalese', 'Goan', 'Iranian', 'Mughlai',
                                        'Rajasthani', 'Mithai', 'Maharashtrian', 'Gujarati', 'Rolls',
                                        'Momos', 'Parsi', 'Modern Indian', 'Andhra', 'Tibetan', 'Kebab',
                                        'Chettinad', 'Bengali', 'Assamese', 'Naga', 'Hyderabadi', 'Awadhi',
                                        'Afghan', 'Lucknowi', 'Charcoal Chicken', 'Mangalorean',
                                        'Egyptian', 'Malwani', 'Armenian', 'Roast Chicken', 'Indonesian',
                                        'Western', 'Dimsum', 'Sunda', 'Kiwi', 'Asian Fusion', 'Pan Asian',
                                        'Balti', 'Scottish', 'Cantonese', 'Sri Lankan', 'Khaleeji',
                                        'South African', 'Drinks Only', 'Durban', 'World Cuisine',
                                        'Izgara', 'Home-made', 'Giblets', 'Fresh Fish', 'Restaurant Cafe',
                                        'Kumpir', 'Döner', 'Turkish Pizza', 'Ottoman', 'Old Turkish Bars',
                                        'Kokoreç'],
                                      default=['Italian', 'Home-made', 'Vegetarian',
                                               'Fast Food','Japanese','Seafood', 'American','BBQ'])


st.sidebar.markdown("""____""")
st.sidebar.markdown('#### Restaurantes')

price_options = st.sidebar.multiselect('Defina categorias de preço',
                                       ["cheap", 'normal', 'expensive', 'gourmet'],
                                      default=["cheap", 'normal', 'expensive', 'gourmet'])

deliver_options = st.sidebar.checkbox('Com Entrega no momento')

online_options = st.sidebar.checkbox('Aceita pedido online')
    
table_options = st.sidebar.checkbox('Com Reserva de mesa')

st.sidebar.markdown("""____""")
st.sidebar.markdown('#### desenvolvido por @tfmeneghello')


#-------------------------------------------------------------------------------------------------------
#LAYOUT--------------------------------------------------------------------------------------------------
st.write("# 🍴 Restaurantes & Culinárias")

with st.container():
    st.markdown('#### Melhores Restaurantes das Principais Culinárias')
    col1, col2, col3, col4, col5 = st.columns([0.15,0.20,0.15,0.2,0.2], gap='small')
    with col1:
        dfaux = best_rest(df1, food='Italian')
        col1.metric(label='Italiana: {}'.format(dfaux.iloc[0,2]), value= '{}/5.0'.format(dfaux.iloc[0,1]),
                    help='País: India // Cidade: Pune // Preço prato para 2: $700 (Indian Rupees(Rs.))')
    
    with col2:
        dfaux = best_rest(df1, food='American')
        col2.metric(label='Americana: {}'.format(dfaux.iloc[0,2]), value= '{}/5.0'.format(dfaux.iloc[0,1]),
                   help='País: England // Cidade: London // Preço prato para 2: $45 (Pounds(Lb.))')
   
    with col3:
        dfaux = best_rest(df1, food='Arabian')
        col3.metric(label='Árabe: {}'.format(dfaux.iloc[0,2]), value= '{}/5.0'.format(dfaux.iloc[0,1]),
                   help='País: India // Cidade: Hyderabad // Preço prato para 2: $600 (Indian Rupees(Rs.))')

    with col4:
        dfaux = best_rest(df1, food='Japanese')
        col4.metric(label='Japonesa: {}'.format(dfaux.iloc[0,2]), value= '{}/5.0'.format(dfaux.iloc[0,1]),
                   help='País: England // Cidade: London // Preço prato para 2: $110 (Pounds(Lb.))')

    with col5:
        dfaux = best_rest(df1, food='Brazilian')
        col5.metric(label='Brasileira: {}'.format(dfaux.iloc[0,2]), value= '{}/5.0'.format(dfaux.iloc[0,1]),
                   help='País: Brazil // Cidade: Rio de Janeiro // Preço prato para 2: $100 (Reais(Brl.))')

if deliver_options:
    linhas = (df1['is_delivering_now'] == 'yes')
    df1 = df1.loc[linhas,:]

if online_options:
    linhas = (df1['has_online_delivery'] == 'yes')
    df1 = df1.loc[linhas,:]

if table_options:
    linhas = (df1['has_table_booking'] == 'yes')
    df1 = df1.loc[linhas,:]
        
linhas_selecionadas = df1['country'].isin(country_options)
df1 = df1.loc[linhas_selecionadas,:]

linhas_selecionadas = df1['price_range'].isin(price_options)
df1 = df1.loc[linhas_selecionadas,:]

linhas_selecionadas = df1['cuisines'].isin(food_options)
df1 = df1.loc[linhas_selecionadas,:]

with st.container():
    st.markdown("""____""")
    st.write("##### Gráficos e tabela interativos dos restaurantes e culinárias registrados (utilize os filtros ao lado)")
    ntop = st.slider("Selecione a quantidade de restaurantes para visualizar", 0, 20, 10)
    st.markdown('#### Top {} melhores restaurantes'.format(ntop))
    cols=['restaurant_id', 'restaurant_name','cuisines', 'aggregate_rating', 
          'city','country','average_cost_for_two', 'votes']
    dfbest=df1.loc[:, cols].sort_values(['aggregate_rating','restaurant_id'], axis=0, ascending=[False, True])
    dfbest = dfbest.head(ntop)
    st.dataframe(dfbest)
        

with st.container():
    col1, col2 = st.columns(2, gap='small')
    with col1:
        st.markdown('#### Top {} culinárias com maior avaliação média'.format(ntop))
        fig=best_cuisines(df2, op=False)
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown('#### Top {} culinárias com menor avaliação média'.format(ntop))
        fig=best_cuisines(df2, op=True)
        st.plotly_chart(fig, use_container_width=True)
        


print("estou aqui")
print(dfaux)
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
import plotly.express as px
from datetime import date, time, datetime
from numerize.numerize import numerize
from streamlit_elements import elements, mui, html
import altair as alt

st.set_page_config(
    page_title="Real-time",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None)

alt.themes.enable("dark")

data_socie = "../New_Data/data_societe.csv"
data_scien = "../New_Data/data_sciences.csv"
data_eco = "../New_Data/data_economie.csv"

df_socie = pd.read_csv(data_socie)
df_scien = pd.read_csv(data_scien)
df_eco = pd.read_csv(data_eco)

data_f1 = pd.DataFrame(df_socie)
data_f2 = pd.DataFrame(df_scien)
data_f3 = pd.DataFrame(df_eco)
df_data = pd.concat([data_f1,data_f2,data_f3], ignore_index=True)
df_data = df_data.drop('Unnamed: 0', axis=1)

print(df_data)

#### Page Configuration ####
#st.set_page_config(page_title=None, page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)


### KPIs ###

total_tracking =len(df_data)
total_economie = len(df_data[df_data.Categorie == "economie"])
total_science = len(df_data[df_data.Categorie == "sciences"])
total_societe = len(df_data[df_data.Categorie == "societe"])


#### Sidebar ####

with st.sidebar:
    st.sidebar.title('🏂 LIVE CORP')

    st.sidebar.markdown("---")
    
    st.sidebar.subheader("🔠 Recherche par mot-clé")
    keyword = st.sidebar.text_input("Entrez un mot-clé")
    col = ["Categorie","Description","PubDate","Title"]

    if keyword:
        df_data = df_data[df_data["Title"].str.contains(keyword, case=False, na=False)]
        if df_data.empty:
            df_data = df_data[df_data["Description"].str.contains(keyword, case=False, na=False)]
            if df_data.empty:
                df_data = df_data[df_data["PubDate"].str.contains(keyword, case=False, na=False)]
                if df_data.empty:
                    df_data = df_data[df_data["Categorie"].str.contains(keyword, case=False, na=False)]
                    
                
            
            

    st.sidebar.markdown("---")
    
    # Filtrer par sentiment
    st.sidebar.subheader("🎭 Filtrer par Catégorie")
    categorie_filter = st.sidebar.radio("", ["Tous", "economie", "sciences", "societe"])
    if categorie_filter != "Tous":
        df_data = df_data[df_data["Categorie"] == categorie_filter]
    
    st.sidebar.markdown("---")
    
    # Filtrer par longueur du texte
    st.sidebar.subheader("📏 Longueur ")
    min_length, max_length = st.sidebar.slider("Choisissez la plage", 0, 500, (0, 500))
    df_data = df_data[df_data["Categorie"].str.len().between(min_length, max_length)]
    
    st.sidebar.markdown("---")
    
    #Coleur d'affichage
    color_theme_list = ['green','aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure',
            'beige', 'bisque', 'black', 'blanchedalmond', 'blue',
            'blueviolet', 'brown', 'burlywood', 'cadetblue',
            'chartreuse', 'chocolate', 'coral', 'cornflowerblue',
            'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan',
            'darkgoldenrod', 'darkgray', 'darkgrey', 'darkgreen',
            'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange',
            'darkorchid', 'darkred', 'darksalmon', 'darkseagreen',
            'darkslateblue', 'darkslategray', 'darkslategrey',
            'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue',
            'dimgray', 'dimgrey', 'dodgerblue', 'firebrick',
            'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro',
            'ghostwhite', 'gold', 'goldenrod', 'gray', 'grey',
            'greenyellow', 'honeydew', 'hotpink', 'indianred', 'indigo',
            'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen',
            'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan',
            'lightgoldenrodyellow', 'lightgray', 'lightgrey',
            'lightgreen', 'lightpink', 'lightsalmon', 'lightseagreen',
            'lightskyblue', 'lightslategray', 'lightslategrey',
            'lightsteelblue', 'lightyellow', 'lime', 'limegreen',
            'linen', 'magenta', 'maroon', 'mediumaquamarine',
            'mediumblue', 'mediumorchid', 'mediumpurple',
            'mediumseagreen', 'mediumslateblue', 'mediumspringgreen',
            'mediumturquoise', 'mediumvioletred', 'midnightblue',
            'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy',
            'oldlace', 'olive', 'olivedrab', 'orange', 'orangered',
            'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise',
            'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink',
            'plum', 'powderblue', 'purple', 'red', 'rosybrown',
            'royalblue', 'rebeccapurple', 'saddlebrown', 'salmon',
            'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver',
            'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow',
            'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato',
            'turquoise', 'violet', 'wheat', 'white', 'whitesmoke',
            'yellow', 'yellowgreen']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)
print(selected_color_theme)

#### Page Principal ####

st.title("📊 Suivi du Flux RSS de France Info")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="📌 Total de données", value=total_tracking)

with col2:
    st.metric(label="✅ Catégorie économie", value=total_economie)

with col3:
    st.metric(label="✅ Catégorie science", value=total_science)
    
with col4:
    st.metric(label="✅ Catégorie société", value=total_societe)

st.markdown("---")

### Affichage des données ###

## Methode de filtrage ##
#def make_topic():
    

fig_col1, fig_col2, fig_col3 = st.columns(3, gap='large')

with fig_col1:
     # Date d'ajout
    df_data['PubDate'] = pd.to_datetime(df_data['PubDate'])
    df_data["Date"] = df_data["PubDate"].dt.strftime('%m/%d/%Y')
    suivi_data = df_data.groupby(['Date']).agg(Nbr_Posts=("Date","count")).reset_index()

    fig = px.line(suivi_data, x="Date", 
                  y="Nbr_Posts")
    fig.update_traces(line_color=selected_color_theme)
    
    st.markdown("#### :blue[**Nombre de posts par intervalle de temps**]")
    
    df_data["Mois"] = df_data["PubDate"].dt.strftime('%B')
    suivi_data1 = df_data.groupby(['Mois']).agg(Nbr_Posts=("Mois","count")).reset_index()

    fig1, ax = plt.subplots(figsize=(6, 4))
    ax.bar(suivi_data1["Mois"], suivi_data1["Nbr_Posts"], edgecolor="black")
    ax.set_xlabel("Mois")
    ax.set_ylabel("Nbr_Posts")
    st.plotly_chart(fig)
    st.markdown("---")
    
    st.pyplot(fig1)
    

    
with fig_col2:
     # Jour de la semaine plus de posts
    df_data["Jour"] = df_data["PubDate"].dt.strftime('%A')
    suivi_data = df_data.groupby(['Jour']).agg(Nbr_Posts=("Jour","count")).reset_index()

    fig2 = px.line(suivi_data, x="Jour", 
                  y="Nbr_Posts")
    fig2.update_traces(line_color=selected_color_theme)
    
    st.markdown("#### :blue[**Répartition dans la semaine (%)**]")
    
    fig2_2 = px.pie(suivi_data, values='Nbr_Posts', names='Jour',)
    
    st.plotly_chart(fig2_2)
    st.markdown("---")
    
    st.plotly_chart(fig2)

    
with fig_col3:
        # Heure de la journée plus de posts
    df_data["Heure"] = df_data["PubDate"].dt.strftime(' %H')
    suivi_data = df_data.groupby(['Heure']).agg(Nbr_Posts=("Heure","count")).reset_index()

    fig3 = px.line(suivi_data, x="Heure", 
                  y="Nbr_Posts")
    fig3.update_traces(line_color=selected_color_theme)
    
    st.markdown("#### :blue[**Flux des heures**]")
    
    st.plotly_chart(fig3)
    st.markdown("---")
    with st.expander('About', expanded=True):
        st.write('''
            - :blue[**A propos**]: Les données du flux RSS de France Info récupérées pour Live Corp permettra de faire un suivi pour notre futur jeu de données.Avec la possibilité de visualiser une petite classification des données en 3 sous-groupes : science, économie et société .
            - :orange[**📌 Total de données**]: Nombre total de posts recupérés via Flux RSS.
            - :orange[**✅ Catégorie économie**]: Nombres total de posts pour la catégorie économie.
            - :orange[**✅ Catégorie science**]: Nombres total de posts pour la catégorie sciences.
            - :orange[**✅ Catégorie sociale**]: Nombres total de posts pour la catégorie société.
            ''')
    
# Tableau filtré ou pas
st.dataframe(df_data)
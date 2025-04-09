import streamlit as st
import pandas as pd
import numpy as np
from typing import List, Tuple
import plotly.express as px
from numerize.numerize import numerize
import altair as alt

#Page Configuration
st.set_page_config(
    page_title="Real-time Tracking of the number of TWEETS by TOPIC",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")


# Load Data

data_l = "./KafkaData.csv"
df_data = pd.read_csv(data_l)

total_Tweets =len(df_data)
total_Topic = len(df_data["Sujets"].unique())
Nbr_T_S = df_data.groupby(["Sujets"]).agg(Nbr_Tweets=("Tweets","count")).reset_index()
# Add a sidebar

with st.sidebar:
    st.title('🏂 Tracking TWEETS by TOPIC')
    
    suject_list = list(df_data.Sujets.unique())[::-1]
    
    selected_suject = st.selectbox('Select a suject', suject_list, index=len(suject_list)-1)
    df_selected_suject = df_data[df_data.Sujets == selected_suject]
    df_selected_suject_sorted = df_selected_suject.sort_values(by="Tweets", ascending=False)

    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)
    
if df_selected_suject is not None:
    Nbr_T_S1 = len(df_selected_suject)

# KPIs
t1,t2,t3 = st.columns(3, gap='large')

with t1:
    st.image("images/impression.png", use_column_width="auto")
    st.metric(label="Total Topics", value=numerize(total_Topic))

with t2:
    st.image("images/conversion.png", use_column_width="auto")
    st.metric(label="Total Tweets", value=numerize(total_Tweets))
    
with t3:
    st.image("images/tap.png", use_column_width="auto")
    st.metric(label="Total Tweets of Topic Selected", value=numerize(Nbr_T_S1))
        
    
    
# Plot and chart types

def make_topic():
        
    # Filtrage des données basé sur la sélection
    suivi_data = df_data.groupby(["Sujets"]).agg(Nbr_Tweets=("Tweets","count")).reset_index()
    print(suivi_data)
    # Mise à jour du graphique
    fig = px.line(suivi_data, x="Sujets", 
                y="Nbr_Tweets")
    st.plotly_chart(fig)
    return suivi_data
    
    
def make_choropleth(input_df, input_id, input_column, input_color_theme, suivi_data_nbr):
    choropleth = px.choropleth(input_df, locations=input_id, color=input_column, locationmode="USA-states",
                               color_continuous_scale=input_color_theme,
                               range_color=(0, max(suivi_data_nbr.Tweets)),
                               scope="usa",
                               labels={'Tweets':'Tweets'}
                              )
    choropleth.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )
    return choropleth

col = st.columns((1.5, 4.5, 2), gap='medium')


with col[0]:
   with st.expander('About', expanded=True):
        st.write('''
            -  :orange[**Total Topics**]: Nombre total de topics recupérés via Reddit.
            - :orange[**Total Tweets**]: Nombres total de tweets récupérés.
            - :orange[**View Tweets**]: Suivi des tweets(commentaires) récupérés pour un topic. Permet de savoir s'il y a des nouveau commentaires ou par de façon manuel.
            ''')
with col[1]:
    nbr = make_topic()
    
    #     st.markdown('#### Total Population')
        
    #     choropleth = make_choropleth(df_selected_suject, 'states_code', 'population', selected_color_theme)
    #     st.plotly_chart(choropleth, use_container_width=True)
        
    #     heatmap = make_heatmap(df_reshaped, 'year', 'states', 'population', selected_color_theme)
    #     st.altair_chart(heatmap, use_container_width=True)

with col[2]:
    
    
    st.markdown('#### Views Tweets')

    st.dataframe(df_selected_suject_sorted,
                 column_order=("Sujets", "Tweets"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "Sujets": st.column_config.TextColumn(
                        "Sujets",
                    ),
                    "Tweets": st.column_config.ProgressColumn(
                        "Tweets",
                        format="%f",
                        min_value=0,
                        max_value=max(df_selected_suject_sorted.Tweets),
                     )}
                 )
   
    

# make_choropleth(,nbr)
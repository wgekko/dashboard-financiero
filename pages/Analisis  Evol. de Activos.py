import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import base64
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn import linear_model, tree, neighbors

import warnings
warnings.simplefilter("ignore", category=FutureWarning)

#""" imagen de background"""
def add_local_background_image(image):
  with open(image, "rb") as image:
    encoded_string = base64.b64encode(image.read())
    st.markdown(
      f"""
      <style>
      .stApp{{
        background-image: url(data:files/{"jpg"};base64,{encoded_string.decode()});
      }}    
      </style>
      """,
      unsafe_allow_html=True
    )
add_local_background_image("img/fondo1.jpg")

#""" imagen de sidebar"""
def add_local_sidebar_image(image):
  with open(image, "rb") as image:
    encoded_string = base64.b64encode(image.read())
    st.markdown(
      f"""
      <style>
      .stSidebar{{
        background-image: url(data:files/{"jpg"};base64,{encoded_string.decode()});
      }}    
      </style>
      """,
      unsafe_allow_html=True
    )

add_local_sidebar_image("img/fondo3.jpg")


#"""### agregar archivo de audio"""
app_musica = open("audio/knockin on heavens door piano full version.mp3", "rb")
audio_byte = app_musica
#st.audio(app_musica)


#"""### gif from local file"""
file_ = open("img/gráfico-combinado.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()


#"""### despliegue de sidebar"""  
with st.sidebar:     
    col1, col2 = st.columns(2, vertical_alignment="center")
    with col1:        
        st.image("img/gráfico-combinado.gif", width=70) 
    with col2:
        st.subheader("Analisis de Activos Financieros")       
    st.write("---")
    st.link_button("Mi LinkedIn", "https://www.linkedin.com/in/walter-gomez-fullstack-developer-jr-java-python-adm-finanzas/")
    #st.write("#")
    st.link_button("Mi Porfolio", "https://walter-portfolio-animado.netlify.app/")
    st.write("#")
    st.write("activar sonido")
    st.audio(app_musica)

# ---- Descripcion de la pagina primera pagina de evol de variables diario----
df = pd.read_excel('datos/basedatos.xlsx')

list_option = ['BITCOIN', 'BLUE', 'MERV', 'AL30D']
option = st.radio("Seleccione una opción : ", (list_option), horizontal=True )

st.write("---")
if option == 'BITCOIN':
    st.subheader(f"Evolución del valor Diario de : {option} (cotización)")
    st.write('el valor : BITCOIN,  está expresado u$d (periodo diario)')
    st.write("---")
    fig= px.line(
        df,
        x='FECHA',
        y= option,
        #markers=True
    )
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    # ---- Descripcion de la segunda pagina de evol de variables nominal vs inflacion mensual----

    st.write("---")
    st.subheader(f"Evolución de {option}/IPC (sin inflación diario)")
    
    fig1= px.line(
            df,
            x='FECHA',
            y='BITCOIN/IPC',
            #markers=True
        )
    st.plotly_chart(fig1, use_container_width=True)


# ---- BLUE ----
elif option == 'BLUE':
    st.subheader(f"Evolución del valor Diario de : {option} (cotización)")
    st.write('el valor : BLUE,  está expresado $ (periodo diario)')
    st.write("---")
    fig= px.line(
        df,
        x='FECHA',
        y= option,
        #markers=True
    )
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    # ---- Descripcion de la segunda pagina de evol de variables nominal vs inflacion mensual----

    st.write("---")
    st.subheader(f"Evolución de {option}/IPC (sin inflación diario)")
    
    fig1= px.line(
            df,
            x='FECHA',
            y='BLUE/IPC',
            #markers=True
        )
    st.plotly_chart(fig1, use_container_width=True)

# ---- INDICE MERVAL ----
elif option == 'MERV':
    st.subheader(f"Evolución del valor Diario de : {option} (cotización)")
    st.write('el valor : INDICE MERVAL,  está expresado $ (periodo diario)')
    st.write("---")
    fig= px.line(
        df,
        x='FECHA',
        y= option,
        #markers=True
    )
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    # ---- Descripcion de la segunda pagina de evol de variables nominal vs inflacion mensual----

    st.write("---")
    st.subheader(f"Evolución de {option}/IPC (sin inflación diario)")    
    fig1= px.line(
            df,
            x='FECHA',
            y='MERVAL/IPC',
            #markers=True
        )
    st.plotly_chart(fig1, use_container_width=True)   
# ----  INDICE MERVAL DOLARES DEFLACTADO ----
    st.write("---")
    st.subheader(f"Evolución de {option}/U$D/IPC (en dolares sin inflación diario)")
    fig1= px.line(
            df,
            x='FECHA',
            y='MERV/DOL/IPC',
            #markers=True
        )
    st.plotly_chart(fig1, use_container_width=True)

# ---- AL30D ----
elif option == 'AL30D':
    st.subheader(f"Evolución del valor Diario de : {option} (cotización)")
    st.write('el valor : AL30D,  está expresado $ (periodo diario)')
    st.write("---")
    fig= px.line(
        df,
        x='FECHA',
        y= option,
        #markers=True
    )
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    # ---- Descripcion de la segunda pagina de evol de variables nominal vs inflacion mensual----

    st.write("---")
    st.subheader(f"Evolución de {option}/IPC (sin inflación diario)")
    
    fig1= px.line(
            df,
            x='FECHA',
            y='AL30D/IPC',
            #markers=True
        )
    st.plotly_chart(fig1, use_container_width=True)   
else:
    st.write("Error, en la opción elegida ")

with st.container():
    st.write("---")
    st.write("&copy; - derechos reservados -  2024 -  Walter Gómez - FullStack Developer - Data Science - Business Intelligence")
    #st.write("##")   


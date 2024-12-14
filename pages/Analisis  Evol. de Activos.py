import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import base64
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn import linear_model, tree, neighbors
import streamlit.components.v1 as components
import base64
import warnings
warnings.simplefilter("ignore", category=FutureWarning)

#"""" codigo de particulas que se agregan en le background""""
particles_js = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Particles.js</title>
  <style>
  #particles-js {
    position: fixed;
    width: 100vw;
    height: 100vh;
    top: 0;
    left: 0;
    z-index: -1; /* Send the animation to the back */
  }
  .content {
    position: relative;
    z-index: 1;
    color: white;
  }
  
</style>
</head>
<body>
  <div id="particles-js"></div>
  <div class="content">
    <!-- Placeholder for Streamlit content -->
  </div>
  <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
  <script>
    particlesJS("particles-js", {
      "particles": {
        "number": {
          "value": 300,
          "density": {
            "enable": true,
            "value_area": 800
          }
        },
        "color": {
          "value": "#ffffff"
        },
        "shape": {
          "type": "circle",
          "stroke": {
            "width": 0,
            "color": "#000000"
          },
          "polygon": {
            "nb_sides": 5
          },
          "image": {
            "src": "img/github.svg",
            "width": 100,
            "height": 100
          }
        },
        "opacity": {
          "value": 0.5,
          "random": false,
          "anim": {
            "enable": false,
            "speed": 1,
            "opacity_min": 0.2,
            "sync": false
          }
        },
        "size": {
          "value": 2,
          "random": true,
          "anim": {
            "enable": false,
            "speed": 40,
            "size_min": 0.1,
            "sync": false
          }
        },
        "line_linked": {
          "enable": true,
          "distance": 100,
          "color": "#ffffff",
          "opacity": 0.22,
          "width": 1
        },
        "move": {
          "enable": true,
          "speed": 0.2,
          "direction": "none",
          "random": false,
          "straight": false,
          "out_mode": "out",
          "bounce": true,
          "attract": {
            "enable": false,
            "rotateX": 600,
            "rotateY": 1200
          }
        }
      },
      "interactivity": {
        "detect_on": "canvas",
        "events": {
          "onhover": {
            "enable": true,
            "mode": "grab"
          },
          "onclick": {
            "enable": true,
            "mode": "repulse"
          },
          "resize": true
        },
        "modes": {
          "grab": {
            "distance": 100,
            "line_linked": {
              "opacity": 1
            }
          },
          "bubble": {
            "distance": 400,
            "size": 2,
            "duration": 2,
            "opacity": 0.5,
            "speed": 1
          },
          "repulse": {
            "distance": 200,
            "duration": 0.4
          },
          "push": {
            "particles_nb": 2
          },
          "remove": {
            "particles_nb": 3
          }
        }
      },
      "retina_detect": true
    });
  </script>
</body>
</html>
"""
st.set_page_config(page_title="Evolucion Activos", page_icon="img/dashboard.png", layout="wide")
components.html(particles_js, height=100,scrolling=False)

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
    #st.write("#")
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
    

components.html(particles_js, height=80,scrolling=False)    

 # --------------------------------FOOTER ---------------------------------------------------------
st.write("---")
with st.container():
  #st.write("---")
  st.write("&copy; - derechos reservados -  2024 -  Walter Gómez - FullStack Developer - Data Science - Business Intelligence")
  #st.write("##")
  left, right = st.columns(2, gap='small', vertical_alignment="bottom")
  with left:
    #st.write('##')
    st.link_button("Mi LinkedIn", "https://www.linkedin.com/in/walter-gomez-fullstack-developer-jr-java-python-adm-finanzas/")
  with right: 
     #st.write('##') 
    st.link_button("Mi Porfolio", "https://walter-portfolio-animado.netlify.app/")
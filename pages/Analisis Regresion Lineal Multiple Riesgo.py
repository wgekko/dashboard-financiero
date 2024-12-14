import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
import plotly.graph_objects as go
import plotly.express as px
#st.set_option('deprecation.showPyplotGlobalUse', False)
from streamlit_extras.metric_cards import style_metric_cards
import seaborn as sns
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
st.set_page_config(page_title="Regresion Lineal Riesgo", page_icon="img/dashboard.png", layout="wide")
components.html(particles_js, height=100,scrolling=False)

# ------------ archivos de background y sidebar
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
    st.write("activar sonido")
    st.audio(app_musica)

colorCards= "#34495E"
colorPrev = "#74f210" 

st.subheader("Regresión Lineal de Riesgo mensual con Machine Learning ")

st.write("REGRESIÓN MÚLTIPLE CON SSE, SE, SSR, SST, R2, ADJ[R2], RESIDUAL")
# load CSS Style / llamando a la archivo de estilos CSS
with open('styles.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

df = pd.read_excel('datos/riesgo-datos.xlsx')

list_option = ['BITCOIN','MERV', 'AL30D']
option = st.radio("Seleccione una opción : ", (list_option), horizontal=True )    

# -------------- desarrollo de analisis de rendimiento esperado sobre el BITCOIN --------------------
st.write("---")
if option == 'BITCOIN':    
    X = df[['RI-MERV','RI-AL30D']]
    Y = df['RI-BIT']

    # Fit a linear regression model / Ajuste un modelo de regresión lineal
    model = LinearRegression()
    X = X.values
    model.fit(X, Y)

    # Make predictions / hacer la prevision 
    predictions = model.predict(X)

    # Predictions on the same data / prevision sobre los mismos datos
    y_pred = model.predict(X)

    #Regression coefficients (B0, B1, B) / Coeficientes de regresión (B0, B1, B2)
    intercept = model.intercept_ #B0
    coefficients = model.coef_ #B1, B2

    # Calculate R-squared Coefficient of determination / Calculate R-squared Coefficient of determination
    r2 = r2_score(Y, predictions)

    # Calculate Adjusted R-squared / calculo ajustado de R-squared
    n = len(Y)
    p = X.shape[1]
    adjusted_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)

    # Calculate Sum Squared Error (SSE) and SSR / calculo del error de la sumatoria cuadrado (SSE ) y SSR 
    sse = np.sum((Y - predictions)**2)
    ssr = np.sum((y_pred - np.mean(Y)) ** 2)

    #regression line / regresion lineal
    with st.expander("COEFICIENTE DE REGRESIÓN"):
        col1,col2,col3=st.columns(3)
        col1.metric('INTERCEPCIÓN:',value= f'{intercept:.4f}',delta="(B0)")
        col2.metric('B1 COEFICIENTE:',value= f'{coefficients[0]:.4f}',delta=" para X1 riesgo de  Merval (B1)")
        col3.metric('B2 COEFICIENTE',value= f'{coefficients[1]:.4f}',delta=" para X2 riesgo de AL30D (B2):")
        style_metric_cards(background_color=colorCards,border_left_color="#9900AD",border_color="#5B2C6F",box_shadow="#283747")

    # Print R-squared, Adjusted R-squared, and SSE / se muestra  R-squared, Adjusted R-squared, y SSE
    with st.expander("MEDIDA DE VARIACIONES"):
        col1,col2,col3=st.columns(3)    
        col1.metric('R-CUADRADO:',value= f'{r2:.4f}',delta="Coeficiente de determinación")
        col2.metric('R-CUADRADO AJUSTADO:',value= f'{adjusted_r2:.4f}',delta="Adj[R2]")
        col3.metric('ERROR DE SUMA CUADRADA (SSE):',value= f'{sse:.4f}',delta="Cuadrado(Y-Y_pred)")
        style_metric_cards(background_color=colorCards,border_left_color="#CB4335",border_color="#5B2C6F",box_shadow="#283747")

    # Print a table with predicted Y / Mostrar una tabla con la Y predicha
    with st.expander("TABLA DE PREDICCIÓN"):
        result_df = pd.DataFrame({'FECHA':df['FECHA'],'NRO DE RIESGO MERVAL':df['RI-MERV'], 'NRO DE RIESGO AL30D': df['RI-AL30D'], 'RIESGO BITCOIN | Actual Y': Y, 'Y_previsto': predictions})
        # Add SSE and SSR to the DataFrame / Agregar SSE y SSR al DataFrame
        result_df['SSE'] = sse
        result_df['SSR'] = ssr
        st.dataframe(result_df,use_container_width=True)
        #download predicted excel / descargar el excel con valores     
        df_download = result_df.to_csv(index=False).encode('utf-8')    
        st.download_button(
            label="DESCARGAR EL CONJUNTO DE DATOS PREVISTOS",
            data=df_download,
            key="download_dataframe.csv",
            file_name="my_dataframe.csv"
        )

    with st.expander("RESIDUAL Y LÍNEA MEJOR AJUSTE"):    
        # Calculate residuals / Calcular residuos
        residuals = Y - predictions
        # Create a new DataFrame to store residuals / Crear un nuevo DataFrame para almacenar residuos
        residuals_df = pd.DataFrame({'Actual': Y, 'Previsto': predictions, 'Residual': residuals})
        # Print the residuals DataFrame / Imprimir el DataFrame de residuos
        st.dataframe(residuals_df,use_container_width=True)
        col1, col2=st.columns(2)
        with col1:
            plt.scatter(Y, predictions)
            plt.plot([min(Y), max(Y)], [min(Y), max(Y)],color='red', label='Línea mejor ajuste')  # Best fit line / Línea de mejor ajuste
            plt.xlabel('Actual Y | riesgo Bitcoin')
            plt.ylabel('Previsto_Y')
            plt.grid(True)
            plt.legend()
            st.pyplot(plt)
        with col2:
            sns.displot(residuals,kind='kde',color='blue', fill=True, legend=True)
            sns.set_style("whitegrid")  # Set the style to whitegrid / Establezca el estilo en cuadrícula blanca
            st.pyplot(plt)

    # User input for X1 and X2 / usuario ingresa x1 y x2
    with st.expander("DESEA AGREGAR DATOS PARA NUEVA PREVISIÓN DE RIESGO"):  
        st.subheader("Desea ingresar nuevo valor en Rend.Esp. para generar nueva previsión")   
        with st.form("input_form",clear_on_submit=True):
            x1 = st.number_input("Digite Riesgo Merval")
            x2 = st.number_input("Digite Riesgo AL30D")
            submit_button = st.form_submit_button(label="Generar Previsión")

    if submit_button:
        # Make predictions / hacer la prevision
        new_data = np.array([[x1, x2]])
        new_prediction = model.predict(new_data)
        # Display prediction / Mostrar la prevision
        predictions_formatted = [f"{value:.2f}" for value in new_prediction] #/ si se quiere ajustar a 2 decimales e lresultado 
        with st.expander(f'("Ver Previsión de Riesgo {option} % ")'):
            #st.write(f"<span style='font-size: 34px;color:green;'>Resultado Previsión de Riesgo % : </span> <span style='font-size: 35px;'> {new_prediction} % mensual </span>", unsafe_allow_html=True)
            # la opcion de arriba es para mostrar los resultados con mas de 2 decimales 
            st.write(f"<span style='font-size: 34px;color:{colorPrev};'>Resultado Previsión de Riesgo : </span> <span style='font-size: 35px;color:{colorPrev};'> {', '.join(predictions_formatted)} % mensual </span>", unsafe_allow_html=True)

# -------------- desarrollo de analisis de rendimiento esperado sobre el INDICE MERVAL --------------------
#st.write("---")
elif option == 'MERV':    
    X = df[['RI-BIT','RI-AL30D']]
    Y = df['RI-MERV']

    # Fit a linear regression model / Ajuste un modelo de regresión lineal
    model = LinearRegression()
    X = X.values
    model.fit(X, Y)

    # Make predictions / hacer la prevision 
    predictions = model.predict(X)

    # Predictions on the same data / prevision sobre los mismos datos
    y_pred = model.predict(X)

    #Regression coefficients (B0, B1, B) / Coeficientes de regresión (B0, B1, B2)
    intercept = model.intercept_ #B0
    coefficients = model.coef_ #B1, B2

    # Calculate R-squared Coefficient of determination / Calculate R-squared Coefficient of determination
    r2 = r2_score(Y, predictions)

    # Calculate Adjusted R-squared / calculo ajustado de R-squared
    n = len(Y)
    p = X.shape[1]
    adjusted_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)

    # Calculate Sum Squared Error (SSE) and SSR / calculo del error de la sumatoria cuadrado (SSE ) y SSR 
    sse = np.sum((Y - predictions)**2)
    ssr = np.sum((y_pred - np.mean(Y)) ** 2)

    #regression line / regresion lineal
    with st.expander("COEFICIENTE DE REGRESIÓN"):
        col1,col2,col3=st.columns(3)
        col1.metric('INTERCEPCIÓN:',value= f'{intercept:.4f}',delta="(B0)")
        col2.metric('B1 COEFICIENTE:',value= f'{coefficients[0]:.4f}',delta=" para X1 riesgo de Bitcoin (B1)")
        col3.metric('B2 COEFICIENTE',value= f'{coefficients[1]:.4f}',delta=" para X2 riesgo de AL30D (B2):")
        style_metric_cards(background_color=colorCards,border_left_color="#9900AD",border_color="#5B2C6F",box_shadow="#283747")

    # Print R-squared, Adjusted R-squared, and SSE / se muestra  R-squared, Adjusted R-squared, y SSE
    with st.expander("MEDIDA DE VARIACIONES"):
        col1,col2,col3=st.columns(3)    
        col1.metric('R-CUADRADO:',value= f'{r2:.4f}',delta="Coeficiente de determinación")
        col2.metric('R-CUADRADO AJUSTADO:',value= f'{adjusted_r2:.4f}',delta="Adj[R2]")
        col3.metric('ERROR DE SUMA CUADRADA (SSE):',value= f'{sse:.4f}',delta="Cuadrado(Y-Y_pred)")
        style_metric_cards(background_color=colorCards,border_left_color="#CB4335",border_color="#5B2C6F",box_shadow="#283747")

    # Print a table with predicted Y / Mostrar una tabla con la Y predicha
    with st.expander("TABLA DE PREDICCIÓN"):
        result_df = pd.DataFrame({'FECHA':df['FECHA'],'NRO DE RIESGO BITCOIN':df['RI-BIT'], 'NRO DE RIESGO AL30D': df['RI-AL30D'], 'RIESGO MERVAL | Actual Y': Y, 'Y_previsto': predictions})
        # Add SSE and SSR to the DataFrame / Agregar SSE y SSR al DataFrame
        result_df['SSE'] = sse
        result_df['SSR'] = ssr
        st.dataframe(result_df,use_container_width=True)
        #download predicted excel / descargar el excel con valores     
        df_download = result_df.to_csv(index=False).encode('utf-8')    
        st.download_button(
            label="DESCARGAR EL CONJUNTO DE DATOS PREVISTOS",
            data=df_download,
            key="download_dataframe.csv",
            file_name="my_dataframe.csv"
        )

    with st.expander("RESIDUAL Y LÍNEA MEJOR AJUSTE"):    
        # Calculate residuals / Calcular residuos
        residuals = Y - predictions
        # Create a new DataFrame to store residuals / Crear un nuevo DataFrame para almacenar residuos
        residuals_df = pd.DataFrame({'Actual': Y, 'Previsto': predictions, 'Residual': residuals})
        # Print the residuals DataFrame / Imprimir el DataFrame de residuos
        st.dataframe(residuals_df,use_container_width=True)
        col1, col2=st.columns(2)
        with col1:
            plt.scatter(Y, predictions)
            plt.plot([min(Y), max(Y)], [min(Y), max(Y)],color='red', label='Línea mejor ajuste')  # Best fit line / Línea de mejor ajuste
            plt.xlabel('Actual Y | riesgo Merval')
            plt.ylabel('Previsto_Y')
            plt.grid(True)
            plt.legend()
            st.pyplot(plt)
        with col2:
            sns.displot(residuals,kind='kde',color='blue', fill=True, legend=True)
            sns.set_style("whitegrid")  # Set the style to whitegrid / Establezca el estilo en cuadrícula blanca
            st.pyplot(plt)

    # User input for X1 and X2 / usuario ingresa x1 y x2
    with st.expander("DESEA AGREGAR DATOS PARA NUEVA PREVISIÓN DE RIESGO"):  
        st.subheader("Desea ingresar nuevo valor en Rend.Esp. para generar nueva previsión")   
        with st.form("input_form",clear_on_submit=True):
            x1 = st.number_input("Digite Riesgo Bitcoin")
            x2 = st.number_input("Digite Riesgo AL30D")
            submit_button = st.form_submit_button(label="Generar Previsión")

    if submit_button:
        # Make predictions / hacer la prevision
        new_data = np.array([[x1, x2]])
        new_prediction = model.predict(new_data)
        # Display prediction / Mostrar la prevision
        predictions_formatted = [f"{value:.2f}" for value in new_prediction] #/ si se quiere ajustar a 2 decimales e lresultado 
        with st.expander(f'("Ver Previsión de Riesgo {option} % ")'):
            #st.write(f"<span style='font-size: 34px;color:green;'>Resultado Previsión de Riesgo % : </span> <span style='font-size: 35px;'> {new_prediction} % mensual </span>", unsafe_allow_html=True)
            # la opcion de arriba es para mostrar los resultados con mas de 2 decimales 
            st.write(f"<span style='font-size: 34px;color:{colorPrev};'>Resultado Previsión de Riesgo : </span> <span style='font-size: 35px;color:{colorPrev};'> {', '.join(predictions_formatted)} % mensual </span>", unsafe_allow_html=True)

# -------------- desarrollo de analisis de rendimiento esperado sobre el AL30D --------------------
#st.write("---")
elif option == 'AL30D':
    
    X = df[['RI-BIT','RI-MERV']]
    Y = df['RI-AL30D']

    # Fit a linear regression model / Ajuste un modelo de regresión lineal
    model = LinearRegression()
    X = X.values
    model.fit(X, Y)

    # Make predictions / hacer la prevision 
    predictions = model.predict(X)

    # Predictions on the same data / prevision sobre los mismos datos
    y_pred = model.predict(X)

    #Regression coefficients (B0, B1, B) / Coeficientes de regresión (B0, B1, B2)
    intercept = model.intercept_ #B0
    coefficients = model.coef_ #B1, B2

    # Calculate R-squared Coefficient of determination / Calculate R-squared Coefficient of determination
    r2 = r2_score(Y, predictions)

    # Calculate Adjusted R-squared / calculo ajustado de R-squared
    n = len(Y)
    p = X.shape[1]
    adjusted_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)

    # Calculate Sum Squared Error (SSE) and SSR / calculo del error de la sumatoria cuadrado (SSE ) y SSR 
    sse = np.sum((Y - predictions)**2)
    ssr = np.sum((y_pred - np.mean(Y)) ** 2)

    #regression line / regresion lineal
    with st.expander("COEFICIENTE DE REGRESIÓN"):
        col1,col2,col3=st.columns(3)
        col1.metric('INTERCEPCIÓN:',value= f'{intercept:.4f}',delta="(B0)")
        col2.metric('B1 COEFICIENTE:',value= f'{coefficients[0]:.4f}',delta=" para X1 riesgo de Bitcoin (B1)")
        col3.metric('B2 COEFICIENTE',value= f'{coefficients[1]:.4f}',delta=" para X2 riesgo de Merval (B2):")
        style_metric_cards(background_color=colorCards,border_left_color="#9900AD",border_color="#5B2C6F",box_shadow="#283747")

    # Print R-squared, Adjusted R-squared, and SSE / se muestra  R-squared, Adjusted R-squared, y SSE
    with st.expander("MEDIDA DE VARIACIONES"):
        col1,col2,col3=st.columns(3)    
        col1.metric('R-CUADRADO:',value= f'{r2:.4f}',delta="Coeficiente de determinación")
        col2.metric('R-CUADRADO AJUSTADO:',value= f'{adjusted_r2:.4f}',delta="Adj[R2]")
        col3.metric('ERROR DE SUMA CUADRADA (SSE):',value= f'{sse:.4f}',delta="Cuadrado(Y-Y_pred)")
        style_metric_cards(background_color=colorCards,border_left_color="#CB4335",border_color="#5B2C6F",box_shadow="#283747")

    # Print a table with predicted Y / Mostrar una tabla con la Y predicha
    with st.expander("TABLA DE PREDICCIÓN"):
        result_df = pd.DataFrame({'FECHA':df['FECHA'],'NRO DE RIESGO BITCOIN':df['RI-BIT'], 'NRO DE RIESGO MERVAL': df['RI-MERV'], 'RIESGO AL30D | Actual Y': Y, 'Y_previsto': predictions})
        # Add SSE and SSR to the DataFrame / Agregar SSE y SSR al DataFrame
        result_df['SSE'] = sse
        result_df['SSR'] = ssr
        st.dataframe(result_df,use_container_width=True)
        #download predicted excel / descargar el excel con valores     
        df_download = result_df.to_csv(index=False).encode('utf-8')    
        st.download_button(
            label="DESCARGAR EL CONJUNTO DE DATOS PREVISTOS",
            data=df_download,
            key="download_dataframe.csv",
            file_name="my_dataframe.csv"
        )

    with st.expander("RESIDUAL Y LÍNEA MEJOR AJUSTE"):    
        # Calculate residuals / Calcular residuos
        residuals = Y - predictions
        # Create a new DataFrame to store residuals / Crear un nuevo DataFrame para almacenar residuos
        residuals_df = pd.DataFrame({'Actual': Y, 'Previsto': predictions, 'Residual': residuals})
        # Print the residuals DataFrame / Imprimir el DataFrame de residuos
        st.dataframe(residuals_df,use_container_width=True)
        col1, col2=st.columns(2)
        with col1:
            plt.scatter(Y, predictions)
            plt.plot([min(Y), max(Y)], [min(Y), max(Y)],color='red', label='Línea mejor ajuste')  # Best fit line / Línea de mejor ajuste
            plt.xlabel('Actual Y | riesgo AL30D')
            plt.ylabel('Previsto_Y')
            plt.grid(True)
            plt.legend()
            st.pyplot(plt)
        with col2:
            sns.displot(residuals,kind='kde',color='blue', fill=True, legend=True)
            sns.set_style("whitegrid")  # Set the style to whitegrid / Establezca el estilo en cuadrícula blanca
            st.pyplot(plt)

    # User input for X1 and X2 / usuario ingresa x1 y x2
    with st.expander("DESEA AGREGAR DATOS PARA NUEVA PREVISIÓN DE RIESGO"):  
        st.subheader("Desea ingresar nuevo valor en Rend.Esp. para generar nueva previsión")   
        with st.form("input_form",clear_on_submit=True):
            x1 = st.number_input("Digite Riesgo Bitcoin")
            x2 = st.number_input("Digite Riesgo Merval")
            submit_button = st.form_submit_button(label="Generar Previsión")

    if submit_button:
        # Make predictions / hacer la prevision
        new_data = np.array([[x1, x2]])
        new_prediction = model.predict(new_data)
        # Display prediction / Mostrar la prevision
        predictions_formatted = [f"{value:.2f}" for value in new_prediction] #/ si se quiere ajustar a 2 decimales e lresultado 
        with st.expander(f'("Ver Previsión de Riesgo {option} % ")'):
            #st.write(f"<span style='font-size: 34px;color:green;'>Resultado Previsión de Riesgo % : </span> <span style='font-size: 35px;'> {new_prediction} % mensual </span>", unsafe_allow_html=True)
            # la opcion de arriba es para mostrar los resultados con mas de 2 decimales 
            st.write(f"<span style='font-size: 34px;color:{colorPrev};'>Resultado Previsión de Riesgo : </span> <span style='font-size: 35px;color:{colorPrev};'> {', '.join(predictions_formatted)} % mensual </span>", unsafe_allow_html=True)


else:
    st.write("Error, en la opción elegida ")

components.html(particles_js, height=100,scrolling=False)

# ------------- FOOTER ---------------------------------------------

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



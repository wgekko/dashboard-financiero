import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import base64
import plotly.graph_objects as go
from scipy.stats import chi2, norm
from sklearn.model_selection import train_test_split
#from sklearn import linear_model, tree, neighbors
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
st.set_page_config(page_title="Intervalo de Confianza", page_icon="img/dashboard.png", layout="wide")
components.html(particles_js, height=90,scrolling=False)

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


#------------------------------------------------------------------------------------------------------------------------
# ---- Descripcion de la pagina primera pagina de evol de variables diario----
df = pd.read_excel('datos/basedatos.xlsx')

list_option = ['BITCOIN', 'BLUE', 'MERV', 'AL30D']
option = st.radio("Seleccione una opción : ", (list_option), horizontal=True )

# Load the dataset / llamamos a los datos desde un excel
df = pd.read_excel('datos/basedatos.xlsx')

# Extract the 'bitcoin' column / extraer los datos de la columna 'bitcoin'
bitcoin = df['BITCOIN']/1000
blue = df['BLUE']
merv = df['MERV']/1000
al30d = df['AL30D']
rbit = df['R-BIT']
rblue = df['R-BLUE']
rmerv = df['R-MERV']
ral30d = df['R-AL30D'] 

# Sample statistics / estadistica de muestra
n = len(bitcoin)
sample_mean = np.mean(bitcoin)
sample_std = np.std(bitcoin, ddof=1)  # Use ddof=1 for sample standard deviation / Utilice ddof=1 para la desviación estándar de la muestra

# Population size / tamaño de la poblacion
N = 5000

# Confidence level / nivel de confianza 
confidence_level = 0.95
alpha = 1 - confidence_level

# Check if FPCF should be applied / hay que verificar si debe aplicar FPCF (factor de corrección de población finita)
# se utiliza cuando se toma una muestra sin reemplazo de más del 5% de una población
fpcf = 1  # Default value (no correction) / Valor predeterminado (sin corrección)
if n / N >= 0.05:
    fpcf = np.sqrt((N - n) / (N - 1))

# Confidence interval for population mean / Intervalo de confianza para la media de la población
sem = sample_std / np.sqrt(n)  # Standard error of the mean / Error estándar de la media
sem_corrected = sem * fpcf  # Apply FPCF if necessary / se aplica FPCF si es necesario
z_critical = norm.ppf(1 - alpha / 2)  # Critical z-value for two-tailed test / Valor z crítico para la prueba de dos colas

margin_of_error_mean = z_critical * sem_corrected
lower_bound_mean = sample_mean - margin_of_error_mean
upper_bound_mean = sample_mean + margin_of_error_mean

# calculo 
# Confidence interval for population standard deviation
# Intervalo de confianza para la desviación estándar de la población
df_degrees = n - 1
chi2_lower = chi2.ppf(alpha / 2, df_degrees)
chi2_upper = chi2.ppf(1 - alpha / 2, df_degrees)

lower_bound_std = np.sqrt((df_degrees * sample_std ** 2) / chi2_upper)
upper_bound_std = np.sqrt((df_degrees * sample_std ** 2) / chi2_lower)

# Define the normal distribution parameters
# Defina los parámetros de distribución normal

x = np.linspace(sample_mean - 4 * sem_corrected, sample_mean + 4 * sem_corrected, 1000)
y = norm.pdf(x, sample_mean, sem_corrected)

#--------------------------------------------------------------------------------------------
st.write("---")
if option == 'BITCOIN':
    st.subheader(f"Intervalo de confianza diario de : {option} (cotización)")  
    #st.write("---")
    
    # Sample statistics / estadistica de muestra
    n = len(bitcoin)
    sample_mean = np.mean(bitcoin)
    sample_std = np.std(bitcoin, ddof=1)  # Use ddof=1 for sample standard deviation / Utilice ddof=1 para la desviación estándar de la muestra
    # Population size / tamaño de la poblacion
    N = 5000
    # Confidence level / nivel de confianza 
    confidence_level = 0.95
    alpha = 1 - confidence_level
    # Check if FPCF should be applied / hay que verificar si debe aplicar FPCF (factor de corrección de población finita)
    # se utiliza cuando se toma una muestra sin reemplazo de más del 5% de una población
    fpcf = 1  # Default value (no correction) / Valor predeterminado (sin corrección)
    if n / N >= 0.05:
        fpcf = np.sqrt((N - n) / (N - 1))
    # Confidence interval for population mean / Intervalo de confianza para la media de la población
    sem = sample_std / np.sqrt(n)  # Standard error of the mean / Error estándar de la media
    sem_corrected = sem * fpcf  # Apply FPCF if necessary / se aplica FPCF si es necesario
    z_critical = norm.ppf(1 - alpha / 2)  # Critical z-value for two-tailed test / Valor z crítico para la prueba de dos colas
    margin_of_error_mean = z_critical * sem_corrected
    lower_bound_mean = sample_mean - margin_of_error_mean
    upper_bound_mean = sample_mean + margin_of_error_mean
    # calculo 
    # Confidence interval for population standard deviation
    # Intervalo de confianza para la desviación estándar de la población
    df_degrees = n - 1
    chi2_lower = chi2.ppf(alpha / 2, df_degrees)
    chi2_upper = chi2.ppf(1 - alpha / 2, df_degrees)
    lower_bound_std = np.sqrt((df_degrees * sample_std ** 2) / chi2_upper)
    upper_bound_std = np.sqrt((df_degrees * sample_std ** 2) / chi2_lower)
    # Define the normal distribution parameters
    # Defina los parámetros de distribución normal
    x = np.linspace(sample_mean - 4 * sem_corrected, sample_mean + 4 * sem_corrected, 1000)
    y = norm.pdf(x, sample_mean, sem_corrected)    
    # Create figure using Plotly
    # se genera el grafico o figura usando libreria plotly
    fig = go.Figure()
    # Add the normal distribution curve
    # Se agregue la curva de distribución normal
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Distribución Nornal'))
    # Calculate y values for shading under the curve
    # Calcular valores y para sombrear debajo de la curva
    shade_x = np.linspace(sample_mean - z_critical * sem_corrected, sample_mean + z_critical * sem_corrected, 100)
    shade_y = norm.pdf(shade_x, sample_mean, sem_corrected)
    # Add shaded area for the confidence interval
    fig.add_trace(go.Scatter(x=np.concatenate([shade_x, shade_x[::-1]]),
                            y=np.concatenate([shade_y, np.zeros_like(shade_x)]),
                            fill='toself', fillcolor='rgba(0,100,80,0.3)',
                            line=dict(color='rgba(255,255,255,0)'), name='Intervalo de confianza',
                            hoverinfo="skip"))

    # Add markers for sample mean and confidence interval boundaries
    fig.add_trace(go.Scatter(x=[sample_mean], y=[norm.pdf(sample_mean, sample_mean, sem_corrected)], mode='markers',
                            marker=dict(color='red', size=10), name='Media de la muestra'))
    fig.add_trace(go.Scatter(x=[lower_bound_mean, upper_bound_mean],
                            y=[norm.pdf(lower_bound_mean, sample_mean, sem_corrected), norm.pdf(upper_bound_mean, sample_mean, sem_corrected)],
                            mode='markers', marker=dict(color='green', size=10), name='Límites del IC'))

    # Update layout
    fig.update_layout(title='Distribución normal con intervalo de confianza',
                    xaxis_title='Bitocoin/1000',
                    yaxis_title='Densidad de probabilidad',
                    showlegend=True,
                    )  
    
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    # cambio de tamaño de legra en el st.metrics-------------------
    st.markdown(
        """
    <style>
    [data-testid="stMetricValue"] {
        font-size: 20px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    ) 
    c1,c2,c3,c4=st.columns(4)
    with c1:
        st.info("Media de la muestra", icon="📊")
        st.metric(label="valor", value=f"{(sample_mean*1000):,.2f}", border=True)
    with c2:
        st.info('Desv. Estándar de la muestra', icon="📊")
        st.metric(label="valor", value=f"{(sample_std*1000):,.2f}", border=True)
    with c3:
        st.info('Tamaño de la población (N)', icon="📊")
        st.metric(label="valor", value=f"{N}", border=True)
    with c4:
        st.info('FPCF (Factor Corrección de Población Finita) Aplicado', icon="📊")
        st.metric(label="#", value=f"{'Yes' if fpcf != 1 else 'No'}", border=True)
    
    c1,c2,c3,c4=st.columns(4)
    with c1:
        st.info("Nivel de confianza", icon="📊")
        st.metric(label="valor",value=f"{confidence_level * 100} %", border=True)
    with c2:
        st.info('Interv. de confianza para la media de la población (min/max)', icon="📊")
        st.metric(label="valor", value=f"{(lower_bound_mean*1000):,.2f}/{(upper_bound_mean*1000):,.2f}", border=True)
    with c3:
        st.info('Interv. de confianza para la Desv. ESTD de la población(min/max)', icon="📊")
        st.metric(label="valor", value=f"{(lower_bound_std*1000):,.2f}/{(upper_bound_std*1000):,.2f}", border=True)
    with c4:
        st.info('Error estándar de la media (SEM)', icon="📊")
        st.metric(label="valor",value=f"{(sem):,.2f}", border=True)           
    #st.write("Media de la muestra (Bitcoin):", round(sample_mean, 2)*1000)
    #st.write("Desviación estándar de la muestra (Bitcoin):", round(sample_std, 2)*1000)
    #st.write("Tamaño de la población (N):", N)
    #st.write(f"FPCF (factor de corrección de población finita) Applicado: {'Yes' if fpcf != 1 else 'No'}")
    #st.write(f"Nivel de confianza: {confidence_level * 100}%")
    #st.write("Intervalo de confianza para la media de la población (Bitcoin): (", round(lower_bound_mean, 2)*1000, ",", round(upper_bound_mean, 2)*1000, ")")
    #st.write("Intervalo de confianza para la desviación estándar de la población (Bitcoin): (", round(lower_bound_std, 2)*1000, ",", round(upper_bound_std, 2)*1000, ")")
    #st.write("Error estándar de la media (SEM):", round(sem, 2))

    # ---- Descripcion de intervalos de confianza del rendimiento ----

    st.write("---")
    st.subheader(f"Intervalos de confianza para el rendimiento  {option} (diario)")
    
   # Sample statistics / estadistica de muestra
    n = len(rbit)
    sample_mean = np.mean(rbit)
    sample_std = np.std(rbit, ddof=1)  # Use ddof=1 for sample standard deviation / Utilice ddof=1 para la desviación estándar de la muestra
    # Population size / tamaño de la poblacion
    N = 5000
    # Confidence level / nivel de confianza 
    confidence_level = 0.95
    alpha = 1 - confidence_level
    # Check if FPCF should be applied / hay que verificar si debe aplicar FPCF (factor de corrección de población finita)
    # se utiliza cuando se toma una muestra sin reemplazo de más del 5% de una población
    fpcf = 1  # Default value (no correction) / Valor predeterminado (sin corrección)
    if n / N >= 0.05:
        fpcf = np.sqrt((N - n) / (N - 1))
    # Confidence interval for population mean / Intervalo de confianza para la media de la población
    sem = sample_std / np.sqrt(n)  # Standard error of the mean / Error estándar de la media
    sem_corrected = sem * fpcf  # Apply FPCF if necessary / se aplica FPCF si es necesario
    z_critical = norm.ppf(1 - alpha / 2)  # Critical z-value for two-tailed test / Valor z crítico para la prueba de dos colas
    margin_of_error_mean = z_critical * sem_corrected
    lower_bound_mean = sample_mean - margin_of_error_mean
    upper_bound_mean = sample_mean + margin_of_error_mean
    # calculo 
    # Confidence interval for population standard deviation
    # Intervalo de confianza para la desviación estándar de la población
    df_degrees = n - 1
    chi2_lower = chi2.ppf(alpha / 2, df_degrees)
    chi2_upper = chi2.ppf(1 - alpha / 2, df_degrees)
    lower_bound_std = np.sqrt((df_degrees * sample_std ** 2) / chi2_upper)
    upper_bound_std = np.sqrt((df_degrees * sample_std ** 2) / chi2_lower)
    # Define the normal distribution parameters
    # Defina los parámetros de distribución normal
    x = np.linspace(sample_mean - 4 * sem_corrected, sample_mean + 4 * sem_corrected, 1000)
    y = norm.pdf(x, sample_mean, sem_corrected)
    
    # Create figure using Plotly
    # se genera el grafico o figura usando libreria plotly
    fig1 = go.Figure()

    # Add the normal distribution curve
    # Se agregue la curva de distribución normal
    fig1.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Distribución Nornal'))

    # Calculate y values for shading under the curve
    # Calcular valores y para sombrear debajo de la curva

    shade_x = np.linspace(sample_mean - z_critical * sem_corrected, sample_mean + z_critical * sem_corrected, 100)
    shade_y = norm.pdf(shade_x, sample_mean, sem_corrected)

    # Add shaded area for the confidence interval
    fig1.add_trace(go.Scatter(x=np.concatenate([shade_x, shade_x[::-1]]),
                            y=np.concatenate([shade_y, np.zeros_like(shade_x)]),
                            fill='toself', fillcolor='rgba(0,100,80,0.3)',
                            line=dict(color='rgba(255,255,255,0)'), name='Intervalo de confianza',
                            hoverinfo="skip"))

    # Add markers for sample mean and confidence interval boundaries
    fig1.add_trace(go.Scatter(x=[sample_mean], y=[norm.pdf(sample_mean, sample_mean, sem_corrected)], mode='markers',
                            marker=dict(color='red', size=10), name='Media de la muestra'))
    fig1.add_trace(go.Scatter(x=[lower_bound_mean, upper_bound_mean],
                            y=[norm.pdf(lower_bound_mean, sample_mean, sem_corrected), norm.pdf(upper_bound_mean, sample_mean, sem_corrected)],
                            mode='markers', marker=dict(color='green', size=10), name='Límites del IC'))

    # Update layout
    fig1.update_layout(title='Distribución normal con intervalo de confianza',
                    xaxis_title='Rendimiento Bitocoin',
                    yaxis_title='Densidad de probabilidad',
                    showlegend=True,
                    )  
    
    #st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
    
    st.plotly_chart(fig1, use_container_width=True)
    # cambio de tamaño de legra en el st.metrics-------------------
    st.markdown(
        """
    <style>
    [data-testid="stMetricValue"] {
        font-size: 20px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    ) 
    c1,c2,c3,c4=st.columns(4)
    with c1:
        st.info("Media de la muestra", icon="📊")
        st.metric(label="valor", value=f"{(sample_mean*1000):,.2f}", border=True)
    with c2:
        st.info('Desv. Estándar de la muestra', icon="📊")
        st.metric(label="valor", value=f"{(sample_std*1000):,.2f}", border=True)
    with c3:
        st.info('Tamaño de la población (N)', icon="📊")
        st.metric(label="valor", value=f"{N}", border=True)
    with c4:
        st.info('FPCF (Factor Corrección de Población Finita) Aplicado', icon="📊")
        st.metric(label="#", value=f"{'Yes' if fpcf != 1 else 'No'}", border=True)
    
    c1,c2,c3,c4=st.columns(4)
    with c1:
        st.info("Nivel de confianza", icon="📊")
        st.metric(label="valor",value=f"{confidence_level * 100} %", border=True)
    with c2:
        st.info('Interv. de confianza para la media de la población (min/max)', icon="📊")
        st.metric(label="valor", value=f"{(lower_bound_mean*1000):,.2f}/{(upper_bound_mean*1000):,.2f}", border=True)
    with c3:
        st.info('Interv. de confianza para la Desv. ESTD de la población (min/max)', icon="📊")
        st.metric(label="valor", value=f"{(lower_bound_std*1000):,.2f}/{(upper_bound_std*1000):,.2f}", border=True)
    with c4:
        st.info('Error estándar de la media(SEM)', icon="📊")
        st.metric(label="valor",value=f"{(sem):,.2f}", border=True)                 
    #st.write("Media de la muestra (Rend.Bitcoin):", round(sample_mean, 2)*100)
    #st.write("Desviación estándar de la muestra (Rend.Bitcoin):", round(sample_std, 2)*100)
    #st.write("Tamaño de la población (N):", N)
    #st.write(f"FPCF (factor de corrección de población finita) Applicado: {'Yes' if fpcf != 1 else 'No'}")
    #st.write(f"Nivel de confianza: {confidence_level * 100}%")
    #st.write("Intervalo de confianza para la media de la población (rend.Bitcoin): (", round(lower_bound_mean, 2)*100, ",", round(upper_bound_mean, 2)*100, ")")
    #st.write("Intervalo de confianza para la desviación estándar de la población (rend.Bitcoin): (", round(lower_bound_std, 2)*100, ",", round(upper_bound_std, 2)*100, ")")
    #st.write("Error estándar de la media (SEM):", round(sem, 2))


# ---- BLUE ----
elif option == 'BLUE':
    st.subheader(f"Intervalo de confianza diario de : {option} (cotización)")  
    #st.write("---")
    
    # Sample statistics / estadistica de muestra
    n = len(blue)
    sample_mean = np.mean(blue)
    sample_std = np.std(blue, ddof=1)  # Use ddof=1 for sample standard deviation / Utilice ddof=1 para la desviación estándar de la muestra
    # Population size / tamaño de la poblacion
    N = 5000
    # Confidence level / nivel de confianza 
    confidence_level = 0.95
    alpha = 1 - confidence_level
    # Check if FPCF should be applied / hay que verificar si debe aplicar FPCF (factor de corrección de población finita)
    # se utiliza cuando se toma una muestra sin reemplazo de más del 5% de una población
    fpcf = 1  # Default value (no correction) / Valor predeterminado (sin corrección)
    if n / N >= 0.05:
        fpcf = np.sqrt((N - n) / (N - 1))
    # Confidence interval for population mean / Intervalo de confianza para la media de la población
    sem = sample_std / np.sqrt(n)  # Standard error of the mean / Error estándar de la media
    sem_corrected = sem * fpcf  # Apply FPCF if necessary / se aplica FPCF si es necesario
    z_critical = norm.ppf(1 - alpha / 2)  # Critical z-value for two-tailed test / Valor z crítico para la prueba de dos colas
    margin_of_error_mean = z_critical * sem_corrected
    lower_bound_mean = sample_mean - margin_of_error_mean
    upper_bound_mean = sample_mean + margin_of_error_mean
    # calculo 
    # Confidence interval for population standard deviation
    # Intervalo de confianza para la desviación estándar de la población
    df_degrees = n - 1
    chi2_lower = chi2.ppf(alpha / 2, df_degrees)
    chi2_upper = chi2.ppf(1 - alpha / 2, df_degrees)
    lower_bound_std = np.sqrt((df_degrees * sample_std ** 2) / chi2_upper)
    upper_bound_std = np.sqrt((df_degrees * sample_std ** 2) / chi2_lower)
    # Define the normal distribution parameters
    # Defina los parámetros de distribución normal
    x = np.linspace(sample_mean - 4 * sem_corrected, sample_mean + 4 * sem_corrected, 1000)
    y = norm.pdf(x, sample_mean, sem_corrected)    
    # Create figure using Plotly
    # se genera el grafico o figura usando libreria plotly
    fig = go.Figure()
    # Add the normal distribution curve
    # Se agregue la curva de distribución normal
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Distribución Nornal'))
    # Calculate y values for shading under the curve
    # Calcular valores y para sombrear debajo de la curva
    shade_x = np.linspace(sample_mean - z_critical * sem_corrected, sample_mean + z_critical * sem_corrected, 100)
    shade_y = norm.pdf(shade_x, sample_mean, sem_corrected)
    # Add shaded area for the confidence interval
    fig.add_trace(go.Scatter(x=np.concatenate([shade_x, shade_x[::-1]]),
                            y=np.concatenate([shade_y, np.zeros_like(shade_x)]),
                            fill='toself', fillcolor='rgba(0,100,80,0.3)',
                            line=dict(color='rgba(255,255,255,0)'), name='Intervalo de confianza',
                            hoverinfo="skip"))

    # Add markers for sample mean and confidence interval boundaries
    fig.add_trace(go.Scatter(x=[sample_mean], y=[norm.pdf(sample_mean, sample_mean, sem_corrected)], mode='markers',
                            marker=dict(color='red', size=10), name='Media de la muestra'))
    fig.add_trace(go.Scatter(x=[lower_bound_mean, upper_bound_mean],
                            y=[norm.pdf(lower_bound_mean, sample_mean, sem_corrected), norm.pdf(upper_bound_mean, sample_mean, sem_corrected)],
                            mode='markers', marker=dict(color='green', size=10), name='Límites del IC'))

    # Update layout
    fig.update_layout(title='Distribución normal con intervalo de confianza',
                    xaxis_title='Blue',
                    yaxis_title='Densidad de probabilidad',
                    showlegend=True,
                    )  
    
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    # cambio de tamaño de legra en el st.metrics-------------------
    st.markdown(
        """
    <style>
    [data-testid="stMetricValue"] {
        font-size: 20px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    ) 
    c1,c2,c3,c4=st.columns(4)
    with c1:
        st.info("Media de la muestra", icon="📊")
        st.metric(label="valor", value=f"{(sample_mean):,.2f}", border=True)
    with c2:
        st.info('Desv. Estándar de la muestra', icon="📊")
        st.metric(label="valor", value=f"{(sample_std):,.2f}", border=True)
    with c3:
        st.info('Tamaño de la población (N)', icon="📊")
        st.metric(label="valor", value=f"{N}", border=True)
    with c4:
        st.info('FPCF (Factor Corrección de Población Finita) Aplicado', icon="📊")
        st.metric(label="#", value=f"{'Yes' if fpcf != 1 else 'No'}", border=True)
    
    c1,c2,c3,c4=st.columns(4)
    with c1:
        st.info("Nivel de confianza", icon="📊")
        st.metric(label="valor",value=f"{confidence_level * 100} %", border=True)
    with c2:
        st.info('Interv. de confianza para la media de la población (min/max)', icon="📊")
        st.metric(label="valor", value=f"{(lower_bound_mean):,.2f}/{(upper_bound_mean):,.2f}", border=True)
    with c3:
        st.info('Interv. de confianza para la Desv. ESTD de la población (min/max)', icon="📊")
        st.metric(label="valor", value=f"{(lower_bound_std):,.2f}/{(upper_bound_std):,.2f}", border=True)
    with c4:
        st.info('Error estándar de la media(SEM)', icon="📊")
        st.metric(label="valor",value=f"{(sem):,.2f}", border=True )   
    
    #st.write("Media de la muestra (Blue):", round(sample_mean, 2))
    #st.write("Desviación estándar de la muestra (Blue):", round(sample_std, 2))
    #st.write("Tamaño de la población (N):", N)
    #st.write(f"FPCF (factor de corrección de población finita) Applicado: {'Yes' if fpcf != 1 else 'No'}")
    #st.write(f"Nivel de confianza: {confidence_level * 100}%")
    #st.write("Intervalo de confianza para la media de la población (Blue): (", round(lower_bound_mean, 2), ",", round(upper_bound_mean, 2), ")")
    #st.write("Intervalo de confianza para la desviación estándar de la población (Blue): (", round(lower_bound_std, 2), ",", round(upper_bound_std, 2), ")")
    #st.write("Error estándar de la media (SEM):", round(sem, 2))

    # ---- Descripcion de intervalos de confianza del rendimiento ----
    st.write("---")
    st.subheader(f"Intervalos de confianza para el rendimiento  {option} (diario)")
    
   # Sample statistics / estadistica de muestra
    n = len(rblue)
    sample_mean = np.mean(rblue)
    sample_std = np.std(rblue, ddof=1)  # Use ddof=1 for sample standard deviation / Utilice ddof=1 para la desviación estándar de la muestra
    # Population size / tamaño de la poblacion
    N = 5000
    # Confidence level / nivel de confianza 
    confidence_level = 0.95
    alpha = 1 - confidence_level
    # Check if FPCF should be applied / hay que verificar si debe aplicar FPCF (factor de corrección de población finita)
    # se utiliza cuando se toma una muestra sin reemplazo de más del 5% de una población
    fpcf = 1  # Default value (no correction) / Valor predeterminado (sin corrección)
    if n / N >= 0.05:
        fpcf = np.sqrt((N - n) / (N - 1))
    # Confidence interval for population mean / Intervalo de confianza para la media de la población
    sem = sample_std / np.sqrt(n)  # Standard error of the mean / Error estándar de la media
    sem_corrected = sem * fpcf  # Apply FPCF if necessary / se aplica FPCF si es necesario
    z_critical = norm.ppf(1 - alpha / 2)  # Critical z-value for two-tailed test / Valor z crítico para la prueba de dos colas
    margin_of_error_mean = z_critical * sem_corrected
    lower_bound_mean = sample_mean - margin_of_error_mean
    upper_bound_mean = sample_mean + margin_of_error_mean
    # calculo 
    # Confidence interval for population standard deviation
    # Intervalo de confianza para la desviación estándar de la población
    df_degrees = n - 1
    chi2_lower = chi2.ppf(alpha / 2, df_degrees)
    chi2_upper = chi2.ppf(1 - alpha / 2, df_degrees)
    lower_bound_std = np.sqrt((df_degrees * sample_std ** 2) / chi2_upper)
    upper_bound_std = np.sqrt((df_degrees * sample_std ** 2) / chi2_lower)
    # Define the normal distribution parameters
    # Defina los parámetros de distribución normal
    x = np.linspace(sample_mean - 4 * sem_corrected, sample_mean + 4 * sem_corrected, 1000)
    y = norm.pdf(x, sample_mean, sem_corrected)
    
    # Create figure using Plotly
    # se genera el grafico o figura usando libreria plotly
    fig1 = go.Figure()

    # Add the normal distribution curve
    # Se agregue la curva de distribución normal
    fig1.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Distribución Nornal'))

    # Calculate y values for shading under the curve
    # Calcular valores y para sombrear debajo de la curva

    shade_x = np.linspace(sample_mean - z_critical * sem_corrected, sample_mean + z_critical * sem_corrected, 100)
    shade_y = norm.pdf(shade_x, sample_mean, sem_corrected)

    # Add shaded area for the confidence interval
    fig1.add_trace(go.Scatter(x=np.concatenate([shade_x, shade_x[::-1]]),
                            y=np.concatenate([shade_y, np.zeros_like(shade_x)]),
                            fill='toself', fillcolor='rgba(0,100,80,0.3)',
                            line=dict(color='rgba(255,255,255,0)'), name='Intervalo de confianza',
                            hoverinfo="skip"))

    # Add markers for sample mean and confidence interval boundaries
    fig1.add_trace(go.Scatter(x=[sample_mean], y=[norm.pdf(sample_mean, sample_mean, sem_corrected)], mode='markers',
                            marker=dict(color='red', size=10), name='Media de la muestra'))
    fig1.add_trace(go.Scatter(x=[lower_bound_mean, upper_bound_mean],
                            y=[norm.pdf(lower_bound_mean, sample_mean, sem_corrected), norm.pdf(upper_bound_mean, sample_mean, sem_corrected)],
                            mode='markers', marker=dict(color='green', size=10), name='Límites del IC'))

    # Update layout
    fig1.update_layout(title='Distribución normal con intervalo de confianza',
                    xaxis_title='Rend. Blue',
                    yaxis_title='Densidad de probabilidad',
                    showlegend=True,
                    )  
    
    #st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
    
    st.plotly_chart(fig1, use_container_width=True)
    
    st.markdown(
        """
    <style>
    [data-testid="stMetricValue"] {
        font-size: 20px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    ) 
    c1,c2,c3,c4=st.columns(4)
    with c1:
        st.info("Media de la muestra", icon="📊")
        st.metric(label="valor", value=f"{(sample_mean*1000):,.2f}", border=True)
    with c2:
        st.info('Desv. Estándar de la muestra', icon="📊")
        st.metric(label="valor", value=f"{(sample_std*1000):,.2f}", border=True)
    with c3:
        st.info('Tamaño de la población (N)', icon="📊")
        st.metric(label="valor", value=f"{N}", border=True)
    with c4:
        st.info('FPCF (Factor Corrección de Población Finita) Aplicado', icon="📊")
        st.metric(label="#", value=f"{'Yes' if fpcf != 1 else 'No'}", border=True)
    
    c1,c2,c3,c4=st.columns(4)
    with c1:
        st.info("Nivel de confianza", icon="📊")
        st.metric(label="valor",value=f"{confidence_level * 100} %", border=True)
    with c2:
        st.info('Interv. de confianza para la media de la población (min/max)', icon="📊")
        st.metric(label="valor", value=f"{(lower_bound_mean):,.2f}/{(upper_bound_mean):,.2f}", border=True)
    with c3:
        st.info('Interv. de confianza para la Desv. ESTD de la población (min/max)', icon="📊")
        st.metric(label="valor", value=f"{(lower_bound_std):,.2f}/{(upper_bound_std):,.2f}", border=True)
    with c4:
        st.info('Error estándar de la media(SEM)', icon="📊")
        st.metric(label="valor",value=f"{(sem):,.2f}", border=True)
    
    #st.write("Media de la muestra (Rend.Blue):", round(sample_mean, 2)*100)
    #st.write("Desviación estándar de la muestra (Rend.Blue):", round(sample_std, 2)*100)
    #st.write("Tamaño de la población (N):", N)
    #st.write(f"FPCF (factor de corrección de población finita) Applicado: {'Yes' if fpcf != 1 else 'No'}")
    #st.write(f"Nivel de confianza: {confidence_level * 100}%")
    #st.write("Intervalo de confianza para la media de la población (rend.Blue): (", round(lower_bound_mean, 2)*100, ",", round(upper_bound_mean, 2)*100, ")")
    #st.write("Intervalo de confianza para la desviación estándar de la población (rend.Blue): (", round(lower_bound_std, 2)*100, ",", round(upper_bound_std, 2)*100, ")")
    #st.write("Error estándar de la media (SEM):", round(sem, 2))
     
   
   
# ----  INDICE MERVAL ----
elif option == 'MERV':
    st.subheader(f"Intervalo de confianza diario de : {option} (cotización)")  
    #st.write("---")
    
    # Sample statistics / estadistica de muestra
    n = len(merv)
    sample_mean = np.mean(merv)
    sample_std = np.std(merv, ddof=1)  # Use ddof=1 for sample standard deviation / Utilice ddof=1 para la desviación estándar de la muestra
    # Population size / tamaño de la poblacion
    N = 5000
    # Confidence level / nivel de confianza 
    confidence_level = 0.95
    alpha = 1 - confidence_level
    # Check if FPCF should be applied / hay que verificar si debe aplicar FPCF (factor de corrección de población finita)
    # se utiliza cuando se toma una muestra sin reemplazo de más del 5% de una población
    fpcf = 1  # Default value (no correction) / Valor predeterminado (sin corrección)
    if n / N >= 0.05:
        fpcf = np.sqrt((N - n) / (N - 1))
    # Confidence interval for population mean / Intervalo de confianza para la media de la población
    sem = sample_std / np.sqrt(n)  # Standard error of the mean / Error estándar de la media
    sem_corrected = sem * fpcf  # Apply FPCF if necessary / se aplica FPCF si es necesario
    z_critical = norm.ppf(1 - alpha / 2)  # Critical z-value for two-tailed test / Valor z crítico para la prueba de dos colas
    margin_of_error_mean = z_critical * sem_corrected
    lower_bound_mean = sample_mean - margin_of_error_mean
    upper_bound_mean = sample_mean + margin_of_error_mean
    # calculo 
    # Confidence interval for population standard deviation
    # Intervalo de confianza para la desviación estándar de la población
    df_degrees = n - 1
    chi2_lower = chi2.ppf(alpha / 2, df_degrees)
    chi2_upper = chi2.ppf(1 - alpha / 2, df_degrees)
    lower_bound_std = np.sqrt((df_degrees * sample_std ** 2) / chi2_upper)
    upper_bound_std = np.sqrt((df_degrees * sample_std ** 2) / chi2_lower)
    # Define the normal distribution parameters
    # Defina los parámetros de distribución normal
    x = np.linspace(sample_mean - 4 * sem_corrected, sample_mean + 4 * sem_corrected, 1000)
    y = norm.pdf(x, sample_mean, sem_corrected)    
    # Create figure using Plotly
    # se genera el grafico o figura usando libreria plotly
    fig = go.Figure()
    # Add the normal distribution curve
    # Se agregue la curva de distribución normal
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Distribución Nornal'))
    # Calculate y values for shading under the curve
    # Calcular valores y para sombrear debajo de la curva
    shade_x = np.linspace(sample_mean - z_critical * sem_corrected, sample_mean + z_critical * sem_corrected, 100)
    shade_y = norm.pdf(shade_x, sample_mean, sem_corrected)
    # Add shaded area for the confidence interval
    fig.add_trace(go.Scatter(x=np.concatenate([shade_x, shade_x[::-1]]),
                            y=np.concatenate([shade_y, np.zeros_like(shade_x)]),
                            fill='toself', fillcolor='rgba(0,100,80,0.3)',
                            line=dict(color='rgba(255,255,255,0)'), name='Intervalo de confianza',
                            hoverinfo="skip"))

    # Add markers for sample mean and confidence interval boundaries
    fig.add_trace(go.Scatter(x=[sample_mean], y=[norm.pdf(sample_mean, sample_mean, sem_corrected)], mode='markers',
                            marker=dict(color='red', size=10), name='Media de la muestra'))
    fig.add_trace(go.Scatter(x=[lower_bound_mean, upper_bound_mean],
                            y=[norm.pdf(lower_bound_mean, sample_mean, sem_corrected), norm.pdf(upper_bound_mean, sample_mean, sem_corrected)],
                            mode='markers', marker=dict(color='green', size=10), name='Límites del IC'))

    # Update layout
    fig.update_layout(title='Distribución normal con intervalo de confianza',
                    xaxis_title='Indice Merval/1000',
                    yaxis_title='Densidad de probabilidad',
                    showlegend=True,
                    )  
    
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    st.markdown(
        """
    <style>
    [data-testid="stMetricValue"] {
        font-size: 20px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    ) 
    c1,c2,c3,c4=st.columns(4)
    with c1:
        st.info("Media de la muestra", icon="📊")
        st.metric(label="valor", value=f"{(sample_mean*1000):,.2f}", border=True)
    with c2:
        st.info('Desv. Estándar de la muestra', icon="📊")
        st.metric(label="valor", value=f"{(sample_std*1000):,.2f}", border=True)
    with c3:
        st.info('Tamaño de la población (N)', icon="📊")
        st.metric(label="valor", value=f"{N}", border=True)
    with c4:
        st.info('FPCF (Factor Corrección de Población Finita) Aplicado', icon="📊")
        st.metric(label="#", value=f"{'Yes' if fpcf != 1 else 'No'}", border=True)
    
    c1,c2,c3,c4=st.columns(4)
    with c1:
        st.info("Nivel de confianza", icon="📊")
        st.metric(label="valor",value=f"{confidence_level * 100} %", border=True)
    with c2:
        st.info('Interv. de confianza para la media de la población (min/max)', icon="📊")
        st.metric(label="valor", value=f"{(lower_bound_mean*1000):,.2f}/{(upper_bound_mean*1000):,.2f}", border=True)
    with c3:
        st.info('Interv. de confianza para la Desv. ESTD de la población (min/max)', icon="📊")
        st.metric(label="valor", value=f"{(lower_bound_std*1000):,.2f}/{(upper_bound_std*1000):,.2f}", border=True)
    with c4:
        st.info('Error estándar de la media(SEM)', icon="📊")
        st.metric(label="valor",value=f"{(sem):,.2f}", border=True)
    
    #st.write("Media de la muestra (Merval):", round(sample_mean, 2)*1000)
    #st.write("Desviación estándar de la muestra (Merval):", round(sample_std, 2)*1000)
    #st.write("Tamaño de la población (N):", N)
    #st.write(f"FPCF (factor de corrección de población finita) Applicado: {'Yes' if fpcf != 1 else 'No'}")
    #st.write(f"Nivel de confianza: {confidence_level * 100}%")
    #st.write("Intervalo de confianza para la media de la población (Merval): (", round(lower_bound_mean, 2)*1000, ",", round(upper_bound_mean, 2)*1000, ")")
    #st.write("Intervalo de confianza para la desviación estándar de la población (Merval): (", round(lower_bound_std, 2)*1000, ",", round(upper_bound_std, 2)*1000, ")")
    #st.write("Error estándar de la media (SEM):", round(sem, 2))

    # ---- Descripcion de intervalos de confianza del rendimiento ----
    st.write("---")
    st.subheader(f"Intervalos de confianza para el rendimiento  {option} (diario)")
    
   # Sample statistics / estadistica de muestra
    n = len(rblue)
    sample_mean = np.mean(rmerv)
    sample_std = np.std(rmerv, ddof=1)  # Use ddof=1 for sample standard deviation / Utilice ddof=1 para la desviación estándar de la muestra
    # Population size / tamaño de la poblacion
    N = 5000
    # Confidence level / nivel de confianza 
    confidence_level = 0.95
    alpha = 1 - confidence_level
    # Check if FPCF should be applied / hay que verificar si debe aplicar FPCF (factor de corrección de población finita)
    # se utiliza cuando se toma una muestra sin reemplazo de más del 5% de una población
    fpcf = 1  # Default value (no correction) / Valor predeterminado (sin corrección)
    if n / N >= 0.05:
        fpcf = np.sqrt((N - n) / (N - 1))
    # Confidence interval for population mean / Intervalo de confianza para la media de la población
    sem = sample_std / np.sqrt(n)  # Standard error of the mean / Error estándar de la media
    sem_corrected = sem * fpcf  # Apply FPCF if necessary / se aplica FPCF si es necesario
    z_critical = norm.ppf(1 - alpha / 2)  # Critical z-value for two-tailed test / Valor z crítico para la prueba de dos colas
    margin_of_error_mean = z_critical * sem_corrected
    lower_bound_mean = sample_mean - margin_of_error_mean
    upper_bound_mean = sample_mean + margin_of_error_mean
    # calculo 
    # Confidence interval for population standard deviation
    # Intervalo de confianza para la desviación estándar de la población
    df_degrees = n - 1
    chi2_lower = chi2.ppf(alpha / 2, df_degrees)
    chi2_upper = chi2.ppf(1 - alpha / 2, df_degrees)
    lower_bound_std = np.sqrt((df_degrees * sample_std ** 2) / chi2_upper)
    upper_bound_std = np.sqrt((df_degrees * sample_std ** 2) / chi2_lower)
    # Define the normal distribution parameters
    # Defina los parámetros de distribución normal
    x = np.linspace(sample_mean - 4 * sem_corrected, sample_mean + 4 * sem_corrected, 1000)
    y = norm.pdf(x, sample_mean, sem_corrected)
    
    # Create figure using Plotly
    # se genera el grafico o figura usando libreria plotly
    fig1 = go.Figure()

    # Add the normal distribution curve
    # Se agregue la curva de distribución normal
    fig1.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Distribución Nornal'))

    # Calculate y values for shading under the curve
    # Calcular valores y para sombrear debajo de la curva

    shade_x = np.linspace(sample_mean - z_critical * sem_corrected, sample_mean + z_critical * sem_corrected, 100)
    shade_y = norm.pdf(shade_x, sample_mean, sem_corrected)

    # Add shaded area for the confidence interval
    fig1.add_trace(go.Scatter(x=np.concatenate([shade_x, shade_x[::-1]]),
                            y=np.concatenate([shade_y, np.zeros_like(shade_x)]),
                            fill='toself', fillcolor='rgba(0,100,80,0.3)',
                            line=dict(color='rgba(255,255,255,0)'), name='Intervalo de confianza',
                            hoverinfo="skip"))

    # Add markers for sample mean and confidence interval boundaries
    fig1.add_trace(go.Scatter(x=[sample_mean], y=[norm.pdf(sample_mean, sample_mean, sem_corrected)], mode='markers',
                            marker=dict(color='red', size=10), name='Media de la muestra'))
    fig1.add_trace(go.Scatter(x=[lower_bound_mean, upper_bound_mean],
                            y=[norm.pdf(lower_bound_mean, sample_mean, sem_corrected), norm.pdf(upper_bound_mean, sample_mean, sem_corrected)],
                            mode='markers', marker=dict(color='green', size=10), name='Límites del IC'))

    # Update layout
    fig1.update_layout(title='Distribución normal con intervalo de confianza',
                    xaxis_title='Rend. Merval',
                    yaxis_title='Densidad de probabilidad',
                    showlegend=True,
                    )  
    
    #st.plotly_chart(fig1, theme="streamlit", use_container_width=True)    
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown(
        """
    <style>
    [data-testid="stMetricValue"] {
        font-size: 15px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    ) 
    c1,c2,c3,c4=st.columns(4)
    with c1:
        st.info("Media de la muestra", icon="📊")
        st.metric(label="valor", value=f"{(sample_mean*1000):,.2f}", border=True)
    with c2:
        st.info('Desv. Estándar de la muestra', icon="📊")
        st.metric(label="valor", value=f"{(sample_std*1000):,.2f}", border=True)
    with c3:
        st.info('Tamaño de la población (N)', icon="📊")
        st.metric(label="valor", value=f"{N}", border=True)
    with c4:
        st.info('FPCF (Factor Corrección de Población Finita) Aplicado', icon="📊")
        st.metric(label="#", value=f"{'Yes' if fpcf != 1 else 'No'}", border=True)
    
    c1,c2,c3,c4=st.columns(4)
    with c1:
        st.info("Nivel de confianza", icon="📊")
        st.metric(label="valor",value=f"{confidence_level * 100} %", border=True)
    with c2:
        st.info('Interv. de confianza para la media de la población (min/max)', icon="📊")
        st.metric(label="valor", value=f"{(lower_bound_mean*1000):,.2f}/{(upper_bound_mean*1000):,.2f}", border=True)
    with c3:
        st.info('Interv. de confianza para la Desv. ESTD de la población (min/max)', icon="📊")
        st.metric(label="valor", value=f"{(lower_bound_std*1000):,.2f}/{(upper_bound_std*1000):,.2f}", border=True)
    with c4:
        st.info('Error estándar de la media(SEM)', icon="📊")
        st.metric(label="valor",value=f"{(sem):,.2f}", border=True)
    
    #st.write("Media de la muestra (Rend.Merval):", round(sample_mean, 2)*100)
    #st.write("Desviación estándar de la muestra (Rend.Merval):", round(sample_std, 2))
    #st.write("Tamaño de la población (N):", N)
    #st.write(f"FPCF (factor de corrección de población finita) Applicado: {'Yes' if fpcf != 1 else 'No'}")
    #st.write(f"Nivel de confianza: {confidence_level * 100}%")
    #st.write("Intervalo de confianza para la media de la población (rend.Merval): (", round(lower_bound_mean, 2)*100, ",", round(upper_bound_mean, 2)*100, ")")
    #st.write("Intervalo de confianza para la desviación estándar de la población (rend.Merval): (", round(lower_bound_std, 2)*100, ",", round(upper_bound_std, 2)*100, ")")
    #st.write("Error estándar de la media (SEM):", round(sem, 2))

# ----  AL30D ----
elif option == 'AL30D':
    st.subheader(f"Intervalo de confianza diario de : {option} (cotización)")  
    #st.write("---")
    
    # Sample statistics / estadistica de muestra
    n = len(al30d)
    sample_mean = np.mean(al30d)
    sample_std = np.std(al30d, ddof=1)  # Use ddof=1 for sample standard deviation / Utilice ddof=1 para la desviación estándar de la muestra
    # Population size / tamaño de la poblacion
    N = 5000
    # Confidence level / nivel de confianza 
    confidence_level = 0.95
    alpha = 1 - confidence_level
    # Check if FPCF should be applied / hay que verificar si debe aplicar FPCF (factor de corrección de población finita)
    # se utiliza cuando se toma una muestra sin reemplazo de más del 5% de una población
    fpcf = 1  # Default value (no correction) / Valor predeterminado (sin corrección)
    if n / N >= 0.05:
        fpcf = np.sqrt((N - n) / (N - 1))
    # Confidence interval for population mean / Intervalo de confianza para la media de la población
    sem = sample_std / np.sqrt(n)  # Standard error of the mean / Error estándar de la media
    sem_corrected = sem * fpcf  # Apply FPCF if necessary / se aplica FPCF si es necesario
    z_critical = norm.ppf(1 - alpha / 2)  # Critical z-value for two-tailed test / Valor z crítico para la prueba de dos colas
    margin_of_error_mean = z_critical * sem_corrected
    lower_bound_mean = sample_mean - margin_of_error_mean
    upper_bound_mean = sample_mean + margin_of_error_mean
    # calculo 
    # Confidence interval for population standard deviation
    # Intervalo de confianza para la desviación estándar de la población
    df_degrees = n - 1
    chi2_lower = chi2.ppf(alpha / 2, df_degrees)
    chi2_upper = chi2.ppf(1 - alpha / 2, df_degrees)
    lower_bound_std = np.sqrt((df_degrees * sample_std ** 2) / chi2_upper)
    upper_bound_std = np.sqrt((df_degrees * sample_std ** 2) / chi2_lower)
    # Define the normal distribution parameters
    # Defina los parámetros de distribución normal
    x = np.linspace(sample_mean - 4 * sem_corrected, sample_mean + 4 * sem_corrected, 1000)
    y = norm.pdf(x, sample_mean, sem_corrected)    
    # Create figure using Plotly
    # se genera el grafico o figura usando libreria plotly
    fig = go.Figure()
    # Add the normal distribution curve
    # Se agregue la curva de distribución normal
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Distribución Nornal'))
    # Calculate y values for shading under the curve
    # Calcular valores y para sombrear debajo de la curva
    shade_x = np.linspace(sample_mean - z_critical * sem_corrected, sample_mean + z_critical * sem_corrected, 100)
    shade_y = norm.pdf(shade_x, sample_mean, sem_corrected)
    # Add shaded area for the confidence interval
    fig.add_trace(go.Scatter(x=np.concatenate([shade_x, shade_x[::-1]]),
                            y=np.concatenate([shade_y, np.zeros_like(shade_x)]),
                            fill='toself', fillcolor='rgba(0,100,80,0.3)',
                            line=dict(color='rgba(255,255,255,0)'), name='Intervalo de confianza',
                            hoverinfo="skip"))

    # Add markers for sample mean and confidence interval boundaries
    fig.add_trace(go.Scatter(x=[sample_mean], y=[norm.pdf(sample_mean, sample_mean, sem_corrected)], mode='markers',
                            marker=dict(color='red', size=10), name='Media de la muestra'))
    fig.add_trace(go.Scatter(x=[lower_bound_mean, upper_bound_mean],
                            y=[norm.pdf(lower_bound_mean, sample_mean, sem_corrected), norm.pdf(upper_bound_mean, sample_mean, sem_corrected)],
                            mode='markers', marker=dict(color='green', size=10), name='Límites del IC'))

    # Update layout
    fig.update_layout(title='Distribución normal con intervalo de confianza',
                    xaxis_title='AL30D',
                    yaxis_title='Densidad de probabilidad',
                    showlegend=True,
                    )  
    
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    # modifico tamaño de letra de st.metrics---------------
    st.markdown(
        """
    <style>
    [data-testid="stMetricValue"] {
        font-size: 20px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )    
    c1,c2,c3,c4=st.columns(4)
    with c1:
        st.info("Media de la muestra", icon="📊")
        st.metric(label="valor", value=f"{(sample_mean):,.2f}", border=True)
    with c2:
        st.info('Desv. Estándar de la muestra', icon="📊")
        st.metric(label="valor", value=f"{(sample_std):,.2f}", border=True)
    with c3:
        st.info('Tamaño de la población (N)', icon="📊")
        st.metric(label="valor", value=f"{N}", border=True)
    with c4:
        st.info('FPCF (Factor Corrección de Población Finita) Aplicado', icon="📊")
        st.metric(label="#", value=f"{'Yes' if fpcf != 1 else 'No'}", border=True)
    
    c1,c2,c3,c4=st.columns(4)
    with c1:
        st.info("Nivel de confianza", icon="📊")
        st.metric(label="valor",value=f"{confidence_level * 100} %", border=True)
    with c2:
        st.info('Interv. de confianza para la media de la población (min/max)', icon="📊")
        st.metric(label="valor", value=f"{(lower_bound_mean):,.2f}/{(upper_bound_mean):,.2f}", border=True)
    with c3:
        st.info('Interv. de confianza para la Desv. ESTD de la población (min/max)', icon="📊")
        st.metric(label="valor", value=f"{(lower_bound_std):,.2f}/{(upper_bound_std):,.2f}", border=True)
    with c4:
        st.info('Error estándar de la media(SEM)', icon="📊")
        st.metric(label="valor",value=f"{(sem):,.2f}", border=True)
    
    #st.write("Media de la muestra (AL30D):", round(sample_mean, 2))
    #st.write("Desviación estándar de la muestra (AL30D):", round(sample_std, 2))
    #st.write("Tamaño de la población (N):", N)
    #st.write(f"FPCF (factor de corrección de población finita) Applicado: {'Yes' if fpcf != 1 else 'No'}")
    #st.write(f"Nivel de confianza: {confidence_level * 100}%")
    #st.write("Intervalo de confianza para la media de la población (AL30D): (", round(lower_bound_mean, 2), ",", round(upper_bound_mean, 2), ")")
    #st.write("Intervalo de confianza para la desviación estándar de la población (AL30D): (", round(lower_bound_std, 2), ",", round(upper_bound_std, 2), ")")
    #st.write("Error estándar de la media (SEM):", round(sem, 2))

    # ---- Descripcion de intervalos de confianza del rendimiento ----
    st.write("---")
    st.subheader(f"Intervalos de confianza para el rendimiento  {option} (diario)")
    
   # Sample statistics / estadistica de muestra
    n = len(ral30d)
    sample_mean = np.mean(ral30d)
    sample_std = np.std(ral30d, ddof=1)  # Use ddof=1 for sample standard deviation / Utilice ddof=1 para la desviación estándar de la muestra
    # Population size / tamaño de la poblacion
    N = 5000
    # Confidence level / nivel de confianza 
    confidence_level = 0.95
    alpha = 1 - confidence_level
    # Check if FPCF should be applied / hay que verificar si debe aplicar FPCF (factor de corrección de población finita)
    # se utiliza cuando se toma una muestra sin reemplazo de más del 5% de una población
    fpcf = 1  # Default value (no correction) / Valor predeterminado (sin corrección)
    if n / N >= 0.05:
        fpcf = np.sqrt((N - n) / (N - 1))
    # Confidence interval for population mean / Intervalo de confianza para la media de la población
    sem = sample_std / np.sqrt(n)  # Standard error of the mean / Error estándar de la media
    sem_corrected = sem * fpcf  # Apply FPCF if necessary / se aplica FPCF si es necesario
    z_critical = norm.ppf(1 - alpha / 2)  # Critical z-value for two-tailed test / Valor z crítico para la prueba de dos colas
    margin_of_error_mean = z_critical * sem_corrected
    lower_bound_mean = sample_mean - margin_of_error_mean
    upper_bound_mean = sample_mean + margin_of_error_mean
    # calculo 
    # Confidence interval for population standard deviation
    # Intervalo de confianza para la desviación estándar de la población
    df_degrees = n - 1
    chi2_lower = chi2.ppf(alpha / 2, df_degrees)
    chi2_upper = chi2.ppf(1 - alpha / 2, df_degrees)
    lower_bound_std = np.sqrt((df_degrees * sample_std ** 2) / chi2_upper)
    upper_bound_std = np.sqrt((df_degrees * sample_std ** 2) / chi2_lower)
    # Define the normal distribution parameters
    # Defina los parámetros de distribución normal
    x = np.linspace(sample_mean - 4 * sem_corrected, sample_mean + 4 * sem_corrected, 1000)
    y = norm.pdf(x, sample_mean, sem_corrected)
    
    # Create figure using Plotly
    # se genera el grafico o figura usando libreria plotly
    fig1 = go.Figure()

    # Add the normal distribution curve
    # Se agregue la curva de distribución normal
    fig1.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Distribución Nornal'))

    # Calculate y values for shading under the curve
    # Calcular valores y para sombrear debajo de la curva

    shade_x = np.linspace(sample_mean - z_critical * sem_corrected, sample_mean + z_critical * sem_corrected, 100)
    shade_y = norm.pdf(shade_x, sample_mean, sem_corrected)

    # Add shaded area for the confidence interval
    fig1.add_trace(go.Scatter(x=np.concatenate([shade_x, shade_x[::-1]]),
                            y=np.concatenate([shade_y, np.zeros_like(shade_x)]),
                            fill='toself', fillcolor='rgba(0,100,80,0.3)',
                            line=dict(color='rgba(255,255,255,0)'), name='Intervalo de confianza',
                            hoverinfo="skip"))

    # Add markers for sample mean and confidence interval boundaries
    fig1.add_trace(go.Scatter(x=[sample_mean], y=[norm.pdf(sample_mean, sample_mean, sem_corrected)], mode='markers',
                            marker=dict(color='red', size=10), name='Media de la muestra'))
    fig1.add_trace(go.Scatter(x=[lower_bound_mean, upper_bound_mean],
                            y=[norm.pdf(lower_bound_mean, sample_mean, sem_corrected), norm.pdf(upper_bound_mean, sample_mean, sem_corrected)],
                            mode='markers', marker=dict(color='green', size=10), name='Límites del IC'))

    # Update layout
    fig1.update_layout(title='Distribución normal con intervalo de confianza',
                    xaxis_title='Rend. AL30D',
                    yaxis_title='Densidad de probabilidad',
                    showlegend=True,
                    )  
    
    #st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
    
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown(
        """
    <style>
    [data-testid="stMetricValue"] {
        font-size: 20px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    c1,c2,c3,c4=st.columns(4)
    with c1:
        st.info("Media de la muestra", icon="📊")
        st.metric(label="valor", value=f"{(sample_mean):,.2f}", border=True)
    with c2:
        st.info('Desv. Estándar de la muestra', icon="📊")
        st.metric(label="valor", value=f"{(sample_std):,.2f}", border=True)
    with c3:
        st.info('Tamaño de la población (N)', icon="📊")
        st.metric(label="valor", value=f"{N}", border=True)
    with c4:
        st.info('FPCF (Factor Corrección de Población Finita) Aplicado', icon="📊")
        st.metric(label="#", value=f"{'Yes' if fpcf != 1 else 'No'}", border=True)
    
    c1,c2,c3,c4=st.columns(4)
    with c1:
        st.info("Nivel de confianza", icon="📊")
        st.metric(label="valor",value=f"{confidence_level * 100} %", border=True)
    with c2:
        st.info('Interv. de confianza para la media de la población (min/max)', icon="📊")
        st.metric(label="valor", value=f"{(lower_bound_mean):,.2f}/{(upper_bound_mean):,.2f}", border=True)
    with c3:
        st.info('Interv. de confianza para la Desv. ESTD de la población (min/max)', icon="📊")
        st.metric(label="valor", value=f"{(lower_bound_std):,.2f}/{(upper_bound_std):,.2f}", border=True)
    with c4:
        st.info('Error estándar de la media(SEM)', icon="📊")
        st.metric(label="valor",value=f"{(sem):,.2f}", border=True)
    
    #st.write("Media de la muestra (Rend.AL30D):", round(sample_mean, 2)*100)
    #st.write("Desviación estándar de la muestra (Rend.AL30D):", round(sample_std, 2))
    #st.write("Tamaño de la población (N):", N)
    #st.write(f"FPCF (factor de corrección de población finita) Applicado: {'Yes' if fpcf != 1 else 'No'}")
    #st.write(f"Nivel de confianza: {confidence_level * 100}%")
    #st.write("Intervalo de confianza para la media de la población (Rend.AL30D): (", round(lower_bound_mean, 2)*100, ",", round(upper_bound_mean, 2)*100, ")")
    #st.write("Intervalo de confianza para la desviación estándar de la población (Rend.AL30D): (", round(lower_bound_std, 2)*100, ",", round(upper_bound_std, 2)*100, ")")
    #st.write("Error estándar de la media (SEM):", round(sem, 2))

    
else:
    st.write("Error, en la opción elegida ")
    
components.html(particles_js, height=90,scrolling=False)    

# ------------------------------ FOOTER -------------------------------------------------   

st.write("---")
with st.container():
  #st.write("---")
  st.write("&copy; - derechos reservados -  2024 -  Walter Gómez - FullStack Developer - Data Science - Business Intelligence")
  #st.write("##")
  left, right = st.columns(2, gap='small', vertical_alignment="bottom")
  with left:
    #st.write('##')
    st.link_button("Mi LinkedIn", "https://www.linkedin.com/in/walter-gomez-fullstack-developer-datascience-businessintelligence-finanzas-python/")
  with right: 
     #st.write('##') 
    st.link_button("Mi Porfolio", "https://walter-portfolio-animado.netlify.app/")
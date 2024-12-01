import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
import plotly.graph_objects as go
import plotly.express as px
import base64
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
    
#---- Descripcion de la pagina primera pagina de evol de variables diario----
df = pd.read_excel('datos/basedatos.xlsx')

dato = pd.DataFrame(df)

#Calculo del dolar CCL como el promedio del CCL de del AL30C y el GD30C
#dato['CCL'] = round(dato['AL30'] /dato['AL30C'],2)
#dato['CCL'] += round(dato['GL30'] /dato['GL30C'],2)
#dato['CCL'] /= 2

#Calculo del dolar MEP como el promedio entre el MEP del AL30D y el GD30D
#dato['MEP'] = round(dato['GL30']  /dato['GL30D'],2)
#dato['MEP'] += round(dato['AL30'] /dato['AL30D'],2)
#dato['MEP'] /= 2
df1= pd.DataFrame()

# ----------- despliegue de la barra de opciones --------------
list_option = ['BITCOIN', 'BLUE', 'MERV', 'AL30D']
option = st.radio("Seleccione una opción : ", (list_option), horizontal=True )
st.subheader(f"Probabilidad de rendimientos diarios de : {option} ")
st.write("---")
# Calcula las variaciones diarias
if option == 'BITCOIN':    
    df1['Daily_Return_bitcoin'] = dato['BITCOIN'].pct_change() * 100
    # Etiqueta las observaciones como 'Up' si la tasa de cambio subió y 'Down' si bajó
    df1['Direction_bitcoin'] = df1['Daily_Return_bitcoin'].apply(lambda x: 1 if x > 0 else 0)

    # Elimina las filas con NaN resultantes de las variaciones diarias
    df1 = df1.dropna()

    # División de datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(df1[['Daily_Return_bitcoin']], df1['Direction_bitcoin'], test_size=0.2, random_state=42)
   
    # Entrenamiento del modelo de Gradient Boosting
    model = GradientBoostingClassifier()
    model.fit(X_train, y_train)

    # Predicciones en el conjunto de prueba
    predictions = model.predict(X_test)

    # Calcula la probabilidad de subida o bajada en el conjunto de prueba
    prob_up = round(sum(predictions) / len(predictions),2)
    prob_down = 1 - prob_up
    
    # Muestra la probabilidad
    st.subheader(f'Probabilidad de suba de {option}: {prob_up:.2%}')
    st.subheader(f'Probabilidad de baja de {option}: {prob_down:.2%}')

    # Grafica la distribución de los rendimientos diarios
    fig = px.histogram(df1, x='Daily_Return_bitcoin', nbins=50, color='Direction_bitcoin',
                        labels={'Daily_Return_blue': 'Rendimiento Diario (%)'},
                        text_auto = True,
                        title=f'Distribución de Rendimientos Diarios del {option}'                    
                    )       
    # Muestra la gráfica histograma de rendimimentos por fecha 
    st.plotly_chart(fig, use_container_width=True)    
    fig1 = px.histogram(df1, x='Daily_Return_bitcoin', nbins=50,
                        histnorm = 'probability density',
                        text_auto = True,
                        labels={'Daily_Return_bitcoin': 'Rendimiento Diario (%)'},
                        title=f'Densidad de Probabilidad Rendimientos Diarios del {option}' 
                    )
                    
    tab1, tab2 = st.tabs(["fondo transparente", "fondo color intenso"])
    with tab1:
                #st.write('se grafica el log a la regresion')
                st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
    with tab2:
                st.plotly_chart(fig1, theme=None, use_container_width=True)
    
    
elif option == 'BLUE':
    df1['Daily_Return_blue'] = dato['BLUE'].pct_change() * 100

    # Etiqueta las observaciones como 'Up' si la tasa de cambio subió y 'Down' si bajó
    df1['Direction_blue'] = df1['Daily_Return_blue'].apply(lambda x: 1 if x > 0 else 0)

    # Elimina las filas con NaN resultantes de las variaciones diarias
    df1 = df1.dropna()

    # División de datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(df1[['Daily_Return_blue']], df1['Direction_blue'], test_size=0.2, random_state=42)

    # Entrenamiento del modelo de Gradient Boosting
    model = GradientBoostingClassifier()
    model.fit(X_train, y_train)

    # Predicciones en el conjunto de prueba
    predictions = model.predict(X_test)

    # Calcula la probabilidad de subida o bajada en el conjunto de prueba
    prob_up = round(sum(predictions) / len(predictions),2)
    prob_down = 1 - prob_up

    # Muestra la probabilidad
    st.subheader(f'Probabilidad de suba de {option}: {prob_up:.2%}')
    st.subheader(f'Probabilidad de baja de {option}: {prob_down:.2%}')

    # Grafica la distribución de los rendimientos diarios
    fig = px.histogram(df1, x='Daily_Return_blue', nbins=50, color='Direction_blue',
                        labels={'Daily_Return_blue': 'Rendimiento Diario (%)'},
                        text_auto = True,
                        title=f'Distribución de Rendimientos Diarios del {option}'                    
                    )       
    # Muestra la gráfica
    st.plotly_chart(fig, theme='streamlit', use_container_width=True)
    fig1 = px.histogram(df1, x='Daily_Return_blue', nbins=50,
                        histnorm = 'probability density',
                        text_auto = True,
                        labels={'Daily_Return_blue': 'Rendimiento Diario (%)'},
                        title=f'Densidad de Probabilidad Rendimientos Diarios del {option}' 
                    )
                    
    tab1, tab2 = st.tabs(["fondo transparente", "fondo color intenso"])
    with tab1:
                #st.write('se grafica el log a la regresion')
                st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
    with tab2:
                st.plotly_chart(fig1, theme=None, use_container_width=True)
elif option == 'MERV':
    df1['Daily_Return_merv'] = dato['MERV'].pct_change() * 100

    # Etiqueta las observaciones como 'Up' si la tasa de cambio subió y 'Down' si bajó
    df1['Direction_merv'] = df1['Daily_Return_merv'].apply(lambda x: 1 if x > 0 else 0)

    # Elimina las filas con NaN resultantes de las variaciones diarias
    df1 = df1.dropna()

    # División de datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(df1[['Daily_Return_merv']], df1['Direction_merv'], test_size=0.2, random_state=42)

    # Entrenamiento del modelo de Gradient Boosting
    model = GradientBoostingClassifier()
    model.fit(X_train, y_train)

    # Predicciones en el conjunto de prueba
    predictions = model.predict(X_test)

    # Calcula la probabilidad de subida o bajada en el conjunto de prueba
    prob_up = round(sum(predictions) / len(predictions),2)
    prob_down = 1 - prob_up

    # Muestra la probabilidad
    st.subheader(f'Probabilidad de suba de {option}: {prob_up:.2%}')
    st.subheader(f'Probabilidad de baja de {option}: {prob_down:.2%}')

    # Grafica la distribución de los rendimientos diarios
    fig = px.histogram(df1, x='Daily_Return_merv', nbins=50, color='Direction_merv',
                        labels={'Daily_Return_merv': 'Rendimiento Diario (%)'},
                        text_auto = True,
                        title=f'Distribución de Rendimientos Diarios del {option}'
                                            
                    )       
    # Muestra la gráfica
    st.plotly_chart(fig, theme='streamlit', use_container_width=True)
    fig1 = px.histogram(df1, x='Daily_Return_merv', nbins=50,
                        histnorm = 'probability density',
                        text_auto = True,
                        labels={'Daily_Return_merv': 'Rendimiento Diario (%)'},
                        title=f'Densidad de Probabilidad Rendimientos Diarios del {option}' 
                    )
                    
    tab1, tab2 = st.tabs(["fondo transparente", "fondo color intenso"])
    with tab1:
                #st.write('se grafica el log a la regresion')
                st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
    with tab2:
                st.plotly_chart(fig1, theme=None, use_container_width=True)
                
elif option == 'AL30D':
    df1['Daily_Return_al30d'] = dato['AL30D'].pct_change() * 100

    # Etiqueta las observaciones como 'Up' si la tasa de cambio subió y 'Down' si bajó
    df1['Direction_al30d'] = df1['Daily_Return_al30d'].apply(lambda x: 1 if x > 0 else 0)

    # Elimina las filas con NaN resultantes de las variaciones diarias
    df1 = df1.dropna()

    # División de datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(df1[['Daily_Return_al30d']], df1['Direction_al30d'], test_size=0.2, random_state=42)

    # Entrenamiento del modelo de Gradient Boosting
    model = GradientBoostingClassifier()
    model.fit(X_train, y_train)

    # Predicciones en el conjunto de prueba
    predictions = model.predict(X_test)

    # Calcula la probabilidad de subida o bajada en el conjunto de prueba
    prob_up = round(sum(predictions) / len(predictions),2)
    prob_down = 1 - prob_up

    # Muestra la probabilidad
    st.subheader(f'Probabilidad de suba de {option}: {prob_up:.2%}')
    st.subheader(f'Probabilidad de baja de {option}: {prob_down:.2%}')

    # Grafica la distribución de los rendimientos diarios
    fig = px.histogram(df1, x='Daily_Return_al30d', nbins=50, color='Direction_al30d',
                        labels={'Daily_Return_al30d': 'Rendimiento Diario (%)'},
                        text_auto = True,
                        title=f'Distribución de Rendimientos Diarios del {option}'
                                            
                    )       
    # Muestra la gráfica
    st.plotly_chart(fig, theme='streamlit', use_container_width=True)
    fig1 = px.histogram(df1, x='Daily_Return_al30d', nbins=50,
                        histnorm = 'probability density',
                        text_auto = True,
                        labels={'Daily_Return_al30d': 'Rendimiento Diario (%)'},
                        title=f'Densidad de Probabilidad Rendimientos Diarios del {option}' 
                    )
                    
    tab1, tab2 = st.tabs(["fondo transparente", "fondo color intenso"])
    with tab1:
                #st.write('se grafica el log a la regresion')
                st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
    with tab2:
                st.plotly_chart(fig1, theme=None, use_container_width=True)
                                
                
else:
    st.write('ERROR, verificar la opción seleccionada...')
 
# ----------------- calculo de correlacion ------------------- 
x = pd.Series(dato['BITCOIN'])
y = pd.Series(dato['MERV'])   
z = pd.Series(dato['AL30D'])   
color ='orange'
xyz= pd.DataFrame({'BITCOIN': x, 'MERV': y, 'AL30D': z })
matrix_corr_per = xyz.corr(method="pearson")
matrix_corr_spear = xyz.corr(method="spearman")
matrix_corr_ken = xyz.corr(method="kendall")
st.markdown('Correlación modelo Pearson')
st.table( matrix_corr_per) 
st.markdown('Correlación modelo Spearman') 
st.table(matrix_corr_spear)  
st.markdown('Correlación modelo Kendall')
st.table(matrix_corr_ken)

with st.container():
    st.write("---")
    st.write("&copy; - derechos reservados -  2024 -  Walter Gómez - FullStack Developer - Data Science - Business Intelligence")
    #st.write("##")  
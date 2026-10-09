import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Validador de Graduandos UAO", page_icon="🎓", layout="centered")

# Estilo visual limpio y institucional
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTextInput > div > div > input { font-size: 20px; }
    </style>
""", unsafe_allow_html=True)

st.title("Validador de Graduandos - UAO")
st.write("Ingrese el número de documento de identidad del graduando para consultar su información y número de ING.")

# Cargar los datos del Excel de forma eficiente
@st.cache_data
def cargar_datos():
    excel_path = "ARCHIVO PARA STICKERS.xlsx"
    df1 = pd.read_excel(excel_path, sheet_name="CEREMONIA 1")
    df1['Ceremonia'] = 'Ceremonia 1'
    
    df2 = pd.read_excel(excel_path, sheet_name="CEREMONIA 2")
    df2['Ceremonia'] = 'Ceremonia 2'
    
    df = pd.concat([df1, df2], ignore_index=True)
    df['Identificación'] = df['Identificación'].astype(str).str.strip()
    return df

try:
    df = cargar_datos()
except Exception as e:
    st.error(f"Error al cargar el archivo de Excel: {e}")
    st.stop()

# Campo de búsqueda por cédula
cedula_ingresada = st.text_input("Número de Cédula o Identificación:", "")

if cedula_ingresada:
    cedula_limpia = cedula_ingresada.strip()
    resultado = df[df['Identificación'] == cedula_limpia]
    
    if resultado.empty:
        st.warning("No se encontró un graduando registrado con este número de documento.")
    else:
        row = resultado.iloc[0]
        st.success("¡Graduando encontrado con éxito!")
        
        # Tarjeta con los resultados grandes y claros
        st.markdown(f"""
        ### Información del Graduando
        - **Nombre Completo:** {row['NOMBRE COMPLETO']}
        - **Programa / Carrera:** {row['Programa']}
        - **Número de ING:** **{row['Unnamed: 3']}**
        - **Ceremonia Asignada:** {row['Ceremonia']}
        """)
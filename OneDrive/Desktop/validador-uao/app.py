from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Nombre exacto del archivo de Excel en tu repositorio
EXCEL_PATH = "ARCHIVO PARA STICKERS.xlsx"

def cargar_datos():
    # Lee ambas hojas del Excel y las combina
    df1 = pd.read_excel(EXCEL_PATH, sheet_name="CEREMONIA 1")
    df1['Ceremonia'] = 'Ceremonia 1'
    
    df2 = pd.read_excel(EXCEL_PATH, sheet_name="CEREMONIA 2")
    df2['Ceremonia'] = 'Ceremonia 2'
    
    df = pd.concat([df1, df2], ignore_index=True)
    
    # Asegura que la cédula se maneje como texto limpio sin espacios
    df['Identificación'] = df['Identificación'].astype(str).str.strip()
    return df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/consultar', methods=['POST'])
def consultar():
    data = request.get_json()
    cedula_ingresada = str(data.get('cedula', '')).strip()
    
    df = cargar_datos()
    
    # Busca la coincidencia exacta en la columna 'Identificación'
    resultado = df[df['Identificación'] == cedula_ingresada]
    
    if resultado.empty:
        return jsonify({"encontrado": False, "mensaje": "No se encontró un graduando registrado con este número de documento."})
    
    row = resultado.iloc[0]
    
    # Extraemos el ING directamente de la columna 'Unnamed: 3' (que contiene el número asignado en tu Excel)
    ing_asignado = str(row['Unnamed: 3'])
    
    info_graduando = {
        "encontrado": True,
        "nombre": str(row['NOMBRE COMPLETO']),
        "carrera": str(row['Programa']),
        "ing": ing_asignado,
        "ceremonia": str(row['Ceremonia'])
    }
    
    return jsonify(info_graduando)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
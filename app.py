
import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="PowerTech Motor", page_icon="🚗", layout="centered")

# Estilos personalizados
st.markdown(
    '''
    <style>
    body {
        background-color: #000000;
    }
    .title {
        color: gold;
        text-align: center;
        font-size: 40px;
        font-weight: bold;
    }
    .subtitle {
        color: gold;
        text-align: center;
        font-size: 25px;
        font-weight: normal;
    }
    .signature {
        color: gray;
        text-align: center;
        font-size: 15px;
    }
    .stTextInput>div>div>input {
        color: white;
        background-color: #333333;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# Encabezados
st.markdown("<div class='title'>PowerTech Motor</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Control de Mantenimiento</div>", unsafe_allow_html=True)
st.markdown("<div class='signature'>Ing. Ronny Calva</div>", unsafe_allow_html=True)

# Conexión a Google Sheets (con link corregido)
sheet_url = 'https://docs.google.com/spreadsheets/d/1Fmwe1G9mM6WQlRb4QIHq4FIoZYl2Jm3-/edit?usp=sharing'
csv_export_url = sheet_url.replace('/edit?usp=sharing', '/export?format=csv')
df = pd.read_csv(csv_export_url)

# Menú de opciones
st.markdown("---")
menu = st.selectbox("Selecciona una opción", ["Buscar Vehículo", "Agregar Vehículo"])
st.markdown("---")

if menu == "Buscar Vehículo":
    placa = st.text_input("Ingrese la placa del vehículo:", "").upper()
    if placa:
        resultado = df[df["Placa"] == placa]
        if not resultado.empty:
            index = resultado.index[0]
            nuevo_datos = {}
            for col in df.columns:
                nuevo_datos[col] = st.text_input(f"{col}:", resultado.iloc[0][col])
            if st.button("Guardar Cambios"):
                for col in df.columns:
                    df.at[index, col] = nuevo_datos[col]
                df.to_csv("/mnt/data/temp.csv", index=False)
                st.success("✅ Datos actualizados correctamente.")
            if st.button("Eliminar Registro"):
                df.drop(index=index, inplace=True)
                df.to_csv("/mnt/data/temp.csv", index=False)
                st.success("✅ Registro eliminado correctamente.")
        else:
            st.warning("🚨 No se encontró esa placa en la base de datos.")

elif menu == "Agregar Vehículo":
    st.subheader("Ingrese los datos del nuevo vehículo:")
    nueva_fila = {}
    for col in df.columns:
        nueva_fila[col] = st.text_input(f"{col}:", key=col)
    if st.button("Agregar Vehículo"):
        df = df.append(nueva_fila, ignore_index=True)
        df.to_csv("/mnt/data/temp.csv", index=False)
        st.success("✅ Vehículo agregado correctamente.")

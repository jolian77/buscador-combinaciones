import streamlit as st
import pandas as pd
from itertools import combinations

st.set_page_config(page_title="Buscador de combinaciones", layout="wide")

def leer_valores(df, columnas):
    datos = df[columnas]
    valores = datos.select_dtypes(include=['number']).values.flatten()
    return [v for v in valores if pd.notna(v)]

def buscar_combinaciones(valores, objetivo, margen):
    resultados = []
    for i in range(1, len(valores)+1):
        for combo in combinations(valores, i):
            suma = sum(combo)
            if objetivo - margen <= suma <= objetivo + margen:
                resultados.append((combo, suma))
    return resultados

st.title("📊 Buscador de combinaciones que suman un valor objetivo")

archivo = st.file_uploader("📂 Sube tu archivo Excel", type=["xlsx"])

if archivo:
    try:
        xls = pd.ExcelFile(archivo)
        hoja = st.selectbox("📄 Selecciona la hoja de Excel", xls.sheet_names)
        df = pd.read_excel(xls, sheet_name=hoja, engine="openpyxl")

        columnas_numericas = df.select_dtypes(include=["number"]).columns.tolist()
        columnas_seleccionadas = st.multiselect("📊 Selecciona columnas con valores numéricos", columnas_numericas)

        if columnas_seleccionadas:
            objetivo = st.number_input("🎯 Ingresa el valor objetivo a buscar", value=1000)
            margen = st.number_input("⚖️ Margen de error permitido", value=0)

            if st.button("🔍 Buscar combinaciones"):
                valores = leer_valores(df, columnas_seleccionadas)
                resultados = buscar_combinaciones(valores, objetivo, margen)

                if resultados:
                    st.success(f"✅ Se encontraron {len(resultados)} combinaciones.")
                    df_resultados = pd.DataFrame([
                        {"Combinación": ", ".join(map(str, combo)), "Suma": suma}
                        for combo, suma in resultados
                    ])
                    st.dataframe(df_resultados, use_container_width=True)
                    csv = df_resultados.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        label="📥 Descargar resultados en CSV",
                        data=csv,
                        file_name="combinaciones_resultado.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("⚠️ No se encontraron combinaciones.")
        else:
            st.info("📌 Selecciona al menos una columna numérica.")
    except Exception as e:
        st.error(f"Ocurrió un error al leer el archivo: {e}")
else:
    st.info("📎 Sube un archivo Excel para comenzar.")

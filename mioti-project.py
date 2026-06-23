import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import spearmanr

# 1. Configuración de la página
st.set_page_config(page_title="Análisis Verde y Salud", layout="wide")

st.title("🌱 Análisis de Zonas Verdes y Salud por Distrito")
st.markdown("Dashboard interactivo para explorar la relación entre indicadores ambientales y de salud.")

# 2. Carga de datos con ruta absoluta
@st.cache_data

def load_data():
    # Como los dos archivos están juntos en GitHub, solo necesitas el nombre:
    return pd.read_csv("tabla_distritos_verde_salud.csv")

df = load_data()

# 2. Carga de datos
@st.cache_data
def load_data():
    return pd.read_csv("tabla_distritos_verde_salud.csv")

df = load_data()
df['DISTRITO'] = df['DISTRITO'].astype(str) # 🌟 ¡NUEVO! Corrige el gradiente de color a colores únicos

# 3. Sidebar: Configuración y Filtros
st.sidebar.header("Configuración del Gráfico")
columnas = df.columns.tolist()
x_axis = st.sidebar.selectbox("Variable Eje X (Entorno):", columnas, index=columnas.index('intensidad_media'))
y_axis = st.sidebar.selectbox("Variable Eje Y (Salud):", columnas, index=columnas.index('n_diagnostico'))

# 🌟 ¡NUEVO! Selector interactivo para el tamaño de las burbujas
size_axis = st.sidebar.selectbox("Variable Tamaño (Burbujas):", columnas, index=columnas.index('n_diagnostico'))



# 4. Gráfico principal
st.subheader(f"Correlación: {x_axis} vs {y_axis}")

# Cálculo de correlación de Spearman
rho, p_val = spearmanr(df[x_axis], df[y_axis])

fig = px.scatter(
    df, 
    x=x_axis, 
    y=y_axis, 
    color='DISTRITO', 
    hover_data=['DISTRITO'],
    trendline="ols",                # Activa el cálculo de la línea de tendencia
    trendline_scope="overall",      # 🌟 ¡EL TRUCO CRÍTICO! Dibuja una sola línea global para todos los puntos
    trendline_color_override="red", # 🌟 Opcional: Pinta la línea de rojo para que resalte frente al azul
    title=f"Correlación de Spearman: {rho:.2f} (p-valor: {p_val:.3f})"
)

# Ajustes visuales para que la línea de tendencia no se rompa por el texto de los distritos
fig.update_layout(showlegend=True)

st.plotly_chart(fig, use_container_width=True)


# 5. Métricas Resumen (KPIs)
st.markdown("---")
col1, col2, col3 = st.columns(3)
col1.metric("Distritos analizados", len(df))
col2.metric(f"Promedio {y_axis}", f"{df[y_axis].mean():.2f}")
col3.metric("Correlación ρ", f"{rho:.2f}")

# 6. Tabla de datos
with st.expander("Ver tabla de datos completa"):
    st.dataframe(df)



st.markdown("---")
st.subheader("🏆 Comparativa y Rankings por Distrito")

# Permitir al usuario elegir qué ordenar
var_ranking = st.selectbox("Selecciona la variable para ordenar el ranking:", columnas, index=columnas.index('cobertura_media'))

# Crear el gráfico ordenando los datos de mayor a menor
df_sorted = df.sort_values(by=var_ranking, ascending=False)
fig_bar = px.bar(
    df_sorted, 
    x='DISTRITO', 
    y=var_ranking, 
    color=var_ranking,
    color_continuous_scale="Viridis",
    title=f"Distritos ordenados por {var_ranking}"
)


fig_bar.update_xaxes(type='category')

st.plotly_chart(fig_bar, use_container_width=True)


st.markdown("---")
st.subheader("📊 mapa de Calor: Correlaciones Globales")
st.markdown("Los tonos azules/verdes indican relación positiva fuerte, los rojos relación negativa.")

# Seleccionamos solo las columnas numéricas clave para no saturar
columnas_corr = ['n_diagnostico', 'pct_diagnostico', 'intensidad_media', 'cobertura_media', 'pct_cumple_300m', 'puntos_media']
matriz_corr = df[columnas_corr].corr(method='spearman')

fig_heatmap = px.imshow(
    matriz_corr,
    text_auto=".2f", # Muestra los números dentro de los cuadrados
    color_continuous_scale='RdBu', # Escala de rojo a azul
    zmin=-1, zmax=1,
    title="Matriz de correlación de Spearman entre variables ambientales y de salud"
)
st.plotly_chart(fig_heatmap, use_container_width=True)



st.markdown("---")
st.subheader("🔮 Análisis Avanzado Multivariable")

fig = px.scatter(
    df,  # 🌟 Tu tabla real
    x="cobertura_media",
    y="pct_diagnostico",
    color="DISTRITO",
    size=size_axis,  # 🌟 ¡CORREGIDO! Ahora el tamaño cambia dinámicamente con la columna elegida
    size_max=30,  
    title="Relación Cobertura Verde vs % Diagnósticos (Tamaño Variable)",
    labels={
        "cobertura_media": "Cobertura Verde Media (%)",
        "pct_diagnostico": "Prevalencia de Diagnósticos (%)",
    },
)

st.plotly_chart(fig, use_container_width=True)

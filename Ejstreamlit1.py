import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Cargar la fuente de datos
archivo = "dataCGP.csv"
data = pd.read_csv(archivo)

# Titulo y descripción
st.title("Dashboard de ventas")
st.write("En este dashboard podrás explorar gráficos de ventas de un periodo")

# Vista previa del dataset
st.sidebar.header("Vista previa del dataset")
if st.sidebar.checkbox("Mostrar dataset"):
    st.write(data)

# Seleccion de opciones de gráficos
st.sidebar.header("Seleccionar gráfico")
graph_options=["Ventas totales por productos","Comparación de ventas entre canales","Evolución de ventas por fecha","Distribución de cantidad comprada"]

graph_choice=st.sidebar.selectbox("Elija un gráfico",graph_options)

#Generar gráficos basados en la selección
st.header(graph_choice)

#Ventas totales por productos
if graph_choice == "Ventas totales por productos":
    totales= data.groupby("Producto")["Total"].sum().reset_index()
    fig, ax = plt.subplots()
    sns.barplot(data=totales,x="Producto",y="Total",ax=ax,palette="viridis")
    ax.set_title("Ventas totales por Producto")
    st.pyplot(fig)
#Comparación de ventas entre canales
elif graph_choice == "Comparación de ventas entre canales":
    canales= data.groupby("Origen")["Total"].sum().reset_index()
    fig, ax = plt.subplots()
    sns.barplot(data=canales,x="Origen", y="Total", ax=ax,palette="magma")
    ax.set_title("Comparación de Ventas por Canal")
    st.pyplot(fig)
# Evolución de ventas por fecha
elif graph_choice == "Evolución de ventas por fecha":
    data["Fecha"]= pd.to_datetime(data["Fecha"])
    ventas = data.groupby("Fecha")["Total"].sum().reset_index()
    fig, ax = plt.subplots()
    sns.lineplot(data=ventas, x="Fecha", y="Total",ax=ax, marker="o")
    ax.set_title("Evolución de Ventas por Fecha")
    st.pyplot(fig)
# Distribución de cantidad comprada
elif graph_choice == "Distribución de cantidad comprada":
    fig, ax = plt.subplots()
    sns.histplot(data["Cantidad"], kde=True, bins=10, color="blue",ax=ax)
    ax.set_title("Distribución de cantidad comprada")
    st.pyplot(fig)

#Titulo posterior
st.sidebar.info("Desarollado por Cibertec")
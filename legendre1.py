# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 16:39:30 2025

@author: jperezr
"""

import streamlit as st
import pandas as pd
from sympy import primerange

# Función para calcular los intervalos de Bertrand con la forma [m, 2m)
def calcular_intervalos_bertrand(n):
    intervalos = []
    # Calcular el límite superior
    limite_superior = (n + 1)**2
    # Los intervalos deben comenzar desde [n^2/2, n^2) y crear los subintervalos [m, 2m)
    m = (n**2 // 2) + 1
    while m * 2 < limite_superior:
        intervalos.append((m, m * 2))
        m += 1
    # Aseguramos que el último intervalo cubra hasta (n+1)^2
    intervalos.append((m, m * 2))  # Se agrega el intervalo final que cubra el límite superior
    return intervalos

# Función para encontrar números primos en un intervalo
def buscar_primos_en_intervalo(intervalo):
    inicio, fin = intervalo
    return sorted(primerange(inicio, fin))  # Ordenar los números primos

# Generar intervalos y números primos para un valor de n, filtrando los primos mayores a n^2 y menores a (n+1)^2
def generar_resultados(n):
    intervalos = calcular_intervalos_bertrand(n)
    resultados = []
    primos_totales = []

    for intervalo in intervalos:
        primos = buscar_primos_en_intervalo(intervalo)
        # Filtrar los números primos que sean mayores a n^2 y menores a (n+1)^2
        primos_filtrados = [p for p in primos if n**2 < p < (n+1)**2]
        primos_totales.extend(primos_filtrados)  # Añadir primos encontrados a la lista total
        resultados.append({
            "Intervalo": f"[{intervalo[0]},{intervalo[1]})",
            "Números primos": ", ".join(map(str, primos_filtrados))
        })

    return pd.DataFrame(resultados), primos_totales

# Interfaz Streamlit
st.title('Conjetura de Legendre Extensa')

# Barra lateral de ayuda
with st.sidebar:
    st.header("Ayuda")
    st.write("""
    Este código calcula los intervalos de Bertrand para un valor dado de \( n \). 
    Para cada intervalo \( [m, 2m) \) dentro del rango \( (n^2, (n+1)^2) \), se buscan los números primos en esos intervalos. 
    Luego, se filtran y se muestran solo los números primos que sean mayores que \( n^2 \) y menores que \( (n+1)^2 \).
    
    Después, se calcula la intersección de esos números primos y se visualiza el número primo mínimo de la intersección, 
    junto con el intervalo en el que se encuentran. 

    **Conjetura de Legendre:**
    La conjetura de Legendre establece que:
    > Hay al menos un número primo entre \( n^2 \) y \( (n+1)^2 \) para todo \( n \geq 1 \).
    """)
    
# Input del usuario
n = st.number_input('Introduce el valor de n:', min_value=2, value=3, step=1)

# Mostrar el valor de n y el intervalo (n^2, (n+1)^2)
intervalo_principal = (n**2, (n+1)**2)
st.write(f"**Valor de n:** {n}")
st.write(f"**Intervalo principal:** ({intervalo_principal[0]}, {intervalo_principal[1]})")

# Generar y mostrar los resultados
df_resultados, primos_totales = generar_resultados(n)

# Mostrar el DataFrame
st.dataframe(df_resultados)

# Si hay primos en la intersección, encontrar el mínimo
if primos_totales:
    primos_interseccion = set(primos_totales)  # Convertir a set para buscar intersección
    minimo_primo = min(primos_interseccion)
    st.write(f"**Al menos el número primo {minimo_primo} se encuentra en el intervalo ({n**2}, {(n+1)**2})**")
else:
    st.write("No se encontraron primos en la intersección.")
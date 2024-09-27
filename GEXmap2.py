import streamlit as st
# Configurar el modo ancho para la aplicación de Streamlit
st.set_page_config(
    page_title="Mi aplicación",
    page_icon=":rocket:",
    layout="centered",
    initial_sidebar_state="collapsed"
)
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Título de la aplicación
st.title("GEXmap del SPY - Tradeknowlogy")

# Obtener la fecha de ayer
yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')

# Descargar datos de 5 minutos del SPY para el día de ayer
st.write("Descargando datos de SPY...")
spy_data = yf.download('SPY', start=yesterday, end=datetime.now().strftime('%Y-%m-%d'), interval='5m', progress=False)

# Convertir el índice a datetime y filtrar los datos solo para la fecha de ayer
spy_data.index = pd.to_datetime(spy_data.index)  # Asegurarse de que el índice es de tipo datetime
spy_data = spy_data[spy_data.index.date == pd.to_datetime(yesterday).date()]

# Verificar si se obtuvieron datos
if spy_data.empty:
    st.write("No se encontraron datos para el día de ayer.")
else:
    # Calcular el valor máximo y mínimo de las velas del día de ayer
    max_price = spy_data['High'].max()
    min_price = spy_data['Low'].min()

    # Calcular los valores de los strikes con un margen de 1.1
    strike_min = min_price * 0.999  # Reducir el 10%
    strike_max = max_price * 1.001  # Aumentar el 10%

    # Generar los strikes en función del rango calculado con un paso de 0.1
    strikes = np.arange(strike_min, strike_max, 0.1)

    # Crear los intervalos de tiempo y valores ficticios de GEX
    # Crear los intervalos de tiempo y valores ficticios de GEX
    time_intervals = pd.date_range(start=f'{yesterday} 09:30', end=f'{yesterday} 16:00', freq='5min')

    #time_intervals = pd.date_range(start=f'{yesterday} 09:30', end=f'{yesterday} 16:00', freq='5T')
    gex_values = np.random.randn(len(time_intervals), len(strikes))  # Valores aleatorios de GEX para ejemplo

    # Crear el DataFrame de GEX
    gex_data = pd.DataFrame(gex_values, index=time_intervals, columns=strikes).reset_index()
    gex_data = gex_data.melt(id_vars=['index'], var_name='Strike', value_name='GEX')
    gex_data.columns = ['Datetime', 'Strike', 'GEX']

    # Crear el gráfico de velas con opacidad ajustada
    fig = go.Figure(data=[go.Candlestick(x=spy_data.index,
                                        open=spy_data['Open'],
                                        high=spy_data['High'],
                                        low=spy_data['Low'],
                                        close=spy_data['Close'],
                                        name='SPY',
                                        opacity=0.9)])  # Ajusta la opacidad

    # Crear el heatmap de GEX con la escala de colores en tonos de azul y personalizado hovertemplate
    fig.add_trace(go.Heatmap(x=gex_data['Datetime'],
                                y=gex_data['Strike'],
                                z=gex_data['GEX'],
                                colorscale='Blues',  # Escala de colores en tonos de azul
                                colorbar=dict(title='GEX'),
                                zmid=0,
                                hovertemplate='Hora: %{x}<br>Strike: %{y}<br>GEX: %{z}<extra></extra>'))

    # Configurar el diseño del gráfico
    fig.update_layout(title='SPY GEXmap (Ayer) Tradeknowlogy',
                        xaxis_title='Hora',
                        yaxis_title='Precio/Strike',
                        xaxis_rangeslider_visible=False,
                        width=10,  # Ancho del gráfico
                        height=500 )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)

# src/api/dashboard.py
import streamlit as st
import requests

# Configuração do Dashboard
st.title("Dashboard de Previsão de Criptoativos")

# Seleção do ativo (Bitcoin ou Ethereum)
asset = st.selectbox("Selecione o Ativo", options=["BTC", "ETH"])

# Entradas do usuário
sma_20 = st.number_input("SMA 20 Dias", value=0.0)
rsi = st.number_input("RSI", value=0.0)
volume = st.number_input("Volume", value=0.0)

# Botão para enviar os dados e receber a previsão
if st.button("Prever"):
    # Ajuste os nomes das chaves para corresponder aos nomes usados no treinamento
    data = {"SMA_20": sma_20, "RSI": rsi, "Volume": volume, "asset": asset}
    response = requests.post("http://api:5000/predict/", json=[data])

    if response.status_code == 200:
        result = response.json()
        prediction = result["predictions"]
        action = result.get("action", "Indefinido")  # Capturar ação recomendada
        st.success(f"Previsão para {asset}: {prediction} | Ação Sugerida: {action}")
    else:
        st.error(f"Erro na previsão: {response.json()['detail']}")

import yfinance as yf
import pandas as pd

def collect_crypto_data(symbol, start_date, end_date):
    # Baixa os dados históricos para a criptomoeda especificada
    data = yf.download(symbol, start=start_date, end=end_date)
    # Salva os dados em um arquivo CSV temporário
    data.to_csv(f"{symbol}_historical_data.csv")
    return data

if __name__ == "__main__":
    # Coleta de dados para o Bitcoin (BTC-USD)
    print("Coletando dados do Bitcoin (BTC-USD)...")
    btc_data = collect_crypto_data("BTC-USD", "2020-01-01", "2024-01-01")
    print(btc_data.head())

    # Coleta de dados para o Ethereum (ETH-USD)
    print("Coletando dados do Ethereum (ETH-USD)...")
    eth_data = collect_crypto_data("ETH-USD", "2020-01-01", "2024-01-01")
    print(eth_data.head())

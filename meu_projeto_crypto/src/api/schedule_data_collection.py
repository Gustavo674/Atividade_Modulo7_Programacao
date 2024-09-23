import schedule
import time
from collect_data import collect_crypto_data  # Importando a função de coleta de dados
import pandas as pd

def job():
    print("Iniciando automação da coleta de dados")
    try:
        # Coleta de dados para o Bitcoin (BTC-USD)
        print("Coletando dados do Bitcoin (BTC-USD)...")
        btc_data = collect_crypto_data("BTC-USD", "2020-01-01", "2024-01-01")
        btc_data['Asset'] = 'BTC'

        # Coleta de dados para o Ethereum (ETH-USD)
        print("Coletando dados do Ethereum (ETH-USD)...")
        eth_data = collect_crypto_data("ETH-USD", "2020-01-01", "2024-01-01")
        eth_data['Asset'] = 'ETH'
        
        # Combine os dados coletados
        combined_data = pd.concat([btc_data, eth_data])

        # Salve os dados em um único arquivo CSV
        combined_data.to_csv('novo_dados_crypto.csv', index=False)
        print("Dados salvos em 'novo_dados_crypto.csv'")
        
        print("Coleta de dados concluída com sucesso")
    except Exception as e:
        print(f"Erro durante a coleta de dados: {e}")

# Agendar a função para rodar a cada minuto para teste
schedule.every(1).minutes.do(job)

print("Agendamento configurado. Esperando pela próxima execução...")

while True:
    try:
        schedule.run_pending()
        print("Aguardando a próxima execução...")
        time.sleep(10)  # Espera 10 segundos entre as verificações de pendência
    except KeyboardInterrupt:
        print("Agendamento interrompido pelo usuário.")
        break
    except Exception as e:
        print(f"Erro no loop de agendamento: {e}")

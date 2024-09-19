import schedule
import time
from collect_data import collect_crypto_data  # Importando a função de coleta de dados

def job():
    print("Iniciando automação da coleta de dados")
    try:
        # Coleta de dados para o Bitcoin (BTC-USD)
        print("Coletando dados do Bitcoin (BTC-USD)...")
        btc_data = collect_crypto_data("BTC-USD", "2020-01-01", "2024-01-01")
        print(btc_data.head())

        # Coleta de dados para o Ethereum (ETH-USD)
        print("Coletando dados do Ethereum (ETH-USD)...")
        eth_data = collect_crypto_data("ETH-USD", "2020-01-01", "2024-01-01")
        print(eth_data.head())
        
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

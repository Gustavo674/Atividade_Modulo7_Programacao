from prefect import flow, task
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os

# Função para calcular RSI
def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Task para carregar novos dados
@task
def load_new_data():
    # Obter o caminho absoluto do arquivo CSV
    file_path = os.path.join(os.path.dirname(__file__), 'novo_dados_crypto.csv')
    
    # Verificar se o arquivo existe
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    
    # Carregar os dados
    data = pd.read_csv(file_path)
    
    # Calcular SMA_20 e RSI
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    data['RSI'] = calculate_rsi(data)
    data = data.dropna()
    return data

# Task para treinar o modelo
@task
def train_model(data):
    features = data[['SMA_20', 'RSI', 'Volume']]
    target = data['Close']
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Salvar o modelo re-treinado
    joblib.dump(model, 'src/api/models/modelos/best_random_forest_model_retrained.pkl')
    print("Modelo re-treinado e salvo com sucesso.")

# Definir o fluxo de retreinamento
@flow
def retrain_flow():
    data = load_new_data()
    train_model(data)

if __name__ == "__main__":
    retrain_flow()

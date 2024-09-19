# hyperparameter_tuning.py
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, train_test_split
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Função para calcular RMSE e MAE
def evaluate_model(y_true, y_pred, model_name):
    rmse = mean_squared_error(y_true, y_pred, squared=False)
    mae = mean_absolute_error(y_true, y_pred)
    print(f'{model_name} - RMSE: {rmse}')
    print(f'{model_name} - MAE: {mae}')

# ================================
# Ajuste de Hiperparâmetros para Bitcoin
# ================================

# Carregar dados do Bitcoin
data_btc = pd.read_csv('BTC-USD_historical_data_cleaned.csv')

# Calcular a Média Móvel de 20 dias e RSI para Bitcoin
data_btc['SMA_20'] = data_btc['Close'].rolling(window=20).mean()

def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

data_btc['RSI'] = calculate_rsi(data_btc)

# Preencher valores ausentes
data_btc = data_btc.dropna()
features_btc = data_btc[['SMA_20', 'RSI', 'Volume']]
target_btc = data_btc['Close']

# Dividir os dados em treino e teste para Bitcoin
X_train_btc, X_test_btc, y_train_btc, y_test_btc = train_test_split(features_btc, target_btc, test_size=0.2, random_state=42)

# Configurar os parâmetros para GridSearchCV
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5, 10]
}

# Inicializar o modelo Random Forest
rf = RandomForestRegressor(random_state=42)

# Inicializar o GridSearchCV para Bitcoin
grid_search_btc = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, scoring='neg_mean_squared_error')
grid_search_btc.fit(X_train_btc, y_train_btc)

# Melhor modelo após o ajuste de hiperparâmetros para Bitcoin
best_rf_btc = grid_search_btc.best_estimator_

# Avaliar o modelo ajustado para Bitcoin
y_pred_btc = best_rf_btc.predict(X_test_btc)
evaluate_model(y_test_btc, y_pred_btc, "Tuned Random Forest (BTC)")

# Exibir os melhores parâmetros encontrados para Bitcoin
print("Melhores Hiperparâmetros (BTC):", grid_search_btc.best_params_)

# ================================
# Ajuste de Hiperparâmetros para Ethereum
# ================================

# Carregar dados do Ethereum
data_eth = pd.read_csv('ETH-USD_historical_data_cleaned.csv')

# Calcular a Média Móvel de 20 dias e RSI para Ethereum
data_eth['SMA_20'] = data_eth['Close'].rolling(window=20).mean()
data_eth['RSI'] = calculate_rsi(data_eth)

# Preencher valores ausentes
data_eth = data_eth.dropna()
features_eth = data_eth[['SMA_20', 'RSI', 'Volume']]
target_eth = data_eth['Close']

# Dividir os dados em treino e teste para Ethereum
X_train_eth, X_test_eth, y_train_eth, y_test_eth = train_test_split(features_eth, target_eth, test_size=0.2, random_state=42)

# Inicializar o GridSearchCV para Ethereum
grid_search_eth = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, scoring='neg_mean_squared_error')
grid_search_eth.fit(X_train_eth, y_train_eth)

# Melhor modelo após o ajuste de hiperparâmetros para Ethereum
best_rf_eth = grid_search_eth.best_estimator_

# Avaliar o modelo ajustado para Ethereum
y_pred_eth = best_rf_eth.predict(X_test_eth)
evaluate_model(y_test_eth, y_pred_eth, "Tuned Random Forest (ETH)")

# Exibir os melhores parâmetros encontrados para Ethereum
print("Melhores Hiperparâmetros (ETH):", grid_search_eth.best_params_)

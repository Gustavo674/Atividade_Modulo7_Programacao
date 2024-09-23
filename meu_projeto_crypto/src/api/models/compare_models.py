from sklearn.metrics import mean_squared_error, mean_absolute_error
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from prophet import Prophet
from sklearn.model_selection import train_test_split
import joblib

# Função para calcular RMSE e MAE para um conjunto de previsões
def evaluate_model(y_true, y_pred, model_name):
    rmse = mean_squared_error(y_true, y_pred, squared=False)
    mae = mean_absolute_error(y_true, y_pred)
    print(f'{model_name} - RMSE: {rmse}')
    print(f'{model_name} - MAE: {mae}')
    return rmse, mae

# Função para calcular o RSI
def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Função para executar Regressão Linear
def run_linear_regression(data, target_col):
    # Calcular SMA_20 e RSI
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    data['RSI'] = calculate_rsi(data)
    data = data.dropna()  # Remover linhas com NaN resultantes dos cálculos
    features = data[['SMA_20', 'RSI', 'Volume']]
    target = data[target_col]
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return y_test, y_pred

# Função para executar Random Forest
def run_random_forest(data, target_col):
    # Calcular SMA_20 e RSI
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    data['RSI'] = calculate_rsi(data)
    data = data.dropna()  
    features = data[['SMA_20', 'RSI', 'Volume']]
    target = data[target_col]
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    # Salvar o modelo treinado
    joblib.dump(model, 'modelos/best_random_forest_model.pkl')
    print("Modelo Random Forest salvo com sucesso em 'modelos/best_random_forest_model.pkl'")
    
    return y_test, y_pred

# Função para executar Prophet
def run_prophet(data):
    data = data[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})
    data['ds'] = pd.to_datetime(data['ds'])
    train_size = int(len(data) * 0.8)
    train, test = data[:train_size], data[train_size:]
    model = Prophet()
    model.fit(train)
    future = model.make_future_dataframe(periods=len(test))
    forecast = model.predict(future)
    y_pred = forecast[['ds', 'yhat']].tail(len(test))
    return test['y'], y_pred['yhat']

# Carregar dados para Bitcoin e Ethereum
data_btc = pd.read_csv('BTC-USD_historical_data_cleaned.csv')
data_eth = pd.read_csv('ETH-USD_historical_data_cleaned.csv')

# Avaliar modelos para Bitcoin
print("\nComparando Modelos para Bitcoin:")
y_test, y_pred = run_linear_regression(data_btc, 'Close')
evaluate_model(y_test, y_pred, "Linear Regression (BTC)")

y_test, y_pred = run_random_forest(data_btc, 'Close')
evaluate_model(y_test, y_pred, "Random Forest (BTC)")

y_test, y_pred = run_prophet(data_btc)
evaluate_model(y_test, y_pred, "Prophet (BTC)")

# Avaliar modelos para Ethereum
print("\nComparando Modelos para Ethereum:")
y_test, y_pred = run_linear_regression(data_eth, 'Close')
evaluate_model(y_test, y_pred, "Linear Regression (ETH)")

y_test, y_pred = run_random_forest(data_eth, 'Close')
evaluate_model(y_test, y_pred, "Random Forest (ETH)")

y_test, y_pred = run_prophet(data_eth)
evaluate_model(y_test, y_pred, "Prophet (ETH)")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd
import joblib

# Definir um modelo de entrada para a API usando Pydantic com nomes de campos correspondentes
class PredictionInput(BaseModel):
    SMA_20: float
    RSI: float
    Volume: float
    asset: str  # Campo adicional para especificar o ativo: 'BTC' ou 'ETH'

# Inicializar a aplicação FastAPI
app = FastAPI()

# Carregar o modelo re-treinado para Bitcoin e Ethereum
# Como o modelo re-treinado é único, ele é usado para ambos os ativos
model_retrained = joblib.load('models/modelos/best_random_forest_model_retrained.pkl')

# Rota para verificar o status da API
@app.get("/")
async def root():
    return {"message": "API de Previsão de Criptoativos está online"}

# Endpoint para previsão
@app.post("/predict/")
async def predict(data: List[PredictionInput]):
    try:
        # Converter os dados recebidos para um DataFrame
        input_df = pd.DataFrame([d.dict() for d in data])

        # Remover a coluna 'asset' antes de fazer a previsão
        input_df = input_df.drop(columns=['asset'])

        # Realizar a previsão usando o modelo re-treinado
        predictions = model_retrained.predict(input_df)

        # Lógica de decisão de compra/venda
        current_price = input_df['SMA_20'][0]  # Usando SMA_20 como proxy para o preço atual
        predicted_price = predictions[0]

        if predicted_price > current_price:
            action = "Compra"
        else:
            action = "Venda"

        # Retornar as previsões e a ação recomendada
        return {"predictions": predictions.tolist(), "action": action}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

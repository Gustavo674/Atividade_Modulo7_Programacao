from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd
import joblib

# Definir um modelo de entrada para a API usando Pydantic com nomes de campos correspondentes
class PredictionInput(BaseModel):
    SMA_20: float  # Corrigir os nomes para exatamente como são enviados
    RSI: float
    Volume: float

# Inicializar a aplicação FastAPI
app = FastAPI()

# Carregar o modelo previamente treinado (exemplo: Random Forest)
model = joblib.load('src/api/models/modelos/best_random_forest_model.pkl')

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

        # Realizar a previsão
        predictions = model.predict(input_df)

        # Retornar as previsões
        return {"predictions": predictions.tolist()}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

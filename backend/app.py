"""API REST para consultar el modelo de detección de fraude."""
from pathlib import Path
import pickle
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.pkl"

if not MODEL_PATH.exists():
    # Facilita el primer arranque local si aún no se generó el artefacto.
    try:
        from .modelo_fraude import entrenar_y_guardar
    except ImportError:
        from modelo_fraude import entrenar_y_guardar
    entrenar_y_guardar()

with MODEL_PATH.open("rb") as f:
    modelo = pickle.load(f)

app = FastAPI(
    title="API de detección de fraude",
    description="Predicción demostrativa con Random Forest y datos sintéticos.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class Transaccion(BaseModel):
    monto: float = Field(..., gt=0, le=1000000, description="Importe de la transacción")
    hora: float = Field(..., ge=0, le=24, description="Hora del día, de 0 a 24")
    pais_riesgoso: int = Field(..., ge=0, le=1, description="1 si el país se considera riesgoso")

class LoteTransacciones(BaseModel):
    transacciones: List[Transaccion]

@app.get("/")
def inicio():
    return {"mensaje": "API de detección de fraude activa", "documentacion": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok", "modelo_cargado": modelo is not None}

@app.post("/predict")
def predecir(transaccion: Transaccion):
    try:
        X = [[transaccion.monto, transaccion.hora, transaccion.pais_riesgoso]]
        pred = int(modelo.predict(X)[0])
        prob = float(modelo.predict_proba(X)[0][1])
        return {
            "prediccion": pred,
            "resultado": "Fraude" if pred == 1 else "Legítima",
            "probabilidad_fraude": round(prob, 4),
            "nivel_riesgo": "Alto" if prob >= 0.7 else ("Medio" if prob >= 0.4 else "Bajo"),
            "umbral_referencia": 0.7,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"No se pudo realizar la predicción: {exc}")

@app.post("/predict/batch")
def predecir_lote(lote: LoteTransacciones):
    resultados = []
    for t in lote.transacciones:
        X = [[t.monto, t.hora, t.pais_riesgoso]]
        pred = int(modelo.predict(X)[0])
        prob = float(modelo.predict_proba(X)[0][1])
        resultados.append({
            "prediccion": pred,
            "resultado": "Fraude" if pred == 1 else "Legítima",
            "probabilidad_fraude": round(prob, 4),
        })
    return {"total": len(resultados), "resultados": resultados}

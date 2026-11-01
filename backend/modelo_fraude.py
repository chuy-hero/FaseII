"""Entrenamiento reproducible del modelo de detección de fraude."""
from pathlib import Path
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.pkl"

def crear_datos():
    """Datos sintéticos basados en las reglas del material académico."""
    rng = np.random.default_rng(42)
    n = 3000
    monto = rng.uniform(1, 1000, n)
    hora = rng.uniform(0, 24, n)
    pais_riesgoso = rng.integers(0, 2, n)
    fraude = (
        (monto > 800)
        | (pais_riesgoso == 1)
        | ((hora < 6) & (monto > 500))
    ).astype(int)
    X = np.column_stack([monto, hora, pais_riesgoso])
    return X, fraude

def entrenar_y_guardar():
    X, y = crear_datos()
    modelo = RandomForestClassifier(
        n_estimators=150, random_state=42, class_weight="balanced"
    )
    modelo.fit(X, y)
    with MODEL_PATH.open("wb") as f:
        pickle.dump(modelo, f)
    print(f"Modelo guardado en: {MODEL_PATH}")
    return modelo

if __name__ == "__main__":
    entrenar_y_guardar()

# Detector de fraude financiero con Random Forest

Proyecto que despliega un modelo de clasificación mediante FastAPI, Docker y una interfaz web.

## 1. Alcance y advertencia

El modelo se entrena con datos sintéticos generados a partir de las reglas del ejercicio:
- monto superior a 800 → etiqueta de fraude;
- país riesgoso igual a 1 → etiqueta de fraude;
- hora anterior a 6 y monto superior a 500 → etiqueta de fraude.

Por ello, el proyecto demuestra el flujo técnico de entrenamiento, serialización, API, frontend y contenedorización. No es un detector validado para operaciones financieras reales y no debe utilizarse para bloquear transacciones reales.

## 2. Estructura

```text
Proyecto_Fraude_IA/
├── backend/
│   ├── app.py
│   ├── modelo_fraude.py
│   ├── model.pkl
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── tests/
│   └── test_api.py
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
└── README.md
```

## 3. Ejecución local sin Docker

Se requiere Python 3.10.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r backend/requirements.txt
python backend/modelo_fraude.py
uvicorn backend.app:app --reload
```

API: http://localhost:8000  
Documentación interactiva: http://localhost:8000/docs

Para abrir el frontend, sirve la carpeta con un servidor estático desde otra terminal:

```bash
python -m http.server 5500 --directory frontend
```

Abre http://localhost:5500. La API permite los orígenes locales `localhost:5500` y `127.0.0.1:5500`. Para producción, agrega el dominio HTTPS real del frontend a `allow_origins`.

## 4. Ejecución con Docker

Desde la raíz del proyecto:

```bash
docker build -t modelo-fraude .
docker run --rm -p 8000:8000 modelo-fraude
```

O con Compose:

```bash
docker compose up --build
```

La imagen contiene la API y el modelo serializado. La interfaz se puede servir localmente con el servidor estático anterior.

## 5. API

### GET `/`
Comprueba que la API responde.

### GET `/health`
Comprueba el estado del servicio.

### POST `/predict`
Ejemplo de cuerpo JSON:

```json
{
  "monto": 650,
  "hora": 2,
  "pais_riesgoso": 0
}
```

La respuesta incluye etiqueta predicha, probabilidad estimada y nivel de riesgo. También existe `POST /predict/batch` para lotes.

## 6. Pruebas

Instala pytest y httpx:

```bash
pip install pytest httpx
pytest -q
```

Casos de prueba sugeridos para registrar evidencias:
- habitual: monto 10, hora 12, país no riesgoso;
- importe alto: monto 999, hora 12, país no riesgoso;
- madrugada: monto 650, hora 2, país no riesgoso;
- país riesgoso: monto 100, hora 12, país riesgoso;
- extremos inválidos: monto negativo y hora 25 (la API debe responder 422).

Las pruebas automatizadas verifican disponibilidad, respuesta del endpoint y validación de datos. Ejecuta los comandos y guarda capturas reales; no declares pruebas aprobadas sin ejecutarlas.

## 7. Despliegue en Render (PaaS)

1. Sube el proyecto a un repositorio GitHub.
2. En Render, crea un **Web Service** y conecta el repositorio.
3. Configura el entorno como Docker.
4. Render construirá la imagen a partir del `Dockerfile`.
5. Cuando termine, abre la URL asignada y verifica `/`, `/health` y `/docs`.
6. Si publicas el frontend por separado, cambia `API_URL` en `frontend/script.js` por la URL HTTPS de la API y configura CORS en FastAPI para permitir el dominio del frontend.

**Nota:** el despliegue no se realiza automáticamente desde este paquete; requiere tu cuenta, repositorio y configuración en Render. No publiques claves ni credenciales en GitHub.

## 8. CORS para frontend desplegado por separado

Añade en `backend/app.py` después de crear `app`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://TU-FRONTEND.onrender.com"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

Para pruebas locales con frontend en `http://localhost:5500`, permite ese origen. En producción sustituye el dominio de ejemplo por el dominio real.

## 9. Limitaciones y trabajo futuro

- Los datos son sintéticos y siguen reglas explícitas; no representan el comportamiento real de fraude.
- Las probabilidades reflejan el modelo entrenado sobre ese conjunto sintético, no una probabilidad financiera calibrada.
- Para producción se necesitarían datos históricos autorizados, evaluación de falsos positivos/negativos, calibración, monitoreo, seguridad, privacidad y revisión humana.
- El archivo `model.pkl` debe generarse con una versión compatible de scikit-learn. Si aparece un aviso de incompatibilidad, vuelve a entrenar con `python backend/modelo_fraude.py` en el mismo entorno.

## 10. Evidencias para la entrega

Incluye capturas propias de:
1. entrenamiento del modelo y generación de `model.pkl`;
2. API activa y `/docs`;
3. frontend conectado y resultado de una predicción;
4. construcción y ejecución del contenedor;
5. pruebas automatizadas;
6. servicio en la nube, si realizas el despliegue.



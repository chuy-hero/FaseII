# Entrega del proyecto – Fase 2
## Despliegue local y preparación para la nube

### 1. Objetivo
Desarrollar una solución técnica desplegable para un modelo de detección de fraude financiero. La solución integra un modelo Random Forest serializado, una API REST construida con FastAPI, una interfaz web y un contenedor Docker.

### 2. Arquitectura
- **Modelo:** Random Forest entrenado con tres variables: monto, hora y país riesgoso.
- **Backend:** FastAPI expone endpoints para estado del servicio y predicción individual o por lote.
- **Frontend:** HTML, CSS y JavaScript envían los datos a la API mediante HTTP.
- **Contenedorización:** Docker empaqueta el backend, dependencias y modelo.
- **Nube:** se propone Render como plataforma PaaS para publicar el contenedor.

### 3. Datos y lógica del ejercicio
El conjunto de datos es sintético y se genera de forma reproducible. Las etiquetas se asignan con las reglas descritas en el material académico: importe mayor a 800, país riesgoso o transacción de madrugada con importe superior a 500. El modelo aprende patrones de ese conjunto.

### 4. Implementación
El script `backend/modelo_fraude.py` genera los datos, entrena Random Forest y guarda `model.pkl`. El archivo `backend/app.py` carga el modelo y publica `/predict`. La interfaz `frontend/` consume ese endpoint y muestra la clasificación y la probabilidad estimada.

### 5. Validación
Se incluyen pruebas automatizadas para:
- comprobar el endpoint raíz;
- comprobar el estado de salud;
- realizar una predicción válida;
- rechazar un monto negativo;
- rechazar una hora fuera del rango.

**Completar con resultados reales:** ejecutar `pytest -q`, registrar fecha, versión de Python, resultado y capturas. No marcar las pruebas como aprobadas antes de ejecutarlas.

### 6. Despliegue local
Comandos previstos:

```bash
docker build -t modelo-fraude .
docker run --rm -p 8000:8000 modelo-fraude
```

Validar `http://localhost:8000/health` y `http://localhost:8000/docs`.

### 7. Preparación para la nube
Se propone Render como PaaS. Se conecta el repositorio GitHub, se selecciona el entorno Docker y se verifica la URL pública. El despliegue requiere acciones desde una cuenta del estudiante y no queda realizado por la mera creación de estos archivos.

### 8. Casos funcionales y extremos
- Monto habitual, hora diurna, país no riesgoso.
- Monto alto.
- Operación de madrugada con monto elevado.
- País riesgoso.
- Monto negativo.
- Hora fuera del rango permitido.

### 9. Limitaciones
El modelo se basa en datos sintéticos y reglas didácticas. No debe utilizarse para decisiones reales. La probabilidad estimada no equivale a una probabilidad calibrada de fraude real.

### 10. Conclusión
El proyecto demuestra el ciclo técnico de entrenamiento, serialización, exposición mediante API, consumo desde frontend y empaquetado con Docker. La publicación en la nube y las evidencias finales deben completarse y verificarse en el entorno del estudiante.

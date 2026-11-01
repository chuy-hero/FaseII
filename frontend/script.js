const API_URL = "http://localhost:8000";
const statusEl = document.getElementById("apiStatus");
const form = document.getElementById("fraudForm");
const button = document.getElementById("submitBtn");

async function checkApi() {
  try {
    const response = await fetch(`${API_URL}/health`);
    if (!response.ok) throw new Error("API no disponible");
    statusEl.textContent = "API conectada";
    document.querySelector(".dot").style.background = "#20a36b";
  } catch {
    statusEl.textContent = "API desconectada: inicia el backend";
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const monto = Number(document.getElementById("monto").value);
  const hora = Number(document.getElementById("hora").value);
  const pais_riesgoso = Number(document.getElementById("pais").value);

  if (!(monto > 0 && monto <= 1000000) || hora < 0 || hora > 24) {
    alert("Verifica que el monto sea mayor que 0 y la hora esté entre 0 y 24.");
    return;
  }

  button.disabled = true;
  button.textContent = "Analizando…";
  try {
    const response = await fetch(`${API_URL}/predict`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({monto, hora, pais_riesgoso})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Error de la API");

    document.getElementById("result").classList.remove("hidden");
    const label = document.getElementById("resultLabel");
    label.textContent = data.resultado;
    label.className = `result-label ${data.prediccion === 1 ? "danger" : "safe"}`;
    document.getElementById("probability").textContent =
      `${(data.probabilidad_fraude * 100).toFixed(1)}%`;
    document.getElementById("risk").textContent = data.nivel_riesgo;
    document.getElementById("meterFill").style.width =
      `${Math.max(0, Math.min(100, data.probabilidad_fraude * 100))}%`;
    document.getElementById("explanation").textContent =
      `Predicción generada por el modelo. Umbral de referencia para riesgo alto: ${data.umbral_referencia}.`;
  } catch (error) {
    alert(`No se pudo analizar la transacción: ${error.message}`);
  } finally {
    button.disabled = false;
    button.textContent = "Analizar transacción";
  }
});

checkApi();

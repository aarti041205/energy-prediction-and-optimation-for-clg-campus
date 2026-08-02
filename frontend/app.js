/* 
   JavaScript Logic for Northwind Ops Theme Campus Energy Command Center
   Connects UI to FastAPI backend endpoints.
*/

const API_BASE = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", () => {
    checkHealth();
    fetchAlerts();
});

async function checkHealth() {
    try {
        const res = await fetch(`${API_BASE}/health`);
        if (res.ok) {
            const data = await res.json();
            document.getElementById("header-status-text").innerText = `FastAPI Status: ${data.status.toUpperCase()} | Model Loaded`;
        }
    } catch (e) {
        document.getElementById("header-status-text").innerText = "FastAPI Offline - Utilizing Baseline Data";
    }
}

async function fetchAlerts() {
    try {
        const res = await fetch(`${API_BASE}/alerts`);
        if (res.ok) {
            const alerts = await res.json();
            if (alerts && alerts.length > 0) {
                document.getElementById("alert-count-badge").innerText = alerts.length;
            }
        }
    } catch (e) {
        console.warn("Alerts fetch error:", e);
    }
}

function openPredictModal() {
    document.getElementById("predict-modal").style.display = "flex";
}

function openChatModal() {
    document.getElementById("chat-modal").style.display = "flex";
}

function closeModal(id) {
    document.getElementById(id).style.display = "none";
}

async function handlePrediction(e) {
    e.preventDefault();
    const building = document.getElementById("p-building").value;
    const temp = parseFloat(document.getElementById("p-temp").value);
    const hour = parseInt(document.getElementById("p-hour").value);
    const load = parseFloat(document.getElementById("p-load").value);

    const resultDiv = document.getElementById("predict-result");
    resultDiv.style.display = "block";
    resultDiv.innerHTML = "<span style='color:#F59E0B;'>Running ML prediction...</span>";

    try {
        const res = await fetch(`${API_BASE}/predict`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                Building: building,
                Building_Type: "Laboratory",
                Temperature: temp,
                Humidity: 65.0,
                Hour: hour,
                Day: 15,
                Month: 8,
                Weekend: 0,
                Holiday: 0,
                Equipment_Load: load
            })
        });

        if (res.ok) {
            const data = await res.json();
            resultDiv.innerHTML = `
                <div style="background:#1E2638; padding:12px; border-radius:8px; border-left:4px solid #10B981;">
                    <div style="font-weight:700; color:#10B981; font-size:16px;">Predicted Energy: ${data.predicted_energy_kwh} kWh</div>
                    <div style="font-size:12px; color:#94A3B8; margin-top:4px;">Confidence: ${(data.confidence_score * 100).toFixed(1)}% | Cost: ₹${data.electricity_cost_inr}</div>
                </div>
            `;
        } else {
            resultDiv.innerHTML = "<span style='color:#F43F5E;'>API error during prediction.</span>";
        }
    } catch (err) {
        resultDiv.innerHTML = `<span style='color:#F43F5E;'>Connection error: ${err.message}</span>`;
    }
}

async function handleChatSubmit(e) {
    e.preventDefault();
    const input = document.getElementById("chat-input");
    const query = input.value.trim();
    if (!query) return;

    const log = document.getElementById("chat-log");
    log.innerHTML += `<div style="margin-top:8px;"><b>You:</b> ${query}</div>`;
    input.value = "";
    log.scrollTop = log.scrollHeight;

    try {
        const res = await fetch(`${API_BASE}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: query })
        });

        if (res.ok) {
            const data = await res.json();
            log.innerHTML += `<div style="margin-top:8px; color:#10B981;"><b>AI Assistant:</b> ${data.answer}</div>`;
        } else {
            log.innerHTML += `<div style="margin-top:8px; color:#F43F5E;"><b>AI Assistant:</b> Error communicating with RAG server.</div>`;
        }
    } catch (err) {
        log.innerHTML += `<div style="margin-top:8px; color:#F43F5E;"><b>AI Assistant:</b> ${err.message}</div>`;
    }
    log.scrollTop = log.scrollHeight;
}

function showSection(name) {
    if (name === 'predict') {
        openPredictModal();
    } else if (name === 'chat') {
        openChatModal();
    } else {
        alert(`Navigating to ${name.toUpperCase()} Section`);
    }
}

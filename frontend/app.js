/**
 * Quantum Self-Learning Matrix — Frontend Logic
 * © 2025 swordenkisk (https://github.com/swordenkisk)
 * All Rights Reserved.
 */

"use strict";

const API_BASE = "http://localhost:5000";

// ── State ─────────────────────────────────────────────────────────────────

const session = {
  history: [],
};

// ── Entry point ───────────────────────────────────────────────────────────

async function startQuantumLearning() {
  const concept = document.getElementById("conceptInput").value.trim();
  if (!concept) {
    showToast("Please enter a concept to learn.", "warn");
    return;
  }

  setLoading(true);
  showToast("🔄 Encoding concept as quantum circuit…", "info");

  try {
    const useEEG = document.getElementById("useEEG").checked;
    const eegData = useEEG ? generateMockEEG() : [];

    const res = await fetch(`${API_BASE}/api/learn`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ concept, eeg_data: eegData }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || `Server error ${res.status}`);
    }

    const data = await res.json();
    renderResults(data);
    session.history.unshift(data);
    renderHistory();
    showToast(`✅ "${concept}" learned — mastery ${data.result.mastery_level}%`, "success");
  } catch (err) {
    showToast(`❌ ${err.message}`, "error");
    console.error(err);
  } finally {
    setLoading(false);
  }
}

// ── Results rendering ─────────────────────────────────────────────────────

function renderResults(data) {
  const { result, explanation, eeg_state } = data;

  document.getElementById("results").classList.remove("hidden");

  // Mastery meter
  const mastery = result.mastery_level;
  const fill = document.getElementById("masteryFill");
  const label = document.getElementById("masteryValue");

  fill.style.width = "0%";
  setTimeout(() => {
    fill.style.width = `${mastery}%`;
    fill.style.background = masteryColor(mastery);
  }, 60);
  label.textContent = `${mastery}%`;

  // EEG state
  if (eeg_state) {
    const stateEl = document.getElementById("eegState");
    const detailEl = document.getElementById("eegDetail");
    stateEl.textContent = eeg_state.optimal_learning_state ? "🟢 Optimal" : "🟡 Sub-optimal";
    detailEl.textContent =
      `Attention: ${(eeg_state.attention_score * 100).toFixed(0)}%  ` +
      `Relaxation: ${(eeg_state.relaxation_score * 100).toFixed(0)}%`;
    document.getElementById("eegBox").style.display = "flex";
  } else {
    document.getElementById("eegBox").style.display = "none";
  }

  // Quantum bar chart
  drawQuantumChart(result.counts);

  // AI explanation
  document.getElementById("explanation").innerHTML =
    `<strong>📖 AI Explanation — "${result.concept}"</strong>` +
    `<p>${explanation.replace(/\n/g, "<br/>")}</p>`;
}

function masteryColor(pct) {
  if (pct >= 80) return "linear-gradient(90deg, #10b981, #059669)";
  if (pct >= 50) return "linear-gradient(90deg, #f59e0b, #d97706)";
  return "linear-gradient(90deg, #ef4444, #dc2626)";
}

// ── Quantum bar chart (canvas) ────────────────────────────────────────────

function drawQuantumChart(counts) {
  const canvas = document.getElementById("quantumCanvas");
  const ctx = canvas.getContext("2d");
  const W = canvas.width;
  const H = canvas.height;

  ctx.clearRect(0, 0, W, H);
  ctx.fillStyle = "#0f172a";
  ctx.fillRect(0, 0, W, H);

  const entries = Object.entries(counts).slice(0, 16); // show top 16 states
  const maxVal = Math.max(...entries.map(([, v]) => v), 1);
  const barW = Math.floor((W - 40) / entries.length) - 4;
  const baseY = H - 30;

  entries.forEach(([label, val], i) => {
    const barH = Math.round(((H - 50) * val) / maxVal);
    const x = 20 + i * (barW + 4);
    const y = baseY - barH;

    // Bar gradient
    const grad = ctx.createLinearGradient(0, y, 0, baseY);
    grad.addColorStop(0, "#6366f1");
    grad.addColorStop(1, "#10b981");
    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.roundRect(x, y, barW, barH, 3);
    ctx.fill();

    // Label
    ctx.fillStyle = "rgba(255,255,255,0.5)";
    ctx.font = "8px monospace";
    ctx.save();
    ctx.translate(x + barW / 2, baseY + 4);
    ctx.rotate(-Math.PI / 4);
    ctx.fillText(label.slice(-4), 0, 0); // show last 4 bits
    ctx.restore();
  });

  // Title
  ctx.fillStyle = "rgba(255,255,255,0.7)";
  ctx.font = "11px monospace";
  ctx.fillText("Quantum Measurement Distribution (top states)", 16, 14);
}

// ── History ───────────────────────────────────────────────────────────────

async function loadHistory() {
  try {
    const res = await fetch(`${API_BASE}/api/history`);
    const data = await res.json();
    session.history = data;
    renderHistory();
  } catch {
    // server not running yet — silently ignore
  }
}

function renderHistory() {
  const container = document.getElementById("historyList");
  if (!session.history.length) {
    container.innerHTML = '<p class="muted">No concepts learned yet.</p>';
    return;
  }
  container.innerHTML = session.history
    .map(
      (item) => `
      <div class="history-item">
        <span class="history-concept">${item.concept || item.result?.concept || "—"}</span>
        <span class="history-mastery" style="color:${
          (item.result?.mastery_level ?? item.mastery_level ?? 0) >= 80
            ? "#10b981"
            : "#f59e0b"
        }">
          ${(item.result?.mastery_level ?? item.mastery_level ?? 0).toFixed(1)}%
        </span>
      </div>`
    )
    .join("");
}

async function resetSession() {
  try {
    await fetch(`${API_BASE}/api/reset`, { method: "POST" });
  } catch {
    // offline — reset locally only
  }
  session.history = [];
  renderHistory();
  document.getElementById("results").classList.add("hidden");
  showToast("Session reset.", "info");
}

// ── EEG mock ──────────────────────────────────────────────────────────────

function generateMockEEG() {
  // Simulate 8-channel EEG values (µV, 0–100 range)
  return Array.from({ length: 8 }, () => Math.random() * 100);
}

// ── UI helpers ────────────────────────────────────────────────────────────

function setLoading(on) {
  const btn = document.getElementById("learnBtn");
  document.getElementById("btnText").classList.toggle("hidden", on);
  document.getElementById("btnSpinner").classList.toggle("hidden", !on);
  btn.disabled = on;
}

let toastTimer;
function showToast(msg, type = "info") {
  const el = document.getElementById("toast");
  el.textContent = msg;
  el.className = `toast toast-${type}`;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.add("hidden"), 4000);
}

// Allow Enter key in the input
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("conceptInput").addEventListener("keydown", (e) => {
    if (e.key === "Enter") startQuantumLearning();
  });
  loadHistory();
});

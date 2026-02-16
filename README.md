# 🧠 Quantum Self-Learning Matrix v1.0

> **AI-powered adaptive learning system combining quantum computing simulation, EEG brainwave analysis, and generative AI to personalize education in real time.**

[![License: All Rights Reserved](https://img.shields.io/badge/License-All%20Rights%20Reserved-red.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Qiskit](https://img.shields.io/badge/Qiskit-1.x-purple)](https://qiskit.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-black)](https://flask.palletsprojects.com)

---

## 🚀 What It Does

Quantum Self-Learning Matrix encodes educational concepts as quantum circuits, simulates them on a local quantum backend (IBM Qiskit Aer), reads optional real-time EEG brainwave data (BrainFlow / OpenBCI), and uses a Llama 4 language model to generate deeply personalized explanations — all without sending sensitive data to the cloud.

| Feature | Technology |
|---|---|
| Quantum circuit encoding | Qiskit + Aer Simulator |
| Brainwave feedback (optional) | BrainFlow / OpenBCI |
| AI content generation | Llama 4 via Groq / HeckAI API |
| REST API backend | Flask (Python) |
| Interactive UI | Vanilla JS + HTML5 Canvas |

---

## 📸 Demo

```
Input  →  "Machine Learning"
Output →  Mastery Score: 92.3%  |  Entanglement Map  |  AI Explanation
```

---

## 🗂️ Project Structure

```
quantum-learning-matrix/
├── backend/
│   ├── server.py            # Flask REST API + Qiskit integration
│   ├── quantum_engine.py    # Advanced quantum learning engine + EEG
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── index.html           # Main UI
│   ├── app.js               # Async JS logic + EEG mock
│   └── style.css            # Dark-mode responsive styles
├── .github/
│   └── FUNDING.yml          # Sponsor button config
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE                  # © swordenkisk — All Rights Reserved
└── README.md
```

---

## ⚡ Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/swordenkisk/quantum-learning-matrix.git
cd quantum-learning-matrix
```

### 2. Install Python dependencies

```bash
pip install -r backend/requirements.txt
```

### 3. Set your API key

```bash
# Linux / macOS
export LLAMA_API_KEY="your-key-here"

# Windows PowerShell
$env:LLAMA_API_KEY="your-key-here"
```

> Get a free key at [console.groq.com](https://console.groq.com) (Llama 4 Scout is free-tier).

### 4. Run the backend

```bash
python backend/server.py
# → Running on http://localhost:5000
```

### 5. Open the frontend

Open `frontend/index.html` in any modern browser. No build step required.

---

## 🧬 How the Quantum Engine Works

1. **Concept → Embedding**: The LLM generates a semantic vector for the input concept.
2. **Quantum Encoding**: The embedding is mapped onto 8 qubits using `RY` rotations.
3. **Entanglement Layer**: A Hadamard + CNOT chain creates long-range qubit correlations simulating memory consolidation.
4. **Measurement & Scoring**: 1024-shot simulation returns a probability distribution; entropy of the distribution becomes the *mastery score*.
5. **EEG Feedback** *(optional)*: Alpha/Theta wave ratios modulate circuit depth for optimal cognitive state alignment.

---

## 💰 Monetization & Commercial Use

This repository is source-available for **demonstration and evaluation only**.

| Use Case | Status |
|---|---|
| Personal / academic use | ✅ Allowed with attribution |
| Commercial deployment | ❌ Requires a paid license |
| White-label / SaaS resale | ❌ Requires enterprise agreement |
| API integration in products | ❌ Requires partnership agreement |

To discuss licensing, SaaS deployment, or white-labeling:
**→ Open an [Issue](https://github.com/swordenkisk/quantum-learning-matrix/issues) or contact via GitHub profile.**

---

## 🛣️ Roadmap

- [x] Quantum circuit encoding + local simulator
- [x] Llama 4 AI explanation generation
- [x] Mock EEG feedback loop
- [ ] Real OpenBCI hardware integration
- [ ] AWS / GCP one-click deployment
- [ ] React Native mobile app
- [ ] Multi-user dashboard with progress analytics
- [ ] Subscription billing via Stripe

---

## 🤝 Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). Feature requests and bug reports via Issues are welcome.

---

## ⚠️ Disclaimer

EEG-based "learning acceleration" is a conceptual prototype. The quantum simulation runs on classical hardware (Aer). Claims about learning speed are illustrative, not clinically validated.

---

**© 2025 [swordenkisk](https://github.com/swordenkisk) — All Rights Reserved**

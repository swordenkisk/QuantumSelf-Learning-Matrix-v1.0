"""
Quantum Self-Learning Matrix — Flask API Server
© 2025 swordenkisk (https://github.com/swordenkisk)
All Rights Reserved.
"""

import os
import time
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
from quantum_engine import QuantumLearningEngine, AdvancedQuantumEngine

load_dotenv()

app = Flask(__name__)
CORS(app)

# ── API client (Groq / HeckAI / any OpenAI-compatible endpoint) ──────────────
client = OpenAI(
    api_key=os.getenv("LLAMA_API_KEY", "your-api-key-here"),
    base_url=os.getenv("LLAMA_API_BASE", "https://api.groq.com/openai/v1"),
)

# ── Shared engine instances ───────────────────────────────────────────────────
engine = QuantumLearningEngine()
advanced = AdvancedQuantumEngine()


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def generate_explanation(concept: str, mastery: float, eeg_state: dict = None) -> str:
    """
    Ask Llama 4 to produce a beginner-friendly explanation of *concept*,
    adapted to the learner's current mastery level and (optionally) cognitive
    state inferred from EEG.
    """
    cognitive_hint = ""
    if eeg_state:
        if eeg_state.get("optimal_learning_state"):
            cognitive_hint = "The learner is in a focused, relaxed state — use rich detail."
        else:
            cognitive_hint = "The learner appears distracted — keep the explanation very short and concrete."

    prompt = (
        f'Explain "{concept}" to a complete beginner.\n'
        f"Current mastery level: {mastery:.1f}%\n"
        f"{cognitive_hint}\n"
        "Use a real-world analogy, one short example, and finish with a single "
        "actionable next step the learner can take today."
    )

    try:
        response = client.chat.completions.create(
            model=os.getenv("LLAMA_MODEL", "meta-llama/llama-4-scout"),
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:  # noqa: BLE001
        app.logger.warning("LLM call failed: %s", exc)
        return (
            f'Explanation for "{concept}" could not be generated right now. '
            "Please check your API key and try again."
        )


# ─────────────────────────────────────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────────────────────────────────────

@app.route("/api/health", methods=["GET"])
def health_check():
    """Simple liveness probe."""
    return jsonify({"status": "ok", "timestamp": time.time()})


@app.route("/api/learn", methods=["POST"])
def learn_concept():
    """
    POST /api/learn
    Body: { "concept": "string", "eeg_data": [float, ...] }  (eeg_data optional)

    Returns quantum learning results + AI-generated explanation.
    """
    body = request.get_json(silent=True) or {}
    concept = body.get("concept", "").strip()
    if not concept:
        return jsonify({"success": False, "error": "concept is required"}), 400

    eeg_raw = body.get("eeg_data", [])

    # Process EEG if provided
    eeg_state = advanced.process_eeg_feedback(eeg_raw) if eeg_raw else None

    # Run quantum learning cycle
    quantum_result = engine.learn_concept(concept, eeg_data=eeg_raw)

    # Generate adaptive explanation
    explanation = generate_explanation(concept, quantum_result["mastery_level"], eeg_state)

    return jsonify(
        {
            "success": True,
            "result": {
                "concept": quantum_result["concept"],
                "mastery_level": quantum_result["mastery_level"],
                "learning_score": quantum_result["learning_score"],
                "counts": quantum_result["counts"],
            },
            "explanation": explanation,
            "eeg_state": eeg_state,
            "timestamp": time.time(),
        }
    )


@app.route("/api/history", methods=["GET"])
def learning_history():
    """Return all concepts stored in the in-memory knowledge graph."""
    return jsonify(list(engine.knowledge_graph.values()))


@app.route("/api/reset", methods=["POST"])
def reset_session():
    """Clear the in-memory knowledge graph (dev / demo helper)."""
    engine.knowledge_graph.clear()
    return jsonify({"success": True, "message": "Session reset."})


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=os.getenv("FLASK_DEBUG", "true").lower() == "true", port=port)

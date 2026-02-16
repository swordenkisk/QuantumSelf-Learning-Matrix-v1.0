"""
Quantum Self-Learning Matrix — Quantum Engine
© 2025 swordenkisk (https://github.com/swordenkisk)
All Rights Reserved.
"""

from __future__ import annotations

import hashlib
import math
from typing import Any

import numpy as np

try:
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator
    QISKIT_AVAILABLE = True
except ImportError:  # graceful degradation for dev environments
    QISKIT_AVAILABLE = False

try:
    from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
    BRAINFLOW_AVAILABLE = True
except ImportError:
    BRAINFLOW_AVAILABLE = False


# ─────────────────────────────────────────────────────────────────────────────
# QuantumLearningEngine
# ─────────────────────────────────────────────────────────────────────────────

class QuantumLearningEngine:
    """
    Encodes educational concepts as quantum circuits and simulates them to
    produce a *mastery score* — a measure of how well a concept is represented
    in the quantum state space.
    """

    NUM_QUBITS = 8
    SHOTS = 1024

    def __init__(self) -> None:
        self.knowledge_graph: dict[str, dict[str, Any]] = {}
        self.user_profile: dict[str, Any] = {}

        if QISKIT_AVAILABLE:
            self._backend = AerSimulator()
        else:
            self._backend = None

    # ── Private helpers ───────────────────────────────────────────────────────

    def _concept_to_embedding(self, concept: str) -> list[float]:
        """
        Deterministically convert a concept string to a normalised float vector.

        In production this would call an embedding API; here we use a seeded
        hash so that the same concept always produces the same embedding.
        """
        seed = int(hashlib.md5(concept.encode()).hexdigest(), 16) % (2**32)
        rng = np.random.default_rng(seed)
        vec = rng.random(self.NUM_QUBITS).tolist()
        return vec

    def _build_circuit(self, embedding: list[float]) -> "QuantumCircuit | None":
        """
        Map an embedding onto a quantum circuit:
          1. RY rotations encode classical amplitudes.
          2. H + CNOT chain creates long-range entanglement
             (simulates memory consolidation).
          3. Full measurement collapses the state.
        """
        if not QISKIT_AVAILABLE:
            return None

        qc = QuantumCircuit(self.NUM_QUBITS, self.NUM_QUBITS)

        # Encode
        for i, amp in enumerate(embedding[: self.NUM_QUBITS]):
            qc.ry(amp * math.pi / 2, i)

        # Entanglement (memory consolidation layer)
        qc.h(0)
        for i in range(1, self.NUM_QUBITS):
            qc.cx(0, i)

        qc.measure_all()
        return qc

    @staticmethod
    def _calculate_learning_efficiency(counts: dict[str, int]) -> float:
        """
        Use Shannon entropy of the measurement distribution as a proxy for
        concept richness / mastery.  Higher entropy → more complex, better
        encoded concept → higher score.
        """
        total = sum(counts.values())
        if total == 0:
            return 0.0

        entropy = 0.0
        for v in counts.values():
            p = v / total
            if p > 0:
                entropy -= p * math.log2(p)

        # Normalise to [0, 1] (max entropy for N qubits = N bits)
        max_entropy = math.log2(total) if total > 1 else 1.0
        return min(entropy / max_entropy, 1.0)

    def _simulate(self, qc: "QuantumCircuit") -> dict[str, int]:
        """Run the circuit on the Aer simulator and return measurement counts."""
        from qiskit import transpile

        compiled = transpile(qc, self._backend)
        job = self._backend.run(compiled, shots=self.SHOTS)
        return job.result().get_counts()

    # ── Public API ────────────────────────────────────────────────────────────

    def learn_concept(self, concept: str, eeg_data: list[float] | None = None) -> dict:
        """
        Full quantum learning cycle for a single concept.

        Returns a dict with keys:
          concept, mastery_level, learning_score, counts
        """
        embedding = self._concept_to_embedding(concept)

        if QISKIT_AVAILABLE and self._backend:
            qc = self._build_circuit(embedding)
            counts = self._simulate(qc)
            score = self._calculate_learning_efficiency(counts)
        else:
            # Fallback: deterministic mock when Qiskit is unavailable
            rng = np.random.default_rng(42)
            counts = {format(i, "08b"): int(v) for i, v in enumerate(rng.integers(1, 200, 8))}
            score = 0.75

        # Optional EEG modulation
        if eeg_data:
            alpha = float(np.mean(eeg_data[1:3])) / 100.0
            score = min(score * (1 + 0.15 * alpha), 1.0)

        result = {
            "concept": concept,
            "mastery_level": round(score * 100, 2),
            "learning_score": round(score, 4),
            "counts": counts,
        }

        # Persist in knowledge graph
        self.knowledge_graph[concept] = result
        return result


# ─────────────────────────────────────────────────────────────────────────────
# AdvancedQuantumEngine  (EEG / BrainFlow integration)
# ─────────────────────────────────────────────────────────────────────────────

class AdvancedQuantumEngine:
    """
    Processes raw EEG channel data and returns cognitive-state metrics that
    the learning engine uses to modulate circuit depth and pacing.
    """

    # BrainFlow band indices (approximations for 8-channel boards)
    ALPHA_CHANNELS = slice(1, 3)   # ~8–12 Hz
    THETA_CHANNELS = slice(4, 8)   # ~4–8 Hz

    def process_eeg_feedback(self, eeg_data: list[float]) -> dict:
        """
        Compute attention and relaxation scores from raw EEG amplitudes.

        Returns:
          attention_score      float  0–1
          relaxation_score     float  0–1
          optimal_learning_state  bool
        """
        if not eeg_data:
            return {
                "attention_score": 0.0,
                "relaxation_score": 0.0,
                "optimal_learning_state": False,
            }

        arr = np.asarray(eeg_data, dtype=float)
        # Normalise to 0–1 (assumes raw values in µV, typically 0–100 range)
        arr = np.clip(arr / 100.0, 0.0, 1.0)

        attention = float(np.mean(arr[self.ALPHA_CHANNELS])) if len(arr) >= 3 else 0.5
        relaxation = float(np.mean(arr[self.THETA_CHANNELS])) if len(arr) >= 8 else 0.5

        return {
            "attention_score": round(attention, 3),
            "relaxation_score": round(relaxation, 3),
            "optimal_learning_state": attention >= 0.7 and relaxation >= 0.5,
        }

    # ── Real hardware (OpenBCI via BrainFlow) — optional ────────────────────

    def start_hardware_stream(self, board_id: int = -1, serial_port: str = "") -> dict:
        """
        Connect to a real OpenBCI board (or synthetic board when board_id=-1).

        board_id=-1 → BrainFlow synthetic board (good for local testing).
        """
        if not BRAINFLOW_AVAILABLE:
            return {"error": "brainflow is not installed. Run: pip install brainflow"}

        params = BrainFlowInputParams()
        if serial_port:
            params.serial_port = serial_port

        board = BoardShim(board_id, params)
        board.prepare_session()
        board.start_stream()
        return {"status": "streaming", "board_id": board_id}

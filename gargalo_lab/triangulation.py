"""Lab 05 - Triangulação: da imagem à medida: por que "triangular tudo" não é um clique.

Ideia Feynman: uma foto de um carrinho de brinquedo perto e uma foto do carro
de verdade longe podem ser IDÊNTICAS. Só com imagens não dá para saber o
tamanho real; precisa de uma régua conhecida na cena. E mesmo com régua, o
erro depende de ruído e da geometria das câmeras.

Modelo: duas câmeras paralelas (estéreo). Dados sintéticos.
"""
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

F, CX, CY = 800.0, 640.0, 360.0  # distância focal e centro da imagem (pixels)
DOOR = np.array([[0.0, 1.5, 8.0], [0.0, -0.5, 8.0]])     # porta de 2,0 m (régua conhecida)
PERSON = np.array([[1.0, 1.5, 9.0], [1.0, -0.3, 9.0]])   # pessoa de 1,8 m (verdade escondida)
KNOWN_DOOR_M = 2.0
TRUE_PERSON_M = 1.8


def project(points: np.ndarray, baseline: float) -> np.ndarray:
    """Retorna colunas [u1, v1, u2, v2] em pixels. X direita, Y para baixo, Z à frente."""
    p = np.asarray(points, dtype=float)
    u1 = F * p[:, 0] / p[:, 2] + CX
    v1 = F * p[:, 1] / p[:, 2] + CY
    u2 = F * (p[:, 0] - baseline) / p[:, 2] + CX
    return np.stack([u1, v1, u2, v1.copy()], axis=1)


def triangulate(obs: np.ndarray, baseline: float) -> np.ndarray:
    u1, v1, u2, v2 = obs.T
    disparity = np.maximum(u1 - u2, 0.5)
    z = F * baseline / disparity
    x = (u1 - CX) * z / F
    y = ((v1 + v2) / 2 - CY) * z / F
    return np.stack([x, y, z], axis=1)


def ambiguity_demo(true_baseline: float = 0.37) -> dict:
    """Mundo A e mundo B (3x maior) geram exatamente os mesmos pixels."""
    obs_a = project(PERSON, true_baseline)
    obs_b = project(PERSON * 3.0, true_baseline * 3.0)
    return {"identical_pixels": bool(np.allclose(obs_a, obs_b)),
            "person_height_world_a_m": TRUE_PERSON_M, "person_height_world_b_m": TRUE_PERSON_M * 3}


def estimate_height(true_baseline: float, noise_px: float, rng: np.random.Generator,
                    assumed_baseline: float = 1.0) -> float:
    """Reconstrói com baseline ASSUMIDO (escala arbitrária) e corrige pela porta conhecida."""
    od = project(DOOR, true_baseline) + rng.normal(0, noise_px, (2, 4))
    op = project(PERSON, true_baseline) + rng.normal(0, noise_px, (2, 4))
    d = triangulate(od, assumed_baseline)
    scale = KNOWN_DOOR_M / np.linalg.norm(d[0] - d[1])
    p = triangulate(op, assumed_baseline)
    return float(np.linalg.norm(p[0] - p[1]) * scale)


def monte_carlo(trials: int = 2000, seed: int = 7) -> list[dict]:
    rng = np.random.default_rng(seed)
    rows = []
    for baseline in (0.1, 0.5, 1.5):
        for noise in (0.25, 0.5, 1.0, 2.0):
            errs = [abs(estimate_height(baseline, noise, rng) - TRUE_PERSON_M) for _ in range(trials)]
            rows.append({"baseline_m": baseline, "noise_px": noise,
                         "mean_abs_error_cm": round(100 * float(np.mean(errs)), 1)})
    return rows


def run(out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = monte_carlo()
    with (out_dir / "05_error_table.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    rng = np.random.default_rng(1)
    no_noise = estimate_height(0.37, 0.0, rng)
    return {"ambiguity": ambiguity_demo(), "height_no_noise_m": round(no_noise, 4),
            "true_height_m": TRUE_PERSON_M, "error_table": rows}

"""Lab 04 - Caçando "batimentos cardíacos" na rede (beaconing).

Ideia Feynman: um malware que pede ordens ao chefe costuma ligar de tempos em
tempos, como um despertador. Gente navegando é bagunçada; despertador é
regular. Medimos a regularidade pelo coeficiente de variação (desvio/média)
dos intervalos entre conexões: quanto menor, mais "relógio".

Dados SINTÉTICOS. IPs de documentação (RFC 5737).
"""
from __future__ import annotations

import csv
import random
from collections import defaultdict
from pathlib import Path

import numpy as np

KNOWN_GOOD = {("192.0.2.123", 123)}  # NTP legítimo (periódico, mas esperado)
MIN_CONNECTIONS = 10
CV_THRESHOLD = 0.35
MAX_MEAN_BYTES = 2000
WINDOW = 6 * 3600


def generate_conn_log(path: Path, seed: int = 1337) -> Path:
    rng = random.Random(seed)
    rows = []
    dsts = [f"198.51.100.{i}" for i in range(1, 31)]
    for h in range(10, 31):
        src = f"10.0.0.{h}"
        t = rng.uniform(0, 60)
        while t < WINDOW:
            rows.append((t, src, rng.choice(dsts), 443, rng.randint(400, 90000)))
            t += rng.expovariate(1 / 70)

    def periodic(src, dst, port, period, jitter, size):
        t = rng.uniform(0, period)
        while t < WINDOW:
            rows.append((t, src, dst, port, size + rng.randint(-20, 20)))
            t += period * (1 + rng.uniform(-jitter, jitter))

    periodic("10.0.0.10", "192.0.2.123", 123, 64, 0.0, 90)       # NTP (benigno)
    periodic("10.0.0.23", "203.0.113.50", 443, 60, 0.10, 310)    # beacon regular
    periodic("10.0.0.31", "203.0.113.77", 443, 300, 0.30, 280)   # beacon com jitter
    rows.sort()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ts", "src", "dst", "dst_port", "bytes_out"])
        for r in rows:
            w.writerow([round(r[0], 3), *r[1:]])
    return path


def load(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        return [{"ts": float(r["ts"]), "src": r["src"], "dst": r["dst"],
                 "dst_port": int(r["dst_port"]), "bytes_out": int(r["bytes_out"])} for r in csv.DictReader(f)]


def analyze(rows: list[dict], known_good=KNOWN_GOOD) -> list[dict]:
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for r in rows:
        groups[(r["src"], r["dst"], r["dst_port"])].append(r)
    findings = []
    for (src, dst, port), g in groups.items():
        if len(g) < MIN_CONNECTIONS or (dst, port) in known_good:
            continue
        ts = np.sort(np.array([x["ts"] for x in g]))
        iv = np.diff(ts)
        mean = float(iv.mean())
        cv = float(iv.std() / mean) if mean else 1.0
        avg_bytes = float(np.mean([x["bytes_out"] for x in g]))
        if cv < CV_THRESHOLD and avg_bytes < MAX_MEAN_BYTES:
            findings.append({"src": src, "dst": dst, "port": port, "connections": len(g),
                             "mean_interval_s": round(mean, 1), "cv": round(cv, 3),
                             "avg_bytes": round(avg_bytes), "attack": "T1071"})
    return sorted(findings, key=lambda f: f["cv"])


def run(out_dir: Path) -> dict:
    p = generate_conn_log(out_dir / "04_conn_log.csv")
    return {"log": str(p), "suspects": analyze(load(p))}

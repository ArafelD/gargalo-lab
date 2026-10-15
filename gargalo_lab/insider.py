"""Lab 07 - Ameaça interna: quem já está dentro já tem o acesso.

Ideia Feynman: o porteiro confere o crachá na entrada, mas e depois? Quem tem
crachá pode abrir gavetas que não são dele. A defesa precisa de três perguntas:
(1) isso é do papel dessa pessoa? (2) é muito mais que o normal para ela?
(3) é fora do horário? Uma resposta "sim" é curiosidade; três são investigação.

Dados SINTÉTICOS.
"""
from __future__ import annotations

import csv
import random
import statistics
from collections import defaultdict
from pathlib import Path

ENTITLEMENTS = {"analyst": ["crypto-data", "reports"], "ops": ["ops-planning", "reports"],
                "dev": ["src", "reports"]}
USERS = {"charlie": "analyst", "ana": "dev", "bruno": "ops", "carla": "analyst",
         "diego": "dev", "elisa": "ops", "fabio": "analyst", "gina": "dev"}
TODAY = 29
Z_LIMIT = 3.0
OFF_HOURS = set(range(22, 24)) | set(range(0, 6))


def generate(seed: int = 11) -> list[dict]:
    rng = random.Random(seed)
    ev = []
    for day in range(TODAY):
        for user, role in USERS.items():
            for _ in range(5):
                ev.append({"user": user, "day": day, "hour": rng.randint(8, 17),
                           "resource": rng.choice(ENTITLEMENTS[role]), "files": max(1, int(rng.gauss(8, 2)))})
    for user, role in USERS.items():
        if user not in ("charlie", "ana"):
            for _ in range(5):
                ev.append({"user": user, "day": TODAY, "hour": rng.randint(8, 17),
                           "resource": rng.choice(ENTITLEMENTS[role]), "files": max(1, int(rng.gauss(8, 2)))})
    ev.append({"user": "charlie", "day": TODAY, "hour": 23, "resource": "ops-planning", "files": 420})
    ev.append({"user": "ana", "day": TODAY, "hour": 10, "resource": "src", "files": 150})
    return ev


def detect(events: list[dict]) -> list[dict]:
    daily = defaultdict(lambda: defaultdict(int))
    for e in events:
        daily[e["user"]][e["day"]] += e["files"]
    alerts = []
    for user, role in USERS.items():
        hist = [v for d, v in daily[user].items() if d < TODAY]
        mean, sd = statistics.mean(hist), max(statistics.pstdev(hist), 1.0)
        today = [e for e in events if e["user"] == user and e["day"] == TODAY]
        total = daily[user].get(TODAY, 0)
        reasons, score = [], 0
        if any(e["resource"] not in ENTITLEMENTS[role] for e in today):
            reasons.append("R1 acesso fora do papel"); score += 3
        z = (total - mean) / sd
        if z > Z_LIMIT:
            reasons.append(f"R2 volume {total} arquivos (z={z:.1f})"); score += 2
        if any(e["hour"] in OFF_HOURS for e in today):
            reasons.append("R3 fora do horário"); score += 1
        if reasons:
            alerts.append({"user": user, "role": role, "score": score, "reasons": reasons,
                           "severity": "alta" if score >= 5 else "média" if score >= 2 else "baixa",
                           "attack": "T1078 / T1213"})
    return sorted(alerts, key=lambda a: -a["score"])


def run(out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    ev = generate()
    with (out_dir / "07_access_log.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(ev[0]))
        w.writeheader()
        w.writerows(ev)
    return {"alerts": detect(ev)}

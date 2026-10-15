"""Lab 03 - Pendrive achado no chão: como a defesa enxerga isso.

Ideia Feynman: o pendrive é uma porta nova na sua casa. A defesa não precisa
adivinhar a intenção de quem o largou; precisa perceber (1) uma porta nova
apareceu, (2) algo começou a rodar a partir dela, (3) o "pendrive" disse ser
teclado e disco ao mesmo tempo.

Tudo aqui é log SINTÉTICO. Nenhum código malicioso é gerado ou executado.
"""
from __future__ import annotations

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

ALLOWLIST = {"0951:1666"}  # pendrives corporativos aprovados (fictício)
WINDOW_SECONDS = 120


def generate_events(path: Path, seed: int = 42) -> Path:
    rng = random.Random(seed)
    t0 = datetime(2026, 10, 8, 9, 0, 0)
    ev = []
    for i in range(1, 6):
        host = f"WS-{i:03d}"
        for k in range(8):
            ev.append({"ts": (t0 + timedelta(minutes=rng.randint(0, 240))).isoformat(), "host": host,
                       "event": "process_start", "image": rng.choice(
                           ["C:\\Windows\\explorer.exe", "C:\\Program Files\\Office\\winword.exe",
                            "C:\\Program Files\\Browser\\browser.exe"]), "parent": "explorer.exe"})
        if i == 2:
            ev.append({"ts": (t0 + timedelta(minutes=30)).isoformat(), "host": host, "event": "device_connected",
                       "vid_pid": "0951:1666", "classes": ["mass_storage"], "drive": "E:"})
    # Cenário A: pendrive desconhecido + executável rodando a partir dele
    ta = t0 + timedelta(hours=1)
    ev.append({"ts": ta.isoformat(), "host": "WS-042", "event": "device_connected",
               "vid_pid": "1234:5678", "classes": ["mass_storage"], "drive": "E:"})
    ev.append({"ts": (ta + timedelta(seconds=40)).isoformat(), "host": "WS-042", "event": "process_start",
               "image": "E:\\leia-me.exe", "parent": "explorer.exe"})
    # Cenário B: dispositivo composto teclado + disco
    tb = t0 + timedelta(hours=2)
    ev.append({"ts": tb.isoformat(), "host": "WS-077", "event": "device_connected",
               "vid_pid": "abcd:0001", "classes": ["hid_keyboard", "mass_storage"], "drive": "F:"})
    ev.sort(key=lambda e: e["ts"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(e) for e in ev) + "\n", encoding="utf-8")
    return path


def load_events(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def detect(events: list[dict], allowlist: set[str] = ALLOWLIST) -> list[dict]:
    alerts = []
    inserts: dict[tuple[str, str], tuple[datetime, dict]] = {}
    for e in sorted(events, key=lambda x: x["ts"]):
        ts = datetime.fromisoformat(e["ts"])
        if e["event"] == "device_connected":
            drive = e.get("drive")
            unknown = e["vid_pid"] not in allowlist
            if drive:
                inserts[(e["host"], drive)] = (ts, e)
            if unknown and "mass_storage" in e["classes"]:
                alerts.append({"rule": "R1-unknown-removable-storage", "severity": "medium", "host": e["host"],
                               "detail": f"dispositivo {e['vid_pid']} fora da allowlist em {drive}",
                               "attack": "T1091"})
            if "hid_keyboard" in e["classes"] and "mass_storage" in e["classes"]:
                alerts.append({"rule": "R3-composite-keyboard-storage", "severity": "high", "host": e["host"],
                               "detail": f"{e['vid_pid']} se apresenta como teclado E disco",
                               "attack": "T1200"})
        elif e["event"] == "process_start":
            img = e["image"]
            drive = img[:2]
            key = (e["host"], drive)
            if key in inserts and (ts - inserts[key][0]).total_seconds() <= WINDOW_SECONDS:
                alerts.append({"rule": "R2-exec-from-removable", "severity": "high", "host": e["host"],
                               "detail": f"{img} executado {int((ts - inserts[key][0]).total_seconds())}s após inserir mídia",
                               "attack": "T1091"})
    return alerts


def run(out_dir: Path) -> dict:
    p = generate_events(out_dir / "03_usb_events.jsonl")
    alerts = detect(load_events(p))
    (out_dir / "03_usb_alerts.json").write_text(json.dumps(alerts, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"events_file": str(p), "alerts": alerts}

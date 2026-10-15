"""Lab 08 - Cadeia de custódia: queimar o laptop não é resposta a incidente.

Ideia Feynman: evidência é como gelo numa mesa quente: o que derrete primeiro
(memória) precisa ser guardado primeiro. E para provar que ninguém mexeu,
cada passo é lacrado com um carimbo (hash) ligado ao anterior, como uma corrente.
"""
from __future__ import annotations

import hashlib
import json

VOLATILITY_ORDER = ["cpu_cache", "memory_ram", "network_state", "running_processes",
                    "disk", "remote_logs", "archival_media"]
LOST_ON_POWER_OFF = {"cpu_cache", "memory_ram", "network_state", "running_processes"}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def collection_plan(sources: list[str]) -> list[str]:
    return sorted(sources, key=VOLATILITY_ORDER.index)


def lost_if_powered_off(sources: list[str]) -> list[str]:
    return [s for s in collection_plan(sources) if s in LOST_ON_POWER_OFF]


class CustodyLog:
    def __init__(self):
        self.entries: list[dict] = []

    @staticmethod
    def _hash_entry(e: dict) -> str:
        body = {k: v for k, v in e.items() if k != "entry_hash"}
        return sha256(json.dumps(body, sort_keys=True).encode())

    def add(self, item_id: str, data: bytes, actor: str, action: str, ts: str) -> dict:
        prev = self.entries[-1]["entry_hash"] if self.entries else "0" * 64
        e = {"seq": len(self.entries), "ts": ts, "actor": actor, "action": action,
             "item_id": item_id, "sha256": sha256(data), "prev": prev}
        e["entry_hash"] = self._hash_entry(e)
        self.entries.append(e)
        return e

    def verify(self, items: dict[str, bytes]) -> list[str]:
        problems, prev = [], "0" * 64
        for e in self.entries:
            if e["prev"] != prev:
                problems.append(f"seq {e['seq']}: elo quebrado na corrente")
            if self._hash_entry(e) != e["entry_hash"]:
                problems.append(f"seq {e['seq']}: registro alterado")
            prev = e["entry_hash"]
        first = {}
        for e in self.entries:
            first.setdefault(e["item_id"], e["sha256"])
        for item_id, h in first.items():
            if item_id in items and sha256(items[item_id]) != h:
                problems.append(f"{item_id}: conteúdo difere do hash na coleta")
        return problems


def run(out_dir=None) -> dict:
    items = {"ram.img": b"memoria-sintetica", "disk.img": b"disco-sintetico", "cctv.mp4": b"video-sintetico"}
    log = CustodyLog()
    for i, (k, v) in enumerate(items.items()):
        log.add(k, v, "perito-1", "coleta", f"2026-10-08T10:0{i}:00")
    log.add("disk.img", items["disk.img"], "perito-2", "transferencia", "2026-10-08T11:00:00")
    ok = log.verify(items)
    snapshot = json.dumps(log.entries, indent=2, ensure_ascii=False)
    tampered_item = dict(items, **{"cctv.mp4": b"video-ALTERADO"})
    t1 = log.verify(tampered_item)
    log.entries[1]["actor"] = "alguem-estranho"
    t2 = log.verify(items)
    srcs = ["disk", "memory_ram", "remote_logs", "network_state"]
    if out_dir is not None:
        from pathlib import Path
        out = Path(out_dir)
        out.mkdir(parents=True, exist_ok=True)
        (out / "08_custody_log.json").write_text(snapshot, encoding="utf-8")
    return {"integrity_ok": ok, "tampered_evidence": t1, "tampered_log": t2,
            "collection_plan": collection_plan(srcs), "lost_if_powered_off": lost_if_powered_off(srcs)}

"""Lab 06 - Dead man's switch: o dilema do "se eu sumir, solte as provas".

Ideia Feynman: é um botão que dispara quando você PARA de apertá-lo. Problema:
parar de apertar não significa que algo grave aconteceu (celular perdido, voo,
sono). Projeto ingênuo = alarme falso. Projeto melhor = aviso + prazo de
tolerância + confirmação humana (quórum de guardiões).

SEGURANÇA: tudo é simulação. A "ação" apenas registra uma mensagem numa lista
em memória. Nenhum envio, vazamento ou conteúdo real existe aqui.
"""
from __future__ import annotations

import math
import random
from enum import Enum


class State(Enum):
    ARMED = "armado"
    WARNED = "avisado"
    TRIGGERED = "disparado"


class Switch:
    def __init__(self, timeout_h=5.0, grace_h=0.0, quorum=0, vote_fn=None, vote_delay_h=1.0):
        self.timeout_h, self.grace_h, self.quorum = timeout_h, grace_h, quorum
        self.vote_fn, self.vote_delay_h = vote_fn, vote_delay_h
        self.state = State.ARMED
        self.last = 0.0
        self.warned_at = None
        self.voted = False
        self.lost_votes = 0
        self.triggered_at = None
        self.outbox: list[tuple[float, str]] = []

    def checkin(self, now: float) -> None:
        if self.state is State.TRIGGERED:
            return
        self.last, self.state, self.warned_at = now, State.ARMED, None
        self.voted, self.lost_votes = False, 0

    def _trigger(self, now: float) -> None:
        self.state, self.triggered_at = State.TRIGGERED, now
        self.outbox.append((now, "AÇÃO SIMULADA (nenhum envio real)"))

    def tick(self, now: float) -> None:
        if self.state is State.TRIGGERED or now - self.last < self.timeout_h:
            return
        if self.grace_h == 0 and self.quorum == 0:
            self._trigger(now)
            return
        if self.state is State.ARMED:
            self.state, self.warned_at = State.WARNED, now
            self.outbox.append((now, "aviso ao dono"))
        if not self.voted and self.vote_fn and now - self.warned_at >= self.vote_delay_h:
            self.lost_votes, self.voted = self.vote_fn(), True
        if now - self.warned_at >= self.grace_h and self.lost_votes >= self.quorum:
            self._trigger(now)


def _one_month(rng: random.Random, days: int = 30, incap_day: int = 20) -> dict:
    step = 0.25
    n = int(days * 24 / step)
    incap_i = int(incap_day * 24 / step)
    away = [False] * n
    i = int(rng.expovariate(1 / (40 / step)))
    while i < incap_i:
        length = int(rng.lognormvariate(math.log(4 / step), 0.8))
        for k in range(i, min(i + length, n)):
            away[k] = True
        i += length + int(rng.expovariate(1 / (40 / step)))
    state = {"incap": False}

    def votes() -> int:
        p = 0.9 if state["incap"] else 0.1
        return sum(rng.random() < p for _ in range(3))

    naive = Switch(timeout_h=5.0)
    hard = Switch(timeout_h=5.0, grace_h=3.0, quorum=2, vote_fn=votes)
    last_checkin = 0.0
    for idx in range(n):
        now = idx * step
        state["incap"] = idx >= incap_i
        if not state["incap"] and not away[idx] and now - last_checkin >= 4.0:
            naive.checkin(now)
            hard.checkin(now)
            last_checkin = now
        naive.tick(now)
        hard.tick(now)
    t_incap = incap_i * step
    out = {}
    for name, sw in (("naive", naive), ("hardened", hard)):
        if sw.triggered_at is None:
            out[name] = ("missed", None)
        elif sw.triggered_at < t_incap:
            out[name] = ("false", None)
        else:
            out[name] = ("ok", sw.triggered_at - t_incap)
    return out


def simulate(n_runs: int = 200, seed: int = 7) -> dict:
    rng = random.Random(seed)
    runs = [_one_month(rng) for _ in range(n_runs)]
    res = {}
    for name in ("naive", "hardened"):
        kinds = [r[name][0] for r in runs]
        delays = [r[name][1] for r in runs if r[name][1] is not None]
        res[name] = {"false_trigger_rate": round(kinds.count("false") / n_runs, 3),
                     "missed_rate": round(kinds.count("missed") / n_runs, 3),
                     "mean_delay_h": round(sum(delays) / len(delays), 2) if delays else None}
    return res


def run(out_dir=None) -> dict:
    import json
    from pathlib import Path
    result = simulate()
    if out_dir is not None:
        out = Path(out_dir)
        out.mkdir(parents=True, exist_ok=True)
        (out / "06_deadman_report.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result

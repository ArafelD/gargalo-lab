"""Confere, por código, cada "resultado de referência" da tabela do artigo (seed fixa)."""
from __future__ import annotations

import tempfile
from pathlib import Path

from . import beacon_hunt, custody, deadman, enhance_myth, exif_osint, insider, triangulation, usb_detect


def run_checks(out_dir: Path | None = None) -> list[dict]:
    rows: list[dict] = []

    def add(lab: str, claim: str, ok: bool, observed: str) -> None:
        rows.append({"lab": lab, "claim": claim, "ok": bool(ok), "observed": observed})

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(out_dir) if out_dir else Path(d)

        r = enhance_myth.run(tmp)
        add("01", "miniatura com ≈1,56% dos pixels", abs(r["info_kept_pct"] - 1.56) < 0.01, f'{r["info_kept_pct"]}%')
        add("01", "≈15 dB de qualidade no 'enhance' bicúbico", 14 <= r["psnr_db_bicubic"] <= 16, f'{r["psnr_db_bicubic"]} dB')
        add("01", "detalhe fino cai de ≈0,134 para ≈0,00008",
            0.12 <= r["hf_energy_original"] <= 0.15 and r["hf_energy_upscaled"] < 0.0005,
            f'{r["hf_energy_original"]} -> {r["hf_energy_upscaled"]}')
        add("01", "duas imagens diferentes viram a mesma miniatura",
            r["collision_demo"]["originals_differ"] and r["collision_demo"]["downscaled_identical"], str(r["collision_demo"]))

        r = exif_osint.run(tmp)
        add("02", "GPS presente antes e ausente depois", r["before"]["gps"] is not None and r["after"]["gps"] is None,
            f'antes={r["before"]["gps"]} depois={r["after"]["gps"]}')

        r = usb_detect.run(tmp)
        got = {(a["rule"], a["host"]) for a in r["alerts"]}
        want = {("R1-unknown-removable-storage", "WS-042"), ("R2-exec-from-removable", "WS-042"),
                ("R1-unknown-removable-storage", "WS-077"), ("R3-composite-keyboard-storage", "WS-077")}
        add("03", "as três regras disparam só nos cenários esperados", got == want, f"{len(got)} alertas")

        r = beacon_hunt.run(tmp)
        dsts = {s["dst"] for s in r["suspects"]}
        add("04", "dois beacons achados e NTP legítimo ignorado", dsts == {"203.0.113.50", "203.0.113.77"}, str(sorted(dsts)))

        r = triangulation.run(tmp)
        tab = {(x["baseline_m"], x["noise_px"]): x["mean_abs_error_cm"] for x in r["error_table"]}
        add("05", "mundos de escalas diferentes geram pixels idênticos", r["ambiguity"]["identical_pixels"], str(r["ambiguity"]))
        add("05", "≈2 cm de erro (câmeras a 1,5 m, ruído 1 px)", 1.0 <= tab[(1.5, 1.0)] <= 4.0, f"{tab[(1.5, 1.0)]} cm")
        add("05", "≈81 cm de erro (câmeras a 10 cm, ruído 1 px)", 60 <= tab[(0.1, 1.0)] <= 100, f"{tab[(0.1, 1.0)]} cm")

        r = deadman.run(tmp)
        n, h = r["naive"], r["hardened"]
        add("06", "disparo falso: 100% (ingênuo) contra ≈8,5% (quórum)",
            n["false_trigger_rate"] == 1.0 and abs(h["false_trigger_rate"] - 0.085) < 0.02,
            f'{n["false_trigger_rate"]} vs {h["false_trigger_rate"]}')
        add("06", "casos perdidos ≈5,5% e atraso ≈5,8 h",
            abs(h["missed_rate"] - 0.055) < 0.02 and 5.5 <= h["mean_delay_h"] <= 6.1,
            f'{h["missed_rate"]} / {h["mean_delay_h"]} h')

        r = insider.run(tmp)
        al = r["alerts"]
        ana = next((a for a in al if a["user"] == "ana"), None)
        add("07", "fora do papel + volume + madrugada = severidade alta",
            bool(al) and al[0]["user"] == "charlie" and al[0]["severity"] == "alta", str(al[0]["reasons"]) if al else "sem alertas")
        add("07", "volume alto dentro do papel = severidade média",
            ana is not None and ana["severity"] == "média" and not any(x.startswith("R1") for x in ana["reasons"]),
            str(ana["reasons"]) if ana else "sem alerta")

        r = custody.run(tmp)
        add("08", "adulteração de evidência ou de registro é detectada",
            r["integrity_ok"] == [] and bool(r["tampered_evidence"]) and bool(r["tampered_log"]),
            f'{len(r["tampered_evidence"])} + {len(r["tampered_log"])} problemas')
        add("08", "desligar a máquina perde memória e estado de rede; memória coletada antes do disco",
            set(r["lost_if_powered_off"]) == {"memory_ram", "network_state"}
            and r["collection_plan"].index("memory_ram") < r["collection_plan"].index("disk"),
            f'perde={r["lost_if_powered_off"]}')
    return rows


def render(rows: list[dict]) -> str:
    lines = ["# Verificação dos resultados de referência", "", "| Lab | Afirmação do artigo | Resultado | Observado |", "|---|---|---|---|"]
    for r in rows:
        lines.append(f'| {r["lab"]} | {r["claim"]} | {"✅" if r["ok"] else "❌"} | {r["observed"]} |')
    total, ok = len(rows), sum(r["ok"] for r in rows)
    lines += ["", f"**{ok}/{total} verificações passaram.**"]
    return "\n".join(lines)


def main(out_dir: Path | None = None) -> int:
    rows = run_checks()
    text = render(rows)
    print(text)
    if out_dir is not None:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "REFERENCE_CHECK.md").write_text(text + "\n", encoding="utf-8")
    return 0 if all(r["ok"] for r in rows) else 1

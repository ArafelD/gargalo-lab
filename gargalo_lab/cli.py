from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import (beacon_hunt, custody, deadman, enhance_myth, exif_osint, insider,
               triangulation, usb_detect, verify)

LABS = {
    "enhance": enhance_myth.run,     # 01
    "exif": exif_osint.run,          # 02
    "usb": usb_detect.run,           # 03
    "beacon": beacon_hunt.run,       # 04
    "photo": triangulation.run,      # 05
    "deadman": deadman.run,          # 06
    "insider": insider.run,          # 07
    "custody": custody.run,          # 08
}
ALIASES = {f"{i + 1:02d}": name for i, name in enumerate(LABS)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="gargalo_lab", description="gargalo-lab: 8 laboratórios defensivos (dados sintéticos)")
    ap.add_argument("lab", choices=[*LABS, *ALIASES, "all", "verify"],
                    help="nome do lab, número 01..08, 'all' ou 'verify' (confere os resultados de referência)")
    ap.add_argument("--out", default="output", help="pasta de saída (padrão: output)")
    a = ap.parse_args(argv)
    out = Path(a.out)
    if a.lab == "verify":
        return verify.main(out)
    key = ALIASES.get(a.lab, a.lab)
    for n in (list(LABS) if key == "all" else [key]):
        print(f"\n=== Lab {list(LABS).index(n) + 1:02d}: {n} ===")
        print(json.dumps(LABS[n](out), indent=2, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

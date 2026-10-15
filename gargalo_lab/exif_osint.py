"""Lab 02 - O que a sua foto conta sobre você (metadados EXIF).

Ideia Feynman: toda foto carrega uma "etiqueta" escondida atrás da imagem
(onde, quando, em qual aparelho). Quem só olha a imagem não vê. Quem lê a
etiqueta vê tudo. Defesa: tirar a etiqueta antes de compartilhar.
Coordenadas usadas aqui são de um marco público (Praça dos Três Poderes, Brasília).
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image

GPS_IFD = 0x8825
SAMPLE_LAT, SAMPLE_LON = -15.7998, -47.8645


def _to_dms(value: float) -> tuple[float, float, float]:
    value = abs(value)
    deg = int(value)
    minutes = int((value - deg) * 60)
    seconds = round((value - deg - minutes / 60) * 3600, 4)
    return float(deg), float(minutes), float(seconds)


def _from_dms(dms, ref: str) -> float:
    d, m, s = (float(x) for x in dms)
    val = d + m / 60 + s / 3600
    return -val if ref in ("S", "W") else val


def create_sample_with_gps(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (200, 120), (30, 90, 160))
    exif = Image.Exif()
    exif[0x010F] = "LabCam"
    exif[0x0110] = "LC-1000"
    exif[0x0132] = "2026:10:08 09:15:00"
    gps = exif.get_ifd(GPS_IFD)
    gps[1] = "S" if SAMPLE_LAT < 0 else "N"
    gps[2] = _to_dms(SAMPLE_LAT)
    gps[3] = "W" if SAMPLE_LON < 0 else "E"
    gps[4] = _to_dms(SAMPLE_LON)
    img.save(path, "JPEG", exif=exif)
    return path


def read_metadata(path: Path) -> dict:
    with Image.open(path) as img:
        exif = img.getexif()
        gps = exif.get_ifd(GPS_IFD)
        meta = {
            "make": exif.get(0x010F),
            "model": exif.get(0x0110),
            "datetime": exif.get(0x0132),
            "gps": None,
        }
        if gps and 2 in gps and 4 in gps:
            meta["gps"] = {
                "lat": round(_from_dms(gps[2], gps.get(1, "N")), 5),
                "lon": round(_from_dms(gps[4], gps.get(3, "E")), 5),
            }
    return meta


def strip_metadata(src: Path, dst: Path) -> Path:
    """Recria a imagem só com os pixels (sem nenhuma etiqueta)."""
    with Image.open(src) as img:
        clean = Image.new(img.mode, img.size)
        clean.paste(img)
        clean.save(dst, "JPEG")
    return dst


def risk_report(meta: dict) -> list[str]:
    findings = []
    if meta.get("gps"):
        findings.append("ALTO: coordenadas GPS presentes (revela onde a foto foi tirada)")
    if meta.get("datetime"):
        findings.append("MÉDIO: data/hora presentes (revela quando você estava lá)")
    if meta.get("make") or meta.get("model"):
        findings.append("BAIXO: marca/modelo do aparelho (ajuda a correlacionar fotos)")
    return findings or ["Nenhum metadado sensível encontrado"]


def run(out_dir: Path) -> dict:
    sample = create_sample_with_gps(out_dir / "02_sample_with_gps.jpg")
    before = read_metadata(sample)
    cleaned = strip_metadata(sample, out_dir / "02_sample_clean.jpg")
    after = read_metadata(cleaned)
    return {"before": before, "after": after, "risks_before": risk_report(before), "risks_after": risk_report(after)}

#!/usr/bin/env python3
"""Generate per-seat QR codes (with printed seat label) and a seat registry.

Each PNG contains the QR code AND the seat identifier printed below it, so
installation crews can tell at a glance which code goes where — even when
the QR itself fails to scan (damaged, wrong angle, etc.).

Example:
  python tools/generate_seat_qr.py \
    --base-url https://club.github.io/stadium-choreo-web/ \
    --stand "Tribune Nord" --block A --rows 50 --cols 50 \
    --out dist/qr-tribune-nord-a

  # With zone/sector (full stadium hierarchy):
  python tools/generate_seat_qr.py \
    --base-url https://club.github.io/stadium-choreo-web/ \
    --stand "Tribune Nord" --zone nord --sector 1 --block A \
    --rows 50 --cols 50 --out dist/qr-tribune-nord-a

The script creates:
  - seat-registry.csv   : all seats, URLs and QR file paths
  - qrs/*.png           : one labelled QR PNG per seat
  - print-sheet.html    : printable grid of all QRs (for A4/A3 sheets)
"""
from __future__ import annotations

import argparse
import csv
import html as html_mod
from pathlib import Path
from urllib.parse import urlencode

try:
    import qrcode
    from PIL import Image, ImageDraw, ImageFont
except ImportError as exc:
    raise SystemExit(
        "Missing dependencies. Install with:\n"
        "  pip install -r requirements.txt\n"
        "(requires: qrcode[pil]  which includes Pillow)"
    ) from exc


# ── Helpers ───────────────────────────────────────────────────────────────────

def seat_id(row: int, col: int) -> str:
    return f"R{row:02d}-C{col:02d}"


def build_url(
    base_url: str,
    stand: str,
    block: str,
    row: int,
    seat: int,
    zone: str = "",
    sector: str = "",
    color: str = "",
) -> str:
    params: dict = {"stand": stand, "block": block, "row": row, "seat": seat}
    if zone:
        params["zone"] = zone
    if sector:
        params["sector"] = sector
    if color:
        params["color"] = color
    sep = "&" if "?" in base_url else "?"
    return base_url.rstrip("/") + "/" + sep + urlencode(params)


def _load_font(size: int) -> ImageFont.ImageFont:
    """Try to load a clean system font; fall back to PIL built-in."""
    candidates = [
        # Linux
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        # macOS
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNSDisplay.ttf",
        # Windows
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except (OSError, IOError):
            continue
    # PIL ≥ 9.2 supports size argument on load_default
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def make_labeled_qr(
    url: str,
    stand: str,
    block: str,
    sid: str,
    zone: str = "",
    sector: str = "",
    box_size: int = 10,
    border: int = 2,
) -> Image.Image:
    """Return a QR PNG with the seat identifier and stand info printed below."""

    # QR code (error correction M = ~15 % damage tolerance)
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=border,
    )
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    qr_w, qr_h = qr_img.size

    # Build location string for label lines
    parts = [p for p in [stand, f"Zone {zone}" if zone else "", f"Secteur {sector}" if sector else "", f"Bloc {block}"] if p]
    location_line = "  ·  ".join(parts)

    font_id   = _load_font(16)  # large: seat ID
    font_loc  = _load_font(11)  # small: stand + block path

    # Measure text heights to size the label area
    tmp = Image.new("RGB", (1, 1))
    tmp_draw = ImageDraw.Draw(tmp)
    _, _, _, id_h  = tmp_draw.textbbox((0, 0), sid, font=font_id)
    _, _, _, loc_h = tmp_draw.textbbox((0, 0), location_line, font=font_loc)

    padding     = 10
    separator_h = 2
    label_h     = padding + separator_h + padding // 2 + id_h + 4 + loc_h + padding

    # Compose final image
    total_h = qr_h + label_h
    canvas  = Image.new("RGB", (qr_w, total_h), "white")
    canvas.paste(qr_img, (0, 0))

    draw = ImageDraw.Draw(canvas)

    # Separator line
    sep_y = qr_h + padding // 2
    draw.line([(12, sep_y), (qr_w - 12, sep_y)], fill="#cccccc", width=1)

    # Seat ID (large, bold, centered)
    id_y = sep_y + padding // 2
    draw.text((qr_w // 2, id_y), sid, fill="#000000", anchor="mt", font=font_id)

    # Location line (small, grey, centered)
    loc_y = id_y + id_h + 4
    draw.text((qr_w // 2, loc_y), location_line, fill="#555555", anchor="mt", font=font_loc)

    return canvas


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description="Generate labelled per-seat QR codes.")
    ap.add_argument("--base-url",  required=True, help="Public URL, e.g. https://org.github.io/stadium-choreo-web/")
    ap.add_argument("--stand",     default="Tribune Nord",  help="Stand name")
    ap.add_argument("--zone",      default="",              help="Zone ID (optional, for full-stadium hierarchy)")
    ap.add_argument("--sector",    default="",              help="Sector ID (optional)")
    ap.add_argument("--block",     default="A",             help="Block ID")
    ap.add_argument("--rows",      type=int, required=True, help="Number of rows")
    ap.add_argument("--cols",      type=int, required=True, help="Seats per row")
    ap.add_argument("--color",     default="",              help="Hex color to embed in URL (e.g. #2563eb)")
    ap.add_argument("--box-size",  type=int, default=10,    help="QR module size in pixels (default 10)")
    ap.add_argument("--out",       default="dist/qr",       help="Output directory")
    ap.add_argument("--sample",    type=int, default=0,     help="Generate only first N rows/cols for quick tests")
    args = ap.parse_args()

    rows = min(args.rows, args.sample) if args.sample else args.rows
    cols = min(args.cols, args.sample) if args.sample else args.cols

    out     = Path(args.out)
    qr_dir  = out / "qrs"
    qr_dir.mkdir(parents=True, exist_ok=True)

    registry_path = out / "seat-registry.csv"
    fieldnames = ["stand", "zone", "sector", "block", "row", "seat", "seat_id", "url", "qr_file"]

    print(f"Generating {rows * cols} QR codes → {out}")

    with registry_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in range(1, rows + 1):
            for c in range(1, cols + 1):
                sid  = seat_id(r, c)
                url  = build_url(args.base_url, args.stand, args.block, r, c,
                                 zone=args.zone, sector=args.sector, color=args.color)
                fname = f"{args.block}-{sid}.png"
                img   = make_labeled_qr(url, args.stand, args.block, sid,
                                        zone=args.zone, sector=args.sector,
                                        box_size=args.box_size)
                img.save(qr_dir / fname)
                writer.writerow({
                    "stand": args.stand, "zone": args.zone, "sector": args.sector,
                    "block": args.block, "row": r, "seat": c,
                    "seat_id": sid, "url": url,
                    "qr_file": f"qrs/{fname}",
                })
            # Progress every 10 rows
            if r % 10 == 0:
                print(f"  Row {r}/{rows} done…")

    # Print sheet (HTML) ───────────────────────────────────────────────────────
    cards = []
    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            sid  = seat_id(r, c)
            fname = f"qrs/{args.block}-{sid}.png"
            loc_parts = [p for p in [args.stand, f"Zone {args.zone}" if args.zone else "",
                                     f"Sec. {args.sector}" if args.sector else "",
                                     f"Bloc {args.block}"] if p]
            loc = "  ·  ".join(loc_parts)
            cards.append(
                f'<div class="card">'
                f'<img src="{html_mod.escape(fname)}" loading="lazy">'
                f'<b>{html_mod.escape(sid)}</b>'
                f'<span>{html_mod.escape(loc)}</span>'
                f'</div>'
            )

    title_parts = [p for p in [args.stand, f"Zone {args.zone}" if args.zone else "",
                                f"Secteur {args.sector}" if args.sector else "",
                                f"Bloc {args.block}"] if p]
    title = " / ".join(title_parts)

    sheet = f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>QR sièges — {html_mod.escape(title)}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 16px; }}
    h1 {{ font-size: 16px; margin-bottom: 12px; }}
    .meta {{ font-size: 12px; color: #555; margin-bottom: 16px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap: 8px; }}
    .card {{ border: 1px solid #ddd; padding: 6px; text-align: center; break-inside: avoid; border-radius: 6px; }}
    .card img {{ width: 100%; height: auto; display: block; }}
    .card b {{ display: block; font-size: 12px; margin-top: 4px; }}
    .card span {{ display: block; font-size: 10px; color: #666; }}
    @media print {{
      .grid {{ grid-template-columns: repeat(5, 1fr); gap: 6px; }}
      body {{ margin: 8px; }}
    }}
  </style>
</head>
<body>
  <h1>QR sièges — {html_mod.escape(title)}</h1>
  <p class="meta">{rows} rangées × {cols} sièges = {rows * cols} QR codes &nbsp;|&nbsp; Généré le {__import__('datetime').date.today()}</p>
  <div class="grid">{''.join(cards)}</div>
</body>
</html>"""

    (out / "print-sheet.html").write_text(sheet, encoding="utf-8")

    print(f"\n✓ {rows * cols} QR codes avec labels → {qr_dir}")
    print(f"✓ Registre CSV         → {registry_path}")
    print(f"✓ Feuille d'impression → {out / 'print-sheet.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

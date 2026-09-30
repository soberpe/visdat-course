"""Generate the QR codes used on the slides.

The links live here, in the repository, and the PNG files are generated from
them. That way a changed link is a one line diff plus a rerun, and nobody has
to remember which image belonged to which URL.

Usage:

    pip install segno
    python tools/make-qr.py

The script only writes files that are listed in CODES below and reports what
it wrote.
"""

from pathlib import Path

import segno

ROOT = Path(__file__).resolve().parent.parent

# output path, relative to the repository root -> the URL it encodes
#
# The short link of the form, not its long response URL. Shorter text means a
# coarser grid, and a coarse grid is what survives a projector and the back row.
# The long form of the same link, in case the short one ever has to be rebuilt:
# https://forms.cloud.microsoft/Pages/ResponsePage.aspx?id=c0uN-LJrmkurx-uW5aZAfDDTS6A6jlNGux0pczJABfZUQ1VGUFFWQkZKTDU1VEhWUkYyUUVLMVlQRS4u
CODES = {
    "static/img/kickoff/forms-qr.png": "https://forms.cloud.microsoft/e/GFLB4sP5Dx",
}

# Error correction M keeps a fifth of the code redundant, which is what makes a
# scan work on a projector with reflections on the screen. The dark colour is
# the one the slide theme uses, not pure black.
ERROR_CORRECTION = "m"
DARK = "#16242c"
SCALE = 10
BORDER = 2


def main() -> None:
    for target, url in CODES.items():
        path = ROOT / target
        path.parent.mkdir(parents=True, exist_ok=True)
        code = segno.make(url, error=ERROR_CORRECTION)
        code.save(path, scale=SCALE, border=BORDER, dark=DARK, light="#ffffff")
        modules = code.symbol_size(scale=1, border=0)[0]
        print(f"{target}: version {code.version}, {modules}x{modules} modules")


if __name__ == "__main__":
    main()

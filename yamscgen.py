try:
    import cairosvg
    cairosvg_installed = True
except ImportError:
    cairosvg_installed = False

import argparse
import sys
from pathlib import Path
import logging

from src.builder import Builder
from src.parser import Parser
from src.colored_formatter import ColoredFormatter

handler = logging.StreamHandler()
handler.setFormatter(ColoredFormatter())
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.INFO)


parser = argparse.ArgumentParser(
    prog="Diagrams",
    description="Generate flexible and customizable sequence diagrams.",
    epilog="Written by Julien Van Roy under supervision of Prof. Bruno Quoitin (UMons).",
)

parser.add_argument(
    "-i",
    "--input",
    help="The input file to read from. If omitted, reads from the standard input.",
    required=False,
    type=Path,
)
parser.add_argument(
    "-o",
    "--output",
    help="The output file to write to.",
    required=True,
    type=Path,
)
parser.add_argument("-t", "--type", choices=["svg", "png", "pdf"], default="svg")
args = parser.parse_args()

if args.type in ('pdf', 'png') and not cairosvg_installed:
    sys.exit("Unable to generate a PNG/PDF because cairosvg is not installed.")

if not args.input:
    # read from stdin (until EOF: CTRL + D)
    text_input = "".join(line for line in sys.stdin)
else:
    # read from a file
    with open(args.input) as f:
        text_input = f.read()

svg = Builder(parser=Parser(text_input)).generate()

if args.type == 'png':
    cairosvg.svg2png(svg, write_to=str(args.output))
elif args.type == 'pdf':
    cairosvg.svg2pdf(svg, write_to=str(args.output))
else:
    with open(args.output, "wb+") as f:
        f.write(svg)

# import biblatex2bibtex
import argparse
import logging
import sys
from pathlib import Path
from biblatex2bibtex import convert


log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="convert biblatex to bibtex files")
    parser.add_argument(
        "biblatexfiles", nargs="+", help="biblatex file(s) to be converted", type=str
    )
    parser.add_argument(
        "--output", nargs="?", help="bibtex output file", type=str, default=None
    )
    args = parser.parse_args()

    for filename in args.biblatexfiles:
        in_file = Path(filename)
        if not in_file.is_file() or in_file.suffix != ".bib":
            log.error("Please enter a path to a .bib file")
            sys.exit()

    if args.output is None:
        out_file = Path(in_file.parent / f"{in_file.stem}_bibtex{in_file.suffix}")
        log.warning(f"No bibtex output specified, saving to {out_file}")
    else:
        out_file = Path(args.output)

    convert(args.biblatexfiles, out_file)

# import biblatex2bibtex
import argparse
from pathlib import Path
from biblatex2bibtex import convert


def main():

    parser = argparse.ArgumentParser(description="convert biblatex to bibtex files")
    parser.add_argument("biblatexfile", help="biblatex file to be converted", type=str)
    parser.add_argument(
        "bibtexfile", nargs="?", help="bibtex output", type=str, default=None
    )
    args = parser.parse_args()

    in_file = Path(args.biblatexfile)
    if not in_file.is_file() or in_file.suffix != ".bib":
        print("Please enter a path to an existing .bib file")

    if args.bibtexfile is None:
        out_file = Path(in_file.parent / f"{in_file.stem}_out{in_file.suffix}")
    else:
        out_file = Path(args.bibtexfile)
    print(in_file, out_file)

    convert(in_file, out_file)

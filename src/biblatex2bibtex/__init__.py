import logging
import re
import subprocess
from pathlib import Path
import bibtexparser
import colorlog
import pkg_resources
from pybtex.database.input import bibtex


handler = colorlog.StreamHandler(None)
handler.setFormatter(
    colorlog.ColoredFormatter("%(log_color)s%(levelname)-7s%(reset)s %(message)s")
)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.propagate = True
log.addHandler(handler)


__author__ = "Florian Matter"
__email__ = "fmatter@mailbox.org"
__version__ = "0.0.4"

macro_expr = re.compile(r"\\.*?\{(?P<content>.*?)\}")


def remove_macros(s):
    return macro_expr.sub(r"\g<content>", s)


def preprocess(biblatex_file):
    biblatex_file = Path(biblatex_file)
    bib_data = bibtex.Parser().parse_file(biblatex_file)
    for entry in bib_data.entries.values():
        if entry.type == "collection":
            entry.fields["booktitle"] = entry.fields["title"]
    temp_file = (
        biblatex_file.parent / f"{biblatex_file.stem}_temp{biblatex_file.suffix}"
    )
    bib_data.to_file(temp_file)

    with open(temp_file, "r", encoding="utf-8") as f:
        content = remove_macros(f.read())
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(content)

    conf_file = pkg_resources.resource_filename(
        "biblatex2bibtex", "data/biblatex2bibtex.conf"
    )
    subprocess.run(
        f"biber --tool --configfile={conf_file} --output-resolve --output-file='{temp_file}' {temp_file}",
        shell=True,
        check=True,
    )
    Path(f"{temp_file}.blg").unlink()
    return temp_file


def modify(temp_file):
    with open(temp_file, "r", encoding="utf-8") as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    for entry in bib_database.entries:
        entry["title"] = entry["title"].replace("{", "").replace("}", "")
        if "booktitle" in entry:
            entry["booktitle"] = entry["booktitle"].replace("{", "").replace("}", "")
        if "pages" in entry:
            entry["pages"] = entry["pages"].replace("--", "–")
        replace = {
            "date": "year",
            "location": "address",
            "journaltitle": "journal",
            "issue": "number",
            "origdate": "year",
            "school": "institution",
            "maintitle": "booktitle",
        }
        for k, v in replace.items():
            if k in entry:
                entry[v] = entry[k]
                del entry[k]
        if "year" in entry and "-" in entry["year"]:
            entry["year"] = entry["year"].split("-")[0]
        if "note" in entry and entry["note"] == "\\textsc{ms}":
            del entry["note"]
            entry["howpublished"] = "Manuscript"
    temp_file.unlink()
    return bib_database


def convert(biblatex_files, bibtex_output):
    temp_files = []
    for biblatex_file in biblatex_files:
        temp_files.append(preprocess(biblatex_file))

    databases = []
    for temp_file in temp_files:
        databases.append(modify(temp_file))

    with open(bibtex_output, "w", encoding="utf-8") as bibtex_file:
        for database in databases:
            bibtexparser.dump(database, bibtex_file)

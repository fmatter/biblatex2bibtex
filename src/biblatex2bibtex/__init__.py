import bibtexparser
from pathlib import Path
import pkg_resources
import subprocess
from pybtex.database.input import bibtex

def convert(path, outpath):

    parser = bibtex.Parser()
    bib_data = parser.parse_file(path)
    for bibkey, entry in bib_data.entries.items():
        if entry.type == "collection":
            entry.fields["booktitle"] = entry.fields["title"]
    bib_data.to_file(outpath)

    conf_file = pkg_resources.resource_filename('biblatex2bibtex', 'data/biblatex2bibtex.conf')
    cmd = f"biber --tool --configfile={conf_file} --output-resolve --output-file='{outpath}' {outpath}"

    subprocess.run(cmd, shell=True, check=True)
    Path(f"{outpath}.blg").unlink()

    with open(outpath) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    for i in bib_database.entries:
        i["title"] = i["title"].replace("{", "").replace("}", "")
        if "booktitle" in i:
            i["booktitle"] = i["booktitle"].replace("{", "").replace("}", "")
        if "pages" in i:
            i["pages"] = i["pages"].replace("--", "–")
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
            if k in i:
                i[v] = i[k]
                del i[k]
        if "note" in i and i["note"] == "\\textsc{ms}":
            del i["note"]
            i["howpublished"] = "Manuscript"

    with open(outpath, "w") as bibtex_file:
        bibtexparser.dump(bib_database, bibtex_file)
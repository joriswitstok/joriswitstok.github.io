# Import the requests package and set your token in a variable for later use
import argparse
import requests
from urllib.parse import urlencode
import json
from datetime import date
current_date = date.today().strftime("%-d %B, %Y")

exclude_bibcodes = ["2024Natur.630E...2M", "2025MNRAS.538..280U"]
exclude_major_contr_bibcodes = ["2025ApJ...988L...5N"]

# Retrieve API token as argument
parser = argparse.ArgumentParser()
parser.add_argument('-t', "--token", help="API token for ADS")
token = parser.parse_args().token
headers = {'Authorization': 'Bearer ' + token}

def get_query_url(query):
    return "https://api.adsabs.harvard.edu/v1/search/query?{}".format(urlencode(query))

# Encode query and retrieve all bibcodes
query_all = {'q': 'author:("Witstok, Joris")'}
n_records = requests.get(get_query_url(query_all), headers=headers).json()["response"]["numFound"]
print("Found {:d} ADS records".format(n_records))
query_all.update(rows=n_records)

query_bib = query_all.copy()
query_bib["fl"] = "bibcode"
bibcodes = [r["bibcode"] for r in requests.get(get_query_url(query_bib), headers=headers).json()["response"]["docs"]]
assert all([bibcode in bibcodes for bibcode in exclude_bibcodes])

# Retrieve total number of publication records
query_pub = query_all.copy()
query_pub['q'] += " bibstem:(-jwst.prop) (-yCat) (-AAS) (-eas..conf) (-hst..prop) (-IAUS) (-Obs)"
query_pub["fl"] = "bibcode,author,title,bibstem,volume,page,year,doi,citation_count"
query_pub["sort"] = "date desc,first_author asc"
publications = requests.get(get_query_url(query_pub), headers=headers).json()
n_papers_tot = publications["response"]["numFound"]

pub_dicts = {}
first_author_bibcodes = []
major_contr_bibcodes = []

title_replacements = {"z   ": "z ~ ", r"$\alpha$": 'α'}
journal_bibstems = {"arXiv": "arXiv e-prints", "A&A": "_Astronomy and Astrophysics_", "ARA&A": "_Annual Review of Astronomy and Astrophysics_",
                    "ApJ": "_The Astrophysical Journal_", "ApJL": "_The Astrophysical Journal Letters_", "ApJS": "_The Astrophysical Journal Supplement Series_",
                    "NatAs": "_Nature Astronomy_", "Natur": "_Nature_", "MNRAS": "_Monthly Notices of the Royal Astronomical Society_",
                    "PASP": "_Publications of the Astronomical Society of the Pacific_",}
trim_first_names = lambda authors: [", ".join([a if ai == 0 else a[0] + '.' for ai, a in enumerate(a.split(", "))]) for a in authors]
for publication in publications["response"]["docs"]:
    if publication["bibcode"] in exclude_bibcodes:
        n_papers_tot -= 1
        continue
    pub_dict = {"ai": ["Witstok" in a for a in publication["author"]].index(True)}

    pub_dict["href"] = "https://doi.org/{}".format(publication["doi"][0]) if "doi" in publication else "https://ui.adsabs.harvard.edu/abs/{}".format(publication["bibcode"])
    if any([tr in publication["title"][0] for tr in title_replacements]):
        for tr in title_replacements:
            publication["title"][0] = publication["title"][0].replace(tr, title_replacements[tr])
    pub_dict["title"] = publication["title"][0]
    
    if pub_dict["ai"] == 0:
        first_author_bibcodes.append(publication["bibcode"])
    elif pub_dict["ai"] < 3 or (pub_dict["ai"] < 5 and len(publication["author"]) > 5) and publication["bibcode"] not in exclude_major_contr_bibcodes:
        major_contr_bibcodes.append(publication["bibcode"])
    
    if pub_dict["ai"] < 5 and len(publication["author"]) > 5:
        pub_dict["authors"] = ", ".join(trim_first_names(publication["author"][slice(None, 4 if pub_dict["ai"] == 0 else pub_dict["ai"]+1)])) + ", et al."
    else:
        pub_dict["authors"] = ", ".join(trim_first_names(publication["author"]))
    pub_dict["year"] = publication["year"]
    if publication["bibstem"][0] in journal_bibstems:
        pub_dict["journal"] = journal_bibstems[publication["bibstem"][0]]
    else:
        print("Unknown bibstem: {}".format(publication["bibstem"][0]))
        pub_dict["journal"] = publication["bibstem"][0]
    if "tmp" in publication["bibcode"]:
        pub_dict["reference"] = "in press"
    elif "volume" in publication:
        pub_dict["reference"] = "{}, {}".format(publication["volume"], publication["page"][0])
    else:
        pub_dict["reference"] = publication["page"][0].replace("arXiv:", '')
    pub_dict["citation_count"] = publication.get("citation_count", 0)
    pub_dicts[publication["bibcode"]] = pub_dict

with open("./src/data/publications.json", mode='w') as f:
    json.dump(pub_dicts, f)

# Retrieve total number of refereed publications
query_ref = query_all.copy()
query_ref["fl"] = "bibcode"
query_ref['q'] += " property:refereed"
publications_ref = requests.get(get_query_url(query_ref), headers=headers).json()
n_papers_ref = publications_ref["response"]["numFound"]
for publication in publications_ref["response"]["docs"]:
    if publication["bibcode"] in exclude_bibcodes:
        n_papers_ref -= 1
print("Found {:d} papers, of which {:d} refereed".format(n_papers_tot, n_papers_ref))

# Retrieve metrics for all bibcodes
headers["Content-type"] = "application/json"
metrics = requests.post("https://api.adsabs.harvard.edu/v1/metrics",
                        headers=headers,
                        data=json.dumps(dict(types=["basic", "citations", "indicators"], bibcodes=bibcodes))).json()
n_downloads = metrics["basic stats"]["total number of downloads"]
n_reads = metrics["basic stats"]["total number of reads"]
n_citations = metrics["citation stats"]["total number of citations"]
h_index = metrics["indicators"]['h']
print("Total reads: {:d}, total downloads: {:d}, total citations: {:d}, h-index: {:d}".format(n_reads, n_downloads, n_citations, h_index))

with open("./src/utils/ADS_metrics.ts", mode='w') as file:
    file.write("export const latest_update = '{}';".format(current_date))
    file.write("\nexport const n_papers_tot = {:d};".format(n_papers_tot))
    file.write("\nexport const n_papers_ref = {:d};".format(n_papers_ref))
    file.write("\nexport const n_reads = {:d};".format(n_reads))
    file.write("\nexport const n_downloads = {:d};".format(n_downloads))
    file.write("\nexport const n_citations = {:d};".format(n_citations))
    file.write("\nexport const h_index = {:d};".format(h_index))

def write_line(pub_dict):
    return "\n\n- {}, {}, {}, [{}]({}). '{}'{}.".format(pub_dict["authors"], pub_dict["year"], pub_dict["journal"],
                                                        pub_dict["reference"], pub_dict["href"], pub_dict["title"],
                                                        " ({} citation{})".format(pub_dict["citation_count"], '' if pub_dict["citation_count"] == 1 else 's') if pub_dict["citation_count"] else '')

major_contr_bibcodes = sorted(major_contr_bibcodes, key=lambda b: [pub_dicts[b]["ai"], -int(pub_dicts[b]["year"])])

with open("./src/pages/about/publications.md", mode='w') as f:
    f.write("---")
    f.write("\ntitle: 'Publication record'")
    f.write("\ndescription: 'Full publication record.'")
    f.write("\nlayout: '~/layouts/MarkdownLayout.astro'")
    f.write("\n---")
    f.write("\n\n## Summary")
    f.write("\n{:d} publications ({:d} refereed), of which {:d} as first author. ".format(n_papers_tot, n_papers_ref, len(first_author_bibcodes)))
    f.write("Metrics:\n- {:d} reads, {:d} downloads, {:d} citations".format(n_reads, n_downloads, n_citations))
    f.write("\n- h-index: {:d}, m-index: {:.1f}, g-index: {:d}".format(*[metrics["indicators"][i] for i in ['h', 'm', 'g']]))
    f.write("\n- i10-index: {:d}, i100-index: {:d}, read10-index: {:.1f}".format(*[metrics["indicators"][i] for i in ["i10", "i100", "read10"]]))
    f.write("\n- tori index: {:.1f}, riq index: {:.1f}".format(*[metrics["indicators"][i] for i in ["tori", "riq"]]))
    f.write("\n\nBased on the [SAO/NASA Astrophysics Data System (ADS)](https://ui.adsabs.harvard.edu/).")
    f.write("\nLast updated: {}.".format(current_date))
    f.write("\n\n## First author ({:d})".format(len(first_author_bibcodes)))
    for bibcode in first_author_bibcodes:
        f.write(write_line(pub_dicts[bibcode]))
    f.write("\n\n## Major contributions ({:d})".format(len(major_contr_bibcodes)))
    for bibcode in major_contr_bibcodes:
        f.write(write_line(pub_dicts[bibcode]))
    f.write("\n\n## Other ({:d})".format(len(pub_dicts)-len(first_author_bibcodes)-len(major_contr_bibcodes)))
    for bibcode, pub_dict in pub_dicts.items():
        if bibcode not in first_author_bibcodes and bibcode not in major_contr_bibcodes:
            f.write(write_line(pub_dict))
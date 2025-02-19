# Import the requests package and set your token in a variable for later use
import argparse
import requests
from urllib.parse import urlencode
import json

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

query_bib = query_all.copy()
query_bib.update(rows=n_records, fl="bibcode")
bibcodes = [r["bibcode"] for r in requests.get(get_query_url(query_bib), headers=headers).json()["response"]["docs"]]

# Retrieve total number of publication records
pub_query = query_all.copy()
pub_query['q'] += " bibstem:(-jwst.prop) (-yCat) (-AAS) (-eas..conf) (-hst..prop) (-Obs)"
n_papers_tot = requests.get(get_query_url(pub_query), headers=headers).json()["response"]["numFound"]

# Retrieve total number of refereed publications
ref_query = query_all.copy()
ref_query['q'] += " property:refereed"
n_papers_ref = requests.get(get_query_url(ref_query), headers=headers).json()["response"]["numFound"]
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
    file.write("export const n_papers_tot = {:d};".format(n_papers_tot))
    file.write("\nexport const n_papers_ref = {:d};".format(n_papers_ref))
    file.write("\nexport const n_reads = {:d};".format(n_reads))
    file.write("\nexport const n_downloads = {:d};".format(n_downloads))
    file.write("\nexport const n_citations = {:d};".format(n_citations))
    file.write("\nexport const h_index = {:d};".format(h_index))
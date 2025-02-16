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

get_query_url = lambda query: "https://api.adsabs.harvard.edu/v1/search/query?{}".format(urlencode(query))

# Encode query and retrieve bibcodes
query = {'q': 'author:("Witstok, Joris")'}
n_papers_tot = requests.get(get_query_url(query), headers=headers).json()["response"]["numFound"]
query.update(rows=n_papers_tot, fl="bibcode")
bibcodes = [r["bibcode"] for r in requests.get(get_query_url(query), headers=headers).json()["response"]["docs"]]
query['q'] += " property:refereed"
n_papers_ref = requests.get(get_query_url(query), headers=headers).json()["response"]["numFound"]

# Retrieve metrics for selected bibcodes
headers["Content-type"] = "application/json"
metrics = requests.post("https://api.adsabs.harvard.edu/v1/metrics",
                        headers=headers,
                        data=json.dumps(dict(bibcodes=bibcodes))).json()
n_citations = metrics["citation stats"]["total number of citations"]
h_index = metrics["indicators"]['h']

with open("./src/utils/metrics.ts", mode='w') as file:
    file.write("export const n_papers_tot = {:d};".format(n_papers_tot))
    file.write("\nexport const n_papers_ref = {:d};".format(n_papers_ref))
    file.write("\nexport const n_citations = {:d};".format(n_citations))
    file.write("\nexport const h_index = {:d};".format(h_index))
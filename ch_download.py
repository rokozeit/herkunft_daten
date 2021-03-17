import requests
import os.path
from pathlib import Path

###
# Data comming from https://www.blv.admin.ch/blv/en/home/lebensmittel-und-ernaehrung/rechts-und-vollzugsgrundlagen/bewilligung-und-meldung/listen-bewilligter-betriebe.html
###

url = 'https://kwk.blv.admin.ch/superglobal/wGlobal/scripts/php/bewilligungsliste/inc.list_to_csv.php?viewmode=csv&lang=en'
filepath = 'ch/list.csv'

if(not os.path.exists(filepath)): # TODO check if it exists and is empty
    r = requests.get(url, allow_redirects=True)
    filename = Path(filepath)
    filename.write_bytes(r.content)

####
# The current version contains some stupid headings. I just remove it.
####

a_file = open(filepath, "r")

lines = a_file.readlines()
a_file.close()

dele = True

new_file = open(filepath, "w")
for line in lines:
    if(line.startswith('"Permit Number"')):
        dele = False

    if(not dele):        
        new_file.write(line)


new_file.close()

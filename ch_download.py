import requests
import os.path
from pathlib import Path

###
# Swizz information on the approval number (german: Genusstauglichkeitskennzeichen)
# Downloads the data from the link. Last checked 30th October 2023.
# The links might be broken by now.
# Link: https://www.blv.admin.ch/blv/en/home/lebensmittel-und-ernaehrung/rechts-und-vollzugsgrundlagen/bewilligung-und-meldung/listen-bewilligter-betriebe.html
###

url = 'https://kwk.blv.admin.ch/superglobal/wGlobal/scripts/php/bewilligungsliste/inc.list_to_csv.php?viewmode=csv&lang=en'
filepath = 'ch/list.csv'

# if(not os.path.exists(filepath)): # TODO check if it exists and is empty
r = requests.get(url, allow_redirects=True)
filename = Path(filepath)
filename.write_bytes(r.content)

####
# The current version of the tables contains some stupid headings. And some stupid extra text. I just remove it.
####

a_file = open(filepath, "r")

lines = a_file.readlines()
a_file.close()

firstHeading = True

new_file = open(filepath, "w")
for line in lines:

    if(line.startswith('"Permit Number"')):
        if(firstHeading):
            firstHeading = False
            new_file.write(line)
            continue
        else:
            continue

    if(line.startswith(('"Sektion', '\n', '"Result', '"Your search', '"Search'))):
        continue

    if(line.startswith('"Codes and legends"')):
        break

    new_file.write(line)


new_file.close()

import pandas as pd
import sqlite3
# import pandas_read_xml as pdx
from lxml import objectify

###
# German information on the approval number (german: Genusstauglichkeitskennzeichen)
# Currently I do not have a download script due to the stupid way they provide the data.
# 
# Link to the data: https://bltu.bvl.bund.de/bltu/app/process/bvl-btl_p_veroeffentlichung?execution=e1s2
# Direct link to the full data set: https://bltu.bvl.bund.de/bltu/app/process/bvl-btl_p_veroeffentlichung?execution=e1s3
# 
# First create a folder with the name 'de'.  
# Then download the XML file from the Link and save it into the folder 'de' as './de/export.xml'.
# Run this script to add a 'de' table to the sqlite data base.
#
# The links might be broken by now. Last checked 30th October 2023
# The CSV version I downloaded (full version) contained some errors. So I switched to XML instread
#
# Parses the XML in the downloaded XML file.
# Adds the content to the sqlite db as table 'de'.
###

# Open DB
cnx = sqlite3.connect('db.sqlite')
cursor = cnx.cursor()
# Delete table if it already exists
cursor.execute("DROP TABLE IF EXISTS de")
cnx.commit()

# Parse the XML file
xml_data = objectify.parse('de/export.xml')

root = xml_data.getroot();

data = [];

# Extract the data for the pandas dataframe
for betrieb in root.getchildren():
    name = str(betrieb.name)
    address = betrieb.strasse + ' ' + str(betrieb.hausnummer) + ', ' + str(betrieb.postleitzahl) + ' ' + betrieb.ort
    approvalNo = betrieb.zulassungsnummer.bundesland + ' ' + str(betrieb.zulassungsnummer.nummer)
    approvalNoOld = str(betrieb.taetigkeit.alteZulassungsnummer)
    comment = str(betrieb.taetigkeit.bemerkung)
    data.append([name, address, approvalNo, approvalNoOld, comment])

cols=['name', 'address', 'approvalNo', 'approvalNoOld', 'comment']

df = pd.DataFrame(data)
df.columns = cols 

### Former csv code - however, since the csv had errors, now I choose xml
# df = pandas.read_csv('de/export.csv', sep=';', quotechar='"', decimal=',', encoding='ansi',
#     usecols=['Name des Betriebs ', 'Straße / Haus-Nr.', 'Ort', 'Alte Zulassungs-nummern', 'Neue Zulassungsnummer', 'Bemerkungen'])
# df = df.rename(columns={"Name des Betriebs ": "name", "Straße / Haus-Nr.": "street", 
#     "Alte Zulassungs-nummern": "approvalNoOld", "Neue Zulassungsnummer": "approvalNo", "Ort" : "place", "Bemerkungen" : "comment" })
# df['address'] = df['street'] + ', ' + df['place']
# df = df.drop(df.columns[[1, 2]], axis=1)

# remove possible duplicates
df = df.drop_duplicates(subset=['approvalNo'])

# write to data base
df.to_sql('de', cnx)

cnx.close()
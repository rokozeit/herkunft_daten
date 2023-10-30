import pandas
import sqlite3

###
# German information on the approval number (german: Genusstauglichkeitskennzeichen)
# Currently I do not have a download script due to the stupid way they provide the data.
# 
# Link: https://apps2.bvl.bund.de/bltu/app/process/bvl-btl_p_veroeffentlichung?execution=e1s2
# 
# First download the file from the Link. The links might be broken by now. Last checked 30th October 2023
# The version I downloaded (full version) contained some errors. This needs to be fixed first.
#
# Parses the tables in the downloaded and fixed file.
# Adds the content to the sqlite db as table 'de'.
###
cnx = sqlite3.connect('db.sqlite')
df = pandas.read_csv('de/export.csv', sep=';', quotechar='"', decimal=',', encoding='ansi',
    usecols=['Name des Betriebs ', 'Straße / Haus-Nr.', 'Ort', 'Alte Zulassungs-nummern', 'Neue Zulassungsnummer', 'Bemerkungen'])
df = df.rename(columns={"Name des Betriebs ": "name", "Straße / Haus-Nr.": "street", 
    "Alte Zulassungs-nummern": "approvalNoOld", "Neue Zulassungsnummer": "approvalNo", "Ort" : "place", "Bemerkungen" : "comment" })
df['address'] = df['street'] + ', ' + df['place']
df = df.drop(df.columns[[1, 2]], axis=1)
df.to_sql('de', cnx)
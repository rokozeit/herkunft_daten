import pandas
import sqlite3

# https://apps2.bvl.bund.de/bltu/app/process/bvl-btl_p_veroeffentlichung?execution=e1s2
cnx = sqlite3.connect('db.sqlite')
df = pandas.read_csv('de/export.csv', sep=';', quotechar='"', decimal=',', encoding='ansi',
    usecols=['Name des Betriebs ', 'Straße / Haus-Nr.', 'Ort', 'Alte Zulassungs-nummern', 'Neue Zulassungsnummer', 'Bemerkungen'])
df = df.rename(columns={"Name des Betriebs ": "name", "Straße / Haus-Nr.": "street", 
    "Alte Zulassungs-nummern": "approvalNoOld", "Neue Zulassungsnummer": "approvalNo", "Ort" : "place", "Bemerkungen" : "comment" })
df['address'] = df['street'] + ', ' + df['place']
df = df.drop(df.columns[[1, 2]], axis=1)
df.to_sql('de', cnx)
import pandas
import sqlite3

###
# Parses the tables in the csv files downloaded with ch_download.py and
# Adds the content to the sqlite db as table 'at'.
# Link https://www.blv.admin.ch/blv/en/home/lebensmittel-und-ernaehrung/rechts-und-vollzugsgrundlagen/bewilligung-und-meldung/listen-bewilligter-betriebe.html
###

cnx = sqlite3.connect('db.sqlite')

cursor = cnx.cursor()
cursor.execute("DROP TABLE IF EXISTS ch")
cnx.commit()



df = pandas.read_csv('ch/list.csv', sep=';', quotechar='"', decimal=',', encoding='ansi',
    usecols=['Permit Number', 'Company Name', 'Address', 'Zipcode', 'City/Region', 'Remark'])
df = df.rename(columns={"Permit Number": "approvalNo", "Company Name": "name", 
    "Address": "street", "Zipcode": "zipcode", "City/Region" : "place", "Remark" : "comment" })
df['address'] = df['street'] + ', ' + str(df['zipcode']) + ' ' + str(df['place'])
df = df.drop(df.columns[[2, 3, 4]], axis=1)
df = df.drop_duplicates(subset=['approvalNo'])
df['approvalNoOld'] = ""

df.to_sql('ch', cnx)

cnx.close()
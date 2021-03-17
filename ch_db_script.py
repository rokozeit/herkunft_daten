import pandas
import sqlite3

###
# Data comming from https://www.blv.admin.ch/blv/en/home/lebensmittel-und-ernaehrung/rechts-und-vollzugsgrundlagen/bewilligung-und-meldung/listen-bewilligter-betriebe.html
###

cnx = sqlite3.connect('db.sqlite')
df = pandas.read_csv('ch/list.csv', sep=';', quotechar='"', decimal=',', encoding='ansi',
    usecols=['Permit Number', 'Company Name', 'Address', 'Zipcode', 'City/Region', 'Remark'])
df = df.rename(columns={"Permit Number": "approvalNo", "Company Name": "name", 
    "Address": "street", "Zipcode": "zipcode", "City/Region" : "place", "Remark" : "comment" })
df['address'] = df['street'] + ', ' + df['zipcode'] + ' ' + df['place']
df = df.drop(df.columns[[2, 3, 4]], axis=1)
df['approvalNoOld'] = ""

df.to_sql('ch', cnx)
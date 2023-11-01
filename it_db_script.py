import pandas as pd
import sqlite3

###
# Italien information on the approval number (german: Genusstauglichkeitskennzeichen)
# Downloads the data from the link. Last checked 17th March 2021.
# 
# Link: http://www.salute.gov.it/consultazioneStabilimenti/ConsultazioneStabilimentiServlet?ACTION=gestioneSingolaCategoria&idNormativa=2
# The links might be broken by now.
#
# Parses the tables in the downloaded files.
# Adds the content to the sqlite db as table 'it'.
# Unfortunatly they encode their page in cp1252 (Windows 1252).
###

pd.options.mode.chained_assignment = None 
tables = pd.read_html('http://www.salute.gov.it/consultazioneStabilimenti/ConsultazioneStabilimentiServlet?ACTION=gestioneSingolaCategoria&idNormativa=2',
skiprows=[0],header=0, encoding="cp1252")

df = tables[0][['APPROVAL NUMBER', 'NAME', 'TOWN/REGION']]

df.columns = ['approvalNo', 'name', 'address']
df["approvalNoOld"] = ""

df = df.drop_duplicates(subset=['approvalNo'])

print(df.head())
cnx = sqlite3.connect('db.sqlite')
cursor = cnx.cursor()
cursor.execute("DROP TABLE IF EXISTS it")
cnx.commit()

df.to_sql('it', cnx)
cnx.close()
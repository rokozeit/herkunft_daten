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
###

pd.options.mode.chained_assignment = None 
tables = pd.read_html('http://www.salute.gov.it/consultazioneStabilimenti/ConsultazioneStabilimentiServlet?ACTION=gestioneSingolaCategoria&idNormativa=2',
skiprows=[0],header=0)

df = tables[0][['APPROVAL NUMBER', 'NAME', 'TOWN/REGION']]

df.columns = ['approvalNo', 'name', 'address']
df["approvalNoOld"] = ""

print(df.head())
cnx = sqlite3.connect('db.sqlite')
df.to_sql('it', cnx)

# dfs = []
# pd.options.mode.chained_assignment = None 
# for x in range(18):
#     tables = pd.read_html('http://www.salute.gov.it/consultazioneStabilimenti/ConsultazioneStabilimentiServlet?ACTION=gestioneSingolaCategoria&idNormativa=2&idCategoria=' + str(x),
#         skiprows=[0],header=0)

#     df = tables[0][['APPROVAL NUMBER', 'NAME', 'TOWN/REGION']]

#     df.columns = ['approvalNo', 'name', 'address']
#     df['approvalNoOld'] = ''

#     dfs.append(df)

# dfall = pd.concat(dfs)

# dfall.drop_duplicates(subset ="approvalNo", 
#                      keep = False, inplace = True) 

# cnx = sqlite3.connect('db.sqlite')

# dfall.to_sql('it', cnx)



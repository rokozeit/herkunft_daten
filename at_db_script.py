import camelot
import pandas as pd
import sqlite3

#######
#
# Install GhostScript (https://www.ghostscript.com/) first 
# Then install camelot (pip install camelot-py)
#
#######

cnx = sqlite3.connect('db.sqlite')
dfs = []

files = ['I1.pdf', 'II2.pdf', 'III3.pdf', 'IV4.pdf', 'V5.pdf', 'VI6.pdf', 'VII7.pdf',
 'VIII8.pdf', 'IX9.pdf', 'X10.pdf', 'XI11.pdf', 'XII56.pdf', 'XIII12.pdf',
 'O20.pdf', 'I21.pdf', 'II22.pdf', 'III23.pdf', 'IV24.pdf', 'V25.pdf', 'VI26.pdf',
 'VII27.pdf', 'VIII28.pdf', 'IX29.pdf', 'X30.pdf', 'XI31.pdf', 'XII32.pdf', 'XIII33.pdf',
 'XIV34.pdf', 'XV35.pdf', '157.pdf', '241.pdf', '342.pdf', '443.pdf', '544.pdf',
 '645.pdf', '746.pdf', '847.pdf', '948.pdf', '1049.pdf', '1150.pdf', '1251.pdf',
 '1352.pdf', '1453.pdf', '1554.pdf', '1655.pdf']


for file in files:
    tables = camelot.read_pdf('at/' + file, pages='all')

    for table in tables:
        df = table.df.replace({ r'\n' : ' '}, regex=True)
        df.columns = df.iloc[2]
        df = df[3:]
        df = df.drop(df.columns[[2, 5, 6, 7, 8, 9]], axis=1)
        df = df.rename(columns={'Approval number': 'approvalNo', 'Old approval number': 'approvalNoOld', 'Name': 'name', 'Remarks': 'comment', 'Adress' : 'address'})
        dfs.append(df)

# all dfs in the list are added to one big ds
dfall = pd.concat(dfs)

dfall.drop_duplicates(subset ="approvalNo", 
                     keep = False, inplace = True) 

# dfall.to_csv('foo.csv')
dfall.to_sql('at', cnx)
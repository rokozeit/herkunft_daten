import pandas as pd
import sqlite3

###
# French information on the approval number (german: Genusstauglichkeitskennzeichen)
# Currently I do not have a download script due to the stupid way they provide the data.
# Parses the tables in the downloaded files.
# Adds the content to the sqlite db as table 'fr'.
###

try:
    cnx = sqlite3.connect('db.sqlite')
    cursor = cnx.cursor()
    cursor.execute("DROP TABLE IF EXISTS fr")
    cnx.commit()

    dfs = []

    files = ['SSA1_ACTIV_GEN.txt', 'SSA1_VIAN_ONG_DOM.txt', 'SSA1_VIAN_COL_LAGO.txt', 'SSA1_VIAN_GIB_ELEV.txt',
             'SSA1_VIAN_GIB_SAUV.txt', 'SSA1_VIAND_HACHE_VSM.txt', 'SSA4_AGSANPROBASEVDE_PRV.txt',
             'SSA4B_AS_CE_PRODCOQUI_COV.txt', 'SSA4B_AS_CE_PRODPECHE_COV.txt', 'SSA1_LAIT.txt', 'SSA1_OEUF.txt',
             'SSA1_GREN_ESCARG.txt', 'SSA4_AGSANGREXPR_PRV.txt', 'SSA4_AGR_ESVEBO_PRV.txt', 'SSA4_AGSANGELAT_PRV.txt',
             'SSA4_AGSANCOLL_PRV.txt', 'SSA_PROD_RAFF.txt', 'SSA4_ASCCC_PRV.txt']

    for file in files:
        cols = pd.read_csv('fr/' + file, nrows=1).columns

        df = pd.read_csv('fr/' + file, dtype=str, usecols=cols)
        df = df.drop(df.columns[[0, 2, 7, 8, 9]], axis=1)
        df['address'] = df['Adresse/Adress'] + ', ' + df['Code postal/Postal code'] + ' ' + df['Commune/Town']
        df = df.drop(df.columns[[2, 3, 4]], axis=1)
        df.columns = ['approvalNo', 'name', 'address']
        df["approvalNoOld"] = ""
        dfs.append(df)

    dfall = pd.concat(dfs)

    dfall.drop_duplicates(subset="approvalNo", keep=False, inplace=True)

    dfall.to_sql('fr', cnx, index=False, if_exists='replace')

    cnx.close()

except FileNotFoundError as file_not_found_error:
    print(f"File not found: {file_not_found_error}")
except pd.errors.EmptyDataError as empty_data_error:
    print(f"No data found in the file: {empty_data_error}")
except sqlite3.Error as sqlite_error:
    print(f"SQLite error: {sqlite_error}")
except Exception as ex:
    print(f"An unexpected error occurred: {ex}")

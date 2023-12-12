import camelot
import pandas as pd
import sqlite3


#######
# Parses the tables in the PDF files downloaded with at_download.py and
# Adds the content to the sqlite db as table 'at'.
#
# It uses the PDF parser package camelot-py (NOT camelot) to do the parsing: 
#  - https://pypi.org/project/camelot-py/
#  - Install GhostScript (https://www.ghostscript.com/) first.
#  - Then install camelot (pip install camelot-py)
# Then I had a ModuleNotfoundError: No module named 'cv2' issue and solved it with
#  - pip install opencv-python
# Currently not working with Python 3.12
#  
#######

try:
    # drop the the table if it already exists
    cnx = sqlite3.connect('db.sqlite')
    cursor = cnx.cursor()
    cursor.execute("DROP TABLE IF EXISTS at")
    cnx.commit()

    dfs = []

    # list of files to be processed
    files = ['I1.pdf', 'II2.pdf', 'III3.pdf', 'IV4.pdf', 'V5.pdf', 'VI6.pdf', 'VII7.pdf',
             'VIII8.pdf', 'IX9.pdf', 'X10.pdf', 'XI11.pdf', 'XII56.pdf', 'XIII12.pdf',
             'O20.pdf', 'I21.pdf', 'II22.pdf', 'III23.pdf', 'IV24.pdf', 'V25.pdf', 'VI26.pdf',
             'VII27.pdf', 'VIII28.pdf', 'IX29.pdf', 'X30.pdf', 'XI31.pdf', 'XII32.pdf', 'XIII33.pdf',
             'XIV34.pdf', 'XV35.pdf', '157.pdf', '241.pdf', '342.pdf', '443.pdf', '544.pdf',
             '645.pdf', '746.pdf', '847.pdf', '948.pdf', '1049.pdf', '1150.pdf', '1251.pdf',
             '1352.pdf', '1453.pdf', '1554.pdf', '1655.pdf']

    # process all PDF files
    for file in files:
        try:
            # extract the table from the PDF file
            tables = camelot.read_pdf('at/' + file, pages='all')
            
            # only for the user to see the progress
            print(f">>>> processing file at/{file}")

            # iterate over all tables
            for table in tables:
                df = table.df.replace({r'\n': ' '}, regex=True)
                df.columns = df.iloc[2]
                df = df[3:]
                df = df.drop(df.columns[[2, 5, 6, 7, 8, 9]], axis=1)
                df = df.rename(columns={'Approval number': 'approvalNo', 'Old approval number': 'approvalNoOld',
                                        'Name': 'name', 'Remarks': 'comment', 'Adress': 'address'})
                # append table to the list
                dfs.append(df)
        except Exception as e:
            print(f"Error processing file '{file}': {e}")

    if dfs:
        # Merge all dataframes into one
        dfall = pd.concat(dfs)
        
        # Remove duplicates based on 'approvalNo' column
        dfall.drop_duplicates(subset="approvalNo", keep=False, inplace=True)
        
        # Write data to SQLite
        dfall.to_sql('at', cnx, if_exists='replace', index=False)

    cnx.close()
except sqlite3.Error as sqlite_error:
    print(f"SQLite error: {sqlite_error}")
except Exception as ex:
    print(f"An unexpected error occurred: {ex}")

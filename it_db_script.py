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

def process_it():
    """
    This function processes the Italian health mark information by connecting to a SQLite database,
    retrieving data from a URL, creating a table from an HTML table, renaming columns, removing
    duplicated rows, and writing the table to the database.

    Parameters:
    None

    Returns:
    None
    """
    try:
        cnx = sqlite3.connect('db.sqlite')

        # the url of the italian health mark information
        url = 'http://www.salute.gov.it/consultazioneStabilimenti/ConsultazioneStabilimentiServlet?ACTION=gestioneSingolaCategoria&idNormativa=2'

        # create table from the html table
        pd.options.mode.chained_assignment = None 
        tables = pd.read_html(url, skiprows=[0], header=0, encoding="cp1252")
        df = tables[0][['APPROVAL NUMBER', 'NAME', 'TOWN/REGION']]

        # rename columns
        df.columns = ['approvalNo', 'name', 'address']
        df["approvalNoOld"] = ""

        # remove duplicated rows
        df = df.drop_duplicates(subset=['approvalNo'])

        # write the table to the db
        df.to_sql('it', cnx, index=False, if_exists='replace')
        cnx.close()

    except FileNotFoundError as file_not_found_error:
        print(f"File not found at the URL: {file_not_found_error}")
    except pd.errors.EmptyDataError as empty_data_error:
        print(f"No data found in the HTML table: {empty_data_error}")
    except sqlite3.Error as sqlite_error:
        print(f"SQLite error: {sqlite_error}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

def main():
    process_it()

if __name__ == "__main__":
    main()
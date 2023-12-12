import pandas as pd
import sqlite3

###
# French information on the approval number (german: Genusstauglichkeitskennzeichen)
# Currently I do not have a download script due to the stupid way they provide the data.
# Parses the tables in the downloaded files.
# Adds the content to the sqlite db as table 'fr'.
###


def process_file(file):
    """
    Processes FR health mark file and return a DataFrame with selected columns.

    Parameters:
        file (str): The path to the file to be processed.

    Returns:
        DataFrame: A DataFrame with the following columns:
            - approvalNo (str): The approval number.
            - name (str): The name.
            - address (str): The address.

    Raises:
        FileNotFoundError: If the specified file is not found.
        EmptyDataError: If no data is found in the file.
        Exception: If an unexpected error occurs.
    """
    try:
        print(f"        processing fr/{file}")
        cols = pd.read_csv("fr/" + file, nrows=1).columns

        df = pd.read_csv("fr/" + file, dtype=str, usecols=cols)
        # remove unnecessary columns
        df = df.drop(df.columns[[0, 2, 7, 8, 9]], axis=1)

        # create one address column from the individual columns
        df["address"] = (
            df["Adresse/Adress"]
            + ", "
            + df["Code postal/Postal code"]
            + " "
            + df["Commune/Town"]
        )
        df = df.drop(df.columns[[2, 3, 4]], axis=1)

        # rename the columns
        df.columns = ["approvalNo", "name", "address"]
        df["approvalNoOld"] = ""
        return df
    except FileNotFoundError as file_not_found_error:
        print(f"File not found: {file_not_found_error}")
    except pd.errors.EmptyDataError as empty_data_error:
        print(f"No data found in the file: {empty_data_error}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")


def process_fr():
    """
    Connects to the 'db.sqlite' database, processes a list of FR health mark files, removes duplicates from the resulting DataFrame based on the 'approvalNo' column, and writes the data to the 'fr' table in the SQLite database.

    :return: None
    """
    try:
        cnx = sqlite3.connect("db.sqlite")

        dfs = []

        # all files to be processed
        files = [
            "SSA1_ACTIV_GEN.txt",
            "SSA1_VIAN_ONG_DOM.txt",
            "SSA1_VIAN_COL_LAGO.txt",
            "SSA1_VIAN_GIB_ELEV.txt",
            "SSA1_VIAN_GIB_SAUV.txt",
            "SSA1_VIAND_HACHE_VSM.txt",
            "SSA4_AGSANPROBASEVDE_PRV.txt",
            "SSA4B_AS_CE_PRODCOQUI_COV.txt",
            "SSA4B_AS_CE_PRODPECHE_COV.txt",
            "SSA1_LAIT.txt",
            "SSA1_OEUF.txt",
            "SSA1_GREN_ESCARG.txt",
            "SSA4_AGSANGREXPR_PRV.txt",
            "SSA4_AGR_ESVEBO_PRV.txt",
            "SSA4_AGSANGELAT_PRV.txt",
            "SSA4_AGSANCOLL_PRV.txt",
            "SSA_PROD_RAFF.txt",
            "SSA4_ASCCC_PRV.txt",
        ]

        for file in files:
            dfs.append(process_file(file))

        dfall = pd.concat(dfs)

        # remove duplicates based on 'approvalNo' column
        dfall.drop_duplicates(subset="approvalNo", keep=False, inplace=True)

        # write data to SQLite
        dfall.to_sql("fr", cnx, index=False, if_exists="replace")

        cnx.close()

    except sqlite3.Error as sqlite_error:
        print(f"SQLite error: {sqlite_error}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

def main():
    process_fr()

if __name__ == "__main__":
    main()
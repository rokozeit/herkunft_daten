import pandas as pd
import sqlite3
from lxml import objectify
import os

###
# German information on the approval number (german: Genusstauglichkeitskennzeichen)
# Currently I do not have a download script due to the stupid way they provide the data.
#
# Link to the data: https://bltu.bvl.bund.de/bltu/app/process/bvl-btl_p_veroeffentlichung?execution=e1s2
# Direct link to the full data set: https://bltu.bvl.bund.de/bltu/app/process/bvl-btl_p_veroeffentlichung?execution=e1s3
#
# First create a folder with the name 'de'.
# Then download the XML file from the Link and save it into the folder 'de' as './de/export.xml'.
# Run this script to add a 'de' table to the sqlite data base.
#
# The links might be broken by now. Last checked 30th October 2023
# The CSV version I downloaded (full version) contained some errors. So I switched to XML instread
#
# Parses the XML in the downloaded XML file.
# Adds the content to the sqlite db as table 'de'.
###

try:
    file = "./de/export.xml"

    if not os.path.isfile(file):
        raise Exception(
            f"File {file} not found. Please download the file first from https://bltu.bvl.bund.de/bltu/app/process/bvl-btl_p_veroeffentlichung?execution=e1s3"
        )

    cnx = sqlite3.connect("db.sqlite")
    cursor = cnx.cursor()
    cursor.execute("DROP TABLE IF EXISTS de")
    cnx.commit()

    # Parse the XML file
    xml_data = objectify.parse(file)
    root = xml_data.getroot()

    data = []

    # Extract the data for the pandas dataframe
    for betrieb in root.getchildren():
        name = str(betrieb.name)
        address = f"{betrieb.strasse} {betrieb.hausnummer}, {betrieb.postleitzahl} {betrieb.ort}"
        approvalNo = (
            f"{betrieb.zulassungsnummer.bundesland} {betrieb.zulassungsnummer.nummer}"
        )
        approvalNoOld = str(betrieb.taetigkeit.alteZulassungsnummer)
        comment = str(betrieb.taetigkeit.bemerkung)
        data.append([name, address, approvalNo, approvalNoOld, comment])

    cols = ["name", "address", "approvalNo", "approvalNoOld", "comment"]

    df = pd.DataFrame(data, columns=cols)

    # remove possible duplicates
    df = df.drop_duplicates(subset=["approvalNo"])

    # write to database
    df.to_sql("de", cnx, if_exists="replace", index=False)

    cnx.close()

except FileNotFoundError as file_not_found_error:
    print(f"File not found: {file_not_found_error}")
except pd.errors.EmptyDataError as empty_data_error:
    print(f"No data found in the XML file: {empty_data_error}")
except sqlite3.Error as sqlite_error:
    print(f"SQLite error: {sqlite_error}")
except Exception as ex:
    print(f"An unexpected error occurred: {ex}")

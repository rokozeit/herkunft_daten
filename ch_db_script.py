import pandas as pd
import sqlite3

###
# Parses the tables in the csv files downloaded with ch_download.py and
# Adds the content to the sqlite db as table 'at'.
# Link https://www.blv.admin.ch/blv/en/home/lebensmittel-und-ernaehrung/rechts-und-vollzugsgrundlagen/bewilligung-und-meldung/listen-bewilligter-betriebe.html
###


try:
    db_connection = sqlite3.connect('db.sqlite')
    cursor = db_connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS ch")
    db_connection.commit()

    df = pd.read_csv('ch/list.csv', sep=';', quotechar='"', decimal=',', encoding='ansi',
                     usecols=['Permit Number', 'Company Name', 'Address', 'Zipcode', 'City/Region', 'Remark'])

    df = df.rename(columns={"Permit Number": "approvalNo", "Company Name": "name",
                            "Address": "street", "Zipcode": "zipcode", "City/Region": "city", "Remark": "comment"})
    df['address'] = df['street'].astype(str) + ', ' + df['zipcode'].astype(str) + ' ' + df['city'].astype(str)

    df = df.drop(['street', 'zipcode', 'city'], axis=1)
    df = df.drop_duplicates(subset=['approvalNo'])

    df['approvalNoOld'] = ""

    df.to_sql('ch', db_connection, index=False, if_exists='replace')

except FileNotFoundError as file_not_found_error:
    print(f"File not found: {file_not_found_error}")
except pd.errors.EmptyDataError as empty_data_error:
    print(f"No data found in the CSV file: {empty_data_error}")
except sqlite3.Error as sqlite_error:
    print(f"SQLite error: {sqlite_error}")
except Exception as ex:
    print(f"An unexpected error occurred: {ex}")
finally:
    try:
        db_connection.close()
    except Exception as close_exception:
        print(f"Error while closing database connection: {close_exception}")

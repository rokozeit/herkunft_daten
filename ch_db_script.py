import pandas as pd
import sqlite3

###
# Parses the tables in the csv files downloaded with ch_download.py and
# Adds the content to the sqlite db as table 'at'.
# Link https://www.blv.admin.ch/blv/en/home/lebensmittel-und-ernaehrung/rechts-und-vollzugsgrundlagen/bewilligung-und-meldung/listen-bewilligter-betriebe.html
###


try:
    # remove the table if it already exists
    db_connection = sqlite3.connect('db.sqlite')
    cursor = db_connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS ch")
    db_connection.commit()

    # read the csv file
    df = pd.read_csv('ch/list.csv', sep=';', quotechar='"', decimal=',', encoding='ansi',
                     usecols=['Permit Number', 'Company Name', 'Address', 'Zipcode', 'City/Region', 'Remark'])

    # normalize the column names
    df = df.rename(columns={"Permit Number": "approvalNo", "Company Name": "name",
                            "Address": "street", "Zipcode": "zipcode", "City/Region": "city", "Remark": "comment"})
    
    # convert colums to one address column
    df['address'] = df['street'].astype(str) + ', ' + df['zipcode'].astype(str) + ' ' + df['city'].astype(str)

    # remove unnecessary columns
    df = df.drop(['street', 'zipcode', 'city'], axis=1)

    # remove duplicates
    df = df.drop_duplicates(subset=['approvalNo'])

    # there is no approvalNoOld column in the csv file. So make all values empty
    df['approvalNoOld'] = ""

    # write to the database
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

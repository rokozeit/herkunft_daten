import pandas as pd
import sqlite3

###
# Parses the tables in the csv files downloaded with ch_download.py and
# Adds the content to the sqlite db as table 'at'.
# Link https://www.blv.admin.ch/blv/en/home/lebensmittel-und-ernaehrung/rechts-und-vollzugsgrundlagen/bewilligung-und-meldung/listen-bewilligter-betriebe.html
###

def process_ch():
    """
    Function to process the 'ch' data.
    
    This function reads a CSV file containing 'ch' data and performs the following steps:
    
    1. Connects to the 'db.sqlite' database.
    2. Reads the CSV file 'ch/list.csv' using pandas, specifying the separator as ';', quotechar as '"', decimal as ',', and encoding as 'ansi'.
    3. Renames the columns of the DataFrame to match the desired format.
    4. Combines the 'street', 'zipcode', and 'city' columns into a single 'address' column.
    5. Drops unnecessary columns from the DataFrame.
    6. Removes duplicate rows based on the 'approvalNo' column.
    7. Adds an empty 'approvalNoOld' column to the DataFrame.
    8. Writes the DataFrame to the 'ch' table in the 'db.sqlite' database, replacing any existing data.
    9. Closes the database connection.
    
    If any of the following exceptions occur, an error message is printed:
    
    - FileNotFoundError: if the CSV file is not found.
    - EmptyDataError: if no data is found in the CSV file.
    - sqlite3.Error: if there is an error with SQLite.
    - Exception: for any other unexpected error.
    
    This function does not return any values.
    """
    try:
        cnx = sqlite3.connect('db.sqlite')
        
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
        df.to_sql('ch', cnx, index=False, if_exists='replace')

        cnx.close()

    except FileNotFoundError as file_not_found_error:
        print(f"File not found: {file_not_found_error}")
    except pd.errors.EmptyDataError as empty_data_error:
        print(f"No data found in the CSV file: {empty_data_error}")
    except sqlite3.Error as sqlite_error:
        print(f"SQLite error: {sqlite_error}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

def main():
    process_ch()

if __name__ == "__main__":
    main()
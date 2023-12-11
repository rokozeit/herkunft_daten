import requests
import os.path
from pathlib import Path
from helper import check_url

###
# Swizz information on the approval number (german: Genusstauglichkeitskennzeichen)
# Downloads the data from the link. Last checked 30th October 2023.
# The links might be broken by now.
# Link: https://www.blv.admin.ch/blv/en/home/lebensmittel-und-ernaehrung/rechts-und-vollzugsgrundlagen/bewilligung-und-meldung/listen-bewilligter-betriebe.html
###

def download_ch():

    # file to write the data to
    file_path = 'ch/list.csv'
    
    # Create 'ch' directory if it doesn't exist
    os.makedirs("ch", exist_ok=True)

    # url to the data
    url = 'https://kwk.blv.admin.ch/superglobal/wGlobal/scripts/php/bewilligungsliste/inc.list_to_csv.php?viewmode=csv&lang=en'

    url_exists = check_url(url)

    if not url_exists:
        print(f"The URL '{url}' does not exist or is unreachable.")
        return

    ####
    # The current version of the tables contains some stupid headings. And some stupid extra text. I just remove it.
    ####

    try:
        # Check if the file already exists and is non-empty before downloading
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            response = requests.get(url, allow_redirects=True)
            if response.status_code == 200:
                with open(file_path, 'wb') as file:
                    file.write(response.content)
            else:
                print(f"Failed to download the file. Status code: {response.status_code}")
                return
        else:
            print("File already exists and is not empty.")
            return
            
        # Clean unnecessary lines from the file
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        with open(file_path, 'w') as new_file:
            first_heading = True
            for line in lines:
                if line.startswith('"Permit Number"'):
                    if first_heading:
                        first_heading = False
                        new_file.write(line)
                    continue

                if line.startswith(('"Sektion', '\n', '"Result', '"Your search', '"Search')):
                    continue

                if line.startswith('"Codes and legends"'):
                    break

                new_file.write(line)

    except requests.RequestException as e:
        print(f"Failed to fetch data. Error: {e}")

    except FileNotFoundError as fe:
        print(f"File not found error: {fe}")

    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

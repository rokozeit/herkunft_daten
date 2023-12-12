import os
import requests
from pathlib import Path

###
# French information on the approval number (german: Genusstauglichkeitskennzeichen)
# Downloads the data from the link. Last checked 30th October 2023.
# Link: https://fichiers-publics.agriculture.gouv.fr/dgal/ListesOfficielles/
# The links might be broken by now.
# I had to add ', verify = False' to re request due to some certificate error.#
# However, this is not recomended. It is a hack.
###

def download_file(url: str, file_path: str):
    """
    Downloads the contents of a file from a URL.

    Args:
        url (str): The URL of the file to download.
        file_path (str): The path of the local file where the contents should be saved.

    Raises:
        requests.RequestException: If the request to the URL fails.
        OSError: If the local file cannot be written to.
    """
    try:
        response = requests.get(url, allow_redirects=True, verify=False)
        if response.status_code == 200:
            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"Downloaded: {file_path}")
        else:
            print(f"Failed to download: {file_path}. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

def download_files(base_url, files, directory):
    """
    Downloads a list of files from a base URL.

    Args:
        base_url (str): The base URL from which the files should be downloaded.
        files (list): A list of the files to download.
        directory (str): The directory where the files should be saved.

    Raises:
        OSError: If the directory cannot be created.
    """
    try:
        os.makedirs(directory, exist_ok=True)

        for file in files:
            url = f"{base_url}/{file}"
            file_path = os.path.join(directory, file)

            if not os.path.exists(file_path):
                download_file(url, file_path)
            else:
                print(f"File already exists: {file_path}")

    except OSError as ose:
        print(f"Failed to create directory: {ose}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

# Base url for the french information on approval numbers
base_url = 'https://fichiers-publics.agriculture.gouv.fr/dgal/ListesOfficielles'

# director to write the files
directory = 'fr'

# list of files to be downloaded
files = ['SSA1_ACTIV_GEN.txt', 'SSA1_VIAN_ONG_DOM.txt', 'SSA1_VIAN_COL_LAGO.txt', 'SSA1_VIAN_GIB_ELEV.txt',
    'SSA1_VIAN_GIB_SAUV.txt', 'SSA1_VIAND_HACHE_VSM.txt', 'SSA4_AGSANPROBASEVDE_PRV.txt', 'SSA4B_AS_CE_PRODCOQUI_COV.txt',
    'SSA4B_AS_CE_PRODPECHE_COV.txt', 'SSA1_LAIT.txt', 'SSA1_OEUF.txt', 'SSA1_GREN_ESCARG.txt',
    'SSA4_AGSANGREXPR_PRV.txt', 'SSA4_AGR_ESVEBO_PRV.txt', 'SSA4_AGSANGELAT_PRV.txt', 'SSA4_AGSANCOLL_PRV.txt',
    'SSA_PROD_RAFF.txt', 'SSA4_ASCCC_PRV.txt']

# start downloading files
def download_fr():
    download_files(base_url, files, directory)
import os
import requests
from pathlib import Path
from helper import check_url

####
# Austrian information on the approval number (german: Genusstauglichkeitskennzeichen)
# The information is distributed over different PDF files. This script downloads the files.
# Last checked 30th October 2023.
# The links might be broken by now. Last time I checked they changed the link. So I updated it.
####

def download_pdf(base_url, file, save_path):
    try:
        print(f"        downloading {file}")
        response = requests.get(base_url + file, allow_redirects=True)
        if response.status_code == 200:
            save_path.write_bytes(response.content)
        else:
            print(f"Failed to download file from {url}. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Failed to download file from {url}. Error: {e}")


def download_at():
    # the base url for all the pdf files
    base_url = 'https://vis.statistik.at/fileadmin/ovis/pdf/'

    # the pdf files
    pdf_files = ['I1.pdf', 'II2.pdf', 'III3.pdf', 'IV4.pdf', 'V5.pdf', 'VI6.pdf', 'VII7.pdf',
        'VIII8.pdf', 'IX9.pdf', 'X10.pdf', 'XI11.pdf', 'XII56.pdf', 'XIII12.pdf',
        'O20.pdf', 'I21.pdf', 'II22.pdf', 'III23.pdf', 'IV24.pdf', 'V25.pdf', 'VI26.pdf',
        'VII27.pdf', 'VIII28.pdf', 'IX29.pdf', 'X30.pdf', 'XI31.pdf', 'XII32.pdf', 'XIII33.pdf',
        'XIV34.pdf', 'XV35.pdf', '157.pdf', '241.pdf', '342.pdf', '443.pdf', '544.pdf',
        '645.pdf', '746.pdf', '847.pdf', '948.pdf', '1049.pdf', '1150.pdf', '1251.pdf',
        '1352.pdf', '1453.pdf', '1554.pdf', '1655.pdf']

    # check if url exists
    if not check_url(base_url):
        print(f"The URL '{base_url}' does not exist or is unreachable.")
        return

    # Create 'at' directory if it doesn't exist
    os.makedirs("at", exist_ok=True)
    
    # Download the pdf files
    for file in pdf_files:
        save_path = Path('at') / file
        if not save_path.is_file():
            download_pdf(base_url, file, save_path)

def main():
    download_at()

if __name__ == "__main__":
    main()
import requests
from pathlib import Path
import os.path

####
# Austrian information on the approval number (german: Genusstauglichkeitskennzeichen)
# The information is distributed over different PDF files. This script downloads the files.
# Last checked 30th October 2023.
# The links might be broken by now. Last time I checked they changed the link. So I updated it.
####

isExist = os.path.exists("at")
if not isExist:
   os.makedirs("at")

url = 'https://vis.statistik.at/fileadmin/ovis/pdf/'

files = ['I1.pdf', 'II2.pdf', 'III3.pdf', 'IV4.pdf', 'V5.pdf', 'VI6.pdf', 'VII7.pdf',
 'VIII8.pdf', 'IX9.pdf', 'X10.pdf', 'XI11.pdf', 'XII56.pdf', 'XIII12.pdf',
 'O20.pdf', 'I21.pdf', 'II22.pdf', 'III23.pdf', 'IV24.pdf', 'V25.pdf', 'VI26.pdf',
 'VII27.pdf', 'VIII28.pdf', 'IX29.pdf', 'X30.pdf', 'XI31.pdf', 'XII32.pdf', 'XIII33.pdf',
 'XIV34.pdf', 'XV35.pdf', '157.pdf', '241.pdf', '342.pdf', '443.pdf', '544.pdf',
 '645.pdf', '746.pdf', '847.pdf', '948.pdf', '1049.pdf', '1150.pdf', '1251.pdf',
 '1352.pdf', '1453.pdf', '1554.pdf', '1655.pdf']

for file in files:
    if(os.path.exists('at/' + file)):
        continue
    r = requests.get(url+file, allow_redirects=True)
    filename = Path('at/' + file)
    filename.write_bytes(r.content)
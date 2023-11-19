import requests
from pathlib import Path
import os.path

###
# French information on the approval number (german: Genusstauglichkeitskennzeichen)
# Downloads the data from the link. Last checked 30th October 2023.
# Link: https://fichiers-publics.agriculture.gouv.fr/dgal/ListesOfficielles/
# The links might be broken by now.
# I had to add ', verify = False' to re request due to some certificate error.#
# However, this is not recomended. It is a hack.
###

isExist = os.path.exists("fr")
if not isExist:
   os.makedirs("fr")

url = 'https://fichiers-publics.agriculture.gouv.fr/dgal/ListesOfficielles/'

files = ['SSA1_ACTIV_GEN.txt', 'SSA1_VIAN_ONG_DOM.txt', 'SSA1_VIAN_COL_LAGO.txt', 'SSA1_VIAN_GIB_ELEV.txt',
    'SSA1_VIAN_GIB_SAUV.txt', 'SSA1_VIAND_HACHE_VSM.txt', 'SSA4_AGSANPROBASEVDE_PRV.txt', 'SSA4B_AS_CE_PRODCOQUI_COV.txt',
    'SSA4B_AS_CE_PRODPECHE_COV.txt', 'SSA1_LAIT.txt', 'SSA1_OEUF.txt', 'SSA1_GREN_ESCARG.txt',
    'SSA4_AGSANGREXPR_PRV.txt', 'SSA4_AGR_ESVEBO_PRV.txt', 'SSA4_AGSANGELAT_PRV.txt', 'SSA4_AGSANCOLL_PRV.txt',
    'SSA_PROD_RAFF.txt', 'SSA4_ASCCC_PRV.txt']

for file in files:
    # I had to add ', verify = False' to re request due to some certificate error.#
    # However, this is not recomended. It is a hack.
    r = requests.get(url+file, allow_redirects=True, verify = False)
    filename = Path('fr/' + file)
    filename.write_bytes(r.content)
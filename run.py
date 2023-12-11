print("> DB creation started.")
print(">> Download started. This may take a while.")
print(">>> Started downloading")

print(">>> Downloading at")
from at_download import download_at
download_at()
print(">>> at download finished")

print(">>> Downloading ch")
from ch_download import download_ch
download_ch()
print(">>> ch download finished")

print(">>> Downloading fr")
from fr_download import download_fr
download_fr()
print(">>> fr download finished")

print(">> Download finished")

print(">> Started creating the DB. This may take a while.")

print(">>> Started at db creation. The processing takes a while. Stay tuned.")
import at_db_script
print(">>> at db creation finished")

print(">>> Started ch db creation")
import ch_db_script
print(">>> ch db creation finished")

print(">>> Started de db creation")
import de_db_script
print(">>> de db creation finished")

print(">>> Started fr db creation")
import fr_db_script
print(">>> fr db creation finished")

print(">>> Started it download and db creation")
import it_db_script
print(">>> it db creation finished")

print(">> DB creation finished")
print("> finished. enjoy")
# This is the main script to start downloading and processing the health mark information.

print("> DB creation started.")
print(">> Download started. This may take a while.")
print(">>> Started downloading")

# download the health mark information for Austria
print(">>> Downloading at")
from at_download import download_at
download_at()
print(">>> at download finished")

# download the health mark information for Switzerland
print(">>> Downloading ch")
from ch_download import download_ch
download_ch()
print(">>> ch download finished")

# download the health mark information for France
print(">>> Downloading fr")
from fr_download import download_fr
download_fr()
print(">>> fr download finished")

print(">> Download finished")

print(">> Started creating the DB. This may take a while.")

# Process the health mark information for Austria
print(">>> Started at db creation. The processing takes a while. Stay tuned.")
import at_db_script
print(">>> at db creation finished")

# Process the health mark information for Switzerland
print(">>> Started ch db creation")
import ch_db_script
print(">>> ch db creation finished")

# Process the health mark information for Germany
# The file needs to be downloaded first. It cannot easily be done due to the stupid implementation on the web site.
# See more information in the individual script.
print(">>> Started de db creation")
import de_db_script
print(">>> de db creation finished")

# Process the health mark information for France
print(">>> Started fr db creation")
import fr_db_script
print(">>> fr db creation finished")

# Process the health mark information for Italy.
# The script directly accesses the information on the web site.
# No download of the file is needed in advance.
print(">>> Started it download and db creation")
import it_db_script
print(">>> it db creation finished")

print(">> DB creation finished")
print("> finished. enjoy")
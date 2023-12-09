print("> DB creation started.")
print(">> Download started. This may take a while.")
print(">>> Started downloading")
from at_download import download_at
download_at()

print(">>> AT download finished")
from ch_download import download_ch
download_ch()

print(">>> CH download finished")
from fr_download import download_fr
download_fr()

print(">>> FR download finished")
print(">> Download finished")

print(">> Started creating the DB. This may take a while.")
import at_db_script
print(">>> AT DB creation finished")
import ch_db_script
print(">>> CH DB creation finished")
import de_db_script
print(">>> DE DB creation finished")
import fr_db_script
print(">>> FR DB creation finished")
import it_db_script
print(">>> IT DB creation finished")
print("> DB creation finished")
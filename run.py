from at_download import download_at
from ch_download import download_ch
from fr_download import download_fr
from at_db_script import process_at
from ch_db_script import process_ch
from de_db_script import process_de
from fr_db_script import process_fr
from it_db_script import process_it

def main():
    print("DB creation started.")
    print("Download started. This may take a while.")

    download_functions = [download_at, download_ch, download_fr]
    process_functions = [process_at, process_ch, process_de, process_fr, process_it]

    for download_function in download_functions:
        try:
            print(f"    Starting {download_function.__name__}")
            download_function()
            print(f"    Finished {download_function.__name__}")
        except Exception as e:
            print(f"    {download_function.__name__} failed: {e}")

    print("Download finished")
    print("Started creating the DB. This may take a while.")

    for process_function in process_functions:
        try:
            print(f"    Starting {process_function.__name__}")
            process_function()
            print(f"    Finished {process_function.__name__}")
        except Exception as e:
            print(f"    {process_function.__name__} failed: {e}")

    print("DB creation finished")
    print("Finished. Enjoy.")


if __name__ == "__main__":
    main()
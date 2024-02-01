# Herkunft daten

Who is the manufacturer of the milk, cheese or sausage, for example? Was the cheaper product produced by the same manufacturer as a well-known brand product?

In order to identify the producer of products of animal origin, the EU has introduced the so-called health mark. It is an oval symbol that includes, among other things, the country of origin and the approval number of the manufacturing company.

<img src="assets/image.png" alt="health mark example" width="200" height="auto">

I created an [App](https://github.com/rokozeit/herkunft) that let you identify manufacturer by selecting the country and the approval number.

**`I do not have an agreement with the authorities managing and maintaining the data to use the data. So I cannot provide the data or the app with the data. You unfortunatly need to do this part of the magic yourself.`**

The python scripts provided here download the content and add them to a sqlite data base. Due to usage rights I did not include the data files nor the data base.

Currently, the countries - Germany (DE), Austria (AT), Switzerland (CH), Italy (IT) and France (FR) are available here.

# Requirements / Known issues
## Python version
I am using the python library `camelot-py` to process the pdf files from Austria. I had some issues with version `0.11.0` and python `3.12`. It worked with python `3.12.1` or `3.11.x`.

## Additional software
In order to do the processing of the pdf file using [camelot-py](https://camelot-py.readthedocs.io/en/master/) you need to install ghostscript first as described [here](https://camelot-py.readthedocs.io/en/master/user/install-deps.html#install-deps).

## Python Package-Dependencies
Install the required packages e.g. like:

    pip install -r requirements.txt

See [requirements.txt](./requirements.txt)

- [pandas](https://pandas.pydata.org/)
master/)
- [requests](https://pypi.org/project/requests/)
- [pathlib](https://docs.python.org/3/library/pathlib.html)
- [lxml](https://lxml.de/)
- [html5lib](https://pypi.org/project/html5lib/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- [opencv-python](https://pypi.org/project/opencv-python/)
- [ghostscript](https://pypi.org/project/ghostscript/)
- [camelot-py](https://camelot-py.readthedocs.io/en/
## Runtime
The download will take some time. However, processing the PDF files from Austria took quite a while as well, really. So if you do not need them, commment out the part in `run.py`.

## German data
The German data cannot be downloaded by a script. So you need to download the data first (see below).

## Italy data
The italian data are downloads and processes in one script. So you will have to wait a view seconds (depending on your hardware) for the last step.

# Run the full scripts
Most of the magic is done automatically within the script `run.py`. If you do not intend to use all of the countries data, you can comment out the parts and the processing is much faster.

## Download German data manually

1. In this project create a folder named `de`
2. Download the XML file provided at the bottom of this [page](https://bltu.bvl.bund.de/bltu/app/process/bvl-btl_p_veroeffentlichung?execution=e1s3) and save it as `export.xml` in the folder `de`. It shoold look like:

        ./de/export.xml

## Run the script

Run the script `run.py` e.g.:

    python run.py

As already stated, it will take a while especially if Austria is included.

# Data format
Each country has its own table. I am using coutry codes as table names. So the table for Germany is called `de`, the table for Austria is called `at` and so on.

Each table has the same columns:
- **name** *(Text)*: The name of the producer
- **address** *(Text)*: The address - street-name number, postcode city - in this case - *however, any format would be ok. I am just handling this as a text field*.
- **approvalNo** *(Text)*: The actuall approval number of the EC identification and health marks
- **approvalNoOld** *(Text)*: The old number (I think this is used mainly in Germany)
- **comment** *(Text)*: Some additional information if it exists.

# How to use and search the data
As stated, there is an [App](https://github.com/rokozeit/herkunft) (currently for Windows and Android) you can use to search within the data.

# Additinal information
The EU provides a [list](https://food.ec.europa.eu/safety/biological-safety/food-hygiene/approved-eu-food-establishments/national-websites_en#list-of-eu-country-approved-establishments) of web pages to the country individual health mark information. All are provided in different formats. So there is no one solution for it all.

Further instructions on the processing of the different formats I am using are given as comment in the individual python scripts. so feel free to explore my solutions and find better once.

The first letters of the scripts indicate the country code: `de` (Germany), `at` (Austria), ... . This is also used as table name in the sqlite database.

Usually there is a file called `at_download.py` which is a download script for the content and a file called `at_db_script.py` which parses the downloaded file and populates the content in the sqlite db.

There was an issue with Python 3.12 and the `at_db_script.py` using the library `camelot`. I could not get it running. With 3.11 and 3.12.1 it worked.

Having created the data base you can use it in the [App](https://github.com/rokozeit/herkunft) (currently available for Windows and Android).

# Data Sources

| Country | Format | Link |
| ------- | ------ | ---- |
| at      | pdf    | https://vis.statistik.at/fileadmin/ovis/pdf/ |
| ch      | html   | https://kwk.blv.admin.ch/superglobal/wGlobal/scripts/php/bewilligungsliste/inc.list_to_csv.php?viewmode=csv&lang=en |
| de      | xml    | https://bltu.bvl.bund.de/bltu/app/process/bvl-btl_p_veroeffentlichung?execution=e1s2 |
| fr      | pdf    | https://fichiers-publics.agriculture.gouv.fr/dgal/ListesOfficielles/ |
| it      | html   | http://www.salute.gov.it/consultazioneStabilimenti/ConsultazioneStabilimentiServlet?ACTION=gestioneSingolaCategoria&idNormativa=2 |

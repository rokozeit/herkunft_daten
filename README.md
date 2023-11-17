# Herkunft daten

Who is the manufacturer of the milk, cheese or sausage, for example? Was the cheaper product produced by the same manufacturer as a well-known brand product?

In order to identify the producer of products of animal origin, the EU has introduced the so-called health mark. It is an oval symbol that includes, among other things, the country of origin and the approval number of the manufacturing company.

<img src="assets/image.png" alt="health mark example" width="200" height="auto">

I created an [app](https://github.com/rokozeit/herkunft) that let you identify manufacturer by selecting the country and the approval number.

I do not have an agreement with the authorities managing and maintaining the data to use the data. So I cannot provide the data or the app with the data. You unfortunatly need to do this part of the magig yourself.

The python scripts provided here download the content and add them to a sqlite data base. Due to usage rights I did not include the files nor the data base.

Instructions are given as comment in the individual python scripts.

The first letters indicate the country: `de` (Germany), `at` (Austria), ...

Usually there is a file called `at_download.py` which is a download script for the content and a file called `at_db_script.py` which parses the downloaded file and writes the content in the sqlite db.

There was an issue with Python 3.12 and the `at_db_script.py` using the library camelot. I could not get it running. With 3.11 it worked.

Currently, the countries - Germany (DE), Austria (AT), Switzerland (CH), Italy (IT) and France (FR) are available in the app.

Having created the data base you can use it in the [app](https://github.com/rokozeit/herkunft).

*__Just because a product comes from the same manufacturer does not mean it is the same product.__*
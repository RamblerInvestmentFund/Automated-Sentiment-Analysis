#!/usr/bin/python

import time
import pycurl
from pathlib import Path
from io import BytesIO



def main():
    buf = BytesIO()
    crl = pycurl.Curl()

    # Set URL value
    crl.setopt(crl.URL, 'https://finance.yahoo.com/')

    # Write bytes that are utf-8 encoded
    crl.setopt(crl.WRITEDATA, buf)

    # Perform a file transfer
    crl.perform()

    # End curl session
    crl.close()

    # Get the content stored in the BytesIO object (in byte characters)
    body = buf.getvalue()


    # Populate .../data subdirectory
    # If subdirectory doesnt exist, create folder
    Path("C:/Users/farin/PycharmProjects/Automated-Sentiment-Analysis/bitcoin scrape/scraper/data/yahoofinance").mkdir(parents=True, exist_ok=True)


    # Decode the bytes stored in get_body to HTML and print the result
    # print('Output of GET request:\n%s' % get_body.decode('utf8'))
    fname = "C:/Users/farin/PycharmProjects/Automated-Sentiment-Analysis/bitcoin scrape/scraper/data/yahoofinance/" + str(int(time.time())) + ".txt"
    with open(fname, "wb") as outfile:
        outfile.write(body)

if __name__ == "__main__":
    main()


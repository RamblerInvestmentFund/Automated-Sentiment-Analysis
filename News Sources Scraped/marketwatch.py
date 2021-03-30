import time
import pycurl
from io import BytesIO



def main():
    buf = BytesIO()
    crl = pycurl.Curl()

    # Set URL value
    crl.setopt(crl.URL, 'https://www.marketwatch.com/markets?mod=top_nav')

    # Write bytes that are utf-8 encoded
    crl.setopt(crl.WRITEDATA, buf)

    # Perform a file transfer
    crl.perform()

    # End curl session
    crl.close()

    # Get the content stored in the BytesIO object (in byte characters)
    body = buf.getvalue()

    # Decode the bytes stored in get_body to HTML and print the result
    # print('Output of GET request:\n%s' % get_body.decode('utf8'))

    fname = "/home/neil/bitcoin/scraper/data/https://www.marketwatch.com/markets?mod=top_nav/" + str(int(time.time())) + ".txt"
    with open(fname, "mw") as outfile:
        outfile.write(body)

if __name__ == "__main__":
    main()


import json
import pycurl
from io import BytesIO


class Binance:

    def __init__(self):
        return

    def getAvgTradePrice(self, symbol):

        buf = BytesIO() 
        crl = pycurl.Curl() 

        # Set URL value
        crl.setopt(crl.URL, 'https://api.binance.com/api/v3/ticker/price?symbol=' + symbol)

        # Write bytes that are utf-8 encoded
        crl.setopt(crl.WRITEDATA, buf)

        # Perform a file transfer 
        crl.perform() 

        # End curl session
        crl.close()

        # Get the content stored in the BytesIO object (in byte characters) 
        body = buf.getvalue()

        return json.loads(body)


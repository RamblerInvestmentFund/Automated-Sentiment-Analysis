#!/usr/bin/python


import pprint
import Binance
import mysql.connector


def main():

    dbc = mysql.connector.connect(host="127.0.0.1", user="root", password="699.tmp", database="bitcoin")


    cursor = dbc.cursor()

    b = Binance.Binance()

    result = b.getAvgTradePrice('BTCUSDT')
    price = float(result['price'])
    cursor.execute("insert into price_history (timestamp,price) values (now()," + str(price) + ")")
    dbc.commit()

if __name__ == "__main__":
    main()


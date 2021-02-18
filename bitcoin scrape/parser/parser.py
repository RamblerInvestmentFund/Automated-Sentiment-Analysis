#!/usr/bin/python


#from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup
import os
import re
import mysql.connector
import statistics
from FrontPage import FrontPage
import time
from tqdm import tqdm

def getBitcoinPrice(timestamp = None):


    if timestamp is not None:
        timestamp = int(timestamp)
    else:
        timestamp = time.time

    dbc = mysql.connector.connect(host="127.0.0.1", user="root", password="699.tmp", database="bitcoin")


    cursor = dbc.cursor()

    sql = 'select AVG(price) from price_history where timestamp >= from_unixtime(%d) and timestamp <= from_unixtime(%d)' % (timestamp, timestamp + 1800)
    cursor.execute(sql)
    price_result = cursor.fetchall()

    return price_result[0][0]


def findHeadlines(html):
    headlines = []

    page = BeautifulSoup(html, "html.parser")

    for tag in page.body.find_all('h3'):
        while ( hasattr (tag, 'contents') ):
            tag = tag.contents[0]
        headlines.append(tag)

    for tag in page.body.find_all('h4'):
        try:
            while ( hasattr (tag, 'contents') ):
                tag = tag.contents[0]
            headlines.append(tag)
        except:
            continue

    return headlines

def findWordPairsInHeadlines(headlines):
    
    pairs = []
    for hl in headlines:
        words = hl.split()

        # Get rid of all non-alphanumeric characters in headlines and 's' at end of words
        for k in range(len(words)-1):
            words[k] = re.sub(r'\W+', '', words[k])
            words[k+1] = re.sub(r'\W+', '', words[k+1])
            words[k] = re.sub(r's+$', '', words[k].lower());
            words[k+1] = re.sub(r's+$', '', words[k+1].lower());
            pairs.append([words[k], words[k+1]])

    return pairs


def findWordPairsInFile(fname):
    with open(fname, "r") as outfile:
        current_html = outfile.read()

    current_headlines = findHeadlines(current_html)

    return findWordPairsInHeadlines(current_headlines)


def main():

    files = os.listdir('/home/neil/bitcoin/scraper/data/wsj.com/')

    files.sort(reverse=True)

    last_page = FrontPage('/home/neil/bitcoin/scraper/data/wsj.com/' + files[1], int(files[1].split(".")[0]))
    most_recent_page = FrontPage('/home/neil/bitcoin/scraper/data/wsj.com/' + files[0], int(files[0].split(".")[0]))

    print("Loading web page data...")
    front_pages = []
    for fname in tqdm(files[72:len(files)]):
        front_pages.append(FrontPage('/home/neil/bitcoin/scraper/data/wsj.com/' + fname, int(fname.split(".")[0])))

    print("finished loading headlines...")

    for pair in most_recent_page.pairs:
        n_articles = 0
        price_deltas = []
        stale_article = False
        for fp in front_pages:
            if (pair in fp.pairs) and (pair not in last_page.pairs) and (stale_article == False):

                # Make sure that we mark that we've already seen this reporting
                stale_article = True

                n_articles += 1

                # Get price when article was scraped
                p1 = getBitcoinPrice(fp.timestamp)

                # Get price three hours later
                p2 = getBitcoinPrice(fp.timestamp + 1 * 3600)

                # Calc price delta
                if (p1 is not None) and (p2 is not None):
                    delta = p2 - p1
                    price_deltas.append(delta)
            elif (pair not in fp.pairs):
                stale_article = False

        if len(price_deltas) > 4:
            if abs(statistics.mean(price_deltas)) > statistics.stdev(price_deltas) / 2:
                print("Price deltas for " + str(pair) + " (based on " + str(n_articles) + " articles): mean = " + str(statistics.mean(price_deltas)) + " stddev = " + str(statistics.stdev(price_deltas)))


    """
    fname = "/home/neil/bitcoin/scraper/data/wsj.com/" + files[0]
    current_word_pairs = findWordPairsInFile(fname)

    # Iterate over each word pair in the most recent WSJ grab
    for pair in current_word_pairs:
        price_deltas = []
        stale_article = False

        # Iterate backwards thru all front page grabs of the WSJ starting at oldest proceeding to newest
        for k in range(len(files)-1, 144, -1):
            if (pair in findWordPairsInFile("/home/neil/bitcoin/scraper/data/wsj.com/" + files[k])) and stale_article == False:
                # Make sure that we mark that we've already seen this reporting
                stale_article = True
                # Get price when article was scraped
                p1 = getBitcoinPrice(files[k].split(".")[0])

                # Get price three hours later
                p2 = getBitcoinPrice(int(files[k].split(".")[0]) + 1 * 3600)

                # Calc price delta
                if (p1 is not None) and (p2 is not None):
                    delta = p2 - p1
                    price_deltas.append(delta)
            elif (pair not in findWordPairsInFile("/home/neil/bitcoin/scraper/data/wsj.com/" + files[k])):
                stale_article = False

        if len(price_deltas) > 4:
            print("Price deltas for pair " + str(pair) + ": mean = " + str(statistics.mean(price_deltas)) + " stddev = " + str(statistics.stdev(price_deltas)))
    """


if __name__ == "__main__":
    main()


# Automated-Sentiment-Analysis
This project looks to scrape news source sites and utilize such NLP transformers like Google’s BERT. The goal is to see if we can take an analyzed news article and correctly predict the direction a stock price will move. 


## Neil's description of bitcoin scrape
The archive has a main directory and three subdirectories: parser, price-grabber, and scraper. scraper.py downloades the WSJ front page using cURL and stores it in the directory bitcoin/scraper/data/wsj.com/XXX.txt. It names files according to the UNIX epoch when they were downloaded (epoch is the number of seconds since Jan 1, 1970 UTC. See http://epochconverter.com). You’ll have to create the data/wsj.com subdirectory inside the scraper directory for the scraper.py script to run correctly. I’m using the cron deamon in Linux to run the scraper every 20 minutes. The price-grabber script uses an API call to the Binance API to capture the current exchange rate from Bitcoin to USD and record it in a database. I’m also using cron daemon to run the price-grabber every 2 minutes. I created a MySQL database on my computer to store the prices. The parser script implements a Bayesian inference model to forecast future exchange rates.


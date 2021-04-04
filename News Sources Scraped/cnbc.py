#!/usr/bin/python

import time
import pycurl
import os
from io import BytesIO

#cd into ../Automated-Sentiment-Analysis/News Sources Scraped/cnbc_scraper before calling python3 cnbc.py
#note: there is some noise on this webiste

def main():
    buf = BytesIO() 
    crl = pycurl.Curl() 

    # Set URL value
    crl.setopt(crl.URL, 'https://www.cnbc.com')

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



    #set up directories
    scraped_data_path =  'data/cnbc.com'                          #directory path containing scraped news source data (should create data/cnbc.com dir within current repo dir)
    dir_command = 'mkdir -p ' + scraped_data_path                 #command to create directories designated in scrape_path
    os.system(dir_command)

    parsed_data_path =  'data/cnbc_headlines'                     #directory path containing parsed raw data
    dir_command = 'mkdir -p ' + parsed_data_path                  #command to create directories designated in parse_path
    os.system(dir_command)

    csv_data_path = 'data/cnbc_csv'                               #directory path containing cnbc csv (timestamp + headlines)
    dir_command = 'mkdir -p ' + csv_data_path                     #command to create directories designated in parse_path
    os.system(dir_command)

    current_scrape = str(int(time.time()))                        #label current scrape according to epoch at download time
    fname = scraped_data_path + '/' + current_scrape + '.txt'     #create file named according to epoch at download time within data path directory
    with open(fname, "wb") as outfile:                            #file contains cnbc front page info in html including headlines...
        outfile.write(body)




if __name__ == "__main__":
    main()


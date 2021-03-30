import os
from bs4 import BeautifulSoup

#parsing is a bit messy - extracts article headlines, but also other titles embedded on the website

def parsehtml():
    parsed = []                                                                                  #folder containing epoch file names that have already been parsed
    data_path = 'data/cnbc.com'                                                                  #path of directories containing news source data (should create data/cnbc.com dir within current repo dir)
    for entry in os.scandir(data_path):                                                          #for each scrape entry in cnbc.com folder
        if (entry.path.endswith(".txt") and entry.is_file() and entry.name[:-4] not in parsed):  #check if file is not in parsed list or has already been parsed
            parsed.append(entry.name[:-4])                                                       #add file to parsed list
            with open(entry.path, "r") as htmlfile:                                              #open html file
                soup = BeautifulSoup(htmlfile,'html.parser')                                     #create beautiful soup object and indicate parser
                infile = 'data/cnbc_headlines/headlines_' + entry.name[:-4] + '.txt'             #file named after epoch to contain headlines
                with open(infile, 'a') as outfile:
                    for title in soup.find_all('a'):                                             #find all <a> tags in html file
                        headline = title.get_text()                                              #get text headline
                        outfile.write(headline + '\n')                                           #write headline to file
                outfile.close()

        else: continue                                                                           #if file has been parsed continue



if __name__ == "__main__":
    parsehtml()

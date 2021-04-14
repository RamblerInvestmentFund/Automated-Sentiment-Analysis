import os
from datetime import timedelta
import datetime
import pandas as pd
from bs4 import BeautifulSoup

#parses Latest News Section and collects Headline + Timestamp
#initially puts data into a 'raw data' text file
#converts text file to csv which includes upload time of headline in epoch


#function to get article's time of upload in epoch
def get_uploadTime(epoch_time, elapsed_time):
    download = datetime.datetime.fromtimestamp(int(epoch_time))                                  #convert epoch to date format (%Y-%m-%d %H:%M:%S")
    elapsed_data = elapsed_time.split()                                                          #split elapsed time into list

    if (elapsed_data[1] == 'Hour' or elapsed_data[1] == 'Hours'):                                #if time elapsed is Hour or Hours
        hour = int(elapsed_data[0])                                                              #set hour to amount of hours elapsed
        minute = 0                                                                               #set minutes to 0
    elif(elapsed_data[1] != 'Minute' or elapsed_data[1] != 'Minutes'):                           #if time elapsed is Minute or Minutes
        hour = 0                                                                                 #set hours to 0
        minute = int(elapsed_data[0])                                                            #set minute to amount of minutes elapsed

    calculate_time = download - timedelta(hours=hour, minutes=minute)                            #calculate upload time by subtracting time at download by time elapsed since upload

    epoch = datetime.datetime.strptime(str(calculate_time), "%Y-%m-%d %H:%M:%S").timestamp()     #convert upload time to epoch format

    return str(epoch)


#function to convert raw data to csv
def to_csv(infile):
    outfile = "data/cnbc_csv/cnbc_ALL_headlines.csv"                                                   #designate outfile (issue its empty at first, will comparisons work with different dim df)
    teslafile = "data/cnbc_csv/tesla_headlines.cvs"
    if((os.path.exists(outfile) == False)):
        df = pd.read_csv(infile, delimiter="\t")                                                       #read raw data into data frame
        for index, row in df.iterrows():                                                               #for each row in data frame
            epoch = row["Download-Time"]                                                               #set download time as epoch at download
            elapsed = row["Elapsed-Time"]                                                              #set elapsed to time elapsed since upload
            upload = get_uploadTime(epoch, elapsed)                                                    #call function get_uploadTime
            df.at[index, 'Upload-Time'] = upload                                                       #append upload time to appropriate row
        df = df.loc[::-1].reset_index(drop = True)
        contains_Tesla = df[df['Headline'].str.contains("Tesla|Tesla Motors|TSLA|SpaceX|Elon Musk|Elon Musk's|Musk")]
        df.to_csv(outfile, index=False)                                                                #write to csv
        contains_Tesla.to_csv(teslafile, index=False)
    elif((os.path.exists(outfile) == True)):
        master = pd.read_csv(outfile)                                                                  #read master csv
        last_headline = master['Headline'].iloc[-1]                                                    #get last recorded headline from ALL headlines file
        df = pd.read_csv(infile, delimiter="\t")                                                       #read raw data into data frame
        i = df.index[df['Headline'] == last_headline].tolist()
        if not i:
            for index, row in df.iterrows():                                                           #for each row in data frame
                epoch = row["Download-Time"]                                                           #set download time as epoch at download
                elapsed = row["Elapsed-Time"]                                                          #set elapsed to time elapsed since upload
                upload = get_uploadTime(epoch, elapsed)                                                #call function get_uploadTime
                df.at[index, 'Upload-Time'] = upload                                                   #append upload time to appropriate row
            df = df.loc[::-1].reset_index(drop = True)
            contains_Tesla = df[df['Headline'].str.contains("Tesla|Tesla Motors|TSLA|SpaceX|Elon Musk|Elon Musk's|Musk")]
            df.to_csv(outfile, mode='a', index=False, header=False)                                    #write to csv
            contains_Tesla.to_csv(teslafile, mode='a', index=False, header=False)
        else:
            new, recorded = df.iloc[:i[0], :], df.iloc[i[0]:, :]
            for index, row in new.iterrows():                                                          #for each row in data frame
                epoch = row["Download-Time"]                                                           #set download time as epoch at download
                elapsed = row["Elapsed-Time"]                                                          #set elapsed to time elapsed since upload
                upload = get_uploadTime(epoch, elapsed)                                                #call function get_uploadTime
                new.at[index, 'Upload-Time'] = upload                                                  #append upload time to appropriate row
            new = new.loc[::-1].reset_index(drop = True)
            contains_Tesla = new[new['Headline'].str.contains("Tesla|Tesla Motors|TSLA|SpaceX|Elon Musk|Elon Musk's|Musk")]
            new.to_csv(outfile,  mode='a', index=False, header=False)                                  #write to csv
            contains_Tesla.to_csv(teslafile, mode='a', index=False, header=False)


#function to parse html content and create text file containing raw data
def parsehtml():
    data_path = 'data/cnbc.com'                                                                           #path of directories containing news source data (should create data/cnbc.com dir within current repo dir)
    for entry in os.scandir(data_path):                                                                   #for each scrape entry in cnbc.com folder
        infile = 'data/cnbc_headlines/raw_data_' + entry.name[:-4] + '.txt'                               #file named after epoch to contain headlines
        if(entry.path.endswith(".txt") and entry.is_file() and (os.path.exists(infile) == False)):        #check if file is not in parsed list or has already been parsed
            with open(entry.path, "r") as htmlfile:                                                       #open html file
                soup = BeautifulSoup(htmlfile,'html.parser')                                              #create beautiful soup object and indicate parser
                with open(infile, 'a') as outfile:
                    outfile.write("Download-Time" + '\t' + "Elapsed-Time" + '\t' + "Upload-Time" + '\t' + "Headline" + '\n')      #write headers to outfile
                    headlines = soup.find_all("a", class_="LatestNews-headline")                                                  #find all Latest News Headlines
                    timestamps = soup.find_all("time", class_="LatestNews-timestamp")                                             #find all Latest News Timestamps
                    for headline, timestamp in zip(headlines, timestamps):                                                        #for each corresponding headline + timestamp
                        if(timestamp.get_text()[0].isdigit() == True):                                                            #if headline was uploaded no later than 24 hours ago
                            outfile.write(entry.name[:-4] + '\t' + timestamp.get_text() + '\t' + 'conversion-needed' + '\t' + headline.get_text() + '\n')    #write to txt file in tab delimited format
                outfile.close()
            htmlfile.close()
            to_csv(infile)                                                                                 #call function to convert raw data to csv
        else: continue                                                                                     #if file has been parsed continue


if __name__ == "__main__":
    parsehtml()



import urllib.request
import csv
import argparse
import re

def downloadData(url):

#Grabs Data from the url received and decodes
    with urllib.request.urlopen(url) as response:
        response = response.read().decode('utf-8')
    return response

def csvParser(file):
#Takes data from a downloaded file and splits it into a list of all information
    dataList = []
    reader = csv.reader(file.strip().split('\n'))
    for line in reader:
        img = line[0]
        date = line[1]
        browser = line[2]
        status = line[3]
        size = line[4]
        all_info = line[0:]
        dataList.append(all_info)
    return dataList
def imageHits(file):
#Finds all image requests by using regex to search for those extensions
    imghits = 0
    allhits = len(file)
    imgPercent = 0
    for lists in file:
        if re.search(r"(jpe?g|gif|png)", lists[0], re.IGNORECASE):
            imghits += 1
            imgPercent = imghits/allhits *100
    print("Image requests account for {}% of all requests".format(imgPercent))

def browserCount(file):
#Finds the most popular browser of the day via regex search within the user-agent data
    browserDict = {
        "FireFox": 0,
        "Internet Explorer": 0,
        "Chrome": 0,
        "Safari": 0
    }

    for lists in file:
        if re.search(r"FireFox", lists[2], re.IGNORECASE):
            browserDict["FireFox"] += 1
        if re.search(r"Internet Explorer", lists[2], re.IGNORECASE):
            browserDict["Internet Explorer"] += 1
        if re.search(r"Chrome", lists[2], re.IGNORECASE):
            browserDict["Chrome"] += 1
        if re.search(r"Safari", lists[2], re.IGNORECASE):
            browserDict["Safari"] += 1

    mostPopular = max(browserDict.values())
    for key in browserDict.keys():
        if browserDict[key] == mostPopular:
            print("Today's most popular browser is " +key)

def main(url):

    csvFile = downloadData(url)
    csvData = csvParser(csvFile)
    imageHits(csvData)
    browserCount(csvData)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
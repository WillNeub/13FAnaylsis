import sqlite3
import pandas as pd
import requests
import xml.etree.ElementTree as ET
import re

def readTable():
    connect = sqlite3.connect(r"C:\Users\willn\OneDrive\Documents\Asset_Managers.db")
    df = pd.read_sql("SELECT * FROM AssetManagers", connect)
    connect.close()
    return df

def fixCIK(input):
    if len(str(input)) < 10:
        return str(input).zfill(10)
    return input

def getFilings(cik):
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"

    response = requests.get(url, headers = HEADERS, timeout = 10)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None
    
def getAccessionNumber(data):
    for index, form in enumerate(data["filings"]["recent"]["form"]):
        if form == "13F-HR":
            accession_with_dashes = data["filings"]["recent"]["accessionNumber"][index]
            accessionNumber = data["filings"]["recent"]["accessionNumber"][index].replace("-", "")
            return accessionNumber, accession_with_dashes
        if form == "13F-NT":
            return "Filed under parent 13F"
    return (None, None)

def getAUM(cik, accessionNumber, accessionNumberDash):
    url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accessionNumber}/{accessionNumberDash}.txt"

    response = requests.get(url, headers = HEADERS, timeout = 10)
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return None
    
    xmlSections = re.findall(r"<XML>.*?</XML>", response.text, re.DOTALL)
    formatedContent = re.findall(r"value>(\d+)<", xmlSections[1], re.DOTALL)
    totalAUM = 0
    for i, values in enumerate(formatedContent):
        totalAUM += int(values)
    formatedAUM = "{:,}".format(totalAUM)
    adjustedAUM = "{:,}".format(totalAUM * 1000)
    if totalAUM * 1000 > 10000000000000:
        return formatedAUM
    else:
        return (adjustedAUM, formatedAUM)
    
# = pd.read_excel(r"C:\Users\willn\OneDrive\Documents\Asset_Managers.xlsx", engine = "openpyxl")
#data = [tuple(x) for x in df[['Fund Name', 'CIK Number']].values]
#for i, aum in enumerate(aumData, start=1):
    #cursor.execute("UPDATE AssetManagers SET Equities_Under_Management = ? WHERE id = ?", (aum, i))

HEADERS = {
    "User-Agent": "MyApp/1.0 (willneubauer31@gmail.com)",
    "Accept": "application/json"
}

connect = sqlite3.connect(r"C:\Users\willn\OneDrive\Documents\Asset_Managers.db")
cursor = connect.cursor()

dateList = ["At_2024_12_31", "At_2024_09_30", "At_2024_06_30", "At_2024_03_31", 
            "At_2023_12_31", "At_2023_09_30", "At_2023_06_30", "At_2023_03_31", 
            "At_2022_12_31", "At_2022_09_30", "At_2022_06_30", "At_2022_03_31",
            "At_2021_12_31", "At_2021_09_30", "At_2021_06_30", "At_2021_03_31",
            "At_2020_12_31", "At_2020_09_30", "At_2020_06_30", "At_2020_03_31",
            "At_2019_12_31", "At_2019_09_30", "At_2019_06_30", "At_2019_03_31",
            "At_2018_12_31", "At_2018_09_30", "At_2018_06_30", "At_2018_03_31",
            "At_2017_12_31", "At_2017_09_30", "At_2017_06_30", "At_2017_03_31",
            "At_2016_12_31", "At_2016_09_30", "At_2016_06_30", "At_2016_03_31",
            "At_2015_12_31", "At_2015_09_30", "At_2015_06_30", "At_2015_03_31",
            "At_2014_12_31", "At_2014_09_30", "At_2014_06_30", "At_2014_03_31",
            "At_2013_12_31", "At_2013_09_30", "At_2013_06_30", "At_2013_03_31",
            "At_2012_12_31", "At_2012_09_30", "At_2012_06_30", "At_2012_03_31",
            "At_2011_12_31", "At_2011_09_30", "At_2011_06_30", "At_2011_03_31",
            "At_2010_12_31", "At_2010_09_30", "At_2010_06_30", "At_2010_03_31"]

data = readTable()
for index, row in data.iterrows():
    id = row['id']
    fundName = row['Fund_Name']
    cikNumber = row['CIK_Number']
    cik = fixCIK(cikNumber)
    print(cik)
    #getFilings(cik)
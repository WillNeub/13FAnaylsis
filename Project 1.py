import requests
import json
import xml.etree.ElementTree as ET
import re
import pandas as pd

HEADERS = {
    "User-Agent": "MyApp/1.0 (willneubauer31@gmail.com)",
    "Accept": "application/json"
}

def addAUM(aum):
    df = pd.read_excel(r"C:\Users\willn\OneDrive\Documents\Asset_Managers.xlsx", engine = "openpyxl")
    df["AUM"] = []
    df.to_excel("", index=False, engine="openpyxl")

def getCIK(fundName):
    df = pd.read_excel(r"C:\Users\willn\OneDrive\Documents\Asset_Managers.xlsx", engine = "openpyxl")
    result = df[df["Fund Name"] == fundName]
    row = result.index[0]
    return(result.at[row, "CIK Number"])

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

data = getFilings("0001390113")
accessionTup = getAccessionNumber(data)
accessionNumber, accessionNumberDash = accessionTup
print(accessionTup)
#aum = getAUM(cik, accessionNumber, accessionNumberDash)
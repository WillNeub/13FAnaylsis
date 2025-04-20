import SQL_Connect as sql_c
import pandas as pd

data = sql_c.readTable()

for index, row in data.iterrows():
    tableCik = row["CIK_Number"]
    cik = sql_c.fixCIK(tableCik)
    file = sql_c.getFilings(cik)
    accessionNumber, accession_with_dashes = sql_c.getAccessionNumberForDate(file, "2024-12-31")
    print(accessionNumber, accession_with_dashes)
    print(cik)
    print(sql_c.getHoldings(cik, accessionNumber, accession_with_dashes))
    break
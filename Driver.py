import SQL_Connect as sql_c
import pandas as pd
import sqlite3

data = sql_c.readTable()

final = pd.DataFrame()
count = 0
index = 0
for index, row in data.iterrows():
    fundName = row["Fund_Name"]
    if fundName == "Greenlight Capital":
        continue
    tableCik = row["CIK_Number"]
    cik = sql_c.fixCIK(tableCik)
    file = sql_c.getFilings(cik)
    accessionNumber, accession_with_dashes = sql_c.getAccessionNumberForDate(file, "2024-12-31")
    df = sql_c.getHoldings(cik, accessionNumber, accession_with_dashes)
    df["Class"] = df["Class"].apply(sql_c.normalizeTitle)
    df.insert(0, "FundName", fundName)
    df.insert(0, "id", range(len(final), len(final) + len(df)))
    index += 1
    if count == 0:
        final = df
        count += 1
        continue
    final = pd.concat([final, df], ignore_index=True)

conn = sqlite3.connect("Asset_Managers.db")
final.to_sql("At_2024_12_31", conn, if_exists="replace", index=False)

conn.close()
"""
fundName = "Baupost Group"
tableCik = 1061768
cik = sql_c.fixCIK(tableCik)
file = sql_c.getFilings(cik)
accessionNumber, accession_with_dashes = sql_c.getAccessionNumberForDate(file, "2024-12-31")
print(accessionNumber, accession_with_dashes)
print(cik)
df = sql_c.getHoldings(cik, accessionNumber, accession_with_dashes)
df["Class"] = df["Class"].apply(sql_c.normalizeTitle)
df.insert(0, "FundName", fundName)
print(df)
"""
import numpy as np
import pandas as pd
from tabulate import tabulate

from urllib.request import urlopen
from bs4 import BeautifulSoup

def getHTMLContent(link):
    html = urlopen(link)
    soup = BeautifulSoup(html, 'html.parser')
    return soup

content = getHTMLContent("https://merolagani.com/LatestMarket.aspx")

table = content.find('table', {'class': 'table table-hover live-trading sortable'})
rows = table.find_all('tr')

data = []
names = ["ALICL (Asian Life Insurance Co. Limited)",
"BOKL (Bank of Kathmandu Ltd.)",
"CHCL (Chilime Hydropower Company Limited)",
"KBL (Kumari Bank Limited)",
"NCCB (Nepal Credit And Commercial Bank Limited)",
"NIB (Nepal Investment Bank Limited)",
"NLICL (National Life Insurance Co. Ltd.)",
"SBL (Siddhartha Bank Limited)",
"SHL (Soaltee Hotel Limited)",
"SICL (Shikhar Insurance Co. Ltd.)"]

initial_prices = {
    "ALICL (Asian Life Insurance Co. Limited)" : 412,
    "BOKL (Bank of Kathmandu Ltd.)" : 328,
    "CHCL (Chilime Hydropower Company Limited)" : 681,
    "KBL (Kumari Bank Limited)" : 248,
    "NCCB (Nepal Credit And Commercial Bank Limited)" : 214,
    "NIB (Nepal Investment Bank Limited)" : 551,
    "NLICL (National Life Insurance Co. Ltd.)" : 603,
    "SBL (Siddhartha Bank Limited)" : 291,
    "SHL (Soaltee Hotel Limited)" : 204,
    "SICL (Shikhar Insurance Co. Ltd.)" : 906
}

quantity = {
    "ALICL (Asian Life Insurance Co. Limited)" : 300,
    "BOKL (Bank of Kathmandu Ltd.)" : 200,
    "CHCL (Chilime Hydropower Company Limited)" : 200,
    "KBL (Kumari Bank Limited)" : 1000,
    "NCCB (Nepal Credit And Commercial Bank Limited)" : 500,
    "NIB (Nepal Investment Bank Limited)" : 200,
    "NLICL (National Life Insurance Co. Ltd.)" : 210,
    "SBL (Siddhartha Bank Limited)" : 296,
    "SHL (Soaltee Hotel Limited)" : 500,
    "SICL (Shikhar Insurance Co. Ltd.)" : 900
}

for row in rows:
    try:    
        name = str(row.find_all('td')[0].find_all('a')[0].get('title'))
    except:
        continue
    price_raw = str(row.find_all('td')[1].renderContents().strip())[2:-1]
    price = int(price_raw.replace(",", "").split(".")[0])

    if name in names:
        data.append([name, price, initial_prices[name], price - initial_prices[name], quantity[name]])

new_df = pd.DataFrame(data)
new_df.columns = ["Name", "Today's Price", "Initial Price", "Profit", "Quantity"]
new_df["Initial Amount"] = new_df["Initial Price"] * new_df["Quantity"]
new_df["Today's Amount"] = new_df["Today's Price"] * new_df["Quantity"]
new_df["Profit Amount"] = new_df["Profit"] * new_df["Quantity"]

print(tabulate(new_df, headers='keys', tablefmt='fancy_grid'))

print("Today's profit amount is: ", new_df["Profit Amount"].sum())
print("The highest profit amount is", new_df["Profit Amount"].max(), "from", new_df["Name"][new_df["Profit Amount"].idxmax()])
print("The least profit amount is", new_df["Profit Amount"].min(), "from", new_df["Name"][new_df["Profit Amount"].idxmin()])
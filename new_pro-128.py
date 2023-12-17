import pandas as pd
import requests
from bs4 import BeautifulSoup


BROWN_DWARF_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"
response = requests.get(BROWN_DWARF_URL)


soup = BeautifulSoup(response.text, "html.parser")
tables = soup.find_all("table",{"class":"wikitable sortable"})
total_table = len(tables)
table_rows = tables[1].find_all('tr')
all_rows = []



for row in table_rows:
    table_cols = row.find_all('td')
    row_data = [col.text.rstrip() for col in table_cols]
    all_rows.append(row_data)


brown_dwarf_data = []
star_name = []
distance = []

for i in range(1, len(all_rows)):
        star_name.append(all_rows[i][0])
        distance.append(all_rows[i][3])

headers_brown_dwarf = ['Star_name', 'Distance']
brown_dwarf_df = pd.DataFrame(list(zip(star_name,distance)), columns=headers_brown_dwarf)
brown_dwarf_df.to_csv("dwarf_star.csv", index=True, index_label='id')

    

import pandas as pd , time
from bs4 import BeautifulSoup
from selenium import webdriver
import requests

BROWN_DWARF_URL = "https://en.wikipedia.org/wiki/Brown_dwarf"

browser = webdriver.Edge()
browser.get(BROWN_DWARF_URL)

scraped_data = []
time.sleep(7)
def scrape():
    soup = BeautifulSoup(browser.page_source, "html.parser")

    bright_star_table = soup.find_all("table", attrs={"class", "sortable"})
    table_body = bright_star_table.find_all('tbody')
    table_rows = table_body.find_all('tr')

    for row in table_rows:
        table_cols = row.find_all('td')

        temp_list = []

        for col_data in table_cols:
            data = col_data.text.strip()
            temp_list.append(data)

        scraped_data.append(temp_list)

scrape()

# Print scraped_data to inspect the structure
for row in scraped_data:
    print(row)

# Update indices based on the structure of the table
stars_data = []

for i in range(0, len(scraped_data)):
    Star_names = scraped_data[i][1]  # Update index
    Distance = scraped_data[i][3]    # Update index

    required_data = [Star_names, Distance]
    stars_data.append(required_data)

headers = ['Star_name', 'Distance']
star_df_1 = pd.DataFrame(stars_data, columns=headers)
star_df_1.to_csv("scraped_data_1.csv", index=True, index_label='id')


response = requests.get(BROWN_DWARF_URL)


soup_brown_dwarf = BeautifulSoup(response.text, "html.parser")
tables = soup_brown_dwarf.find_all("table", class_="wikitable")


all_rows = []

for table in tables:
    table_body = table.find_all('tbody')
    table_rows = table_body.find_all('tr')

    for row in table_rows:
        table_cols = row.find_all('td')
        row_data = [col.text.strip() for col in table_cols]
        all_rows.append(row_data)


brown_dwarf_data = []

for i in range(0, len(all_rows)):
    if len(all_rows[i]) >= 4: 
        star_name = all_rows[i][0]
        radius = all_rows[i][1]
        mass = all_rows[i][2]
        distance = all_rows[i][3]

        brown_dwarf_data.append([star_name, radius, mass, distance])

headers_brown_dwarf = ['Star_name', 'Radius', 'Mass', 'Distance']
brown_dwarf_df = pd.DataFrame(brown_dwarf_data, columns=headers_brown_dwarf)
brown_dwarf_df.to_csv("scraped_data_brown_dwarf.csv", index=True, index_label='id')

    


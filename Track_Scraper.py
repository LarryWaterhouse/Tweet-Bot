from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv

#Get Track Data for given event & year
event = 1
page = 0
url = 'https://www.athletic.net/TrackAndField/Division/Event.aspx?DivID=125809&Event='+ str(event) + '&page='+ str(page) +'&restrict=1'
row_data = []
def get_track_times(page):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    table = soup.find('table', class_='HLData DataTable table table-hover table-striped blur-results')


    for row in table.findAll('tr'):
        col = row.findAll('td')
        col = [ele.text.strip() for ele in col]
        row_data.append(col)
    return row_data

for x in range(0,400):
        get_track_times(x)

data = get_track_times(url)

df = pd.DataFrame(data)
print(df)

import os
from bs4 import BeautifulSoup
import requests
import json
import getXGByGame
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()
URI = os.getenv('URI')

# Set the Stable API version when creating a new client
client = MongoClient(URI)
db = client['chelsea-stats']
coll = db['chelsea-xg']
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    exit()

originalUrl = "https://fbref.com/en/squads/cff3d9bb/Chelsea-Stats"
req = requests.get(originalUrl)
text = req.text
soup = BeautifulSoup(text, 'html.parser')
script = soup.find_all('script', type='application/ld+json')
entries = []

urls = json.loads(script[1].text)
for url in urls:
    date = url['startDate']
    if url['location']['name'] == "Stamford Bridge":
        competitor = url['competitor'][0]['name']
    else:
        competitor = url['competitor'][1]['name']
    print(f"Scraping the {competitor} game on {date}")
    entry = getXGByGame.main(url['url'], date, competitor)
    # print(entry)
    if entry: 
        print("hit in entries")
        entries.append(entry)
    else:
        pass

for documents in entries:
    for document in documents:
        coll.insert_one(document)
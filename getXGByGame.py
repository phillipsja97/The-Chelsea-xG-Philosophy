import os
from bs4 import BeautifulSoup
import requests
import json

def main(args1, args2, args3):
    gameUrl = f"{args1}"
    req = requests.get(gameUrl)
    text = req.text
    # if text.
    chelsea_id = "shots_cff3d9bb"
    soup = BeautifulSoup(text, 'html.parser')
    statsList = []
    xg = ""
    outcome = ""
    distance = ""
    body_part = ""

    if soup.find(class_="stats_table sortable min_width"):
        table = soup.find(class_="stats_table sortable min_width")
        stats = table.find_all(class_=chelsea_id)
        date = args2
        competitor = args3
        for stat in stats:
            # Get Name
            href = stat.find_all('a')
            name = href[0].get_text()
            # Get xG and stats
            tds = stat.find_all('td')
            for td in tds:
                if "psxg_shot" in str(td):
                    pass
                elif "xg_shot" in str(td):
                    xg = td.text
                if "outcome" in str(td):
                    outcome = td.text
                elif "distance" in str(td):
                    distance = td.text
                elif "body_part" in str(td):
                    body_part = td.text
                else:
                    pass
            mydict = { "date": date, "competitor": competitor, "name": name, "xg": xg, "outcome": outcome, "distance": distance, "bodyPart": body_part }
            statsList.append(mydict)
        return statsList
    else:
        pass
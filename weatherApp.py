from flask import Flask, render_template

import requests
import json

app = Flask(__name__)                   # flask application server

@app.route("/")                         # controller routing to method handler
def airiesInlet():
    host = "www.bom.gov.au"
    headers = {
    'User-Agent': 'My User Agent 1.0'
    }                                   # pretend not to be a bot
    try:
        url = "http://" + host + "/fwo/IDV60801/IDV60801.94846.json"
        r = requests.get(url, headers=headers) # added header to pretend not to be a bot
        # print(r.text) # for testing
        json_data = r.json()
        windDirection = str(json_data["observations"]["data"][0]["wind_dir"])   # most recent measurement [0]
        windSpeed = float(json_data["observations"]["data"][0]["wind_spd_kt"])
        windGusts = float(json_data["observations"]["data"][0]["gust_kt"])
        localDateTime =  str(json_data["observations"]["data"][0]["local_date_time"])   # can use reading time
        title =  str(json_data["observations"]["header"][0]["name"])   # can use tile from name field
    except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
        windDirection = "NA"
        windSpeed = -1
        windGusts = -1
        # add lkalTime, title
# model (data format)

    templateData = {
        'title' : title,
        'time': localDateTime,
        'windSpeed' : windSpeed,
        'windDirection' : windDirection,
        'windGusts' : windGusts
        }
    return render_template('main.html', **templateData)     # view - (data display template)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=True)   # port 80 used already
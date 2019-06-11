import urllib.request
import time
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify
import os
import requests

app=Flask(__name__) #creates the app

@app.route("/", methods=['GET'])
def home():
    return 'hello'

@app.route("/track/<tracking_number>")
def get_tracking_info(tracking_number):
    url = "http://mk.brzapratka.com/public/tracking.php/?submit=true"
    response = requests.post(url, data={'bCode': tracking_number, 'Submit': 'Внеси'})
    soup = BeautifulSoup(response.text, "html.parser")

    events = []
    trs = soup.findAll('tr')
    for tr in trs:
        tds = tr.findAll('td')
        if tds == []:
            continue

        timestamp = tds[0].text
        title = tds[2].text
        description = tds[3].text

        event = {"timestamp":timestamp, "title":title, "description":description}
        events.append(event)

    events.reverse()


    print(events)
    return render_template('event.html', events=events)


# Start a development server if the file is executed directly
# name = main when program is run directly
# otherwise main = name of program being imported
# when running locally debug = true debugs and allows program to run
if __name__=="__main__":
    app.run(debug=True)

import urllib.request
import time
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify
import os
import requests

app=Flask(__name__) #creates the app

@app.route("/track/<tracking_number>")
def get_tracking_info(tracking_number):
    url = "http://mk.brzapratka.com/public/tracking.php/?submit=true"
    try:
        response = requests.post(url, data={'bCode': tracking_number, 'Submit': 'Внеси'}, timeout=5)
    except:
        error_msg = "Сервисот на Брза Пратка во моментов не функционира. Ве молиме обидете се повторно."
        return render_template('event.html', events=[], error_msg=error_msg)
    soup = BeautifulSoup(response.text, "html.parser")
    events = []
    trs = soup.findAll('tr')
    if trs == []:
        error_msg = "Невалиден број на товарителница."
        return render_template('event.html', events=[], error_msg=error_msg)
    for tr in trs:
        tds = tr.findAll('td')
        # ignores trs that dont contain tds
        # such as the table header
        if tds == []:
            continue

        timestamp = tds[0].text
        title = tds[2].text
        description = tds[3].text

        event = {"timestamp":timestamp, "title":title, "description":description}
        events.append(event)

    # brza pratka lists events in chronological order
    # but we want to show the last event first
    events.reverse()

    return render_template('event.html', events=events)


# Start a development server if the file is executed directly
# name = main when program is run directly
# otherwise main = name of program being imported
# when running locally debug = true debugs and allows program to run
if __name__=="__main__":
    app.run(debug=True)

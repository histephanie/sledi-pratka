import urllib.request
import time
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
import flask
import os
import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from validate_email import validate_email
from dotenv import load_dotenv

# Load secrets and configuration from the .env file
load_dotenv()

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

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    msg_sent = False

    if request.method == 'POST':
        email = flask.request.values.get('email')
        name = flask.request.values.get('name')
        message = flask.request.values.get('text')

        error_msgs = []
        if email == '':
            error_msgs.append("email is required")
        elif not validate_email(email):
            error_msgs.append("Invalid email")
        if name == '':
            error_msgs.append("Name is required")
        if message == '':
            error_msgs.append("Please enter a message")

        if len(error_msgs) > 0:
            return render_template("contact.html", error_msgs=error_msgs, name=name, email=email, message=message)


        message = Mail(
            from_email=email,
            to_emails='stephanie.bogantes@gmail.com',
            subject='New Message',
            html_content=message)
        try:
            sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
            response = sg.send(message)

        except Exception as e:
            print(e)

        msg_sent = True


    return render_template('contact.html', msg_sent=msg_sent)

@app.route("/privacy")
def privacy():
    return render_template('privacy.html')


# Start a development server if the file is executed directly
# name = main when program is run directly
# otherwise main = name of program being imported
# when running locally debug = true debugs and allows program to run
if __name__=="__main__":
    app.run(debug=True)

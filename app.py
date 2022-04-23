from flask import Flask, render_template
import requests
from datetime import date, datetime

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/<name>')
def temp(name):
    results = []
    timestamps = []
    url = 'https://api.thingspeak.com/channels/202842/feeds.json'
    r = requests.get(url)
    payloads = r.json()

    # print single field values
    title = payloads['channel'][f'field{name}']
    for i in range(len(payloads['feeds'])):
        mesure = payloads['feeds'][i][f'field{name}']
        labels = payloads['feeds'][i]['created_at']
        if mesure != None:
            results.append(mesure)
            labels = datetime.fromisoformat(labels[:-1])
            timestamps.append(labels.strftime('%d-%m %H:%M'))
            results.append(mesure)
    return render_template('result.html', results=results, timestamps=timestamps, title=title)


@ app.route("/AboutMe")
def GetAboutMe():
    return render_template('AboutMe.html', title="O Autorze", AboutMe_active="class=active")


if __name__ == '__main__':
    app.run()

from flask import Flask, render_template
import requests
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def index():
    results = []
    for i in range(1, 9):
        url = f'https://api.thingspeak.com/channels/202842/fields/{i}/last.json'
        r = requests.get(url)
        payloads = r.json()
        results.append(payloads[f'field{i}'])
    return render_template("index.html", first=results[0], second=results[1], third=results[2], fourth=results[3], fifth=results[4], sixth=results[5], seventh=results[6], eighth=results[7])


@app.route('/<name>')
def temp(name):
    results = []
    timestamps = []
    url = 'https://api.thingspeak.com/channels/202842/feeds.json'
    r = requests.get(url)
    payloads = r.json()

    # parse json data to get the values
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

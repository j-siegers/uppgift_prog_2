import urllib.request
import ssl
from flask import Flask, render_template, request
import json


app = Flask(__name__)


@app.route('/')
def index():
    """
    Kod för första sidan index.html

    """
    return render_template('index.html')


@app.route('/api', methods=['POST'])
def api_post():
    """
    Funktion som tar emot inmatad data från formuläret på indexsidan,
    skickar den till externt API och returnerar data.

    :return: Sidan result.html med priser för sökt dag
    """
    # Variabler som sparar inmatad data från formuläret på index.html
    year = request.form['year']
    month = request.form['month']
    day = request.form['day']
    price_class = request.form['pclass']
    # API:ets URL med valda datum infogade som f-sträng
    api_url = f'https://www.elprisetjustnu.se/api/v1/prices/{year}/{month}-{day}_{price_class}'
    context = ssl._create_unverified_context()
    json_data = urllib.request.urlopen(api_url, context=context).read()
    result_data = json.loads(json_data)
    return render_template('result.html')


@app.route('/result')
def result():
    """
    Funktion som hanterar utskrift av sökresultat från första
    sidans formulär
    """
    return render_template('result.html')


@app.errorhandler(405)
def method_not_allowed(error):
    """
    Felhanterare om användare försöker ansluta till /api direkt.
    """
    return render_template('index.html')

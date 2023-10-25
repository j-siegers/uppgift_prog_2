import urllib.request
import ssl
from flask import Flask, render_template, request
import json
import pandas as pd
import datetime

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
    Funktion som tar emot inmatad data från formuläret på indexsidan
    och skickar vidare URL:en till funktionen json_to_html.

    :return: Sidan result.html med priser för sökt dag
    """
    # Variabler som sparar inmatad data från formuläret på index.html
    year = request.form['year']
    month = request.form['month']
    day = request.form['day']
    price_class = request.form['pclass']

    # Dagens datum sparas för jämförelse.
    todays_date = datetime.datetime.now()

    # Felhantering av inmatade datum.
    # Datumet görs om till en integer (date) som sedan jämförs mot datumet 2022-11-01
    # i int format. Vid fel skrivs meddelande ut.

    try:  # Felhanterare om användaren inte fyller i alla fält.
        date = int(year + month + day)
    except ValueError:
        err_msg = 'Vänligen fyll i all fält!'
        return render_template('index.html', err_msg=err_msg)

    if date < 20221101:
        err_msg = 'Fel: välj ett datum från 2022-11-01 och framåt!'
        return render_template('index.html', err_msg=err_msg)

    # Om datumet är längre fram än 1 dag från dagens datum skrivs felmeddelande ut.
    elif date > 1 + int(todays_date.strftime("%Y%m%d")):
        err_msg = 'Fel: Du kan max se en dag framåt!'
        return render_template('index.html', err_msg=err_msg)

    # API:ets URL med valda datum infogade som f-sträng.
    api_url = f'https://www.elprisetjustnu.se/api/v1/prices/{year}/{month}-{day}_{price_class}.json'

    # URL:en skickas till json_to_html funktionen där den omvandlas till en HTML tabell.
    html_data = json_to_html(api_url)

    # HTML tabellen skickas till result.html där den skrivs ut.
    return render_template('result.html', html_data=html_data)


@app.route('/result')
def result():
    """
    Funktion som hanterar utskrift av sökresultat från första
    sidans formulär.
    """
    return render_template('result.html')


@app.errorhandler(404)
def error_not_found(error):
    """
    Felhanterare om användare försöker ansluta till en sida som inte existerar.
    :return: Felmeddelande
    """
    err_msg = 'Sidan du sökte finns inte'
    return render_template('index.html', err_msg=err_msg)


@app.errorhandler(405)
def method_not_allowed(error):
    """
    Felhanterare om användare försöker ansluta till /api direkt.
    :return: index.html
    """
    return render_template('index.html')


# Ytterligare funktioner utöver Flask.

def json_to_html(url):
    """
    Tar emot en URL och skickar sedan en förfrågan till API. Omvandlar svaret
    från JSON till en lista med dictionarys som formateras i Pandas.
    :return: HTML tabell
    """
    context = ssl._create_unverified_context()

    # Felhantering om API returnerar felaktig data eller inte svarar.
    try:
        # Data hämtas från URL:en.
        json_data = urllib.request.urlopen(url, context=context).read()
        # Gör om från JSON format till en lista med dictionarys.
        result_data = json.loads(json_data)

        # Loop för att ändra time_start i varje dictionary till bara timmar och minuter.
        # Strängen delas vid bokstaven T och timmar och minuter sparas i ny
        # variabel som sedan uppdaterar ursprungliga time_start.
        for row in result_data:
            time_start = row["time_start"].split("T")[1][:5]
            row["time_start"] = time_start

        # En Pandas DataFrame skapas med innehållet från result_data.
        df = pd.DataFrame(result_data)

        # Namnen på kolumnerna byts ut så det ser snyggare ut.
        new_column_names = {'SEK_per_kWh': 'SEK / kWh', 'time_start': 'Tid'}
        df = df.rename(columns=new_column_names)

        # Utvalda kolumner väljs ut för att skickas till tabellen.
        columns = ['Tid', 'SEK / kWh']
        # DataFrame omvandlas till en HTML tabell
        table_data = df.to_html(columns=columns, classes="table p-5", justify="left")

    # Vid fel returneras ett felmeddelande och index laddas.
    except Exception as error:
        err_msg = f'{error} (sidan du sökte finns inte)'
        return render_template('index.html', err_msg=err_msg)

    return table_data

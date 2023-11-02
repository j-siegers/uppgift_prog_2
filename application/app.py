from flask import Flask, render_template, request
from datetime import datetime, timedelta
from application import func


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
    och skickar vidare URL:en till funktionerna json_to_dataframe
    och dataframe_to_plotly.

    :return: result.html med priser för sökt dag i tabellformat och Plotly diagram.
    """
    # Variabler som sparar inmatad data från formuläret på index.html
    year = request.form['year']
    month = request.form['month']
    day = request.form['day']
    price_class = request.form['pclass']

    # Dagens datum + 1 dag sparas för jämförelse.
    todays_date_plus1 = datetime.now() + timedelta(days=1)

    # Inmatad data sparas i int-format för att jämföras med minsta möjliga datum
    try:
        date = int(year + month + day)
    except ValueError:
        date = 0

    if date < 20221101:
        err_msg = 'Fel: välj ett datum från 2022-11-01 och framåt!'
        return render_template('index.html', err_msg=err_msg)

    # Om datumet är längre fram än 1 dag från dagens datum skrivs felmeddelande ut.
    elif date > int(todays_date_plus1.strftime("%Y%m%d")):
        err_msg = 'Fel: Du kan max se en dag framåt!'
        return render_template('index.html', err_msg=err_msg)

    # API:ets URL med valda datum infogade som f-sträng.
    api_url = f'https://www.elprisetjustnu.se/api/v1/prices/{year}/{month}-{day}_{price_class}.json'
    try:
        # URL:en skickas till json_to_dataframe där den omvandlas till en Pandas DF
        dataframe = func.json_to_dataframe(api_url)
        # Utvalda kolumner väljs ut för att skickas till tabellen.
        columns = ['Tid', 'SEK / kWh']
        # DataFrame omvandlas till en HTML tabell
        html_data = dataframe.to_html(columns=columns, index=False, classes="table p-5 table-striped", justify="left")
        # Dataframe skickas till en Plotly funktion
        bar_chart = func.dataframe_to_plotly(dataframe)

        # Tabellerna skickas till result.html där de skrivs ut med datum och prisklass.
        return render_template('result.html', html_data=html_data, bar_chart=bar_chart,
                               price_class=price_class, date=date)

    except Exception as e:
        # Felhanterare om användaren inte fyller i alla fält eller felaktigt datum.
        err_msg = f'Fel: {e}: Vänligen försök igen!'
        return render_template('index.html', err_msg=err_msg)


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
    err_msg = 'Error 405: Du har inte behörighet att ansluta till URL:en'
    return render_template('index.html', err_msg=err_msg)

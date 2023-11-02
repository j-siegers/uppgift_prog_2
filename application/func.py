import urllib.request
import ssl
import json
import pandas as pd
import plotly.express as px
import plotly.offline as pyo


# Ytterligare funktioner utöver Flask.
def json_to_dataframe(url):
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
        return df

        # Vid fel returneras ett felmeddelande.
    except Exception as error:
        return error


def dataframe_to_plotly(dataframe):
    """
    Tar emot en Pandas dataframe och skapar ett Plotly diagram
    :return: Plotly diagram i HTML
    """
    fig = px.line(data_frame=dataframe, x='Tid', y='SEK / kWh')
    return pyo.plot(fig, output_type='div')

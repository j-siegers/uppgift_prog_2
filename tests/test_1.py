import urllib.request
import ssl
import sys
import os
import pandas as pd
import plotly as px

# Används för att korrekt kunna importera application/app i PyCharm
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from application import func

'''
# Testcases
1. Testa att servern är igång (index)
2. Testa att alla endpoints finns (/api och /result)
3. Testa att API är nåbar och ger ett svar
4. Testa att json_to_dataframe funktionen returnerar förväntad data
5. Testa att servern ger meddelande vid felaktig sida(404)
6. 

'''

context = ssl._create_unverified_context()


def test_server_running_index():
    """
    Testar att servern är igång och ger ett svar tillbaka från index
    """
    assert urllib.request.urlopen("http://127.0.0.1:5000", context=context, timeout=10)


def test_server_running_api():
    """
    Testar att servern ger ett svar tillbaka från /api
    """
    assert urllib.request.urlopen("http://127.0.0.1:5000/api", context=context, timeout=10)


def test_server_running_result():
    """
    Testar att servern ger ett svar tillbaka från result
    """
    assert urllib.request.urlopen("http://127.0.0.1:5000/result", context=context, timeout=10)


def test_api_response():
    """
       Testar att API:et är online och ger ett svar tillbaka
    """
    assert urllib.request.urlopen("https://www.elprisetjustnu.se/api/v1/prices/2023/10-24_SE3.json",
                                  context=context, timeout=10)


def test_json_to_dataframe():
    """
    Testar funktionen json_to_dataframe att den tar emot en url, öppnar den och skapar en Pandas dataframe.
    """
    url = "https://www.elprisetjustnu.se/api/v1/prices/2023/10-24_SE3.json"
    response = func.json_to_dataframe(url)
    assert isinstance(response, pd.DataFrame)


def test_page_not_found():
    """
    Kontrollerar att servern skriver ut ett felmeddelande när en sida inte finns.
    """
    with urllib.request.urlopen("http://127.0.0.1:5000/info", context=context, timeout=10) as response:
        html = str(response.read())
    assert "finns inte" in html


def test_dataframe_to_plotly():
    """
    Kontrollerar att funktionen returnerar en Plotly chart
    """
    url = "https://www.elprisetjustnu.se/api/v1/prices/2023/10-24_SE3.json"
    response = func.json_to_dataframe(url)
    plotly_df = func.dataframe_to_plotly(response)
    assert 'plotly' in plotly_df

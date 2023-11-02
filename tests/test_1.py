import urllib.request
import ssl
import pandas as pd
from application import func


'''
# Testcases
1. Testa att servern är igång (index)
2. Testa att endpoint /api ger felmeddelande vid anslut (405)
3. Testa att API är nåbar och ger ett svar
4. Testa att json_to_dataframe funktionen returnerar förväntad data
5. Testa att servern ger meddelande vid felaktig sida(404)
6. Testar att plotly funktionen skickar ett plotly diagram
7. Testar att json_to_dataframe funktionen ger felmedddelande vid felaktigt datum
8. Testar att det finns ett sökformulär på index-sidan
'''

context = ssl._create_unverified_context()


def test_server_running_index():
    """
    Testar att servern är igång och ger ett svar tillbaka från index
    """
    assert urllib.request.urlopen("http://127.0.0.1:5000", context=context, timeout=10)


def test_server_error_api():
    """
    Testar att servern ger ett felmeddelande från /api
    """
    with urllib.request.urlopen("http://127.0.0.1:5000/api", context=context, timeout=10) as response:
        html = str(response.read())
    assert "Error 405" in html


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
    Kontrollerar att funktionen returnerar en Plotly chart i HTML format
    """
    url = "https://www.elprisetjustnu.se/api/v1/prices/2023/10-24_SE3.json"
    response = func.json_to_dataframe(url)
    plotly_html = func.dataframe_to_plotly(response)
    assert isinstance(plotly_html, str)
    assert 'Plotly' in plotly_html


def test_json_to_dataframe_error():
    """
    Testar funktionen json_to_dataframe att den tar emot en url, försöker öppna den och ger ett felmeddelande
    vid felaktigt datum bakåt i tiden.
    """
    url = "https://www.elprisetjustnu.se/api/v1/prices/2022/01-01_SE3.json"
    response = func.json_to_dataframe(url)
    assert isinstance(response, Exception)


def test_index_form_field():
    """
    Testar att det finns ett sökformulär på index-sidan.
    """
    with urllib.request.urlopen("http://127.0.0.1:5000", context=context, timeout=10) as response:
        html = str(response.read())
    assert "</form>" in html

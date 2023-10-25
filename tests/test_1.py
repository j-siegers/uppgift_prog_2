import urllib.request
import ssl
import sys
import os

# Används för att korrekt kunna importera application/app i PyCharm
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from application import app


'''
# Testcases
1. Testa att servern är igång (index)
2. Testa att alla endpoints finns (/api och /result)
3. Testa att API är nåbar och ger ett svar
4. Testa att json_to_html funktion returnerar förväntad data
5. Testa att servern ger meddelande vid felaktig sida(404)
6. Testa att server ger felmeddelande vid felaktigt datum 

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


def test_json_to_html():
    """
    Testar funktionen json_to_url att den tar emot en url, öppnar den och skapar en Pandas dataframe.
    :return: En HTML tabell
    """
    url = "https://www.elprisetjustnu.se/api/v1/prices/2023/10-24_SE3.json"
    response = app.json_to_html(url)
    assert "</table>" in response


def test_page_not_found():
    """
    Kontrollerar att servern skriver ut ett felmeddelande när en sida inte finns.
    """
    with urllib.request.urlopen("http://127.0.0.1:5000/info", context=context, timeout=10) as response:
        html = str(response.read())
    assert "finns inte" in html

# todo:
'''
def test_date_error():
    """
    Testar att funktionen json_to_url ger ett felmeddelande om datumet är felaktigt.
    """
    url = "https://www.elprisetjustnu.se/api/v1/prices/2023/10-27_SE3.json"
    with app.app_context():
        response = app.json_to_html(url)
    assert RuntimeError in response
'''
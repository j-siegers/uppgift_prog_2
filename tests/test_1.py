import pytest
import urllib.request
import ssl

'''
# Testcases
1. Testa att servern är igång
2. Testa att alla endpoints finns
3. Testa API är nåbar och ger ett svar
4. Testa att formuläret returnerar förväntad data från result
5. Testa att servern ger meddelande vid felaktig sida
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
       Testar att API:et ger ett svar tillbaka
    """
    assert urllib.request.urlopen("https://www.elprisetjustnu.se/api/v1/prices/2023/10-24_SE3.json",
                                  context=context, timeout=10)


import requests
from bs4 import BeautifulSoup

def get_fear_and_greed():
    url = "https://edition.cnn.com/markets/fear-and-greed"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    try:
        value = soup.find("div", class_="FearGreedIndex__Dial-value").text.strip()
        label = soup.find("div", class_="FearGreedIndex__Dial-status").text.strip()
        return int(value), label
    except:
        return None, "Errore parsing"

# Esempio d'uso
index, label = get_fear_and_greed()
print(f"Fear & Greed Index: {index} ({label})")

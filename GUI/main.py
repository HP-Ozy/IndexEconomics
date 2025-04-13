import streamlit as st
import yfinance as yf
import time
import requests
from bs4 import BeautifulSoup

# Mappatura nomi -> ticker Yahoo Finance
index_map = {
    "S&P 500": "^GSPC",
    "NASDAQ 100": "^NDX",
    "Dow Jones": "^DJI",
    "DAX (Germania)": "^GDAXI",
    "FTSE 100 (UK)": "^FTSE",
    "Nikkei 225 (Giappone)": "^N225",
    "VIX (Volatilità)": "^VIX",
    "Gold (Oro)": "GC=F",
    "Brent Oil (Petrolio)": "BZ=F"
}

# Funzione per ottenere il Fear & Greed Index (CNN)
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
        return None, "Errore nel parsing"

# UI Streamlit
st.title("📈 Dashboard Indici Finanziari - Realtime Yahoo Finance")
st.markdown("Seleziona gli indici da monitorare:")

# Selezione indici
selected_indices = st.multiselect(
    "Scegli gli indici:",
    list(index_map.keys()),
    default=["S&P 500", "NASDAQ 100"]
)

# Checkbox per attivare Fear & Greed Index
show_fg_index = st.checkbox("Mostra Fear & Greed Index (CNN)")

# Slider per aggiornamento
refresh_interval = st.slider("Aggiorna ogni (secondi):", 5, 60, 10)

# Placeholder per l'output
placeholder = st.empty()

# Funzione per ottenere il prezzo attuale
def get_yahoo_price(ticker):
    try:
        data = yf.Ticker(ticker).history(period="1d", interval="1m")
        if not data.empty:
            return round(data['Close'].iloc[-1], 2)
        else:
            return "N/D"
    except:
        return "Errore"

# Avvia live update
if selected_indices or show_fg_index:
    while True:
        with placeholder.container():
            st.subheader("💹 Valori attuali (Yahoo Finance)")
            for name in selected_indices:
                ticker = index_map[name]
                price = get_yahoo_price(ticker)
                st.write(f"**{name}** ({ticker}): {price}")

            if show_fg_index:
                st.subheader("😨 Fear & Greed Index (CNN)")
                fg_value, fg_label = get_fear_and_greed()
                st.write(f"**Valore:** {fg_value}")
                st.write(f"**Sentiment:** {fg_label}")

            st.markdown(f"_Ultimo aggiornamento: {time.strftime('%H:%M:%S')}_")

        time.sleep(refresh_interval)
else:
    st.warning("Seleziona almeno un indice o attiva il Fear & Greed Index per iniziare.")

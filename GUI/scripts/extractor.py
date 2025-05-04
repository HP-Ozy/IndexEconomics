import requests
from bs4 import BeautifulSoup
import streamlit as st
import yfinance as yf
import time
import pandas as pd


# 🔽 FUNZIONE: Fear & Greed Index da API CNN
def get_fear_and_greed():
    try:
        url = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            st.error(f"❌ Status code: {response.status_code}")
            st.write("⚠️ Contenuto risposta:", response.text)
            return None, "Errore nella risposta HTTP"

        data = response.json()
        latest = data["fear_and_greed"]["now"]
        label = data["fear_and_greed"]["classification"]["now"]
        return int(latest), label

    except Exception as e:
        st.error(f"❌ Errore: {e}")
        return None, "Errore nel parsing"

# 🔽 FUNZIONE: Ottieni valore VIX
def get_vix_value():
    try:
        vix = yf.Ticker("^VIX")
        data = vix.history(period="1d", interval="1m")
        if data.empty:
            return None
        last_value = data["Close"].iloc[-1]
        return round(float(last_value), 2)
    except Exception as e:
        st.error(f"❌ Errore nel recupero VIX: {e}")
        return None
    
def get_yahoo_price(ticker):
    try:
        data = yf.Ticker(ticker).history(period="1d", interval="1m")
        if not data.empty:
            return round(data['Close'].iloc[-1], 2)
        else:
            return "N/D"
    except:
        return "Errore"

def get_historical_data(ticker):
    try:
        data = yf.Ticker(ticker).history(period="1y", interval="1d")
        return data
    except:
        return pd.DataFrame()
    
import re

def get_cost_of_living_index(country_name, api_key=None):
    """
    Tenta di ottenere il costo della vita da Numbeo.
    Se non disponibile o fallisce, usa WorldData.info.
    """
    if api_key:
        url = f"https://www.numbeo.com/api/country_prices?api_key={api_key}&country={country_name}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            index = data.get('cost_of_living_index')
            if index:
                return index

    # --- FALLBACK: WorldData.info ---
    try:
        country_url_name = country_name.lower().replace(" ", "-")
        url = f"https://www.worlddata.info/{country_url_name}.php"
        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            if "Cost of Living Index" in html:
                idx = html.find("Cost of Living Index")
                snippet = html[idx:idx+300]
                match = re.search(r"(\d{1,3}\.?\d*)", snippet)
                if match:
                    return float(match.group(1))
    except:
        pass

    return None

def get_world_bank_data(country_code, indicator):
    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}?format=json&per_page=1&date=2023"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data and len(data) > 1 and data[1]:
            return data[1][0]['value']
    return None
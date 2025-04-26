import requests
from bs4 import BeautifulSoup
import streamlit as st
import yfinance as yf
import time
import json
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
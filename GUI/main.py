import streamlit as st
import yfinance as yf
import time
import requests
import json
from scripts.extractor import get_vix_value  # Assumendo che funzioni correttamente

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

# UI Streamlit
st.title("📈 Dashboard Indici Finanziari - Realtime Yahoo Finance")
st.markdown("Seleziona gli indici da monitorare:")

# Selezione indici
selected_indices = st.multiselect(
    "Scegli gli indici:",
    list(index_map.keys()),
    default=["S&P 500", "NASDAQ 100"]
)

# Checkbox per mostrare VIX
show_fg_index = st.checkbox("Mostra VIX (Indice di volatilità CBOE)")

# Slider per aggiornamento
refresh_interval = st.slider("Aggiorna ogni (secondi):", 5, 60, 10)

# Placeholder dinamico
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

# Avvio del loop di aggiornamento
if selected_indices or show_fg_index:
    while True:
        with placeholder.container():
            st.subheader("💹 Valori attuali (Yahoo Finance)")
            for name in selected_indices:
                ticker = index_map[name]
                price = get_yahoo_price(ticker)
                st.write(f"**{name}** ({ticker}): {price}")

            # Mostra VIX solo se selezionato
            if show_fg_index:
                st.subheader("💥 Volatilità VIX (CBOE)")
                vix_value = get_vix_value()
                if vix_value is not None:
                    st.write(f"**Valore VIX:** {vix_value}")
                    if vix_value > 30:
                        st.error("🚨 Alta volatilità!")
                    elif vix_value > 20:
                        st.warning("⚠️ Volatilità moderata")
                    else:
                        st.success("✅ Volatilità bassa")
                else:
                    st.warning("⚠️ VIX non disponibile")

            st.markdown(f"_Ultimo aggiornamento: {time.strftime('%H:%M:%S')}_")

        time.sleep(refresh_interval)
else:
    st.warning("Seleziona almeno un indice o attiva il VIX per iniziare.")

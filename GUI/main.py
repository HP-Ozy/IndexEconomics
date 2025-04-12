import streamlit as st
import yfinance as yf
import time

# Mappatura nomi -> ticker Yahoo Finance
index_map = {
    "S&P 500": "^GSPC",
    "NASDAQ 100": "^NDX",
    "VIX": "^VIX",
    "Gold": "GC=F",       # Futures sull'oro
    "Brent Oil": "BZ=F"   # Futures sul Brent
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
if selected_indices:
    while True:
        with placeholder.container():
            st.subheader("💹 Valori attuali (Yahoo Finance)")
            for name in selected_indices:
                ticker = index_map[name]
                price = get_yahoo_price(ticker)
                st.write(f"**{name}** ({ticker}): {price}")
            st.markdown(f"_Ultimo aggiornamento: {time.strftime('%H:%M:%S')}_")
        time.sleep(refresh_interval)
else:
    st.warning("Seleziona almeno un indice per iniziare.")

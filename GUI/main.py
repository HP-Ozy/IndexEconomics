import streamlit as st
import yfinance as yf
import time
import pandas as pd
import plotly.express as px
from scripts.extractor import get_vix_value  # Importa il tuo get_vix_value personalizzato
from scripts.extractor import get_historical_data
from scripts.extractor import get_yahoo_price


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

# --- UI Streamlit ---
st.title("📈 Dashboard Indici Finanziari - Realtime + Storico")

st.markdown("Seleziona gli indici da monitorare:")

# Selezione indici
selected_indices = st.multiselect(
    "Scegli gli indici:",
    list(index_map.keys()),
    default=["Gold (Oro)"]
)

# Checkbox per mostrare VIX
show_fg_index = st.checkbox("Mostra VIX (Indice di volatilità CBOE)")

# Slider per aggiornamento
refresh_interval = st.slider("Aggiorna ogni (secondi):", 5, 60, 10)

# --- Placeholder dinamico per aggiornamento ---
placeholder = st.empty()

# --- Visualizza dati ---

# Grafico storico
if selected_indices:
    st.subheader(" Storico ultimi 12 mesi")
    for name in selected_indices:
        ticker = index_map[name]
        hist_data = get_historical_data(ticker)
        if not hist_data.empty:
            fig = px.line(hist_data, x=hist_data.index, y="Close", title=f"Andamento di {name}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"Dati storici non disponibili per {name}.")

# --- INTEGRAZIONE: Analisi Economica Mondiale ---
st.title("🌍 Analisi Economica per Nazione")

# Flag per attivare l'analisi economica mondiale
show_economic_analysis = st.checkbox("Mostra Analisi Economica Mondiale")

if show_economic_analysis:
    st.markdown("Seleziona i paesi di cui vuoi analizzare Debito/PIL, PIL e Costo della Vita:")

    countries = ["United States", "Germany", "France", "Italy", "Japan", "China", "India", "Brazil", "South Africa"]

    selected_countries = st.multiselect("Scegli i Paesi:", countries, default=["United States", "Germany", "Italy"])

    if selected_countries:
        # Dati simulati di esempio (puoi collegare vere API in futuro)
        economic_data = {
            "United States": {"Debt_GDP": 123.0, "GDP": 25000000, "Cost_of_Living_Index": 70},
            "Germany": {"Debt_GDP": 65.0, "GDP": 4500000, "Cost_of_Living_Index": 60},
            "France": {"Debt_GDP": 111.0, "GDP": 3100000, "Cost_of_Living_Index": 65},
            "Italy": {"Debt_GDP": 134.0, "GDP": 2100000, "Cost_of_Living_Index": 58},
            "Japan": {"Debt_GDP": 250.0, "GDP": 5000000, "Cost_of_Living_Index": 68},
            "China": {"Debt_GDP": 77.0, "GDP": 18000000, "Cost_of_Living_Index": 45},
            "India": {"Debt_GDP": 85.0, "GDP": 3500000, "Cost_of_Living_Index": 32},
            "Brazil": {"Debt_GDP": 91.0, "GDP": 2100000, "Cost_of_Living_Index": 40},
            "South Africa": {"Debt_GDP": 70.0, "GDP": 400000, "Cost_of_Living_Index": 38},
        }

        # Crea il DataFrame
        df = pd.DataFrame(
            {country: economic_data[country] for country in selected_countries}
        ).T
        df.index.name = "Country"

        # --- FIX: reset index per avere 'Country' come colonna ---
        df = df.reset_index()

        # Mostra la tabella
        st.dataframe(df)

        # Grafico Debito/PIL
        fig_debt = px.bar(
            df,
            x="Country",
            y="Debt_GDP",
            title="Debito Pubblico (% del PIL)",
            labels={"Debt_GDP": "Debito % PIL"},
        )
        st.plotly_chart(fig_debt, use_container_width=True)

        # Grafico Costo della Vita
        fig_col = px.bar(
            df,
            x="Country",
            y="Cost_of_Living_Index",
            title="Indice del Costo della Vita",
            labels={"Cost_of_Living_Index": "Indice Costo Vita"},
            color="Cost_of_Living_Index",
        )
        st.plotly_chart(fig_col, use_container_width=True)

        # Grafico PIL
        fig_gdp = px.bar(
            df,
            x="Country",
            y="GDP",
            title="Prodotto Interno Lordo (PIL) in Milioni di $",
            labels={"GDP": "PIL ($M)"},
        )
        st.plotly_chart(fig_gdp, use_container_width=True)

        # --- NUOVA PARTE: Mappa geografica ---
        st.subheader("🌎 Visualizzazione sulla Mappa del Mondo")

        # Codici ISO Alpha-3
        iso_codes = {
            "United States": "USA",
            "Germany": "DEU",
            "France": "FRA",
            "Italy": "ITA",
            "Japan": "JPN",
            "China": "CHN",
            "India": "IND",
            "Brazil": "BRA",
            "South Africa": "ZAF"
        }

        # Aggiungi la colonna ISO
        df['ISO_Code'] = df['Country'].map(iso_codes)

        # Scelta del parametro da visualizzare
        parameter_to_map = st.selectbox(
            "Scegli il parametro da visualizzare sulla mappa:",
            options=["GDP", "Debt_GDP", "Cost_of_Living_Index"],
            index=0
        )

        # Mappa Plotly
        fig_map = px.choropleth(
            df,
            locations="ISO_Code",
            color=parameter_to_map,
            hover_name="Country",
            color_continuous_scale="Viridis",
            projection="natural earth",
            title=f"Mappa Mondiale basata su {parameter_to_map.replace('_', ' ')}"
        )

        st.plotly_chart(fig_map, use_container_width=True)

    else:
        st.warning("Seleziona almeno un paese per visualizzare i dati.")


if selected_indices or show_fg_index:
    while True:
        with placeholder.container():
            st.subheader(" Valori attuali (Yahoo Finance)")
            for name in selected_indices:
                ticker = index_map[name]
                price = get_yahoo_price(ticker)
                st.write(f"**{name}** ({ticker}): {price}")

            if show_fg_index:
                st.subheader(" Volatilità VIX (CBOE)")
                vix_value = get_vix_value()
                if vix_value is not None:
                    st.write(f"**Valore VIX:** {vix_value}")
                    if vix_value > 30:
                        st.error(" Alta volatilità!")
                    elif vix_value > 20:
                        st.warning(" Volatilità moderata")
                    else:
                        st.success(" Volatilità bassa")
                else:
                    st.warning(" VIX non disponibile")

            st.markdown(f"_Ultimo aggiornamento: {time.strftime('%H:%M:%S')}_")

        time.sleep(refresh_interval)
else:
    st.warning("Seleziona almeno un indice o attiva il VIX per iniziare.")



import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import datetime
from itertools import combinations

st.set_page_config(layout="wide")

# Logo
col100, col101, col102, col103, col104, col105, col106 = st.columns(7)
with col103:
    st.image("images/NITIVAN_Logo.png", width=150)

col107, col108, col109 = st.columns([1, 2, 1])
with col108:
    st.markdown(
        "<div style='text-align: center; font-size: 20px;'>Scopri i dati su <b>carburante</b> e <b>distributori</b><br>per poter prendere decisioni più consapevoli per <b>NITIVAN</b><br> <br></div>",
        unsafe_allow_html=True
    )

# Titolo e descrizione
st.markdown(
    "<div style='text-align: center; font-size: 40px; font-weight: bold;'>Qual è il Brand di carburante più conveniente per noi?</div>",
    unsafe_allow_html=True
)

#spazio a capo
st.markdown(
    "<div style='text-align: center; font-size: 10px;'><br><br></div>",
    unsafe_allow_html=True
)
##################### CREO ELENCHI A TENDINA ######################
# Lettura dei file CSV
caselli_partenza_df = pd.read_csv("dim_caselli/dim_caselli_partenza.csv")
caselli_arrivo_df = pd.read_csv("dim_caselli/dim_caselli_arrivo.csv")
carburante_df = pd.read_csv("dim_carburante/dim_carburante.csv")
consumo_medio_df = pd.read_csv("dim_carburante/consumo_medio.csv")

# Estrazione dei valori unici
caselli_partenza = caselli_partenza_df["nodo_name"].dropna().unique()
caselli_arrivo = caselli_arrivo_df["nodo_name"].dropna().unique()
tipi_carburante = carburante_df["carburante"].dropna().unique()

# Valori di default per partenza e arrivo
default_partenza = "MILANO EST"
default_arrivo = "NAPOLI EST"
# Trova l'indice dei valori di default
index_partenza = list(caselli_partenza).index(default_partenza) if default_partenza in caselli_partenza else 0
index_arrivo = list(caselli_arrivo).index(default_arrivo) if default_arrivo in caselli_arrivo else 0

# Prima riga di selectbox
col1, col2, col3 = st.columns(3)
with col1:
    partenza = st.selectbox("Seleziona il punto di partenza", caselli_partenza, index=index_partenza)
with col2:
    arrivo = st.selectbox("Seleziona il punto di arrivo", caselli_arrivo, index=index_arrivo)
with col3:   # Intervallo di date
    start_date_2025 = datetime.date(2025, 1, 1)
    end_date_2025 = datetime.date(2025, 12, 31)
    date_range = st.date_input(
        "Seleziona l'intervallo di date",
        value=(start_date_2025, end_date_2025),
        min_value=start_date_2025,
        max_value=end_date_2025
    )

# Seconda riga di selectbox
col4, col5, col6 = st.columns(3)
with col4:
    carburante = st.selectbox("Seleziona il tipo di carburante", tipi_carburante)

# Filtra le cilindrate in base al carburante selezionato
cilindrate_filtrate = consumo_medio_df[consumo_medio_df["tipo_carburante"] == carburante]["cilindrata(cc)"].dropna().unique()
with col5:
    cilindrata = st.selectbox("Seleziona la cilindrata (cc)", cilindrate_filtrate)
with col6:   # Campo di input manuale per la capacità del serbatoio (in litri)
    capacita_serbatoio = st.number_input(
        "Inserisci la capacità del serbatoio (l)",
        min_value=10,
        max_value=100,
        value=50, # valore visualizzato di default
        step=1
    )


# Recupero il consumo medio per la cilindrata selezionata e il carburante selezionato
# Filtra il DataFrame in base alla selezione
filtro = (
    (consumo_medio_df["cilindrata(cc)"] == cilindrata) &
    (consumo_medio_df["tipo_carburante"] == carburante)
)
#spazio a capo
st.markdown(
    "<div style='text-align: center; font-size: 10px;'><br><br></div>",
    unsafe_allow_html=True
)

col7, col8, col9 = st.columns(3)
with col7:
# Estrai il valore km/l
    if not consumo_medio_df[filtro].empty:
        consumo_medio_km_l = consumo_medio_df.loc[filtro, "km/l"].values[0]
        st.markdown(
            f"<div style='text-align: center; font-size: 16px;'><br>Secondo il tipo di carburante e la cilindrata (cc) selezionati, <br>il consumo medio è di <b>{consumo_medio_km_l} km/l</b></div>",
            unsafe_allow_html=True
        )
    else:
        st.warning("Nessun dato disponibile per il consumo medio per la combinazione selezionata.")
        consumo_medio_km_l = None

################### NETWORKX ###################
df = pd.read_csv('dim_input_networkx/dim_input_networkx.csv')
G = nx.DiGraph()
for _, row in df.iterrows():
    G.add_edge(row['nodo_id_1'], row['nodo_id_2'], weight=row['distanza'])

# --- Mappe ID -> nome (direzionali) ---
map_src = (
    df[['nodo_id_1', 'nodo_name_1']]
    .dropna()
    .astype({'nodo_id_1': 'string'})
    .drop_duplicates(subset=['nodo_id_1'])
    .set_index('nodo_id_1')['nodo_name_1']
    .to_dict()
)
map_dst = (
    df[['nodo_id_2', 'nodo_name_2']]
    .dropna()
    .astype({'nodo_id_2': 'string'})
    .drop_duplicates(subset=['nodo_id_2'])
    .set_index('nodo_id_2')['nodo_name_2']
    .to_dict()
)
# Fallback "any"
map_any = {**map_src, **map_dst}

partenza_networkx = caselli_partenza_df.loc[
    caselli_partenza_df["nodo_name"] == partenza, "nodo_id"
].values[0]
arrivo_networkx = caselli_arrivo_df.loc[
    caselli_arrivo_df["nodo_name"] == arrivo, "nodo_id"
].values[0]

try:
    percorso = nx.shortest_path(G, source=partenza_networkx, target=arrivo_networkx, weight='weight')
    distanza_totale = nx.shortest_path_length(G, source=partenza_networkx, target=arrivo_networkx, weight='weight')
    # --- Traduzione ID -> NOME con orientamento: primo da map_src, poi map_dst ---
    percorso_nomi = []
    if percorso:
        first = percorso[0]
        nome_first = map_src.get(first) or map_any.get(first, str(first))
        percorso_nomi.append(nome_first)
        for v in percorso[1:]:
            nome_v = map_dst.get(v) or map_any.get(v, str(v))
            percorso_nomi.append(nome_v)

        # Trasformazione in maiuscolo
        percorso_nomi = [nome.upper() for nome in percorso_nomi]
    if st.toggle("Mostra dettagli del percorso più breve"):
        st.write("Percorso più breve: " + " → ".join((percorso_nomi)))
    with col8:
        st.markdown(
            f"<div style='text-align: center; font-size: 16px;'><br>Distanza totale del percorso più breve: <b>{round(distanza_totale,2)} km</b></div>",
            unsafe_allow_html=True
        )
except nx.NetworkXNoPath:
    st.write("Non esiste un percorso tra i nodi indicati.")
    percorso = []

#################### PREZZI CARBURANTE ####################
prezzi_df = pd.read_csv("fact_prezzi_autostrade/fact_prezzi_completo.csv")
prezzi_df["data_update"] = pd.to_datetime(prezzi_df["data_update"], format="%d/%m/%Y")
prezzi_df["distributore_id"] = prezzi_df["distributore_id"].astype(str)

if date_range and len(date_range) == 2:
    prezzi_filtrati = prezzi_df[
        (prezzi_df["data_update"] >= pd.to_datetime(date_range[0])) &
        (prezzi_df["data_update"] <= pd.to_datetime(date_range[1])) &
        (prezzi_df["tipo_carburante"] == carburante)
    ]
else:
    st.warning("Per favore, seleziona **sia la data di inizio che quella di fine** per continuare.")
    st.stop()  
    prezzi_filtrati = pd.DataFrame()

#################### UNISCI INFO PER I NODI ####################
info_nodi_df = pd.read_csv("dim_nodi/dim_nodi.csv")
distributori_df = pd.read_csv("dim_distributori/dim_distributori.csv")
distributori_df["dtx"] = distributori_df["dtx"].astype(str)

info_percorso_df = info_nodi_df[info_nodi_df["nodo_id"].isin(percorso)]
info_percorso_df["ordine"] = info_percorso_df["nodo_id"].apply(lambda x: percorso.index(x))
info_percorso_df = info_percorso_df.sort_values("ordine")

nodo_partenza = info_percorso_df.iloc[0:1]
nodo_uscita = info_percorso_df.iloc[-1:]
nodi_intermedi = info_percorso_df.iloc[1:-1]
nodi_distributori = nodi_intermedi[nodi_intermedi["tipo_nodo"] == "DISTRIBUTORE"]

nodi_distributori = nodi_distributori.merge(
    distributori_df[["dtx", "Brand"]],
    left_on="nodo_id",
    right_on="dtx",
    how="left"
)

distributori_con_prezzi = prezzi_filtrati["distributore_id"].unique()
nodi_distributori = nodi_distributori[nodi_distributori["nodo_id"].isin(distributori_con_prezzi)]

info_filtrata_df = pd.concat([nodo_partenza, nodi_distributori, nodo_uscita])
############# PREZZI MEDI #############
# Calcola il prezzo medio per ciascun distributore
media_prezzi_df = prezzi_filtrati.groupby("distributore_id")["prezzo"].mean().reset_index().round(3)
media_prezzi_df.rename(columns={"prezzo": "prezzo_medio"}, inplace=True)

# Unisci la media dei prezzi con la tabella dei nodi distributori
info_filtrata_df = info_filtrata_df.merge(
    media_prezzi_df,
    left_on="nodo_id",
    right_on="distributore_id",
    how="left"
)

# Rimuovi la colonna di join se non ti serve
info_filtrata_df.drop(columns=["distributore_id"], inplace=True)

# Calcola il prezzo medio totale per i distributori nel percorso
prezzo_medio_totale = info_filtrata_df["prezzo_medio"].mean()

### Frase con prezzo medio di quella tartta di quel carburante
with col9:
    if pd.notnull(prezzo_medio_totale):
        frase_prezzo_medio = (
            f"Il prezzo medio del carburante <b>{carburante}</b><br>nei distributori presenti lungo il percorso selezionato<br>"
            f"nel periodo "
            f"<b>({date_range[0].strftime('%d/%m/%Y')} → {date_range[1].strftime('%d/%m/%Y')})</b><br>"
            f"è di <b>{prezzo_medio_totale:.3f} € al litro</b>."
        )
        st.markdown(
            f"<div style='text-align: center; font-size: 16px;'>{frase_prezzo_medio}</div>",
            unsafe_allow_html=True
        )
    else:
        st.warning("Nessun prezzo disponibile per il carburante selezionato nei distributori del percorso.")


############### AGGIUNGI DISTANZE ################
nodi_segmentati = info_filtrata_df["nodo_id"].tolist()
distanze_cumulative = [0]
for i in range(1, len(nodi_segmentati)):
    try:
        distanza = nx.shortest_path_length(G, source=nodi_segmentati[0], target=nodi_segmentati[i], weight='weight')
    except nx.NetworkXNoPath:
        distanza = None
    distanze_cumulative.append(distanza)

info_filtrata_df = info_filtrata_df.reset_index(drop=True)
info_filtrata_df["Km dall'Entrata"] = distanze_cumulative

distanze_segmentali = [0]
for i in range(1, len(nodi_segmentati)):
    try:
        distanza = nx.shortest_path_length(G, source=nodi_segmentati[i - 1], target=nodi_segmentati[i], weight='weight')
    except nx.NetworkXNoPath:
        distanza = None
    distanze_segmentali.append(distanza)

info_filtrata_df["Km dal nodo precedente"] = distanze_segmentali

############### VISUALIZZA TABELLA ################
st.markdown(
    "<div style='text-align: center; font-size: 25px; font-weight: bold;'><br>I distributori lungo il percorso</div>",
    unsafe_allow_html=True
)

#spazio a capo
st.markdown(
    "<div style='text-align: center; font-size: 10px;'><br><br></div>",
    unsafe_allow_html=True
)

# Rinomina le colonne prima di mostrarle
df_visualizzato = info_filtrata_df.rename(columns={
    "nodo_name": "Nome",
    "tipo_nodo": "Tipologia",
    "prezzo_medio": "Prezzo medio (€)"
})

if nodi_distributori.empty:
    st.warning("Nessun distributore nel percorso ha prezzi disponibili per il carburante selezionato nel periodo scelto.")
else:
    st.dataframe(df_visualizzato.drop(columns=["ordine", "nodo_id", "dtx", "autostrada_id", "km"]), use_container_width=True)
    # postilla
    st.markdown(
        "<div style='text-align: right; font-size: 10px;'>*La tabella dei distributori non tiene conto della selezione dei Brand</div>",
        unsafe_allow_html=True
    )
    
    ##################### MAPPA INTERATTIVA #####################
    st.markdown(
    "<div style='text-align: center; font-size: 25px; font-weight: bold;'><br>Mappa del percorso</div>",
    unsafe_allow_html=True
    )
    fig = go.Figure()
    for i, row in info_filtrata_df.iterrows():
        if i == 0:
            color = 'green'
            label = 'Entrata'
            testo = f"{label}:<br>{row['nodo_name']}"
        elif i == len(info_filtrata_df) - 1:
            color = 'red'
            label = 'Uscita'
            testo = f"{label}:<br>{row['nodo_name']}"
        else:
            color = 'blue'
            label = 'Distributore'
            testo = f"{label}:<br>{row['nodo_name']}<br>{row['Brand']}"
        posizione_testo = "top center" if i % 2 == 0 else "bottom center"
        fig.add_trace(go.Scatter(
            x=[i],
            y=[0],
            mode='markers+text',
            marker=dict(size=12, color=color),
            text=[testo],
            textposition=posizione_testo,
            hoverinfo='text'
        ))
    fig.add_trace(go.Scatter(
        x=list(range(len(info_filtrata_df))),
        y=[0]*len(info_filtrata_df),
        mode='lines',
        line=dict(color='gray', width=2),
        hoverinfo='skip'
    ))
    fig.update_layout(
        showlegend=False,
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        margin=dict(l=20, r=20, t=20, b=20),
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)
    # postilla
    st.markdown(
        "<div style='text-align: right; font-size: 10px;'>*La mappa dei distributori non tiene conto della selezione dei Brand</div>",
        unsafe_allow_html=True
    )
    ##################### ELENCO A TENDINA BRAND #####################
    # Sidebar per i filtri
    brand_unici = nodi_distributori["Brand"].dropna().unique()
    brand_opzioni = sorted(brand_unici.tolist())
    brand_selezionati = st.sidebar.multiselect("Seleziona uno o più Brand (opzionale)", options=brand_opzioni)

    ##################### ANDAMENTO PREZZI #####################
    st.markdown(
        "<div style='text-align: center; font-size: 25px; font-weight: bold;'><br>Andamento prezzi per distributore</div>",
        unsafe_allow_html=True
    )

    # Unisci le informazioni sui distributori
    prezzi_con_info = prezzi_filtrati.merge(
        nodi_distributori[["nodo_id", "nodo_name", "Brand"]],
        left_on="distributore_id",
        right_on="nodo_id",
        how="inner"
    )


    # Calcola la media giornaliera totale (prima del filtro)
    media_giornaliera_df = prezzi_con_info.groupby("data_update")["prezzo"].mean().reset_index()
    media_giornaliera_df.rename(columns={"prezzo": "prezzo_medio_giornaliero"}, inplace=True)

    # Se non è stato selezionato alcun brand, mostra tutti
    if not brand_selezionati:
        prezzi_con_info_filtrato = prezzi_con_info
    else:
        prezzi_con_info_filtrato = prezzi_con_info[prezzi_con_info["Brand"].isin(brand_selezionati)]
    
    fig_prezzi = go.Figure()

    # Linee per ogni distributore filtrato
    for distributore_id, gruppo in prezzi_con_info_filtrato.groupby("distributore_id"):
        nome = gruppo["nodo_name"].iloc[0]
        brand = gruppo["Brand"].iloc[0]
        etichetta = f"{nome} ({brand})"

        fig_prezzi.add_trace(go.Scatter(
            x=gruppo["data_update"],
            y=gruppo["prezzo"],
            mode='lines+markers',
            name=etichetta
        ))

    # Linea della media giornaliera totale (non filtrata)
    fig_prezzi.add_trace(go.Scatter(
        x=media_giornaliera_df["data_update"],
        y=media_giornaliera_df["prezzo_medio_giornaliero"],
        mode='lines+markers',
        name='Media giornaliera totale',
        line=dict(color='lightgrey', dash='dash'),
        hoverinfo='x+y'
    ))

    fig_prezzi.update_layout(
        xaxis_title="Data",
        yaxis_title="Prezzo (€)",
        height=500,
        margin=dict(l=20, r=20, t=40, b=20),
        legend_title="Distributori"
    )

    st.plotly_chart(fig_prezzi, use_container_width=True)


    ##################### ANDAMENTO PREZZI PER BRAND #####################
    st.markdown(
        "<div style='text-align: center; font-size: 25px; font-weight: bold;'><br>Andamento prezzi medi per Brand</div>",
        unsafe_allow_html=True
    )

    # Media giornaliera per ciascun brand (filtrata se necessario)
    prezzi_brand_df = prezzi_con_info_filtrato.groupby(["data_update", "Brand"])["prezzo"].mean().reset_index()
    prezzi_brand_df.rename(columns={"prezzo": "prezzo_medio_brand"}, inplace=True)

    fig_brand = go.Figure()

    # Conta quanti distributori per brand ci sono nel percorso
    brand_counts = nodi_distributori.groupby("Brand")["nodo_id"].nunique().to_dict()

    # Linee per ciascun brand filtrato
    for brand, gruppo in prezzi_brand_df.groupby("Brand"):
        count = brand_counts.get(brand, 0)
        fig_brand.add_trace(go.Scatter(
            x=gruppo["data_update"],
            y=gruppo["prezzo_medio_brand"],
            mode='lines+markers',
            name=f"{brand} ({count} distr.)"  # aggiunge il numero tra parentesi
        ))

    # Linea della media giornaliera totale (non filtrata)
    fig_brand.add_trace(go.Scatter(
        x=media_giornaliera_df["data_update"],
        y=media_giornaliera_df["prezzo_medio_giornaliero"],
        mode='lines+markers',
        name='Media giornaliera totale',
        line=dict(color='lightgrey', dash='dash'),
        hoverinfo='x+y'
    ))

    fig_brand.update_layout(
        xaxis_title="Data",
        yaxis_title="Prezzo medio (€)",
        height=500,
        margin=dict(l=20, r=20, t=40, b=20),
        legend_title="Brand"
    )

    st.plotly_chart(fig_brand, use_container_width=True)


#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
st.markdown(
    "<div style='text-align: center; font-size: 40px;'<br><br><br><br></div>",
    unsafe_allow_html=True
)
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# Titolo e descrizione
st.markdown(
    "<div style='text-align: center; font-size: 40px; font-weight: bold;'>Dove conviene fare rifornimento?</div>",
    unsafe_allow_html=True
)

###############################################################
# parte 1 (non importa quanti litri voglio tenere alla fine) #
###############################################################
col13, col14 = st.columns(2)
with col13:
    st.markdown(
        "<div style='text-align: center; font-size: 25px; font-weight: bold;'><br>Percorso migliore per<br>minimizzare il costo del carburante</div>",
        unsafe_allow_html=True
    )
col10, col11 = st.columns(2)
with col10:    
    st.markdown(
        "<div style='text-align: center; font-size: 10px;'>*Assunzioni: partenza con il serbatoio pieno; ogni rifornimento raggiunge la capacità massima del serbatoio<br>Precauzione: arrivo con almeno 3l di carburante nel serbatoio</div>",
        unsafe_allow_html=True
    )


# Ordina il DataFrame per 'ordine'
info_filtrata_df = info_filtrata_df.sort_values(by="ordine").reset_index(drop=True)

if info_filtrata_df.empty:
    st.warning("Nessun nodo disponibile per il brand selezionato.")
    st.stop()

# Crea tutte le combinazioni di due nodi con ordine crescente
combinazioni = list(combinations(info_filtrata_df.itertuples(index=False), 2))

# Costruisci la matrice con somma delle distanze
matrice = []

for nodo1, nodo2 in combinazioni:
    # Verifica che l'ordine sia crescente
    if nodo1.ordine < nodo2.ordine:
        # Filtra i nodi intermedi tra nodo1 e nodo2 (inclusi)
        intervallo = info_filtrata_df[
            (info_filtrata_df["ordine"] > nodo1.ordine) &
            (info_filtrata_df["ordine"] <= nodo2.ordine)
        ]
        
        # Somma delle distanze dal precedente
        distanza_totale = intervallo["Km dal nodo precedente"].sum()

        # Aggiungi colonna con consumo medio
        consumo_medio=distanza_totale / consumo_medio_km_l if consumo_medio_km_l else None
        # Aggiungi colonna con prezzo_medio
        if pd.notnull(nodo2.prezzo_medio):
            prezzo_medio_arrivo = nodo2.prezzo_medio
        else:
            prezzo_medio_arrivo = 0 # se voglio mettere come peso dell'ultimo arco il prezzo medio --> media_giornaliera_df["prezzo_medio_giornaliero"].mean().round(3)
        # Aggiungi colonna con consumo_l
        consumo_l = round(consumo_medio,3)
        # Aggiungi colonna con peso dell'arco
        peso_arco = round(consumo_l * prezzo_medio_arrivo, 2)

        # Aggiungi colonna con brand del nodo di arrivo
        brand_arrivo = nodo2.Brand if hasattr(nodo2, "Brand") else None
        
        if consumo_medio_km_l is not None:
            matrice.append({
                "nodo_id_partenza": nodo1.nodo_id,
                "nodo_name_partenza": nodo1.nodo_name,
                "nodo_id_arrivo": nodo2.nodo_id,
                "nodo_name_arrivo": nodo2.nodo_name,
                "ordine_partenza": nodo1.ordine,
                "ordine_arrivo": nodo2.ordine,
                "prezzo_medio_arrivo": prezzo_medio_arrivo,
                "distanza_totale_km": distanza_totale,
                "consumo_l": consumo_l,
                "peso_arco" : peso_arco,
                "brand_arrivo" : brand_arrivo
            })
        else:
            st.warning("Consumo medio non disponibile per questa combinazione.")

# Penalizzazione per archi con nodo2 non appartenente ai brand selezionati
penalizzazione = 1.15  # ad esempio +15% sul costo

for arco in matrice:
    brand_nodo2 = info_filtrata_df.loc[
        info_filtrata_df["nodo_id"] == arco["nodo_id_arrivo"], "Brand"
    ].values[0] if "Brand" in info_filtrata_df.columns else None

    if brand_selezionati and brand_nodo2 not in brand_selezionati:
        arco["peso_arco"] = round(arco["peso_arco"] * penalizzazione, 2)

# Converti in DataFrame
matrice_df = pd.DataFrame(matrice)

# Filtra la matrice in base alla capacità del serbatoio
if not matrice_df.empty and "consumo_l" in matrice_df.columns:
    matrice_filtrata_df = matrice_df[matrice_df["consumo_l"] <= capacita_serbatoio-3] # Mantieni un margine di 3 litri
else:
    matrice_filtrata_df = pd.DataFrame()
    st.warning("La matrice è vuota o la colonna 'consumo_l' non esiste.")

################### NETWORKX_2 ###################
# il dataframe è --> matrice_filtrata_df
G = nx.DiGraph()
for _, row in matrice_filtrata_df.iterrows():
    G.add_edge(row['nodo_id_partenza'], row['nodo_id_arrivo'], weight=row['peso_arco'])

partenza_networkx = caselli_partenza_df.loc[
    caselli_partenza_df["nodo_name"] == partenza, "nodo_id"
].values[0]
arrivo_networkx = caselli_arrivo_df.loc[
    caselli_arrivo_df["nodo_name"] == arrivo, "nodo_id"
].values[0]

try:
    percorso_2 = nx.shortest_path(G, source=partenza_networkx, target=arrivo_networkx, weight='weight')
    costo_totale = nx.shortest_path_length(G, source=partenza_networkx, target=arrivo_networkx, weight='weight')
    #-#st.write(f"Percorso più efficiente: {percorso_2}")
    #-#st.write(f"Costo carburante totale: **{round(costo_totale,2)} €**")
except nx.NetworkXNoPath:
    #-#st.write("Non esiste un percorso tra i nodi indicati.")
    percorso_2 = []

##################### MOSTRA TABELLA PERCORSO EFFICIENTE #####################
# Costruisci le coppie (nodo_partenza, nodo_arrivo) dal percorso
coppie_percorso = list(zip(percorso_2[:-1], percorso_2[1:]))

# Filtra la matrice per le coppie presenti nel percorso
df_percorso_filtrato = matrice_filtrata_df[
    matrice_filtrata_df.apply(
        lambda row: (row['nodo_id_partenza'], row['nodo_id_arrivo']) in coppie_percorso,
        axis=1
    )
]

# Elimina alcune colonne e Rinomina le colonne prima di mostrarle
df_percorso_filtrato = df_percorso_filtrato.drop(columns={"nodo_id_partenza","nodo_id_arrivo","ordine_partenza", "ordine_arrivo"}).rename(columns={
    "nodo_name_partenza": "Nome partenza",
    "nodo_name_arrivo": "Nome arrivo",
    "brand_arrivo" : "Brand arrivo",
    "prezzo_medio_arrivo": "Prezzo medio arrivo (€)",
    "distanza_totale_km": "Distanza totale (km)",
    "peso_arco": "Costo carburante utilizzato (€)",
    "consumo_l" : "Consumo (l)"
})

# Ordina colonne
df_percorso_filtrato = df_percorso_filtrato[[
    "Nome partenza",
    "Nome arrivo",
    "Brand arrivo",
    "Prezzo medio arrivo (€)",
    "Distanza totale (km)",
    "Consumo (l)",
    "Costo carburante utilizzato (€)"
]]

col15, col16 = st.columns(2)
with col15:
    st.dataframe(df_percorso_filtrato)
col17, col18 = st.columns(2)
with col17:
    st.markdown(
        f"<div style='text-align: center; font-size: 16px;'>Costo carburante totale: <b>{round(costo_totale,2)} €</b></div>",
        unsafe_allow_html=True
    )

####################### CALCOLO LITRI RIMANENTI #####################
# Calcola litri rimanenti a fine percorso
if not df_percorso_filtrato.empty:
    # Estrai l'ultimo arco del percorso
    ultimo_arco = df_percorso_filtrato.iloc[-1]
    consumo_ultimo_arco = ultimo_arco["Consumo (l)"]
    
    # Calcola litri rimanenti
    litri_rimanenti = round(capacita_serbatoio - consumo_ultimo_arco, 2)
    with col17:
        st.markdown(
            f"<div style='text-align: center; font-size: 16px;'>Litri rimanenti nel serbatoio alla fine del percorso: <b>{litri_rimanenti} l</b></div>",
            unsafe_allow_html=True
        )    
    
    # Mostra avviso se litri rimanenti sono inferiori a 3
    if litri_rimanenti < 3:
        st.warning("Attenzione: il livello del carburante è inferiore a 3 litri.")
else:
    st.warning("Impossibile calcolare i litri rimanenti: percorso vuoto.")



##################### MAPPA PERCORSO EFFICIENTE (VERTICALE) #####################

# Filtra e ordina il percorso
df_percorso_eff = info_filtrata_df[info_filtrata_df["nodo_id"].isin(percorso_2)]
df_percorso_eff["ordine"] = df_percorso_eff["nodo_id"].apply(lambda x: percorso_2.index(x))
df_percorso_eff = df_percorso_eff.sort_values("ordine").reset_index(drop=True)

# Separa i nodi
nodo_partenza_eff = df_percorso_eff.iloc[0:1]
nodo_uscita_eff = df_percorso_eff.iloc[-1:]
nodi_intermedi_eff = df_percorso_eff.iloc[1:-1]

# Ricompone il DataFrame
df_percorso_eff = pd.concat([nodo_partenza_eff, nodi_intermedi_eff, nodo_uscita_eff])

# Crea la figura
fig_eff = go.Figure()

# Aggiungi i nodi con posizione invertita sull'asse y
for i, row in df_percorso_eff.iterrows():
    y_pos = len(df_percorso_eff) - 1 - i  # Inverti la posizione verticale

    if i == 0:
        color = 'green'
        label = 'Entrata'
        testo = f"{label}:<br>{row['nodo_name']}"
    elif i == len(df_percorso_eff) - 1:
        color = 'red'
        label = 'Uscita'
        testo = f"{label}:<br>{row['nodo_name']}"
    else:
        color = 'blue'
        label = 'Distributore'
        testo = f"{label}:<br>{row['nodo_name']}<br>{row['Brand']}"

    posizione_testo = "middle right" if i % 2 == 0 else "middle left"

    fig_eff.add_trace(go.Scatter(
        x=[0],
        y=[y_pos],
        mode='markers+text',
        marker=dict(size=12, color=color),
        text=[testo],
        textposition=posizione_testo,
        hoverinfo='text'
    ))

# Linea verticale di collegamento (invertita)
fig_eff.add_trace(go.Scatter(
    x=[0]*len(df_percorso_eff),
    y=list(reversed(range(len(df_percorso_eff)))),  # Inverti l'ordine
    mode='lines',
    line=dict(color='gray', width=2),
    hoverinfo='skip'
))

# Layout della figura
fig_eff.update_layout(
    showlegend=False,
    xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
    yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
    margin=dict(l=20, r=20, t=20, b=20),
    height=600
)


col19, col20 = st.columns(2)
with col19:
    st.plotly_chart(fig_eff, use_container_width=True, key='fig_eff')


###############################################################
# parte 2 (voglio arrivare con il "pieno") #
###############################################################
with col14:
    st.markdown(
        "<div style='text-align: center; font-size: 25px; font-weight: bold;'><br>Percorso migliore per<br>minimizzare il costo del carburante e<br>massimizzare i litri del serbatoio</div>",
        unsafe_allow_html=True
    )
with col11:    
    st.markdown(
        "<div style='text-align: center; font-size: 10px;'>*Assunzioni: partenza con il serbatoio pieno; ogni rifornimento raggiunge la capacità massima del serbatoio<br>Precauzione: arrivo con almeno 3l di carburante nel serbatoio</div>",
        unsafe_allow_html=True
    )

# Ordina il DataFrame per 'ordine'
info_filtrata_df = info_filtrata_df.sort_values(by="ordine").reset_index(drop=True)

if info_filtrata_df.empty:
    st.warning("Nessun nodo disponibile per il brand selezionato.")
    st.stop()


# Crea tutte le combinazioni di due nodi con ordine crescente
combinazioni = list(combinations(info_filtrata_df.itertuples(index=False), 2))

# Costruisci la matrice con somma delle distanze
matrice = []

for nodo1, nodo2 in combinazioni:
    # Verifica che l'ordine sia crescente
    if nodo1.ordine < nodo2.ordine:
        # Filtra i nodi intermedi tra nodo1 e nodo2 (inclusi)
        intervallo = info_filtrata_df[
            (info_filtrata_df["ordine"] > nodo1.ordine) &
            (info_filtrata_df["ordine"] <= nodo2.ordine)
        ]
        
        # Somma delle distanze dal precedente
        distanza_totale = intervallo["Km dal nodo precedente"].sum()

        # Aggiungi colonna con consumo medio
        consumo_medio=distanza_totale / consumo_medio_km_l if consumo_medio_km_l else None
        # Aggiungi colonna con prezzo_medio
        if pd.notnull(nodo2.prezzo_medio):
            prezzo_medio_arrivo = nodo2.prezzo_medio
        else:
            prezzo_medio_arrivo = media_giornaliera_df["prezzo_medio_giornaliero"].mean().round(3)
        # Aggiungi colonna con consumo_l
        consumo_l = round(consumo_medio,3)
        # Aggiungi colonna con peso dell'arco
        peso_arco = round(consumo_l * prezzo_medio_arrivo, 2)

        # Aggiungi colonna con brand del nodo di arrivo
        brand_arrivo = nodo2.Brand if hasattr(nodo2, "Brand") else None
        
        if consumo_medio_km_l is not None:
            matrice.append({
                "nodo_id_partenza": nodo1.nodo_id,
                "nodo_name_partenza": nodo1.nodo_name,
                "nodo_id_arrivo": nodo2.nodo_id,
                "nodo_name_arrivo": nodo2.nodo_name,
                "ordine_partenza": nodo1.ordine,
                "ordine_arrivo": nodo2.ordine,
                "prezzo_medio_arrivo": prezzo_medio_arrivo,
                "distanza_totale_km": distanza_totale,
                "consumo_l": consumo_l,
                "peso_arco" : peso_arco,
                "brand_arrivo" : brand_arrivo
            })
        else:
            st.warning("Consumo medio non disponibile per questa combinazione.")

# Penalizzazione per archi con nodo2 non appartenente ai brand selezionati
penalizzazione = 1.15  # ad esempio +15% sul costo

for arco in matrice:
    brand_nodo2 = info_filtrata_df.loc[
        info_filtrata_df["nodo_id"] == arco["nodo_id_arrivo"], "Brand"
    ].values[0] if "Brand" in info_filtrata_df.columns else None

    if brand_selezionati and brand_nodo2 not in brand_selezionati:
        arco["peso_arco"] = round(arco["peso_arco"] * penalizzazione, 2)

# Converti in DataFrame
matrice_df = pd.DataFrame(matrice)

# Filtra la matrice in base alla capacità del serbatoio
if not matrice_df.empty and "consumo_l" in matrice_df.columns:
    matrice_filtrata_df = matrice_df[matrice_df["consumo_l"] <= capacita_serbatoio]
else:
    matrice_filtrata_df = pd.DataFrame()
    st.warning("La matrice è vuota o la colonna 'consumo_l' non esiste.")

################### NETWORKX_2 ###################
# il dataframe è --> matrice_filtrata_df
G = nx.DiGraph()
for _, row in matrice_filtrata_df.iterrows():
    G.add_edge(row['nodo_id_partenza'], row['nodo_id_arrivo'], weight=row['peso_arco'])

partenza_networkx = caselli_partenza_df.loc[
    caselli_partenza_df["nodo_name"] == partenza, "nodo_id"
].values[0]
arrivo_networkx = caselli_arrivo_df.loc[
    caselli_arrivo_df["nodo_name"] == arrivo, "nodo_id"
].values[0]

try:
    percorso_2 = nx.shortest_path(G, source=partenza_networkx, target=arrivo_networkx, weight='weight')
    costo_totale = nx.shortest_path_length(G, source=partenza_networkx, target=arrivo_networkx, weight='weight')
    #-#st.write(f"Percorso più efficiente: {percorso_2}")
    #-#st.write(f"Costo carburante totale: **{round(costo_totale,2)} €**")
except nx.NetworkXNoPath:
    #-#st.write("Non esiste un percorso tra i nodi indicati.")
    percorso_2 = []

##################### MOSTRA TABELLA PERCORSO EFFICIENTE #####################
# Costruisci le coppie (nodo_partenza, nodo_arrivo) dal percorso
coppie_percorso = list(zip(percorso_2[:-1], percorso_2[1:]))

# Filtra la matrice per le coppie presenti nel percorso
df_percorso_filtrato = matrice_filtrata_df[
    matrice_filtrata_df.apply(
        lambda row: (row['nodo_id_partenza'], row['nodo_id_arrivo']) in coppie_percorso,
        axis=1
    )
]

# Elimina alcune colonne e Rinomina le colonne prima di mostrarle
df_percorso_filtrato = df_percorso_filtrato.drop(columns={"nodo_id_partenza","nodo_id_arrivo","ordine_partenza", "ordine_arrivo"}).rename(columns={
    "nodo_name_partenza": "Nome partenza",
    "nodo_name_arrivo": "Nome arrivo",
    "brand_arrivo" : "Brand arrivo",
    "prezzo_medio_arrivo": "Prezzo medio arrivo (€)",
    "distanza_totale_km": "Distanza totale (km)",
    "peso_arco": "Costo carburante utilizzato (€)",
    "consumo_l" : "Consumo (l)"
})

# Ordina colonne
df_percorso_filtrato = df_percorso_filtrato[[
    "Nome partenza",
    "Nome arrivo",
    "Brand arrivo",
    "Prezzo medio arrivo (€)",
    "Distanza totale (km)",
    "Consumo (l)",
    "Costo carburante utilizzato (€)"
]]

# Ricalcola il costo totale escludendo l'ultimo arco (perché effettivamente non viene effettuato il rifornimento al casello di uscita)
if not df_percorso_filtrato.empty:
    costo_senza_ultimo_arco = df_percorso_filtrato.iloc[:-1]["Costo carburante utilizzato (€)"].sum()
else:
    costo_senza_ultimo_arco = 0

with col16:
    st.dataframe(df_percorso_filtrato)
with col18:
    st.markdown(
            f"<div style='text-align: center; font-size: 16px;'>Costo carburante totale: <b>{round(costo_senza_ultimo_arco,2)} €</b></div>",
            unsafe_allow_html=True
        )


####################### CALCOLO LITRI RIMANENTI #####################
# Calcola litri rimanenti a fine percorso
if not df_percorso_filtrato.empty:
    # Estrai l'ultimo arco del percorso
    ultimo_arco = df_percorso_filtrato.iloc[-1]
    consumo_ultimo_arco = ultimo_arco["Consumo (l)"]
    
    # Calcola litri rimanenti
    litri_rimanenti = round(capacita_serbatoio - consumo_ultimo_arco, 2)
    with col18:
        st.markdown(
            f"<div style='text-align: center; font-size: 16px;'>Litri rimanenti nel serbatoio alla fine del percorso: <b>{litri_rimanenti} l</b></div>",
            unsafe_allow_html=True
        )    
else:
    st.warning("Impossibile calcolare i litri rimanenti: percorso vuoto.")


##################### MAPPA PERCORSO EFFICIENTE (VERTICALE) #####################

# Filtra e ordina il percorso
df_percorso_eff = info_filtrata_df[info_filtrata_df["nodo_id"].isin(percorso_2)]
df_percorso_eff["ordine"] = df_percorso_eff["nodo_id"].apply(lambda x: percorso_2.index(x))
df_percorso_eff = df_percorso_eff.sort_values("ordine").reset_index(drop=True)

# Separa nodi
nodo_partenza_eff = df_percorso_eff.iloc[0:1]
nodo_uscita_eff = df_percorso_eff.iloc[-1:]
nodi_intermedi_eff = df_percorso_eff.iloc[1:-1]

# Ricompone il percorso
df_percorso_eff = pd.concat([nodo_partenza_eff, nodi_intermedi_eff, nodo_uscita_eff])

# Crea il grafico verticale
fig_eff_litri = go.Figure()

for i, row in df_percorso_eff.iterrows():
    y_pos = len(df_percorso_eff) - 1 - i  # Inverti la posizione verticale 
    if i == 0:
        color = 'green'
        label = 'Entrata'
        testo = f"{label}:<br>{row['nodo_name']}"
    elif i == len(df_percorso_eff) - 1:
        color = 'red'
        label = 'Uscita'
        testo = f"{label}:<br>{row['nodo_name']}"
    else:
        color = 'blue'
        label = 'Distributore'
        testo = f"{label}:<br>{row['nodo_name']}<br>{row['Brand']}"
    
    posizione_testo = "middle right" if i % 2 == 0 else "middle left"
    
    fig_eff_litri.add_trace(go.Scatter(
        x=[0],
        y=[y_pos],
        mode='markers+text',
        marker=dict(size=12, color=color),
        text=[testo],
        textposition=posizione_testo,
        hoverinfo='text'
    ))

# Linea verticale di collegamento
fig_eff_litri.add_trace(go.Scatter(
    x=[0]*len(df_percorso_eff),
    y=list(reversed(range(len(df_percorso_eff)))),
    mode='lines',
    line=dict(color='gray', width=2),
    hoverinfo='skip'
))

# Layout aggiornato per visualizzazione verticale
fig_eff_litri.update_layout(
    showlegend=False,
    xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
    yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
    margin=dict(l=20, r=20, t=20, b=20),
    height=600  # Puoi aumentare se hai più nodi
)

# Visualizzazione con Streamlit
with col20:
    st.plotly_chart(fig_eff_litri, use_container_width=True, key='fig_eff_litri')

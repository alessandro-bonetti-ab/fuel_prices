import requests
import json
from datetime import datetime
import os
import pandas as pd
import csv
import ast # Per convertire la stringa in un dizionario
import zoneinfo
from bs4 import BeautifulSoup
import time
from io import StringIO


# timestamp
oggi = datetime.now().strftime("%Y.%m.%d")

# RAMI AUTOSTRADALI
# Crea cartella per il CSV CASELLI-ALLACCIAMENTI se non esiste
os.makedirs("caselli_allacciamenti", exist_ok=True)
# Esempio: trovi gli URL dati esplorando Network in DevTools del browser
base_url = "https://www2.autostrade.it/BVS/portale/rete/"
pagina = "stradeRami.jsp"
url4 = base_url + pagina

csv_filename = f"caselli_allacciamenti/{oggi}_ramo_autostrada.csv"
csv_output_rami = f"caselli_allacciamenti/{oggi}_output_ramo_autostrada.csv"

response = requests.get(url4)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('table')
rows = []

for tr in table.find_all('tr')[1:]:
    tds = tr.find_all('td')
    if len(tds) < 2:
        continue

    a_tag = tds[0].find('a')
    link = ""
    if a_tag and 'href' in a_tag.attrs:
        href = a_tag['href']
        if href.startswith("http"):
            link = href
        else:
            link = base_url + href.lstrip("/")

    nome_strada = tds[0].get_text(strip=True)
    ramo = tds[1].get_text(strip=True)

    rows.append([link, nome_strada, ramo])

df = pd.DataFrame(rows, columns=["link", "cd_autostrada", "ramo"])
df.to_csv(csv_filename, index=False)
print("CSV creato con link funzionanti")

# Leggi il csv appena creato ispezionandone i singoli links
# Carica i link e le informazioni dei rami
df_links = pd.read_csv(csv_filename)
# DataFrame per accumulare i dati
dati_completi = []
# Nomi di colonna standard attesi
colonne_standard = [
    "Codice",
    "Nome",
    "Allacciamento",
    "Carr. Destra",
    "Carr. Sinistra",
    "Km",
    "Societa' Comp."
]
# Estrai i dati da ogni pagina (max 3 per test)
for idx, row in df_links.iterrows():
    url4 = row["link"]
    cd_autostrada = row["cd_autostrada"]
    ramo = row["ramo"]
    try:
        print(f"🔗 Elaboro: {url4}")
        response = requests.get(url4, timeout=10)
        response.raise_for_status()
        # Estrai le tabelle HTML
        tabelle = pd.read_html(StringIO(response.text), header=0)
        for tabella in tabelle:
            if tabella.shape[1] == 7:
                # Imposta intestazioni corrette
                tabella.columns = colonne_standard
                # ✅ Filtra via eventuali righe "intestazione duplicata"
                righe_valide = ~tabella.eq(colonne_standard).all(axis=1)
                tabella = tabella[righe_valide]
                # Inserisce le colonne di contesto
                tabella.insert(0, "ramo", ramo)
                tabella.insert(0, "cd_autostrada", cd_autostrada)
                tabella.insert(0, "link", url4)
                dati_completi.append(tabella)
        time.sleep(1.5)
    except Exception as e:
        print(f"❌ Errore con {url4}: {e}")
        continue
# Salva il risultato finale in un CSV
if dati_completi:
    df_finale = pd.concat(dati_completi, ignore_index=True)
    df_finale.to_csv(csv_output_rami, index=False)
    print("✅ File finale salvato come 'output_tabelle_rami_standard.csv'")
else:
    print("⚠️ Nessuna tabella utile trovata.")
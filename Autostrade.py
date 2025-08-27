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

# timestamp
oggi = datetime.now().strftime("%Y.%m.%d")

# Crea cartella per il CSV DISTR MINISTERO MIMIT se non esiste
os.makedirs("distr_mimit", exist_ok=True)
url = "https://www.mimit.gov.it/images/exportCSV/prezzo_alle_8.csv"
mimit_distr_path = f"distr_mimit/{oggi}_prezzi_mimit.csv"
response = requests.get(url)
if response.status_code == 200:
    with open(mimit_distr_path, "wb") as f:
        f.write(response.content)
    print("Download completato e salvato in distr_mimit!")
else:
    print(f"Errore nel download: {response.status_code}")

# Crea cartella per il CSV ANAGRAFICA MINISTERO MIMIT se non esiste
os.makedirs("anag_impianti_mimit", exist_ok=True)
url = "https://www.mimit.gov.it/images/exportCSV/anagrafica_impianti_attivi.csv"
mimit_anag_path = f"anag_impianti_mimit/{oggi}_anag_imp_att_mimit.csv"
response = requests.get(url)
if response.status_code == 200:
    with open(mimit_anag_path, "wb") as f:
        f.write(response.content)
    print("Download completato e salvato in anag_impianti_mimit!")
else:
    print(f"Errore nel download: {response.status_code}")


# Crea cartella per il JSON ADPS se non esiste
os.makedirs("adps", exist_ok=True)
url = "https://viabilita.autostrade.it/json/adps.json"
adps_path = f"adps/{oggi}_adps.json"
response = requests.get(url)
if response.status_code == 200:
    with open(adps_path, "wb") as f:
        f.write(response.content)
    print("Download completato e salvato in adps!")
else:
    print(f"Errore nel download: {response.status_code}")


# Crea cartella per il JSON anag_autostrade se non esiste
os.makedirs("anag_autostrade", exist_ok=True)
url = "https://viabilita.autostrade.it/json/autostrade.json"
autostrade_anag_path = f"anag_autostrade/{oggi}_anag_autostrade.json"
response = requests.get(url)
if response.status_code == 200:
    with open(autostrade_anag_path, "wb") as f:
        f.write(response.content)
    print("Download completato e salvato in anag_autostrade!")
else:
    print(f"Errore nel download: {response.status_code}")


# Crea cartella per il JSON anag_regioni se non esiste
os.makedirs("anag_regioni", exist_ok=True)
url = "https://viabilita.autostrade.it/json/regioni.json"
regioni_anag_path = f"anag_regioni/{oggi}_anag_regioni.json"
response = requests.get(url)
if response.status_code == 200:
    with open(regioni_anag_path, "wb") as f:
        f.write(response.content)
    print("Download completato e salvato in anag_regioni!")
else:
    print(f"Errore nel download: {response.status_code}")

# Crea cartella per il CSV TRAIFFE se non esiste --> utile per anag_società
os.makedirs("tariffe", exist_ok=True)
url = "https://viabilita.autostrade.it/json/tariffe.json"
tariffe_path = f"tariffe/{oggi}_tariffe.csv"
response = requests.get(url)
if response.status_code == 200:
    with open(tariffe_path, "wb") as f:
        f.write(response.content)
    print("Download completato e salvato in tariffe!")
else:
    print(f"Errore nel download: {response.status_code}")


# Crea cartella per lo STORICO DISTRIBUTORI se non esiste
os.makedirs("storico_distributori", exist_ok=True)
# Richiesta all'endpoint
url = "https://viabilita.autostrade.it/json/adss.json"
response = requests.get(url)
data = response.json()
# Salva con timestamp
json_path = f"storico_distributori/{oggi}_distr.json"
csv_path = f"storico_distributori/{oggi}_distr.csv"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"Salvati {len(data)} record in {json_path}")

# Se il JSON è un dizionario, cerca la lista di record
if isinstance(data, dict):
    # Se sai la chiave (es. 'distributori'), usa quella direttamente:
    # data = data["distributori"]
    # Se NON sai la chiave, cerca la prima lista trovata
    for key, value in data.items():
        if isinstance(value, list):
            data = value
            print(f"Estratta lista dalla chiave '{key}'")
            break
# Verifica che sia una lista di dizionari
if isinstance(data, list) and all(isinstance(item, dict) for item in data):
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False, encoding='utf-8',quoting=csv.QUOTE_ALL)
    print(f"CSV salvato correttamente come '{csv_path}'")
else:
    print("I dati non sono in formato lista di dizionari.")





# colonnine
# Crea cartella per lo storico colonnine se non esiste
os.makedirs("storico_colonnine", exist_ok=True)

url_2= "https://viabilita.autostrade.it/json/colonnine.json"
response_2 = requests.get(url_2)
data_2 = response_2.json()

# Salva con timestamp
json_path_2 = f"storico_colonnine/{oggi}_colonnine.json"
csv_path_2 = f"storico_colonnine/{oggi}_colonnine.csv"

with open(json_path_2, "w", encoding="utf-8") as f:
    json.dump(data_2, f, ensure_ascii=False, indent=2)

print(f"Salvati {len(data_2)} record in {json_path_2}")


# Se il JSON è un dizionario, cerca la lista di record
if isinstance(data_2, dict):
    # Se sai la chiave (es. 'distributori'), usa quella direttamente:
    # data = data["distributori"]

    # Se NON sai la chiave, cerca la prima lista trovata
    for key, value in data_2.items():
        if isinstance(value, list):
            data_2 = value
            print(f"Estratta lista dalla chiave '{key}'")
            break

# Verifica che sia una lista di dizionari
if isinstance(data_2, list) and all(isinstance(item, dict) for item in data_2):
    df = pd.DataFrame(data_2)
    df.to_csv(csv_path_2, index=False, encoding='utf-8',quoting=csv.QUOTE_ALL)
    print(f"CSV salvato correttamente come '{csv_path_2}'")
else:
    print("I dati non sono in formato lista di dizionari.")





# caselli
# Crea cartella per lo storico caselli se non esiste
os.makedirs("storico_caselli", exist_ok=True)

url_3= "https://viabilita.autostrade.it/json/caselli.json"
response_3 = requests.get(url_3)
data_3 = response_3.json()

# Salva con timestamp
json_path_3 = f"storico_caselli/{oggi}_caselli.json"
csv_path_3 = f"storico_caselli/{oggi}_caselli.csv"

with open(json_path_3, "w", encoding="utf-8") as f:
    json.dump(data_3, f, ensure_ascii=False, indent=2)

print(f"Salvati {len(data_3)} record in {json_path_3}")


# Se il JSON è un dizionario, cerca la lista di record
if isinstance(data_3, dict):
    # Se sai la chiave (es. 'distributori'), usa quella direttamente:
    # data = data["distributori"]

    # Se NON sai la chiave, cerca la prima lista trovata
    for key_3, value_3 in data_3.items():
        if isinstance(value_3, list):
            data_3 = value_3
            print(f"Estratta lista dalla chiave '{key_3}'")
            break

# Verifica che sia una lista di dizionari
if isinstance(data_3, list) and all(isinstance(item, dict) for item in data_3):
    df = pd.DataFrame(data_3)
    df.to_csv(csv_path_3, index=False, encoding='utf-8',quoting=csv.QUOTE_ALL)
    print(f"CSV salvato correttamente come '{csv_path_3}'")
else:
    print("I dati non sono in formato lista di dizionari.")
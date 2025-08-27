import pandas as pd
import os
import csv

# Crea la cartella di destinazione se non esiste
os.makedirs("dim_distributori", exist_ok=True)

# Carica il file CSV principale
df = pd.read_csv("storico_distributori/2025.08.20_distr.csv", encoding="utf-8")

# Rimuove le colonne non necessarie
colonne_da_rimuovere = [
    "bhvoUpd", "bgnsUpd", "srvsn", "srvsb", "events", "indPmrs",
    "prevs", "nexts", "benPrice", "benUpd", "bdisPrice", "bdisUpd",
    "bgplPrice", "bgplUpd", "bhvoPrice", "bgnsPrice", "bmetPrice", "bmetUpd"
]
df_cleaned = df.drop(columns=[col for col in colonne_da_rimuovere if col in df.columns])

# Converte 'dtx' in object
df_cleaned["dtx"] = df_cleaned["dtx"].astype(str)

# Carica il file di decodifica e converte 'autostrade_dtx' in object
df_decodifica = pd.read_csv("decodifiche/decodifica_distributori.csv", encoding="utf-8", sep=",")
df_decodifica["autostrade_dtx"] = df_decodifica["autostrade_dtx"].astype(str)

# Merge tra df_cleaned e df_decodifica su 'dtx' e 'autostrade_dtx'
df_merged = pd.merge(
    df_cleaned,
    df_decodifica[["autostrade_dtx", "idImpianto", "nome_impianto"]],
    left_on="dtx",
    right_on="autostrade_dtx",
    how="left"
)

# Carica il file anagrafico saltando la prima riga

df_anagrafica = pd.read_csv("anag_impianti_mimit/2025.08.20_anag_imp_att_mimit.csv",
    sep=";",
    skiprows=1,
    quoting=csv.QUOTE_ALL,
    on_bad_lines='skip', # salta righe malformate perché dà un errore nella riga 550 in cui dice esserci una colonna in più
    encoding="utf-8"
)
# Merge su 'idImpianto' per ottenere la colonna 'Bandiera'
df_merged = pd.merge(
    df_merged,
    df_anagrafica[["idImpianto", "Bandiera"]],
    on="idImpianto",
    how="left"
)

# Crea la colonna 'Brand' basata su 'carbDesbrd' se non nullo, altrimenti 'Bandiera'
df_merged["Brand"] = df_merged["carbDesbrd"].combine_first(df_merged["Bandiera"])
# Trasforma i nomi in maiuscolo
df_merged["Brand"] = df_merged["Brand"].str.upper()

# Uniforma API-IP e ENI
df_merged["Brand"] = df_merged["Brand"].replace({
    "ENI": "AGIP ENI",
    "API-IP": "IP GRUPPO API"
})

# Salva il file finale
df_merged.to_csv("dim_distributori/dim_distributori.csv", index=False, encoding="utf-8")

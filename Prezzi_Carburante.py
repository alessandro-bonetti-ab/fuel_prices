import pandas as pd
import os
import csv
from datetime import datetime, timedelta
import time
import locale

# timestamp
oggi = datetime.now().strftime("%Y.%m.%d")

# Imposta la localizzazione italiana per formattare i mesi (se disponibile sul tuo sistema)
locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8')

# Crea cartella per la fact_prezzi_autostrade se non esiste
os.makedirs("fact_prezzi_autostrade", exist_ok=True)
# Leggi il file CSV
csv_file_path = f"storico_distributori/{oggi}_distr.csv"
df = pd.read_csv(csv_file_path, sep=",")
# Funzione per convertire il Upd in data e ora separate
def estrai_data_ora(ms):
    try:
        ts_s = float(ms) / 1000  # da millisecondi a secondi
        dt = datetime.fromtimestamp(ts_s)
        data = dt.strftime('%d/%m/%Y')     # es. '27/07/2025'
        ora = dt.strftime('%H:%M:%S')      # es. '14:56:23'
        return pd.Series([data, ora])
    except:
        return pd.Series(['',''])

########################### BENZINA ###########################
# Tieni le colonne necessarie
df_benzina = df[['dtx', 'benPrice', 'benUpd']].copy()
# Aggiungi colonna etichetta tipo carburante
df_benzina['tipo_carburante'] = 'BENZINA'
# Applichiamo la conversione e aggiungiamo le nuove colonne
df_benzina[['data_update', 'ora_update']] = df_benzina['benUpd'].apply(estrai_data_ora)
# Rinominare le colonne esistenti
df_benzina = df_benzina.rename(columns={
    'dtx': 'distributore_id',
    'benPrice': 'prezzo'
})
df_benzina = df_benzina[['distributore_id', 'prezzo', 'data_update', 'ora_update', 'tipo_carburante']]
# Accoda i dati al fila CSV esistente
df_benzina.to_csv('fact_prezzi_autostrade/fact_prezzi_autostrade.csv', mode='a', header=False, index=False)
print("Accodato prezzi benzina in fact_prezzi_autostrade.csv'")

########################### DIESEL ###########################
# Tieni le colonne necessarie
df_diesel = df[['dtx', 'bdisPrice', 'bdisUpd']].copy()
# Aggiungi colonna etichetta tipo carburante
df_diesel['tipo_carburante'] = 'DIESEL'
# Applichiamo la conversione e aggiungiamo le nuove colonne
df_diesel[['data_update', 'ora_update']] = df_diesel['bdisUpd'].apply(estrai_data_ora)
# Rinominare le colonne esistenti
df_diesel = df_diesel.rename(columns={
    'dtx': 'distributore_id',
    'bdisPrice': 'prezzo'
})
df_diesel = df_diesel[['distributore_id', 'prezzo', 'data_update', 'ora_update', 'tipo_carburante']]
# Accoda i dati al fila CSV esistente
df_diesel.to_csv('fact_prezzi_autostrade/fact_prezzi_autostrade.csv', mode='a', header=False, index=False)
print("Accodato prezzi diesel in fact_prezzi_autostrade.csv'")

########################### GPL ###########################
# Tieni le colonne necessarie
df_gpl = df[['dtx', 'bgplPrice', 'bgplUpd']].copy()
# Aggiungi colonna etichetta tipo carburante
df_gpl['tipo_carburante'] = 'GPL'
# Applichiamo la conversione e aggiungiamo le nuove colonne
df_gpl[['data_update', 'ora_update']] = df_gpl['bgplUpd'].apply(estrai_data_ora)
# Rinominare le colonne esistenti
df_gpl = df_gpl.rename(columns={
    'dtx': 'distributore_id',
    'bgplPrice': 'prezzo'
})
df_gpl = df_gpl[['distributore_id', 'prezzo', 'data_update', 'ora_update', 'tipo_carburante']]
# Accoda i dati al fila CSV esistente
df_gpl.to_csv('fact_prezzi_autostrade/fact_prezzi_autostrade.csv', mode='a', header=False, index=False)
print("Accodato prezzi gpl in fact_prezzi_autostrade.csv'")

########################### HVO ###########################
# Tieni le colonne necessarie
df_hvo = df[['dtx', 'bhvoPrice', 'bhvoUpd']].copy()
# Aggiungi colonna etichetta tipo carburante
df_hvo['tipo_carburante'] = 'HVO'
# Applichiamo la conversione e aggiungiamo le nuove colonne
df_hvo[['data_update', 'ora_update']] = df_hvo['bhvoUpd'].apply(estrai_data_ora)
# Rinominare le colonne esistenti
df_hvo = df_hvo.rename(columns={
    'dtx': 'distributore_id',
    'bhvoPrice': 'prezzo'
})
df_hvo = df_hvo[['distributore_id', 'prezzo', 'data_update', 'ora_update', 'tipo_carburante']]
# Accoda i dati al fila CSV esistente
df_hvo.to_csv('fact_prezzi_autostrade/fact_prezzi_autostrade.csv', mode='a', header=False, index=False)
print("Accodato prezzi hvo in fact_prezzi_autostrade.csv'")

########################### GNS ##############################
# Tieni le colonne necessarie
df_gns = df[['dtx', 'bgnsPrice', 'bgnsUpd']].copy()
# Aggiungi colonna etichetta tipo carburante
df_gns['tipo_carburante'] = 'GNS'
# Applichiamo la conversione e aggiungiamo le nuove colonne
df_gns[['data_update', 'ora_update']] = df_gns['bgnsUpd'].apply(estrai_data_ora)
# Rinominare le colonne esistenti
df_gns = df_gns.rename(columns={
    'dtx': 'distributore_id',
    'bgnsPrice': 'prezzo'
})
df_gns = df_gns[['distributore_id', 'prezzo', 'data_update', 'ora_update', 'tipo_carburante']]
# Accoda i dati al fila CSV esistente
df_gns.to_csv('fact_prezzi_autostrade/fact_prezzi_autostrade.csv', mode='a', header=False, index=False)
print("Accodato prezzi gns in fact_prezzi_autostrade.csv'")

########################### METANO ###########################
# Tieni le colonne necessarie
df_metano = df[['dtx', 'bmetPrice', 'bmetUpd']].copy()
# Aggiungi colonna etichetta tipo carburante
df_metano['tipo_carburante'] = 'METANO'
# Applichiamo la conversione e aggiungiamo le nuove colonne
df_metano[['data_update', 'ora_update']] = df_metano['bmetUpd'].apply(estrai_data_ora)
# Rinominare le colonne esistenti
df_metano = df_metano.rename(columns={
    'dtx': 'distributore_id',
    'bmetPrice': 'prezzo'
})
df_metano = df_metano[['distributore_id', 'prezzo', 'data_update', 'ora_update', 'tipo_carburante']]
# Accoda i dati al fila CSV esistente
df_metano.to_csv('fact_prezzi_autostrade/fact_prezzi_autostrade.csv', mode='a', header=False, index=False)
print("Accodato prezzi metano in fact_prezzi_autostrade.csv'")

########################### ORDINA E RIMUOVI DUPLICATI ###########################
# Ordina per 'data_update' e 'ora_update' in ordine crescente e rimuovi i duplicati dal fact_prezzi_autostrade.csv
df = pd.read_csv('fact_prezzi_autostrade/fact_prezzi_autostrade.csv')
df_sorted = df.sort_values(by=['data_update', 'ora_update', 'distributore_id', 'tipo_carburante'])
df_prezzi = df_sorted.drop_duplicates()
df_prezzi.to_csv('fact_prezzi_autostrade/fact_prezzi_autostrade.csv', index=False)
print("Rimossi duplicati in fact_prezzi_autostrade.csv'")


########################### ACCODO PREZZI MIMIT E AGGANCIO LA DECODIFICA DISTRIBUTORI ###########################
# Leggi il file CSV
csv_file_path = f"distr_mimit/{oggi}_prezzi_mimit.csv"
df = pd.read_csv(csv_file_path, sep=";", skiprows=1) # skiprows=1 permette di salatre la prima riga
# Divido il campo stComu in data e ora di update
df[['data_update', 'ora_update']] = df['dtComu'].str.split(' ', expand=True)
# Filtra le righe dove isSelf == 1
df_filtrato = df[df['isSelf'] == 1].copy()
# Rinomina colonna descCarburante e converte in maiuscolo
df_filtrato.rename(columns={'descCarburante': 'tipo_carburante'}, inplace=True)
df_filtrato['tipo_carburante'] = df_filtrato['tipo_carburante'].str.upper()

# Leggi il file di decodifica
df_decodifica = pd.read_csv('decodifiche/decodifica_distributori.csv')
# Convert both to string
df_filtrato['idImpianto'] = df_filtrato['idImpianto'].astype(str)
df_decodifica['idImpianto'] = df_decodifica['idImpianto'].astype(str)
# Unisci i due DataFrame sulla colonna 'idImpianto'
df_completo = pd.merge(df_filtrato, df_decodifica, on='idImpianto', how='inner')
# Rinomina colonna autostrade_dtx
df_completo.rename(columns={'autostrade_dtx': 'distributore_id'}, inplace=True)

# Accodo nel file fact_prezzi_mimit.csv
df_completo = df_completo[['distributore_id', 'prezzo', 'data_update', 'ora_update', 'tipo_carburante']]
df_completo.to_csv('fact_prezzi_autostrade/fact_prezzi_mimit.csv', mode='a', header=True, index=False)
print("Accodato file in fact_prezzi_mimit.csv'")

########################### ORDINA E RIMUOVI DUPLICATI ###########################
# Ordina per 'data_update' e 'ora_update' in ordine crescente e rimuovi i duplicati dal fact_prezzi_mimit.csv
df = pd.read_csv('fact_prezzi_autostrade/fact_prezzi_mimit.csv', low_memory=False)
df_sorted = df.sort_values(by=['data_update', 'ora_update', 'distributore_id', 'tipo_carburante'])
df_prezzi = df_sorted.drop_duplicates()
df_prezzi.to_csv('fact_prezzi_autostrade/fact_prezzi_mimit.csv', index=False)
print("Rimossi duplicati in fact_prezzi_mimit.csv'")

########################### ACCODO PREZZI MIMIT A PREZZI AUTOSTRADE ###########################
df_autostrade = pd.read_csv('fact_prezzi_autostrade/fact_prezzi_autostrade.csv')
df_mimit = pd.read_csv('fact_prezzi_autostrade/fact_prezzi_mimit.csv', low_memory=False)
df_completo = pd.concat([df_autostrade, df_mimit], ignore_index=True)
# Ordina per 'data_update' e 'ora_update' in ordine crescente e rimuovi i duplicati dal fact_prezzi_autostrade.csv
df_completo_sorted = df_completo.sort_values(by=['data_update', 'ora_update', 'distributore_id', 'tipo_carburante'])
df_completo_prezzi = df_completo_sorted.drop_duplicates()
# Salva il file completo
df_completo_prezzi.to_csv('fact_prezzi_autostrade/fact_prezzi.csv', index=False)
print("Accodati prezzi MIMIT e prezzi autostrade in fact_prezzi")
      
########################### ORDINA E RIMUOVI DUPLICATI ###########################
df = pd.read_csv('fact_prezzi_autostrade/fact_prezzi.csv', low_memory=False)
# Rimuovo le righe con data_update vuota o contiene 'data_update' (c'era una riga uguale all'intestazione)
df = df[
    df['data_update'].notna() & 
    (df['data_update'].str.strip() != '') & 
    (df['data_update'].str.strip() != 'data_update')]
# Ordina per 'data_update' e 'ora_update' in ordine crescente e rimuovi i duplicati dal fact_prezzi_autostrade.csv
df_sorted = df.sort_values(by=['data_update', 'ora_update', 'distributore_id', 'tipo_carburante'])
df_prezzi = df_sorted.drop_duplicates()
df_prezzi.to_csv('fact_prezzi_autostrade/fact_prezzi.csv', index=False)
print("Rimossi duplicati in fact_prezzi.csv'")


########################### CREO DIM TIPO CARBURANTE ###########################
# Crea cartella per la fact_prezzi_autostrade se non esiste
os.makedirs("dim_carburante", exist_ok=True)
# Leggi il fil csv
df = pd.read_csv('fact_prezzi_autostrade/fact_prezzi.csv')
# Crea un DataFrame con i tipi di carburante unici
df_tipo_carburante = pd.DataFrame(df['tipo_carburante'].unique())
# metti in ordine alfabetico
df_tipo_carburante = df_tipo_carburante.sort_values(by=0).reset_index(drop=True)
# Rinomina la colonna
df_tipo_carburante.columns = ['tipo_carburante']
# Aggiungi colonna "carburante" secodno la seguente mappatura oppure lascia quello esistente
mappatura = {
    'BENZINA PLUS 98': 'BENZINA PREMIUM',
    'BENZINA SPECIALE': 'BENZINA PREMIUM',
    'BENZINA WR 100': 'BENZINA PREMIUM',
    'BLUE DIESEL': 'DIESEL',
    'BLUE SUPER': 'DIESEL',
    'GASOLIO': 'DIESEL',
    'GASOLIO ECOPLUS': 'DIESEL',
    'GASOLIO GELO': 'DIESEL',
    'GASOLIO HVO': 'DIESEL',
    'HIQ PERFORM+': 'BENZINA PREMIUM'
}
df_tipo_carburante['carburante'] = df_tipo_carburante['tipo_carburante'].map(mappatura).fillna(df_tipo_carburante['tipo_carburante'])
# Tieni solo i tipi di carburante in (DIESEL, BENZINA, BENZINA PREMIUM, METANO)
df_tipo_carburante = df_tipo_carburante[df_tipo_carburante['carburante'].isin(['DIESEL', 'BENZINA', 'BENZINA PREMIUM', 'METANO'])]
# Salva il file
df_tipo_carburante.to_csv('dim_carburante/dim_carburante.csv', index=False, header=True)
print("Creato dim_carburante.csv con i tipi di carburante unici")



############################# FACT PREZZI COMLPETO ###########################
# --- 1. Carica il file Excel base ---
df_fact_prezzi = pd.read_csv(r"fact_prezzi_autostrade/fact_prezzi.csv")
# Mantieni solo le colonne distributore_id e tipo_carburante e rimuovi i duplicati
df_base = df_fact_prezzi[['distributore_id', 'tipo_carburante']].drop_duplicates().reset_index(drop=True)

# --- 2. Genera intervallo di date per tutto il 2025 ---
date_range = pd.date_range(start="2025-01-01", end="2025-12-31", freq="D")
df_date = pd.DataFrame({'data_update': date_range})

# --- 3. Prodotto cartesiano tra distributori e date -- 
#Ovvero ci crea per ogni distributore 365 righe
df = df_base.merge(df_date, how='cross')

# --- 4. Conversione sicura delle date e filtra solo l'ultimo aggiornamento ---
#converte le dare in formato corretto
#se per un distributore+carburante+giorno ci sono più prezzi, conserva solo quello con la ora maggione(ultimo aggiornamento)
df_fact_prezzi["data_update"] = pd.to_datetime(df_fact_prezzi["data_update"], errors="coerce")
df_filtered = df_fact_prezzi.loc[
    df_fact_prezzi.groupby(["distributore_id", "tipo_carburante", "data_update"])["ora_update"].idxmax()
][["distributore_id", "tipo_carburante", "data_update", "prezzo"]]

# --- 5. Merge ---
df = pd.merge(
    df,
    df_filtered,
    on=["distributore_id", "tipo_carburante", "data_update"],
    how="left"
)

# --- 6. Converte prezzo in numerico ---
df["prezzo"] = pd.to_numeric(df["prezzo"], errors="coerce")

# --- 7. Mantieni ordine per ricostruire sequenza ---
df["__order__"] = range(len(df))
df = df.sort_values(["distributore_id", "tipo_carburante", "data_update"])

# --- 8. Riempie i NaN col prezzo precedente ---
df["prezzo"] = df.groupby(["distributore_id", "tipo_carburante"])["prezzo"].transform(lambda s: s.ffill())

# --- 9. Cancella i prezzi futuri ---
oggi = datetime.now().date()
df.loc[df["data_update"].dt.date > oggi, "prezzo"] = None

# --- 10. Ripristina ordine originale ---
df = df.sort_values("__order__").drop(columns="__order__")

# --- 11. Trasforma la colonna con le date come strftime("%Y.%m.%d")---
df["data_update"] = df["data_update"].dt.strftime("%d/%m/%Y")

# --- 12. Trasforma alcuni tipo_carburante ---
df['tipo_carburante'] = df['tipo_carburante'].replace({
    'BENZINA PLUS 98': 'BENZINA PREMIUM',
    'BENZINA SPECIALE': 'BENZINA PREMIUM',
    'BENZINA WR 100': 'BENZINA PREMIUM',
    'BLUE DIESEL': 'DIESEL',
    'BLUE SUPER': 'DIESEL',
    'GASOLIO': 'DIESEL',
    'GASOLIO ECOPLUS': 'DIESEL',
    'GASOLIO GELO': 'DIESEL',
    'GASOLIO HVO': 'DIESEL',
    'HIQ PERFORM+': 'BENZINA PREMIUM'
})

# --- 13. Tieni solo le righe con tipo_carburante in (DIESEL, BENZINA, BENZINA PREMIUM, METANO) ---
df = df[df['tipo_carburante'].isin(['DIESEL', 'BENZINA', 'BENZINA PREMIUM', 'METANO'])]

# --- 14. Salva SOLO alla fine ---
df.to_csv(r"fact_prezzi_autostrade/fact_prezzi_completo.csv", index=False)
print("File finale generato: fact_prezzi_completo.csv")

import pandas as pd
import os
import csv
from datetime import datetime
import time
import locale

# timestamp
oggi = datetime.now().strftime("%Y.%m.%d")

# Crea cartella per la dim_input_networkx se non esiste
os.makedirs("dim_input_networkx", exist_ok=True)

# Leggo i csv di cui ho bisogno
df_distributori = pd.read_csv('dim_distributori/dim_distributori.csv', sep=',')
df_ramificazioni = pd.read_csv('caselli_allacciamenti/2025.07.21_output_ramo_autostrada.csv', sep=',')
df_decodifica = pd.read_csv('decodifiche/decodifica_autostrade.csv', sep=',')

################## DISTRIBUTORI ##################
# Dall'anagrafica distributori prendo solo le colonne necessarie
df_distributori = df_distributori [['dtx', 'nome', 'n_prg_km', 'c_str', 'c_ram', 'c_dir']].copy()

# Creo il concat per poi unire con la decodifica autostrade
df_distributori["concat"] = df_distributori["c_str"] + "-" + df_distributori["c_ram"]

# Unisci i due DataFrame sulla colonna 'concat'
df_merge = pd.merge(df_distributori, df_decodifica, on='concat', how='left')

# Tengo le colonne che mi servono per accodare le ramificazioni
df_distributori = df_merge[['dtx', 'nome', 'n_prg_km', 'c_dir', 'cd_autostrada']].copy()

# Aggiungi colonna etichetta tipo nodo
df_distributori['tipo_nodo'] = 'DISTRIBUTORE'
df_distributori = df_distributori.rename(columns={
    'dtx': 'nodo_id',
    'nome': 'nodo_name',
    'n_prg_km': 'km',
    'c_dir' : 'direzione',
    'cd_autostrada': 'autostrada_id',
    'tipo_nodo': 'tipo_nodo'
})


################## RAMIFICAZIONI ##################
# Dalle ramificazioni prendo solo le colonne necessarie
df_ramificazioni = df_ramificazioni [['Codice', 'Nome', 'Km', 'cd_autostrada', 'Allacciamento']].copy()
# Aggiungo colonna etichetta tipo nodo
df_ramificazioni['tipo_nodo'] = df_ramificazioni["Allacciamento"].apply(lambda x: "CASELLO" if pd.isna(x) or str(x).strip() == "" else "ALLACCIAMENTO")

# Creo elenco con D
df_ramificazioni_D = df_ramificazioni.copy()
df_ramificazioni_D['c_dir'] = 'D'
df_ramificazioni_D = df_ramificazioni_D [['Codice', 'Nome', 'Km', 'c_dir', 'cd_autostrada', 'tipo_nodo']]

# Creo elenco con S
df_ramificazioni_S = df_ramificazioni.copy()
df_ramificazioni_S['c_dir'] = 'S'
df_ramificazioni_S = df_ramificazioni_S [['Codice', 'Nome', 'Km', 'c_dir', 'cd_autostrada', 'tipo_nodo']]

# Accodo i due elenchi
df_ramificazioni = pd.concat([df_ramificazioni_D, df_ramificazioni_S], ignore_index=True)

# Rinomino le colonne
df_ramificazioni = df_ramificazioni.rename(columns={
    'Codice': 'nodo_id',
    'Nome': 'nodo_name',
    'Km': 'km',
    'c_dir' : 'direzione',
    'cd_autostrada': 'autostrada_id',
    'tipo_nodo': 'tipo_nodo'
})

################## ACCODO ##################
df = pd.concat([df_distributori, df_ramificazioni], ignore_index=True)
df_sorted = df.sort_values(by=['direzione', 'autostrada_id', 'km'])

################ OFF TOPIC ##################
################## DIM NODI ##################
# Crea cartella per i caselli se non esiste
os.makedirs("dim_nodi", exist_ok=True)
# Tengo colonne che mi servono per i nodi
df_dim_nodi = df_sorted[['nodo_id', 'nodo_name', 'tipo_nodo', 'autostrada_id', 'km']].copy()
# Rimuovo i duplicati
df_dim_nodi = df_dim_nodi.drop_duplicates(subset=['nodo_id', 'nodo_name', 'tipo_nodo', 'autostrada_id', 'km'])
# Trasforma i nomi in maiuscolo
df_dim_nodi['nodo_name'] = df_dim_nodi['nodo_name'].str.upper()

df_dim_nodi.to_csv('dim_nodi/dim_nodi.csv', index=False, header=True)

################## DIM CASELLI ##################
# Crea cartella per i caselli se non esiste
os.makedirs("dim_caselli", exist_ok=True)

# Crea elenco caselli
df_caselli = df_sorted[df_sorted['tipo_nodo'] == 'CASELLO'].copy()

# Trasforma i nomi in maiuscolo
df_caselli['nodo_name'] = df_caselli['nodo_name'].str.upper()

# Rimuove i nodo_name che contengono "ALL." o "BIVIO" ecc
df_caselli = df_caselli[~df_caselli['nodo_name'].str.contains("ALL\\.|AL\\.|ALLACCIAMENTO|BIVIO|BIV\\.|CAMBIO COMP", regex=True)]

# Ordina alfabeticamente per nome del casello
df_caselli = df_caselli.sort_values(by='nodo_name')
df_caselli.to_csv('dim_caselli/dim_caselli_partenza.csv', index=False, header=True)
df_caselli.to_csv('dim_caselli/dim_caselli_arrivo.csv', index=False, header=True)

################## LAVORO GLI D ##################
df_sorted_D = df_sorted[df_sorted['direzione'] == 'D'].copy()
df_sorted_D.reset_index(drop=True, inplace=True)  # Reimposta l'indice
df_sorted_D['indice_1'] = df_sorted_D.index
df_sorted_D['indice_2'] = df_sorted_D.index + 1

# Merge di se stessa
df_merge_D = pd.merge(df_sorted_D, df_sorted_D, left_on='indice_2', right_on='indice_1')

# Calcola la colonna 'distanza' solo se 'autostrada_id_x' è uguale a 'autostrada_id_y'
df_merge_D["distanza"] = df_merge_D.apply(
    lambda row: round(row["km_y"] - row["km_x"], 2) if row["autostrada_id_x"] == row["autostrada_id_y"] else None,
    axis=1
)
# Rimuovo le righe dove 'distanza' è None
df_merge_D = df_merge_D[df_merge_D["distanza"].notna()]

# Tengo le colonne necessarie
df_merge_D = df_merge_D[['nodo_id_x', 'nodo_name_x', 'tipo_nodo_x', 'nodo_id_y', 'nodo_name_y', 'tipo_nodo_y', 'distanza']].copy()


################## LAVORO GLI S ##################
df_sorted_S = df_sorted[df_sorted['direzione'] == 'S'].copy()
df_sorted_S = df_sorted_S.sort_values(by=['autostrada_id', 'km'], ascending=False)
df_sorted_S.reset_index(drop=True, inplace=True)  # Reimposta l'indice
df_sorted_S['indice_1'] = df_sorted_S.index
df_sorted_S['indice_2'] = df_sorted_S.index + 1

# Merge di se stessa
df_merge_S = pd.merge(df_sorted_S, df_sorted_S, left_on='indice_2', right_on='indice_1')

# Calcola la colonna 'distanza' solo se 'autostrada_id_x' è uguale a 'autostrada_id_y'
df_merge_S["distanza"] = df_merge_S.apply(
    lambda row: round(row["km_x"] - row["km_y"], 2) if row["autostrada_id_x"] == row["autostrada_id_y"] else None,
    axis=1
)
# Rimuovo le righe dove 'distanza' è None
df_merge_S = df_merge_S[df_merge_S["distanza"].notna()]

# Tengo le colonne necessarie
df_merge_S = df_merge_S[['nodo_id_x', 'nodo_name_x', 'tipo_nodo_x', 'nodo_id_y', 'nodo_name_y', 'tipo_nodo_y', 'distanza']].copy()


################## ACCODO GLI D E GLI S ##################
df_input_networkx = pd.concat([df_merge_D, df_merge_S], ignore_index=True)
df_input_networkx = df_input_networkx.rename(columns={
    'nodo_id_x': 'nodo_id_1',
    'nodo_name_x': 'nodo_name_1',
    'tipo_nodo_x': 'nodo_type_1',
    'nodo_id_y': 'nodo_id_2',
    'nodo_name_y': 'nodo_name_2',
    'tipo_nodo_y': 'nodo_type_2',
    'distanza': 'distanza'
})

# Salva il DataFrame in un file CSV
df_input_networkx.to_csv('dim_input_networkx/dim_input_networkx.csv', index=False, header=True)
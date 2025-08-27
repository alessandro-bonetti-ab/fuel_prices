import pandas as pd

# Glossario del csv veicoli --> https://www.fueleconomy.gov/feg/ws/index.shtml

# Leggo il csv veicoli
df_veicoli = pd.read_csv('veicoli/vehicles.csv', usecols=['year', 'make', 'model', 'trany', 'fuelType1', 'fuelType2', 'highway08', 'displ'])

# Crea una nuova colonna 'fuel_type' che converte i valori di 'fuelType1' in altri valori
df_veicoli['fuel_type'] = df_veicoli['fuelType1'].replace({
    'Regular Gasoline': 'BENZINA',
    'Diesel': 'DIESEL',
    'Electricity': 'ELETTRICO',
    'Premium Gasoline': 'BENZINA PREMIUM',
    'Natural Gas': 'METANO',
    'Midgrade Gasoline': 'BENZINA',
    'Hydrogen': 'IDROGENO'
})

# Tengo le righe per cui 'fuelType2' è NaN (quindi ogni veicolo ha un solo tipo di carburante)
df_veicoli = df_veicoli[df_veicoli['fuelType2'].isna()]

# Rimuovo le colonne 'fuelType1' e 'fuelType2' poiché non sono più necessarie
df_veicoli = df_veicoli.drop(columns=['fuelType1', 'fuelType2'])

# Rimuovo le righe con year < 2000 (non voglio considerare veicoli troppo vecchi)
df_veicoli = df_veicoli[df_veicoli['year'] >= 2000]

# Rimuovo le righe che hanno fuel_type uguale a 'Electricity' e 'Hydrogen' (perché non sono veicoli per cui abbiamo dati dei distributori)
df_veicoli = df_veicoli[df_veicoli['fuel_type'].isin(['ELETTRICO', 'IDROGENO']) == False]

print(df_veicoli.head())
print(df_veicoli['fuel_type'].unique())

# Raggruppa per fuel_type, 'cylinders' e calcola la media di highway08
df_media = df_veicoli.groupby(['fuel_type', 'displ'])['highway08'].mean().reset_index()

# Trasforma la media da miglia per gallone a km per litro (1 miglio = 1.60934 km, 1 gallone = 3.78541 litri, quindi 1 mpg = 1.60934 / 3.78541 km/litro)
df_media['highway08'] = round(df_media['highway08'] * 0.425144,2)
# Trsformo displ da litri a cc
df_media['displ'] = round(df_media['displ'] * 1000,0)

# Rinomina le colonne per chiarezza
df_media.columns = ['tipo_carburante', 'cilindrata(cc)', 'km/l']

# Ordina per tipo_carburante e cilindrata
df_media = df_media.sort_values(by=['tipo_carburante', 'cilindrata(cc)'])

# Salva il risultato in un nuovo CSV
df_media.to_csv('dim_carburante/consumo_medio.csv', index=False)
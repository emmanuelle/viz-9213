import pandas as pd
import geopy
from geopy.geocoders import Nominatim, ArcGIS
from utils import df_to_geojson

df = pd.read_excel('../raw_data/92-13 - Concaténation actions Porte à Porte législatives 2024.xlsx', header=1)

df['latitude'] = pd.Series(dtype='float')
df['longitude'] = pd.Series(dtype='float')


# Solve duplicates
df.loc[df['type action'] == 'Porte à porte', 'type action'] = 'Porte à Porte'
df.loc[df['type action'] == 'tractage', 'type action'] = 'Tractage'
df.loc[df['type action'] == 'tractage ', 'type action'] = 'Tractage'

geolocator = ArcGIS(user_agent='mapper')

for index, row in df.iterrows():
    if (index % 10) == 0:
        print(index)
    try:
        address = str(row['n° voie']) + ' ' + row['Type de voie'] + ' ' + row['Nom de voie (donnée extrapolée)'] + ' ' + row['Commune']
        location = geolocator.geocode(address, timeout=4)
        df.at[index, 'latitude'] = location.latitude
        df.at[index, 'longitude'] = location.longitude
    except:
        print(index, 'problem with ', row)

df['Date action'] = df['Date action'].astype(str)


df.to_excel('../raw_data/export_actions.xlsx')

columns = ['Date action', 'ID action', 'type action',
       'Commune',
       'Si action = PàP, type de logements', 'n° voie', 'Type de voie',
       'Nom de voie (donnée extrapolée)',
       'Nombre de participants']

df_pap = df.query("`type action` == 'Porte à Porte'")
df_pap = df_pap[df_pap['longitude'].notna()]
df_pap = df_pap[df_pap['longitude']!='']
gj = df_to_geojson(df_pap, columns)

with open("../raw_data/actions_campagne.geojson", 'w') as outfile:
     geojson.dump(gj, outfile)



"""
Geocoding of all addresses in Antony.

The default Nominatim geocoder only finds the coordinates for the street (same 
coordinates for all street numbers) so we use ArcGIS instead.
"""

import geopy
from geopy.geocoders import Nominatim, ArcGIS
import pandas as pd
import geojson

df_orig = pd.read_excel('original_data/liste_electeurs_antony.xlsx')

df_orig['latitude'] = pd.Series(dtype='float')
df_orig['longitude'] = pd.Series(dtype='float')

geolocator = ArcGIS(user_agent='mapper')

for index, row in df.iterrows():
    if (index % 1000) == 0:
        print(index)
    address = str(row['numéro de voie']) + ' ' + row['libellé de voie'] + ' ' + ' 92160 Antony France'
    try:
        location = geolocator.geocode(address, timeout=4)
        df_orig.at[index, 'latitude'] = location.latitude
        df_orig.at[index, 'longitude'] = location.longitude
    except:
        print(index, 'problem with %s' %address)


df_orig.to_excel('original_data/liste_electeurs_coordonnees_antony.xlsx')

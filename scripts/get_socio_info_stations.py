import pandas as pd
import geopandas as gpd
import shapely
import numpy as np

gdf = gpd.read_file('../raw_data/carreaux_geo.geojson')
stations = gpd.read_file('../raw_data/circo_contours_bvnames_results.geojson')

socio_cols = gdf.columns[6:-1]
for col in gdf.columns[6:-1]:
    stations[col] = pd.Series(dtype='float')
    stations[col] = 0

for j, station in stations.iterrows(): 
    for i, row in gdf.iterrows():
        poly = shapely.intersection(row['geometry'], station['geometry'])
        if not poly.is_empty:
            car_area = row['geometry'].area
            poly_area = poly.area
            ratio = poly_area / car_area
            stations.loc[j, socio_cols] = stations.loc[j, socio_cols] + ratio * row[socio_cols]

stations['revenu_moyen'] = stations['ind_snv'] / stations['ind']
for col in stations.columns:
    if 'men_' in col:
        stations[col+'_rel'] = stations[col] / stations['men']

stations.to_file('../raw_data/circo_contours_bvnames_filosofi+results.geojson', driver='GeoJSON')


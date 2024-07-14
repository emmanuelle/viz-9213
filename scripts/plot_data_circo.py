import geopandas as gpd
import pandas as pd

df_places = gpd.read_file('../raw_data/circo_contours.geojson')
df = pd.read_excel('../raw_data/legislatives2024_t2_9213.xlsx')

df['id_bv'] = df['Code commune'].astype(str) + '_' + df['Code BV'].astype(str)
merged = gpd.GeoDataFrame(pd.merge(df, df_places, on='id_bv'))

# Plot % of votes for Brice Gaillard
merged.plot(column=merged['% Voix/exprimés 1'].map(lambda x: float(x[:-1].replace(',', '.'))),
        legend=True,
        legend_kwds={'label':'% votes NFP'})



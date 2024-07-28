import pandas as pd

df = pd.read_excel('../raw_data/original_data/liste_electeurs_antony.xlsx')

def find_housing_type(label, number):
    if type(label) is str:
        return label
    else:
        if number >= 7:
            return 'coll'
        else:
            return 'ind'


df['estimated type'] = df.apply(lambda x: find_housing_type(x["type logement"], x["nombre d'electeurs"]), axis=1)
df['habitants en collectif'] = (df['estimated type'] == 'coll') * df["nombre d'electeurs"]

df_grouped = df[['libellé du bureau de vote', "nombre d'electeurs", "habitants en collectif"]].groupby(['libellé du bureau de vote']).sum()

df_grouped['ratio_collectif'] = df_grouped['habitants en collectif'] / df_grouped["nombre d'electeurs"]

df_grouped.reset_index(inplace=True)
df_grouped['numeroBureauVote'] = df_grouped['libellé du bureau de vote'].apply(lambda x: x[:4])

import geopandas as gpd
gdf = gpd.read_file('../raw_data/circo_contours_bvnames_results.geojson')
gdf = gdf.query("codeCommune == '92002'")
merged = gpd.GeoDataFrame(pd.merge(gdf, df_grouped, on='numeroBureauVote'))

merged.to_file('../raw_data/circo_contours_bvnames_adresses.geojson', driver='GeoJSON')

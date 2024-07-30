import pandas as pd

df = pd.read_csv('../raw_data/original_data/ListesArrêtées-com92002-15-06-2024-22h12-BV_AnneeNaissance_Sexe.csv', sep=';')
df['age'] = 2024 - df['date de naissance']
df = df.drop(columns=["date de naissance"])

# We group together the different genders
dfg = df.groupby(['libellé du bureau de vote', 'age'])[["nombre d'electeurs"]].sum()
dfg = dfg.reset_index()

def w_avg(df, values, weights):
    d = df[values]
    w = df[weights]
    return (d * w).sum() / w.sum()


dfgg = dfg.groupby(["libellé du bureau de vote"]).apply(w_avg, "age", "nombre d'electeurs")
dfgg = dfgg.reset_index()
dfgg = dfgg.rename(columns={0: "age"})

dfgg['numeroBureauVote'] = dfgg['libellé du bureau de vote'].apply(lambda x: x[:4])

import geopandas as gpd
gdf = gpd.read_file('../raw_data/circo_contours_bvnames_results.geojson')
gdf = gdf.query("codeCommune == '92002'")

merged = gpd.GeoDataFrame(pd.merge(gdf, dfgg, on='numeroBureauVote'))

merged.to_file('../raw_data/circo_contours_bvnames_age.geojson', driver='GeoJSON')

import plotly.express as px
fig = px.scatter(merged, x='age', y='vote_2024_t2_Gaillard', trendline='ols', hover_data=['libellé du bureau de vote'])
fig.show()

fig.write_html('../docs/effet_of_age.html', include_plotlyjs='cdn')

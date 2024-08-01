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
fig = px.scatter(merged, x='age', 
                 y=[
                      
                     'vote_2024_t1_Gaillard',
                     'vote_2024_t1_Bregeon',
                     'vote_2024_t1_Yvars',
                     'vote_2024_t1_Isnard',
                     'participation_2024_t1', 
                     'participation_2024_t2', 
                 ], 
                 trendline='ols', hover_data=['libellé du bureau de vote'], facet_col='variable', 
                 facet_col_wrap=3,
                 #height=500,
                 title="Vote en fonction de l'âge moyen du bureau de vote"
                )

from plotly.subplots import make_subplots
fig2 = make_subplots(cols=3, rows=2, vertical_spacing=0.22)
for i in range(6):
    fig2.add_trace(fig.data[2*i], col=i%3 + 1, row=i // 3 + 1)
    fig2.add_trace(fig.data[2*i + 1], col=i%3 + 1, row=i // 3 +1)
fig2.update_layout(annotations=fig['layout']['annotations'], showlegend=False, 
                    #height=600, 
                    template='simple_white+gridon',
                  title=fig.layout.title)
for i, annotation in enumerate(fig2['layout']['annotations']):
    if i in [0, 3, 4, 5]:
        annotation['text'] = "Vote t1 %s" %(annotation['text'].split('_')[-1])
    else:
        annotation['text'] = "Participation %s" %(annotation['text'].split('_')[-1])
fig2.update_xaxes(title_text='âge moyen', row=2)
fig2.show()

fig2.write_html('../docs/effet_age.html', include_plotlyjs='cdn')

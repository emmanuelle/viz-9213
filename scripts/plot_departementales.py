import pandas as pd
import numpy as np
import geopandas as gpd


import geojson

with open('../raw_data/circo_contours_bvnames.geojson') as f:
    gj = geojson.load(f)

gdf = gpd.read_file('../raw_data/circo_contours_bvnames_results.geojson')
gdf = pd.DataFrame(gdf[gdf.columns[:-1]])


df = pd.read_excel('../raw_data/departementales_2021_t1.xlsx')
df_canton = df[df['Code du canton'] == 1]

df_canton['Code_commune'] = '92002'
df_canton['id_bv'] = df_canton['Code_commune'].astype(str) + '_' + \
                     df_canton['Code du b.vote'].astype(str)

df_canton = pd.merge(df_canton, gdf[['id_bv', 'nomBureauVote']], on='id_bv')

number_voters = df_canton['Votants'].sum()
avg_edouard = df_canton['Unnamed: 48'].sum() / number_voters
print(avg_edouard)
avg_doyen = df_canton['Unnamed: 60'].sum() / number_voters
print(avg_doyen)

# Fig 1
df_canton['relative_edouard'] = df_canton['Unnamed: 50'] - avg_edouard * 100
df_canton['relative_doyen'] = df_canton['Unnamed: 62'] - avg_doyen * 100
df_canton['total_gauche'] = df_canton['Unnamed: 62'] + df_canton['Unnamed: 50']
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.0,
                    vertical_spacing=0.0,
                     specs=[[{"type": "scattergeo"}, 
                             {"type": "scattergeo"}, 
                             {"type": "scattergeo"}], 
                         ],
                    )

hovertemplate = "<b>%{customdata[0]}</b><br>%{z:.1f}<extra></extra>"
i = 0
fig.add_trace(go.Choropleth(locations=df_canton['id_bv'], 
                            z=df_canton['total_gauche'], geojson=gj,
                            colorscale='PuRd',
                            colorbar=dict(orientation='h', len=0.28, x=0.33*i + 0.13,
                                                  xref='paper', title='total<br>gauche',
                                                  ticks="outside",
                                                  tickvals=[19.5, 27.6, 38],
                                                  tickformat='.1f'),
                            customdata=np.dstack(df_canton['nomBureauVote']).T,
                            hovertemplate=hovertemplate,
                            featureidkey='properties.id_bv',
                            ),
              row=1, col=1)

i = 1
fig.add_trace(go.Choropleth(locations=df_canton['id_bv'], 
                            z=df_canton['Unnamed: 50'], 
                            geojson=gj,
                            colorscale='Reds',
                            colorbar=dict(orientation='h', len=0.28, x=0.33*i + 0.13,
                                                  xref='paper', 
                                                  title="Edouard<br>Huard",
                                                  ticks="outside",
                                                  tickvals=[5, 10.6, 20],
                                                  tickformat='.1f'
                            ),
                            customdata=np.dstack(df_canton['nomBureauVote']).T,
                            hovertemplate=hovertemplate,
                            featureidkey='properties.id_bv',
                            ),
              row=1, col=2)
i = 2
fig.add_trace(go.Choropleth(locations=df_canton['id_bv'], 
                            z=df_canton['Unnamed: 62'], geojson=gj,
                            colorscale='Greens',
                            colorbar=dict(orientation='h', len=0.28, x=0.33*i + 0.13,
                                                  xref='paper', 
                                                  title='Doyen<br>Formentin',
                                                  ticks="outside",
                                                  tickvals=[12, 16.9, 21.7],
                                                  tickformat='.1f'
                                                  ),
                            customdata=np.dstack(df_canton['nomBureauVote']).T,
                            hovertemplate=hovertemplate,
                            featureidkey='properties.id_bv',
                            ),
              row=1, col=3)

fig.add_annotation(text="Elections départementales 2021, canton d'Antony",
                      xref="paper", yref="paper",
                      font_size=14,
                      x=0.1, y=0.98, showarrow=False)
fig.add_annotation(text="La moyenne sur le canton est indiquée sur la colorbar",
                      xref="paper", yref="paper",
                      font_size=11,
                      x=0.1, y=0.02, showarrow=False)


fig.update_layout(margin_b=0.1, margin_t=0.1)

for trace in fig.data:
    trace.pop('coloraxis')

fig.update_geos(fitbounds="locations", projection_type='mercator')
fig.show()

fig.write_html('../docs/departementales_cartes_gauche.html', include_plotlyjs='cdn')

fig_scatter = px.scatter(df_canton, x='Unnamed: 50', y='Unnamed: 62',
                 labels={'Unnamed: 50': 'Vote Edouard/Huard', 'Unnamed: 62': 'Vote Doyen/Fromentin-Denoziere'},
                  trendline='ols', color='% Vot/Ins', hover_data=['nomBureauVote'],
                  title="Départementales 2021: corrélation entre les listes de gauche, en pourcent des votants",
                 )
fig_scatter.update_traces(marker_size=10)
fig_scatter.add_hline(y=avg_doyen * 100, line_dash="dash", line_color="gray",
        annotation_text="moyenne: %.1f" %(100*avg_doyen))
fig_scatter.add_vline(x=avg_edouard * 100, line_dash="dash", line_color="gray",
        annotation_text="moyenne: %.1f" %(100*avg_edouard))

fig_scatter.write_html('../docs/departementales_correlation_listes_gauche.html', include_plotlyjs='cdn')

fig_scatter = px.scatter(df_canton, x='Unnamed: 49', y='Unnamed: 61',
                 labels={'Unnamed: 49': "Vote Edouard/Huard (/ inscrits)", 'Unnamed: 61': 'Vote Doyen/Fromentin-Denoziere (/ inscrits)'},
                  trendline='ols', color='% Vot/Ins', hover_data=['nomBureauVote'],
                  title="Départementales 2021: corrélation entre les listes de gauche, en pourcent des inscrits",
                 )
fig_scatter.update_traces(marker_size=10)
fig_scatter.write_html('../docs/departementales_correlation_listes_gauche_inscrits.html', include_plotlyjs='cdn')

fig_scatter.show()

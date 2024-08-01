import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import geojson

gdf = gpd.read_file('../raw_data/circo_contours_bvnames_results.geojson')
df_all = pd.DataFrame(gdf[gdf.columns[:-1]])

with open('../raw_data/circo_contours_bvnames_corrected.geojson') as f:
    gj = geojson.load(f)

columns_to_plot = [col for col in df_all.columns if col.startswith('vote_2024_t1')]

# Dataset for Antony only
df_antony = df_all.query("nomCommune == 'Antony'")
gj_antony = gj.copy()
gj_antony['features'] = [feat for feat in gj['features'] 
        if feat['properties']["nomCommune"] == "Antony"]

# Dataset for Antony only
df_chatenay = df_all.query("nomCommune == 'Châtenay-Malabry'")
gj_chatenay = gj.copy()
gj_chatenay['features'] = [feat for feat in gj['features'] 
        if feat['properties']["nomCommune"] == 'Châtenay-Malabry']


# Contours communes
with open('../raw_data/contour_communes.geojson') as f:
    gj_communes = geojson.load(f)
pts = []
for poly_collection in gj_communes['coordinates']:
    for poly in poly_collection:
        pts.extend(poly)
        pts.append([None, None]) #end of polygon
lon_communes, lat_communes = zip(*pts)

clip_color_interval = True

df_agg = pd.read_excel('../raw_data/aggregated_results_circo.xlsx')
global_results = dict(df_agg.iloc[-1])

from plotly.subplots import make_subplots
n_rows, n_cols = (1, 4)

suffix_list = ['', '_antony', '_chatenay']

for index, (df, geoj) in enumerate([(df_all, gj), 
                                    (df_antony, gj_antony),
                                    (df_chatenay, gj_chatenay)]):
    suffix = suffix_list[index]
    fig = make_subplots(rows=n_rows, cols=n_cols, horizontal_spacing=0.0,
                        vertical_spacing=0.0,
                         specs=[[{"type": "scattergeo"}]*n_cols]*n_rows,
                        )
    candidate_order = {'Gaillard':0, 'Bregeon':1, 'Yvars':2, 'Isnard':3}
    cmap_dict = {'Gaillard':'Reds', 'Bregeon':'Blues', 'Yvars':'YlOrBr', 'Isnard':'Oranges'}


    for col in columns_to_plot:
        candidate_name = col.split('_')[-1]
        i = candidate_order[candidate_name]
        average = float(global_results[candidate_name + '_t1'])
        if clip_color_interval:
            quantile = 0.05
            range_color = (df[col].quantile(0.05), df[col].quantile(0.95))
        else:
            range_color = (df[col].min(), df[col].max()) 
        tickvals = [range_color[0], average, range_color[1]]
        hovertemplate = "<b>%{customdata[0]}</b><br>%{z:.1f}<extra></extra>"
        fig.add_trace(go.Choropleth(locations=df['id_bv'], z=df[col], geojson=geoj,
                                    colorscale=cmap_dict[candidate_name],
                                    colorbar=dict(orientation='h', len=0.22, x=0.25*i + 0.13,
                                                  xref='paper', title=candidate_name,
                                                  ticks="outside",
                                                  tickvals=tickvals,
                                                  tickformat='.1f'),
                                    featureidkey='properties.id_bv',
                                    customdata=np.dstack(df['nomBureauVote']).T,
                                    hovertemplate=hovertemplate
                                    ), 
                      row=i // n_cols + 1, col=i%n_cols + 1)
    fig.update_geos(fitbounds="locations", projection_type='mercator')
    fig.update_layout(template='plotly_white', margin={'l':0, 'r':0.01, 'b':0.05})

    for j in range(n_rows * n_cols):
        fig.data[j].pop('coloraxis')

    fig.add_annotation(text="Les chiffres sur la colorbar correspondent aux quantiles 0.05 et 0.95, et à la moyenne de la circo",
                      xref="paper", yref="paper",
                      x=0.1, y=0.02, showarrow=False)
    fig.write_html(f'../docs/results_circo_t1{suffix}.html', include_plotlyjs='cdn')
    if index == 0:
        for j in range(n_rows * n_cols):
            fig.add_trace(go.Scattergeo(lat=lat_communes, lon=lon_communes, hoverinfo='skip',
                                     mode='lines', line=dict(width=2, color='black'),
                                     showlegend=False),
                                     row=j // n_cols + 1, col=j % n_cols + 1)
        fig.write_html(f'../docs/results_circo_t1_contours{suffix}.html', include_plotlyjs='cdn')

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import geojson

gdf = gpd.read_file('../raw_data/circo_contours_bvnames_results.geojson')
df = pd.DataFrame(gdf[gdf.columns[:-1]])

with open('../raw_data/circo_contours_bvnames_corrected.geojson') as f:
    gj = geojson.load(f)

columns_to_plot = [col for col in df.columns 
                    if (col.startswith('vote') or col.startswith('participation'))
                    ]

# Contours communes
with open('../raw_data/contour_communes.geojson') as f:
    gj_communes = geojson.load(f)
pts = []
for poly_collection in gj_communes['coordinates']:
    for poly in poly_collection:
        pts.extend(poly)
        pts.append([None, None]) #end of polygon
lon_communes, lat_communes = zip(*pts)


for col in columns_to_plot:
    print(col)
    fig = px.choropleth(df, geojson=gj, locations='id_bv',
                               color=col,
                               color_continuous_scale='Reds',
                               #hover_name='nomBureauVote',
                               hover_data={ 'nomBureauVote': True,
                                            'id_bv':False,
                                           col:':.2f'},
                           title=f"Résultats législatives (% des votants)",
                           center={"lat": 48.77, "lon": 2.27},
                           featureidkey='properties.id_bv',
                           projection="mercator"
)
    fig.add_trace(go.Scattergeo(lat=lat_communes, lon=lon_communes, hoverinfo='skip',
                                 mode='lines', line=dict(width=3, color='black')))
    fig.update_geos(fitbounds="locations")
    fig.update_layout(template='plotly_white')
    fig.write_html(f'../docs/result_{col}.html', include_plotlyjs='cdn')

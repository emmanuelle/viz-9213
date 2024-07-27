import plotly.express as px
import pandas as pd
import geojson


df = pd.read_excel('../raw_data/legislatives2024_t2_9213.xlsx')
df['id_bv'] = df['Code commune'].astype(str) + '_' + df['Code BV'].astype(str)

with open('../raw_data/circo_contours.geojson') as f:
    gj = geojson.load(f)


fig = px.choropleth(df, geojson=gj, locations='id_bv', 
                    color='Inscrits', featureidkey='properties.id_bv')
fig.update_geos(fitbounds="locations")
fig.show()

fig = px.choropleth_mapbox(df, geojson=gj, locations='id_bv', 
                    color=df['% Voix/exprimés 1'].map(lambda x: float(x[:-1].replace(',', '.'))), 
                        featureidkey='properties.id_bv',
                          mapbox_style='open-street-map',
                          opacity=0.5,
                           zoom=11,
                           center={"lat": 48.77, "lon": 2.27},
                           height=600,
                           width=800
                          )
fig.update_geos(fitbounds="locations")
fig.show()

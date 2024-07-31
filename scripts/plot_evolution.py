import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import geojson
import numpy as np
# Custom function to make_colormap
from utils import make_colormap


## READ data
# Contours bureaux de vote
with open('../raw_data/circo_contours_bvnames_corrected.geojson') as f:
    gj = geojson.load(f)

# Contours communes
with open('../raw_data/contour_communes.geojson') as f:
    gj_communes = geojson.load(f)
pts = []
for poly_collection in gj_communes['coordinates']:
    for poly in poly_collection:
        pts.extend(poly)
        pts.append([None, None]) #end of polygon
lon_communes, lat_communes = zip(*pts)

# Dataframe
df = pd.read_csv("../raw_data/evolution_data.csv")

# Ajouter nom bureau de vote au dataframe
for idbv, nbv in zip([feat['properties']['id_bv'] for feat in gj['features']], 
                         [feat['properties']['nomBureauVote'] for feat in gj['features']]):
    df.loc[df['id_bv']==idbv, 'nom_bv'] = nbv


## Evolution europeennes vers premier tour des legislatives
code_dict = {'NFP': {'label_abs': 'Nb de voix en plus pour le NFP',
                     'titre': 'du vote NFP',
                     'cscale': 'RdBu_r',
                     'midpoint': 0},
             'LREM': {'label_abs': 'Nb de voix en plus pour LREM',
                      'titre': 'du vote LREM',
                      'cscale': 'Blues',
                      'midpoint': None},
             'LR': {'label_abs': 'Nb de voix en plus pour LR',
                      'titre': 'du vote LR',
                      'cscale': 'RdBu',
                      'midpoint': 0},
             'LR+LREM': {'label_abs': 'Nb de voix en plus pour LR et LREM',
                         'titre': 'du vote LR + LREM',
                         'cscale': 'Blues',
                         'midpoint': None},
             'RN': {'label_abs': 'Nb de voix en plus pour le RN',
                    'titre': 'du vote RN',
                    'cscale': 'Earth',
                    'midpoint': 0,
                    'cmap_method': 'minmax'},
             'Reqt': {'label_abs': 'Nb de voix en plus pour Reconquête',
                      'titre': 'du vote Reconquête',
                      'cscale': 'gray',
                      'midpoint': None},
             'EXD': {'label_abs': "Nb de voix en plus pour l'EXD",
                     'titre': "du vote d'extrême droite",
                     'cscale': 'RdBu',
                     'midpoint': 0},
             'Blancs': {'label_abs': "Nb de blancs en plus",
                        'titre': "du vote blanc",
                        'cscale': 'PuOr',
                        'midpoint': 0},
             'Participation': {'label_abs': "Nb de votes en plus",
                               'titre': "de la participation",
                               'cscale': 'Greys',
                               'midpoint': None},
             }


for code, code_values in code_dict.items():
    colname = f'evolution_{code}_eur_t1_pct'
    if code_values['midpoint'] == 0:
        cmap_method = 'quantile' if 'cmap_method' not in code_values.keys() else code_values['cmap_method']
        cmap, color_range = make_colormap(df[colname], method=cmap_method)
    else:
        cmap, color_range = code_values['cscale'], None
    fig = px.choropleth_mapbox(df, geojson=gj, locations='id_bv', 
                               color=colname,
                               color_continuous_scale=cmap,
                               color_continuous_midpoint=code_values['midpoint'],
                               mapbox_style='open-street-map',
                               hover_name='nom_bv',
                               hover_data={f'evolution_{code}_eur_t1_abs': True,
                                           'id_bv': False,
                                           f'evolution_{code}_eur_t1_pct':':.2f'},
                           labels={f'evolution_{code}_eur_t1_abs': code_values['label_abs'],
                                   'id_bv': False, 
                                   f'evolution_{code}_eur_t1_pct': f"En pourcentage d'inscrits"},
                           title=f"Évolution {code_values['titre']} (Européennes vers premier tour des législatives)",
                           opacity=0.5,
                           zoom=11,
                           center={"lat": 48.77, "lon": 2.27},
                           # height=600,
                           # width=800,
                           featureidkey='properties.id_bv')
    fig.update_geos(fitbounds="locations")
    # Ajouter les contours des communes
    fig.update_layout(mapbox_layers=[{
        "below": 'traces',
        "sourcetype": "geojson",
        "type": "line",
        "line": {"width": 3},
        "color": "black",
        "source": gj_communes
    }])
    if color_range is not None:
        fig.update_layout(coloraxis=dict(cmin=color_range[0], cmax=color_range[1]))
    fig.write_html(f'../docs/evolution_{code}_euros_t1_2024.html', include_plotlyjs='cdn')

    fig2 = px.choropleth(df, geojson=gj, locations='id_bv',
                               color=colname,
                               color_continuous_scale=cmap,
                               hover_name='nom_bv',
                               hover_data={f'evolution_{code}_eur_t1_abs': True,
                                           'id_bv': False,
                                           f'evolution_{code}_eur_t1_pct':':.2f'},
                           title=f"Évolution (Européennes vers premier tour des législatives)",
                           center={"lat": 48.77, "lon": 2.27},
                           featureidkey='properties.id_bv',
                           projection="mercator"
)
    fig2.add_trace(go.Scattergeo(lat=lat_communes, lon=lon_communes, 
                                 mode='lines', line=dict(width=3, color='black')))
    fig2.update_geos(fitbounds="locations")
    fig2.update_layout(template='plotly_white')
    if color_range is not None:
        fig2.update_layout(coloraxis=dict(cmin=color_range[0], cmax=color_range[1]))
    fig2.write_html(f'../docs/evolution_{code}_euros_t1_2024_simple.html', include_plotlyjs='cdn')



## Evolution premier vers deuxieme tour des legislatives
code_dict = {'Gaillard': {'label_abs': 'Nb de voix en plus pour Gaillard',
                     'titre': 'du vote Gaillard',
                     'cscale': 'RdBu_r',
                     'midpoint': 0},
             'Bregeon': {'label_abs': 'Nb de voix en plus pour Bregeon',
                      'titre': 'du vote Bregeon',
                      'cscale': 'Blues',
                      'midpoint': None},
             'BregeonIsnard': {'label_abs': 'Nb de voix en plus pour Bregeon que pour Bregeon+Isnard',
                    'titre': 'du vote LREM+LR',
                    'cscale': 'RdBu',
                    'midpoint': 0,
                    'cmap_method': 'minmax'},
             'Blancs': {'label_abs': "Nb de blancs en plus",
                        'titre': "du vote blanc",
                        'cscale': 'Greys',
                        'midpoint': None},
             'Participation': {'label_abs': "Nb de votes en plus",
                               'titre': "de la participation",
                               'cscale': 'PuOr',
                               'midpoint': 0,
                               'cmap_method': 'minmax'},
             }


for code, code_values in code_dict.items():
    colname = f'evolution_{code}_t1_t2_pct'
    if code_values['midpoint'] == 0:
        cmap_method = 'quantile' if 'cmap_method' not in code_values.keys() else code_values['cmap_method']
        cmap, color_range = make_colormap(df[colname], method=cmap_method)
    else:
        cmap, color_range = code_values['cscale'], None
    fig = px.choropleth_mapbox(df, geojson=gj, locations='id_bv', 
                               color=colname,
                               color_continuous_scale=cmap,
                               color_continuous_midpoint=code_values['midpoint'],
                               mapbox_style='open-street-map',
                               hover_name='nom_bv',
                               hover_data={f'evolution_{code}_t1_t2_abs': True,
                                           'id_bv': False,
                                           f'evolution_{code}_t1_t2_pct':':.2f'},
                           labels={f'evolution_{code}_t1_t2_abs': code_values['label_abs'],
                                   'id_bv': False, 
                                   f'evolution_{code}_t1_t2_pct': f"En pourcentage d'inscrits"},
                           title=f"Évolution {code_values['titre']} (Premier vers deuxième tour des législatives)",
                           opacity=0.5,
                           zoom=11,
                           center={"lat": 48.77, "lon": 2.27},
                           featureidkey='properties.id_bv')
    fig.update_geos(fitbounds="locations")
    if color_range is not None:
        fig.update_layout(coloraxis=dict(cmin=color_range[0], cmax=color_range[1]))
    # Ajouter les contours des communes
    fig.update_layout(mapbox_layers=[{
        "below": 'traces',
        "sourcetype": "geojson",
        "type": "line",
        "line": {"width": 3},
        "color": "black",
        "source": gj_communes
    }])
    fig.write_html(f'../docs/evolution_{code}_t1_t2_2024.html', include_plotlyjs='cdn')
    # Now simple choropleth
    fig2 = px.choropleth(df, geojson=gj, locations='id_bv',
                               color=colname,
                               color_continuous_scale=cmap,
                               hover_name='nom_bv',
                               hover_data={f'evolution_{code}_t1_t2_abs': True,
                                           'id_bv': False,
                                           f'evolution_{code}_t1_t2_pct':':.2f'},
                           labels={f'evolution_{code}_t1_t2_abs': code_values['label_abs'],
                                   'id_bv': False, 
                                   f'evolution_{code}_t1_t2_pct': f"En pourcentage d'inscrits"},
                           title=f"Évolution {code_values['titre']} (Premier vers deuxième tour des législatives)",
                           center={"lat": 48.77, "lon": 2.27},
                           featureidkey='properties.id_bv',
                           projection="mercator"
)
    fig2.add_trace(go.Scattergeo(lat=lat_communes, lon=lon_communes, 
                                 mode='lines', line=dict(width=3, color='black')))
    fig2.update_geos(fitbounds="locations")
    fig2.update_layout(template='plotly_white')
    if color_range is not None:
        fig2.update_layout(coloraxis=dict(cmin=color_range[0], cmax=color_range[1]))
    fig2.write_html(f'../docs/evolution_{code}_t1_t2_2024_simple.html', include_plotlyjs='cdn')

    

import plotly.express as px
import pandas as pd
import geojson

def format_series(s):
    return float(s[:-1].replace(',', '.'))

with open('../raw_data/circo_contours.geojson') as f:
    gj = geojson.load(f)

bv_names = pd.read_excel('../raw_data/noms_bureaux_votes.xlsx').rename(columns={'Unnamed: 0': 'Code'})
dict_bv_names = dict(zip(bv_names.Code, bv_names.names))

## Add 2024 T1
df = pd.read_excel('../raw_data/legislatives2024_t1_9213.xlsx')
df['id_bv'] = df['Code commune'].astype(str) + '_' + df['Code BV'].astype(str)
for feat in gj['features']:
    feat['properties']['vote_2024_t1_Gaillard'] = format_series(df[df['id_bv']==feat['properties']['id_bv']]['% Voix/exprimés 2'].iloc[0])
    feat['properties']['vote_2024_t1_Isnard'] = format_series(df[df['id_bv']==feat['properties']['id_bv']]['% Voix/exprimés 3'].iloc[0])
    feat['properties']['vote_2024_t1_Bregeon'] = format_series(df[df['id_bv']==feat['properties']['id_bv']]['% Voix/exprimés 4'].iloc[0])
    feat['properties']['vote_2024_t1_Yvars'] = format_series(df[df['id_bv']==feat['properties']['id_bv']]['% Voix/exprimés 6'].iloc[0])
    feat['properties']['participation_2024_t1'] = format_series(df[df['id_bv']==feat['properties']['id_bv']]['% Votants'].iloc[0])


## Add 2024 T2
df = pd.read_excel('../raw_data/legislatives2024_t2_9213.xlsx')
df['id_bv'] = df['Code commune'].astype(str) + '_' + df['Code BV'].astype(str)

for feat in gj['features']:
    feat['properties']['nomBureauVote'] = dict_bv_names[feat['properties']['id_bv']]
    feat['properties']['vote_2024_t2_Gaillard'] = format_series(df[df['id_bv']==feat['properties']['id_bv']]['% Voix/exprimés 1'].iloc[0])
    feat['properties']['participation_2024_t2'] = format_series(df[df['id_bv']==feat['properties']['id_bv']]['% Votants'].iloc[0][:-1].replace(',', '.'))

with open("../raw_data/circo_contours_bvnames_results.geojson", 'w') as outfile:
     geojson.dump(gj, outfile)

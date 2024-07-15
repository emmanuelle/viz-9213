import plotly.express as px
import pandas as pd
import geojson


df = pd.read_excel('../raw_data/legislatives2024_t2_9213.xlsx')
df['id_bv'] = df['Code commune'].astype(str) + '_' + df['Code BV'].astype(str)

with open('../raw_data/circo_contours.geojson') as f:
    gj = geojson.load(f)

bv_names = pd.read_excel('../raw_data/noms_bureaux_votes.xlsx').rename(columns={'Unnamed: 0': 'Code'})
dict_bv_names = dict(zip(bv_names.Code, bv_names.names))

for feat in gj['features']:
    feat['properties']['nomBureauVote'] = dict_bv_names[feat['properties']['id_bv']]
    feat['properties']['voteNFP_2024_t2'] = float(df[df['id_bv']==feat['properties']['id_bv']]['% Voix/exprimés 1'].iloc[0][:-1].replace(',', '.'))

with open("../raw_data/circo_contours_bvnames_results.geojson", 'w') as outfile:
     geojson.dump(gj, outfile)

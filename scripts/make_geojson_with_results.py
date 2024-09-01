import plotly.express as px
import pandas as pd
import geojson

def format_series(s):
    return float(s[:-1].replace(',', '.'))

with open('../raw_data/circo_contours_bvnames_corrected.geojson') as f:
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


# Europeennes
df = pd.read_excel('../raw_data/europeennes_2024.xlsx')
parties = {4:'Aubry', 6:'Toussaint', 3:'Maréchal', 18:'Bellamy', 11:'Hayer', 27: 'Glucksmann', 5:'Bardella', 33:'Deffontaines'}

df['id_bv'] = df['Code commune'].astype(str) + '_' + df['Code BV'].astype(str)

for feat in gj['features']:
    for party in parties.values():
        feat['properties']['vote_2024_euro_%s' %party] = df[df['id_bv']==feat['properties']['id_bv']][party].iloc[0]
    feat['properties']['participation_2024_euro'] = format_series(df[df['id_bv']==feat['properties']['id_bv']]['% Votants'].iloc[0][:-1].replace(',', '.'))

# Municipales 2020
df = pd.read_excel('../raw_data/municipales_2020_t1_antony.xlsx')

parties = {'Senant':'', 'Aschehoug':'.1', 'Lajeunie':'.2', 'Desbois':'.3'}
df['id_bv'] = '92002' + '_' + df['Code B.Vote'].astype(str)

for feat in gj['features']:
    if feat['properties']['nomCommune'] == 'Antony':
        for party, code in parties.items():
            feat['properties']['vote_2020_muni_%s' %party] = float(df[df['id_bv']==feat['properties']['id_bv']]['% Voix/Exp' + code].iloc[0])
        feat['properties']['participation_2020_muni'] = float(df[df['id_bv']==feat['properties']['id_bv']]['% Exp/Ins'].iloc[0])

# Municipales 2014
df = pd.read_excel('../raw_data/municipales_2014_t1_antony.xlsx')
df['id_bv'] = '92002' + '_' + df['No bureau vote'].astype(str).str.lstrip('0')
parties = ['SÉNANT', 'MEUNIER', 'RIVET', 'BUGAT']

for feat in gj['features']:
    if feat['properties']['nomCommune'] == 'Antony':
        for party in parties:
            row = df[(df['id_bv']==feat['properties']['id_bv']) & (df['Nom'] == party)].iloc[0]
            feat['properties']['vote_2014_muni_%s' %party] = float(100 * row['Voix'] / row['Exprimés'])
        # All candidate lines have the same info for Inscrits / exprimes
        feat['properties']['participation_2014_muni'] = float(100 * row['Exprimés'] / row['Inscrits'])      

# Now save results
with open("../raw_data/circo_contours_bvnames_results.geojson", 'w') as outfile:
     geojson.dump(gj, outfile)

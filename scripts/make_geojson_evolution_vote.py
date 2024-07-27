import pandas as pd
import geojson


## Read premier tour 2024
df = pd.read_excel('../raw_data/legislatives2024_t1_9213.xlsx')
df['id_bv'] = df['Code commune'].astype(str) + '_' + df['Code BV'].astype(str)

nb_voix_t1_dict = {}
# Initialisation avec les noms des 7 candidat-es comme clés
for idx in range(1, 8):
    nb_voix_t1_dict[df.loc[0, 'Nom candidat %d'%idx]] = {}

# Ajout du nombre de voix par BV
for bv_idx, bv in df.iterrows():
    for idx in range(1, 8): 
        nb_voix_t1_dict[bv['Nom candidat %d' % idx]][bv['id_bv']] = bv['Voix %d' % idx]


## Read deuxième tour 2024
df = pd.read_excel('../raw_data/legislatives2024_t2_9213.xlsx')
df['id_bv'] = df['Code commune'].astype(str) + '_' + df['Code BV'].astype(str)

nb_voix_t2_dict = {}
# Initialisation avec les noms des 2 candidat-es comme clés
for idx in range(1, 3):
    nb_voix_t2_dict[df.loc[0, 'Nom candidat %d'%idx]] = {}

# Ajout du nombre de voix par BV
for bv_idx, bv in df.iterrows():
    for idx in range(1, 3): 
        nb_voix_t2_dict[bv['Nom candidat %d' % idx]][bv['id_bv']] = bv['Voix %d' % idx]


# Read Europeennes
df = pd.read_excel('../raw_data/europeennes_2024.xlsx')
df['id_bv'] = df['Code commune'].astype(str) + '_' + df['Code BV'].astype(str)

tetes_de_liste_europeennes = {3: "MARECHAL", 
                              4: "AUBRY", 
                              5: "BARDELLA",
                              6: "TOUSSAINT", 
                              11: "HAYER", 
                              18: "BELLAMY",
                              27: "GLUCKSMANN",
                              33: "DEFFONTAINES"}

nb_voix_europeennes_dict = {}
# Initialisation avec les noms des tetes des principales listes comme clés
for idx, candidate in tetes_de_liste_europeennes.items():
    nb_voix_europeennes_dict[candidate] = {}

# Ajout du nombre de voix par BV
for bv_idx, bv in df.iterrows():
    for idx, candidate in tetes_de_liste_europeennes.items():
        nb_voix_europeennes_dict[candidate][bv['id_bv']] = bv['Voix %d' % idx]

# Nombre d'inscrits par bureau
nb_inscrits_dict = {}
for bv_idx, bv in df.iterrows():
    nb_inscrits_dict[bv['id_bv']] = bv['Inscrits']


## Open geojson file
with open('../raw_data/circo_contours_bvnames_corrected.geojson') as f:
    gj = geojson.load(f)

bv_names = pd.read_excel('../raw_data/noms_bureaux_votes.xlsx').rename(columns={'Unnamed: 0': 'Code'})
dict_bv_names = dict(zip(bv_names.Code, bv_names.names)) # key: code, value: name

## Ajout des infos au geojson
for feat in gj['features']:
    idbv = feat['properties']['id_bv']
    
    nb_inscrits = nb_inscrits_dict[idbv]
    feat['properties']['nb_inscrits'] = nb_inscrits_dict[idbv]
    
    evol_gaillard = nb_voix_t2_dict['GAILLARD'][idbv] - nb_voix_t1_dict['GAILLARD'][idbv]
    feat['properties']['evolution_Gaillard_t1_t2_abs'] = evol_gaillard
    feat['properties']['evolution_Gaillard_t1_t2_pct'] = "%.2f" % ((evol_gaillard/nb_inscrits)*100)

    evol_bregeon = nb_voix_t2_dict['BREGEON'][idbv] - nb_voix_t1_dict['BREGEON'][idbv]
    feat['properties']['evolution_Bregeon_t1_t2_abs'] = evol_bregeon
    feat['properties']['evolution_Bregeon_t1_t2_pct'] = "%.2f" % ((evol_bregeon/nb_inscrits)*100)

    
    evol_bregeon_lr = nb_voix_t2_dict['BREGEON'][idbv] - (nb_voix_t1_dict['BREGEON'][idbv] + \
                                                          nb_voix_t1_dict['ISNARD'][idbv])
    feat['properties']['evolution_Bregeon+LR_t1_t2_abs'] = evol_bregeon_lr
    feat['properties']['evolution_Bregeon+LR_t1_t2_pct'] = "%.2f" % ((evol_bregeon_lr/nb_inscrits)*100) 

with open("../raw_data/evolution_t1_t2.geojson", 'w') as outfile:
     geojson.dump(gj, outfile)

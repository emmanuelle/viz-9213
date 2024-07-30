import pandas as pd

### Read data and store in dictionaries

## Read premier tour 2024
df = pd.read_excel('../raw_data/legislatives2024_t1_9213.xlsx')
df['id_bv'] = df['Code commune'].astype(str) + '_' + df['Code BV'].astype(str)

nb_voix_t1_dict = {}

# Initialisation avec les noms des 7 candidat-es comme clés
for idx in range(1, 8):
    nb_voix_t1_dict[df.loc[0, 'Nom candidat %d'%idx]] = {}
nb_voix_t1_dict['Votants'] = {}
nb_voix_t1_dict['Blancs'] = {}
nb_voix_t1_dict['Nuls'] = {}
nb_voix_t1_dict['Inscrits'] = {}

# Ajout du nombre de voix et votants par BV
for bv_idx, bv in df.iterrows():
    nb_voix_t1_dict['Votants'][bv['id_bv']] = bv['Votants']
    nb_voix_t1_dict['Blancs'][bv['id_bv']] = bv['Blancs']
    nb_voix_t1_dict['Nuls'][bv['id_bv']] = bv['Nuls']
    nb_voix_t1_dict['Inscrits'][bv['id_bv']] = bv['Inscrits']
    for idx in range(1, 8): 
        nb_voix_t1_dict[bv['Nom candidat %d' % idx]][bv['id_bv']] = bv['Voix %d' % idx]

## Read deuxième tour 2024
df = pd.read_excel('../raw_data/legislatives2024_t2_9213.xlsx')
df['id_bv'] = df['Code commune'].astype(str) + '_' + df['Code BV'].astype(str)

nb_voix_t2_dict = {}

# Initialisation avec les noms des 2 candidat-es comme clés
for idx in range(1, 3):
    nb_voix_t2_dict[df.loc[0, 'Nom candidat %d'%idx]] = {}
nb_voix_t2_dict['Votants'] = {}
nb_voix_t2_dict['Blancs'] = {}
nb_voix_t2_dict['Nuls'] = {}
nb_voix_t2_dict['Inscrits'] = {}

# Ajout du nombre de voix par BV
for bv_idx, bv in df.iterrows():
    nb_voix_t2_dict['Votants'][bv['id_bv']] = bv['Votants']
    nb_voix_t2_dict['Blancs'][bv['id_bv']] = bv['Blancs']
    nb_voix_t2_dict['Nuls'][bv['id_bv']] = bv['Nuls']
    nb_voix_t2_dict['Inscrits'][bv['id_bv']] = bv['Inscrits']
    for idx in range(1, 3): 
        nb_voix_t2_dict[bv['Nom candidat %d' % idx]][bv['id_bv']] = bv['Voix %d' % idx]

## Read Europeennes
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
nb_voix_europeennes_dict['Votants'] = {}
nb_voix_europeennes_dict['Blancs'] = {}
nb_voix_europeennes_dict['Nuls'] = {}
nb_voix_europeennes_dict['Inscrits'] = {}

# Ajout du nombre de voix par BV
for bv_idx, bv in df.iterrows():    
    nb_voix_europeennes_dict['Votants'][bv['id_bv']] = bv['Votants']
    nb_voix_europeennes_dict['Blancs'][bv['id_bv']] = bv['Blancs']
    nb_voix_europeennes_dict['Nuls'][bv['id_bv']] = bv['Nuls']
    nb_voix_europeennes_dict['Inscrits'][bv['id_bv']] = bv['Inscrits']
    for idx, candidate in tetes_de_liste_europeennes.items():
        nb_voix_europeennes_dict[candidate][bv['id_bv']] = bv['Voix %d' % idx]


### Create dataframe with relevant data
new_df = df[['Code commune', 'Libellé commune', 'Code BV', 'id_bv']].copy()

## Comptes absolus
for key, val in nb_voix_europeennes_dict.items():
    new_df.loc[:, ('%s_eur' % key)] = [val[idbv] for idbv in new_df['id_bv']]

for key, val in nb_voix_t1_dict.items():
    new_df.loc[:, ('%s_t1' % key)] = [val[idbv] for idbv in new_df['id_bv']]
    
for key, val in nb_voix_t2_dict.items():
    new_df.loc[:, ('%s_t2' % key)] = [val[idbv] for idbv in new_df['id_bv']]

## Evolution entre tour 1 et tour 2
new_df.loc[:, 'evolution_Gaillard_t1_t2_abs'] = new_df["GAILLARD_t2"] - new_df["GAILLARD_t1"]
new_df.loc[:, 'evolution_Gaillard_t1_t2_pct'] = new_df['evolution_Gaillard_t1_t2_abs'] / new_df["Inscrits_eur"]*100

new_df.loc[:, 'evolution_Bregeon_t1_t2_abs'] = new_df["BREGEON_t2"] - new_df["BREGEON_t1"]
new_df.loc[:, 'evolution_Bregeon_t1_t2_pct'] = new_df['evolution_Bregeon_t1_t2_abs'] / new_df["Inscrits_eur"]*100

new_df.loc[:, 'evolution_Participation_t1_t2_abs'] = new_df["Votants_t2"] - new_df["Votants_t1"]
new_df.loc[:, 'evolution_Participation_t1_t2_pct'] = new_df['evolution_Participation_t1_t2_abs'] / new_df["Inscrits_eur"]*100

new_df.loc[:, 'evolution_Blancs_t1_t2_abs'] = new_df["Blancs_t2"] - new_df["Blancs_t1"]
new_df.loc[:, 'evolution_Blancs_t1_t2_pct'] = new_df['evolution_Blancs_t1_t2_abs'] / new_df["Inscrits_eur"]*100

new_df.loc[:, 'evolution_BregeonIsnard_t1_t2_abs'] = new_df["BREGEON_t2"] - (new_df["BREGEON_t1"] + new_df["ISNARD_t1"])
new_df.loc[:, 'evolution_BregeonIsnard_t1_t2_pct'] = new_df['evolution_BregeonIsnard_t1_t2_abs'] / new_df["Inscrits_eur"]*100

## Evolution entre européennes et tour 1
new_df.loc[:, 'evolution_NFP_eur_t1_abs'] = new_df["GAILLARD_t1"] - (new_df["AUBRY_eur"] + \
                                                                     new_df["TOUSSAINT_eur"] + \
                                                                     new_df["GLUCKSMANN_eur"] + \
                                                                     new_df["DEFFONTAINES_eur"])
new_df.loc[:, 'evolution_NFP_eur_t1_pct'] = new_df['evolution_NFP_eur_t1_abs'] / new_df["Inscrits_eur"]*100

new_df.loc[:, 'evolution_LREM_eur_t1_abs'] = new_df["BREGEON_t1"] - new_df["HAYER_eur"]
new_df.loc[:, 'evolution_LREM_eur_t1_pct'] = new_df['evolution_LREM_eur_t1_abs'] / new_df["Inscrits_eur"]*100

new_df.loc[:, 'evolution_LR_eur_t1_abs'] = new_df["ISNARD_t1"] - new_df["BELLAMY_eur"]
new_df.loc[:, 'evolution_LR_eur_t1_pct'] = new_df['evolution_LR_eur_t1_abs'] / new_df["Inscrits_eur"]*100

new_df.loc[:, 'evolution_LR+LREM_eur_t1_abs'] = (new_df.loc[:, 'evolution_LR_eur_t1_abs'] + \
                                                 new_df.loc[:, 'evolution_LREM_eur_t1_abs'])
new_df.loc[:, 'evolution_LR+LREM_eur_t1_pct'] = new_df['evolution_LR+LREM_eur_t1_abs'] / new_df["Inscrits_eur"]*100

new_df.loc[:, 'evolution_RN_eur_t1_abs'] = new_df["YVARS_t1"] - new_df["BARDELLA_eur"]
new_df.loc[:, 'evolution_RN_eur_t1_pct'] = new_df['evolution_RN_eur_t1_abs'] / new_df["Inscrits_eur"]*100

new_df.loc[:, 'evolution_Reqt_eur_t1_abs'] = new_df["PRETO_t1"] - new_df["MARECHAL_eur"]
new_df.loc[:, 'evolution_Reqt_eur_t1_pct'] = new_df['evolution_Reqt_eur_t1_abs'] / new_df["Inscrits_eur"]*100

new_df.loc[:, 'evolution_EXD_eur_t1_abs'] = new_df["evolution_RN_eur_t1_abs"] + new_df["evolution_Reqt_eur_t1_abs"]
new_df.loc[:, 'evolution_EXD_eur_t1_pct'] = new_df['evolution_EXD_eur_t1_abs'] / new_df["Inscrits_eur"]*100

new_df.loc[:, 'evolution_Participation_eur_t1_abs'] = new_df["Votants_t1"] - new_df["Votants_eur"]
new_df.loc[:, 'evolution_Participation_eur_t1_pct'] = new_df['evolution_Participation_eur_t1_abs'] / new_df["Inscrits_eur"]*100

new_df.loc[:, 'evolution_Blancs_eur_t1_abs'] = new_df["Blancs_t1"] - new_df["Blancs_eur"]
new_df.loc[:, 'evolution_Blancs_eur_t1_pct'] = new_df['evolution_Blancs_eur_t1_abs'] / new_df["Inscrits_eur"]*100

new_df.to_csv("../raw_data/evolution_data.csv")



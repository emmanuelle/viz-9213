import pandas as pd

# Data from https://www.data.gouv.fr/fr/datasets/elections-legislatives-des-30-juin-et-7-juillet-2024-resultats-definitifs-du-2nd-tour/
df = pd.read_excel('resultats-definitifs-par-bureau-de-vote.xlsx')
df_circo = df[df['Code commune'].isin(['92019', '92014', '92071', '92002'])]
df_circo.to_excel('legislatives2024_t2_9213.xlsx')

# Data from https://www.data.gouv.fr/fr/datasets/elections-legislatives-des-30-juin-et-7-juillet-2024-resultats-definitifs-du-1er-tour/
df = pd.read_excel('resultats-provisoires-par-bureau-de-votevmn.xlsx')
df_circo = df[df['Code commune'].isin(['92019', '92014', '92071', '92002'])]
df_circo.to_excel('legislatives2024_t1_9213.xlsx')

# Data from https://public.opendatasoft.com/explore/dataset/elections-france-legislatives-2022-2nd-tour-par-bureau-de-vote/export/?flg=fr-fr
df = pd.read_excel('elections-france-legislatives-2022-2nd-tour-par-bureau-de-vote.xlsx')
df_circo = df[df['Code de la commune'].isin(['92019', '92014', '92071', '92002'])]
df_circo['id_bv'] = df_circo['Code de la commune'] + '_' + df_circo['Code du b.vote']
df_circo.to_excel('legislatives2022_t2_9213.xlsx')

dict_bv_names = dict(zip(df_circo.id_bv,
                         df_circo['Libellé du bureau de vote']))
df_bv = pd.DataFrame.from_dict(dict_bv_names, orient='index',
                               columns=['names'])
df_bv.to_excel('noms_bureaux_votes.xlsx')


# Departementales
# Data from https://www.data.gouv.fr/fr/datasets/elections-departementales-2021-resultats-du-1er-tour/

df = pd.read_excel('original_data/resultats-par-niveau-burvot-t1-france-entiere.xlsx')
df['Code_commune'] = df['Code du département'].astype(str) + '_' + df['Code de la commune'].astype(str).map(lambda x: x.zfill(3))
df_circo = df[df['Code_commune'].isin(['92_019', '92_014', '92_071', '92_002'])]

df_circo.to_excel('departementales_2021_t1.xlsx')

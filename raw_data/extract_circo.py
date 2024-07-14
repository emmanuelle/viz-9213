import pandas as pd

# Data from https://www.data.gouv.fr/fr/datasets/elections-legislatives-des-30-juin-et-7-juillet-2024-resultats-definitifs-du-2nd-tour/
df = pd.read_excel('resultats-definitifs-par-bureau-de-vote.xlsx')
df_circo = df[df['Code commune'].isin(['92019', '92014', '92071', '92002'])]
df_circo.to_excel('legislatives2024_t2_9213.xlsx')

# Data from https://www.data.gouv.fr/fr/datasets/elections-legislatives-des-30-juin-et-7-juillet-2024-resultats-definitifs-du-1er-tour/
df = pd.read_excel('resultats-provisoires-par-bureau-de-votevmn.xlsx')
df_circo = df[df['Code commune'].isin(['92019', '92014', '92071', '92002'])]
df_circo.to_excel('legislatives2024_t1_9213.xlsx')

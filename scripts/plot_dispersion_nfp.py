import pandas as pd


df = pd.read_excel('../raw_data/original_data/resultats-definitifs-par-bureau-de-vote.xlsx')

df['Nuance candidat 2'].fillna('no', inplace=True)
df['Nuance candidat 3'].fillna('no', inplace=True)

df['Nuances'] = list(zip(df['Nuance candidat 1'], df['Nuance candidat 2'], df['Nuance candidat 3']))


df_UG_ENS = df[df['Nuances'].isin([('UG', 'ENS', 'no'), ('ENS', 'UG', 'no'), 
                                   ('UG', 'LR', 'no'), ('LR', 'UG', 'no'), 
                                   ('HOR', 'UG', 'no'), ('UG', 'HOR', 'no'),
                                   ('UG', 'UDI', 'no'), ('UDI', 'UG', 'no'),
                                   ('UG', 'DVD', 'no'), ('DVD', 'UG', 'no'),
                                  ])]


def select_gauche(score_1, score_2, nuance_1, nuance_2):
    return score_1 if nuance_1 == 'UG' else score_2


def select_candidat_gauche(name_1, name_2, nuance_1, nuance_2):
    return name_1 + '/' + name_2 if nuance_1 == 'UG' else name_2 + '/' + name_1


df_UG_ENS['candidat'] = [select_candidat_gauche(*a) for a in tuple(zip(df_UG_ENS["Nom candidat 1"], df_UG_ENS["Nom candidat 2"], 
                                                                  df_UG_ENS["Nuance candidat 1"], df_UG_ENS["Nuance candidat 2"]))]


df_UG_ENS['score_gauche'] = [select_gauche(*a) for a in tuple(zip(df_UG_ENS["% Voix/exprimés 1"], df_UG_ENS["% Voix/exprimés 2"], 
                                                                  df_UG_ENS["Nuance candidat 1"], df_UG_ENS["Nuance candidat 2"]))]


df_UG_ENS = df_UG_ENS[df['Code département'] != 'ZZ']



def format_series(s):
    """
    Replace '35,2%' by 35.2 (type float) to manipulate numbers instead of str
    """
    return float(s[:-1].replace(',', '.'))


df_UG_ENS['score NFP'] = df_UG_ENS['score_gauche'].map(format_series)

df_UG_ENS['is_gaillard'] = (df_UG_ENS['candidat'] == 'GAILLARD/BREGEON').astype(int)


import plotly.express as px

fig = px.violin(df_UG_ENS.query("`Code département` == '92'"), x='candidat', y='score NFP', color='is_gaillard',
                #color='Code département',
                points='all',
                violinmode='overlay',
                color_discrete_sequence=[px.colors.qualitative.Plotly[1], px.colors.qualitative.Plotly[0]],
                height=420,
                title='Législatives 2024 2e tour, Hauts-de-Seine'
               )
fig.update_traces(jitter=0.5)
fig.update_layout(showlegend=False, xaxis_title=None)
fig.update_yaxes(
    range=(0, 100))
fig.write_image('violin_nfp_results.png')
fig.show()

fig = px.box(df_UG_ENS.query("`Code département` == '92'"), x='candidat', y='score NFP', color='is_gaillard',
                #color='Code département',
                points='all',
                boxmode='overlay',
                color_discrete_sequence=[px.colors.qualitative.Plotly[1], px.colors.qualitative.Plotly[0]],
                height=420,
                title='Législatives 2024 2e tour, Hauts-de-Seine'
               )
fig.update_traces(jitter=0.5)
fig.update_layout(showlegend=False, xaxis_title=None)
fig.update_yaxes(
    range=(0, 100))
fig.write_image('box_nfp_results.png')
fig.show()





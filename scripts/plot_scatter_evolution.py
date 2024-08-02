import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import geojson
import numpy as np


## READ data
# Contours bureaux de vote
with open('../raw_data/circo_contours_bvnames_corrected.geojson') as f:
    gj = geojson.load(f)

# Dataframe
df = pd.read_csv("../raw_data/evolution_data.csv")

# Ajouter nom bureau de vote au dataframe
for idbv, nbv in zip([feat['properties']['id_bv'] for feat in gj['features']], 
                         [feat['properties']['nomBureauVote'] for feat in gj['features']]):
    df.loc[df['id_bv']==idbv, 'nom_bv'] = nbv


# More systematic naming scheme and
# add percentage version of results
renaming_dict = {}
for colname in ['MARECHAL_eur', 'AUBRY_eur', 'BARDELLA_eur', 'TOUSSAINT_eur',
                'HAYER_eur', 'BELLAMY_eur', 'GLUCKSMANN_eur', 'DEFFONTAINES_eur',
                'TOUNSI_t1', 'GAILLARD_t1', 'ISNARD_t1', 'BREGEON_t1', 'PRETO_t1', 'YVARS_t1',
                'MARTIN_t1', 'GAILLARD_t2', 'BREGEON_t2']:
    colname_split = colname.split("_")
    new_base_str = '%s_%s' % (colname_split[0].capitalize(), colname_split[1])
    renaming_dict[colname] = '%s_abs' % new_base_str

    # Compute in percentage of registered voters
    df[('%s_pct' % new_base_str)] = (df[colname] / df[("Inscrits_%s"% colname_split[1])]) * 100


## Add evolution LR+LREM t1 vers t2
df['evolution_LR+LREM_t1_t2_abs'] = df['evolution_Bregeon_t1_t2_abs'] - df['ISNARD_t1']
df['evolution_LR+LREM_t1_t2_pct'] = (df['evolution_LR+LREM_t1_t2_abs'] / df["Inscrits_eur"]) * 100

    
for colname in ['Votants_eur', 'Blancs_eur', 'Nuls_eur', 'Inscrits_eur', 'Votants_t1',
                'Blancs_t1', 'Nuls_t1', 'Inscrits_t1', 'Votants_t2', 'Blancs_t2', 'Nuls_t2',
                'Inscrits_t2']:
    colname_split = colname.split("_")
    if colname_split[0] == 'Votants':
        new_base_str = 'Participation_%s' % colname_split[1]
    elif colname_split[0] == 'Blancs':
        new_base_str = 'blanc_%s' % colname_split[1]
    else:
        new_base_str = colname
    renaming_dict[colname] = '%s_abs' % new_base_str

    # Compute in percentage of registered voters
    df[('%s_pct' % new_base_str)] = (df[colname] / df[("Inscrits_%s"% colname_split[1])]) * 100



def compute_label(colname, num=1):
    """
    Compute axis label for <num> values plotted on this axis.
    """
    colname_split = colname.split("_")
    if num==1:
        if colname_split[0] == "evolution":
            my_label = "Évolution"
            if colname_split[1] == "Participation":
                my_label += " de la participation"
            else:
                my_label += f" du vote {colname_split[1]}" 
                my_label += f" ({colname_split[2]} vers {colname_split[3]}, % inscrits)" 
        elif colname_split[0] == "Participation":
            my_label = f"Participation ({colname_split[1]}, % inscrits)"
        else:
            my_label = f"Vote {colname_split[0]} ({colname_split[1]}, % inscrits)"
    else:
        if colname_split[0] == "evolution":
            my_label = "Évolution du vote ... (% inscrits)"
        else:
            my_label = "Vote ... (% inscrits)"
    return my_label


def compute_code(colname=1):
    """
    Compute legend short code for a given colname.
    """
    colname_split = colname.split("_")
    if colname_split[0] == "evolution":
        my_code = colname_split[1]
    else:
        my_code = colname_split[0]
    return my_code




def make_scatter_one_vs_one(y_colname, x_colname):
    """
    Scatter plot of two columns of the data frame.
    """
    # We always work with percentages
    x_colname_pct = x_colname + "_pct"
    y_colname_pct = y_colname + "_pct"
    
    # Compute Pearson's correlation between the two columns
    pears_corr = df[[x_colname_pct, y_colname_pct]].corr().iloc[0, 1]

    fig = px.scatter(df, 
                     x=x_colname_pct,
                     y=y_colname_pct,
                     labels={x_colname_pct: compute_label(x_colname),
                             y_colname_pct: compute_label(y_colname)
                             },
                     hover_name='nom_bv',
                     hover_data={'nom_bv': False, 
                                 x_colname_pct: ':.2f', 
                                 y_colname_pct: ':.2f'},   
                     title=f"R = {pears_corr:.2f}"
                     )
    
    fig.update_traces(marker=dict(size=8))

    fig.update_layout(autosize=False,
                      width=600,
                      height=600,
                      font=dict(size=16))

    #fig.show()
    fig_fname = f'../figs/scatter_{y_colname}_vs_{x_colname}_2024.html'
    print(f'Writing {fig_fname}')
    fig.write_html(fig_fname, include_plotlyjs='cdn')


def make_scatter_two_vs_one(y1_colname, y2_colname, x_colname):
    """
    Two scatterplots on the same graph, one for df[y1_colname] vs df[x_colname], 
    the other for df[y2_colname] vs df[xcolname]
    """
    # We always work with percentages
    x_colname_pct = x_colname + "_pct"
    y1_colname_pct = y1_colname + "_pct"
    y2_colname_pct = y2_colname + "_pct"
    
    # Compute temporary dataframe with four columns:
    # nom_bv, x_colname, y, code
    # y can be either y1_colname or y2_colname, code indicates which it is
    # the dataframe contains twice as many rows as df
    tmp_df1 = df[['nom_bv', x_colname_pct, y1_colname_pct]].copy()
    tmp_df1 = tmp_df1.rename(columns={y1_colname_pct: 'y'})
    code_y1 = compute_code(y1_colname)
    tmp_df1['code'] = code_y1
    
    tmp_df2 = df[['nom_bv', x_colname_pct, y2_colname_pct]].copy()
    tmp_df2 = tmp_df2.rename(columns={y2_colname_pct: 'y'})
    code_y2 = compute_code(y2_colname)
    tmp_df2['code'] = code_y2

    tmp_df = pd.concat((tmp_df1, tmp_df2), ignore_index=True)

    # Compute Pearson's correlation for the two point clouds
    pears_corr1 = tmp_df.loc[tmp_df["code"]==code_y1,
                             [x_colname_pct, 'y']].corr().iloc[0, 1]
    pears_corr2 = tmp_df.loc[tmp_df["code"]==code_y2,
                             [x_colname_pct, 'y']].corr().iloc[0, 1]

    fig = px.scatter(tmp_df, 
                     x=x_colname_pct,
                     y='y',
                     color='code',
                     labels={x_colname_pct: compute_label(x_colname),
                             'y': compute_label(y1_colname, num=2),
                             'code': 'Vote'},
                     hover_name='nom_bv',
                     hover_data={'nom_bv': False,
                                 x_colname_pct: ':.2f', 
                                 'y': ':.2f'},   
                     title=f"R ({code_y1}) = {pears_corr1:.2f}, R ({code_y2}) = {pears_corr2:.2f}" 
                     )

    fig.update_traces(marker=dict(size=8))
    
    fig.update_layout(autosize=False,
                      width=600,
                      height=600,
                      font=dict(size=16))

    #fig.show()
    fig_fname = f'../figs/scatter_{y1_colname}_and_{y2_colname}_vs_{x_colname}_2024.html'
    print(f'Writing {fig_fname}')
    fig.write_html(fig_fname, include_plotlyjs='cdn')

    
def make_scatter_evolution_vote_vs_evolution_participation():
    # europeennes vers legislatives t1
    tmp_df1 = df[['nom_bv', 'evolution_Participation_eur_t1_pct', 'evolution_LREM_eur_t1_pct']].copy()
    tmp_df1 = tmp_df1.rename(columns={'evolution_LREM_eur_t1_pct': 'y'})
    pears_corr = tmp_df1[['evolution_Participation_eur_t1_pct', 'y']].corr().iloc[0, 1]
    tmp_df1['code'] = f'LREM (R={pears_corr:.2f})'

    tmp_df2 = df[['nom_bv', 'evolution_Participation_eur_t1_pct', 'evolution_NFP_eur_t1_pct']].copy()
    tmp_df2 = tmp_df2.rename(columns={'evolution_NFP_eur_t1_pct': 'y'})
    pears_corr = tmp_df2[['evolution_Participation_eur_t1_pct', 'y']].corr().iloc[0, 1]
    tmp_df2['code'] = f'NFP (R={pears_corr:.2f})'

    tmp_df3 = df[['nom_bv', 'evolution_Participation_eur_t1_pct', 'evolution_LR_eur_t1_pct']].copy()
    tmp_df3 = tmp_df3.rename(columns={'evolution_LR_eur_t1_pct': 'y'})
    pears_corr = tmp_df3[['evolution_Participation_eur_t1_pct', 'y']].corr().iloc[0, 1]
    tmp_df3['code'] = f'LR (R={pears_corr:.2f})'

    tmp_df4 = df[['nom_bv', 'evolution_Participation_eur_t1_pct', 'evolution_EXD_eur_t1_pct']].copy()
    tmp_df4 = tmp_df4.rename(columns={'evolution_EXD_eur_t1_pct': 'y'})
    pears_corr = tmp_df4[['evolution_Participation_eur_t1_pct', 'y']].corr().iloc[0, 1]
    tmp_df4['code'] = f'EXD (R={pears_corr:.2f})'

    tmp_df = pd.concat((tmp_df1, tmp_df2, tmp_df3, tmp_df4), ignore_index=True)

    fig = px.scatter(tmp_df, 
                     x='evolution_Participation_eur_t1_pct',
                     y='y',
                     color='code',
                     opacity=0.8,
                     labels={'evolution_Participation_eur_t1_pct': "Évolution de la participation",
                             'y': "Évolution du vote",
                             'code': 'Vote'},
                     hover_name='nom_bv',
                     hover_data={'nom_bv': False,
                                 'evolution_Participation_eur_t1_pct': ':.2f', 
                                 'y': ':.2f'},   
                     title=f"Européennes vers 1er tour des législatives 2024" 
                     )

    fig.update_traces(marker=dict(size=6))

    fig.update_layout(autosize=False,
                      width=600,
                      height=600,
                      font=dict(size=16))

    # fig.show()
    fig_fname = '../figs/scatter_evolution_vote_vs_evolution_participation_eur_t1_2024.html'
    print(f'Writing {fig_fname}')
    fig.write_html(fig_fname, include_plotlyjs='cdn')


    # legislatives 2024 t1 vers t2
    tmp_df1 = df[['nom_bv', 'evolution_Participation_t1_t2_pct', 'evolution_Bregeon_t1_t2_pct']].copy()
    tmp_df1 = tmp_df1.rename(columns={'evolution_Bregeon_t1_t2_pct': 'y'})
    pears_corr = tmp_df1[['evolution_Participation_t1_t2_pct', 'y']].corr().iloc[0, 1]
    tmp_df1['code'] = f'Bregeon (R={pears_corr:.2f})'

    tmp_df2 = df[['nom_bv', 'evolution_Participation_t1_t2_pct', 'evolution_Gaillard_t1_t2_pct']].copy()
    tmp_df2 = tmp_df2.rename(columns={'evolution_Gaillard_t1_t2_pct': 'y'})
    pears_corr = tmp_df2[['evolution_Participation_t1_t2_pct', 'y']].corr().iloc[0, 1]
    tmp_df2['code'] = f'Gaillard (R={pears_corr:.2f})'

    tmp_df3 = df[['nom_bv', 'evolution_Participation_t1_t2_pct', 'evolution_LR+LREM_t1_t2_pct']].copy()
    tmp_df3 = tmp_df3.rename(columns={'evolution_LR+LREM_t1_t2_pct': 'y'})
    pears_corr = tmp_df3[['evolution_Participation_t1_t2_pct', 'y']].corr().iloc[0, 1]
    tmp_df3['code'] = f'LR+LREM (R={pears_corr:.2f})'

    tmp_df4 = df[['nom_bv', 'evolution_Participation_t1_t2_pct', 'evolution_Blancs_t1_t2_pct']].copy()
    tmp_df4 = tmp_df4.rename(columns={'evolution_Blancs_t1_t2_pct': 'y'})
    pears_corr = tmp_df4[['evolution_Participation_t1_t2_pct', 'y']].corr().iloc[0, 1]
    tmp_df4['code'] = f'Blancs (R={pears_corr:.2f})'

    tmp_df = pd.concat((tmp_df1, tmp_df2, tmp_df3, tmp_df4), ignore_index=True)

    fig = px.scatter(tmp_df, 
                     x='evolution_Participation_t1_t2_pct',
                     y='y',
                     color='code',
                     opacity=0.8,
                     labels={'evolution_Participation_t1_t2_pct': "Évolution de la participation",
                             'y': "Évolution du vote",
                             'code': 'Vote'},
                     hover_name='nom_bv',
                     hover_data={'nom_bv': False,
                                 'evolution_Participation_t1_t2_pct': ':.2f', 
                                 'y': ':.2f'},   
                     title=f"Premier vers deuxième tour des législatives 2024" 
                     )

    fig.update_traces(marker=dict(size=6))

    fig.update_layout(autosize=False,
                      width=600,
                      height=600,
                      font=dict(size=16))

    #fig.show()
    fig_fname = '../figs/scatter_evolution_vote_vs_evolution_participation_t1_t2_2024.html'
    print(f'Writing {fig_fname}')
    fig.write_html(fig_fname, include_plotlyjs='cdn')



def make_scatter_evolution_vote_vs_participation():
    # europeennes vers legislatives t1
    tmp_df1 = df[['nom_bv', 'Participation_eur_pct', 'evolution_LREM_eur_t1_pct']].copy()
    tmp_df1 = tmp_df1.rename(columns={'evolution_LREM_eur_t1_pct': 'y'})
    pears_corr = tmp_df1[['Participation_eur_pct', 'y']].corr().iloc[0, 1]
    tmp_df1['code'] = f'LREM (R={pears_corr:.2f})'

    tmp_df2 = df[['nom_bv', 'Participation_eur_pct', 'evolution_NFP_eur_t1_pct']].copy()
    tmp_df2 = tmp_df2.rename(columns={'evolution_NFP_eur_t1_pct': 'y'})
    pears_corr = tmp_df2[['Participation_eur_pct', 'y']].corr().iloc[0, 1]
    tmp_df2['code'] = f'NFP (R={pears_corr:.2f})'

    tmp_df3 = df[['nom_bv', 'Participation_eur_pct', 'evolution_LR_eur_t1_pct']].copy()
    tmp_df3 = tmp_df3.rename(columns={'evolution_LR_eur_t1_pct': 'y'})
    pears_corr = tmp_df3[['Participation_eur_pct', 'y']].corr().iloc[0, 1]
    tmp_df3['code'] = f'LR (R={pears_corr:.2f})'

    tmp_df4 = df[['nom_bv', 'Participation_eur_pct', 'evolution_EXD_eur_t1_pct']].copy()
    tmp_df4 = tmp_df4.rename(columns={'evolution_EXD_eur_t1_pct': 'y'})
    pears_corr = tmp_df4[['Participation_eur_pct', 'y']].corr().iloc[0, 1]
    tmp_df4['code'] = f'EXD (R={pears_corr:.2f})'

    tmp_df = pd.concat((tmp_df1, tmp_df2, tmp_df3, tmp_df4), ignore_index=True)

    fig = px.scatter(tmp_df, 
                     x='Participation_eur_pct',
                     y='y',
                     color='code',
                     opacity=0.8,
                     labels={'Participation_eur_pct': "Participation aux européennes",
                             'y': "Évolution du vote",
                             'code': 'Vote'},
                     hover_name='nom_bv',
                     hover_data={'nom_bv': False,
                                 'Participation_eur_pct': ':.2f', 
                                 'y': ':.2f'},   
                     title=f"Européennes vers 1er tour des législatives 2024" 
                     )

    fig.update_traces(marker=dict(size=6))

    fig.update_layout(autosize=False,
                      width=600,
                      height=600,
                      font=dict(size=16))

    # fig.show()
    fig_fname = '../figs/scatter_evolution_vote_vs_participation_eur_t1_2024.html'
    print(f'Writing {fig_fname}')
    fig.write_html(fig_fname, include_plotlyjs='cdn')


    # legislatives 2024 t1 vers t2
    tmp_df1 = df[['nom_bv', 'Participation_t1_pct', 'evolution_Bregeon_t1_t2_pct']].copy()
    tmp_df1 = tmp_df1.rename(columns={'evolution_Bregeon_t1_t2_pct': 'y'})
    pears_corr = tmp_df1[['Participation_t1_pct', 'y']].corr().iloc[0, 1]
    tmp_df1['code'] = f'Bregeon (R={pears_corr:.2f})'

    tmp_df2 = df[['nom_bv', 'Participation_t1_pct', 'evolution_Gaillard_t1_t2_pct']].copy()
    tmp_df2 = tmp_df2.rename(columns={'evolution_Gaillard_t1_t2_pct': 'y'})
    pears_corr = tmp_df2[['Participation_t1_pct', 'y']].corr().iloc[0, 1]
    tmp_df2['code'] = f'Gaillard (R={pears_corr:.2f})'

    tmp_df3 = df[['nom_bv', 'Participation_t1_pct', 'evolution_LR+LREM_t1_t2_pct']].copy()
    tmp_df3 = tmp_df3.rename(columns={'evolution_LR+LREM_t1_t2_pct': 'y'})
    pears_corr = tmp_df3[['Participation_t1_pct', 'y']].corr().iloc[0, 1]
    tmp_df3['code'] = f'LR+LREM (R={pears_corr:.2f})'

    tmp_df4 = df[['nom_bv', 'Participation_t1_pct', 'evolution_Blancs_t1_t2_pct']].copy()
    tmp_df4 = tmp_df4.rename(columns={'evolution_Blancs_t1_t2_pct': 'y'})
    pears_corr = tmp_df4[['Participation_t1_pct', 'y']].corr().iloc[0, 1]
    tmp_df4['code'] = f'Blancs (R={pears_corr:.2f})'

    tmp_df = pd.concat((tmp_df1, tmp_df2, tmp_df3, tmp_df4), ignore_index=True)

    fig = px.scatter(tmp_df, 
                     x='Participation_t1_pct',
                     y='y',
                     color='code',
                     opacity=0.8,
                     labels={'Participation_t1_pct': "Participation au 1er tour",
                             'y': "Évolution du vote",
                             'code': 'Vote'},
                     hover_name='nom_bv',
                     hover_data={'nom_bv': False,
                                 'Participation_t1_pct': ':.2f', 
                                 'y': ':.2f'},   
                     title=f"Premier vers deuxième tour des législatives 2024" 
                     )

    fig.update_traces(marker=dict(size=6))

    fig.update_layout(autosize=False,
                      width=600,
                      height=600,
                      font=dict(size=16))

    #fig.show()
    fig_fname = '../figs/scatter_evolution_vote_vs_participation_t1_t2_2024.html'
    print(f'Writing {fig_fname}')
    fig.write_html(fig_fname, include_plotlyjs='cdn')
    

    
## Evolution of one quantity with respect to the value of another

make_scatter_one_vs_one("evolution_Participation_eur_t1", "Participation_eur")
make_scatter_one_vs_one("evolution_Participation_t1_t2", "Participation_t1")

# make_scatter_one_vs_one("evolution_LREM_eur_t1", "Hayer_eur")
# make_scatter_one_vs_one("evolution_Bregeon_t1_t2", "Bregeon_eur")

# make_scatter_one_vs_one("evolution_NFP_eur_t1", "Bardella_eur")
# make_scatter_one_vs_one("evolution_Gaillard_t1_t2", "Yvars_t1")



## Compare how two quantities evolved with respect to the value of a third one

# make_scatter_two_vs_one("evolution_LREM_eur_t1", "evolution_NFP_eur_t1", "Participation_eur")
#make_scatter_two_vs_one("evolution_Bregeon_t1_t2", "evolution_Gaillard_t1_t2", "Participation_t1")

#make_scatter_evolution_vote_vs_participation()
#make_scatter_evolution_vote_vs_evolution_participation()


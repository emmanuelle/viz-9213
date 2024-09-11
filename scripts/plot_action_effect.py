import numpy as np
import geopandas as gpd
import plotly.express as px
from scipy import spatial

actions = gpd.read_file('../raw_data/actions_campagne.geojson')
stations = gpd.read_file('../raw_data/circo_contours_bvnames_filosofi+results.geojson')

stations['actions'] = 0
for index, row in stations.iterrows():
    count = 0
    for point in actions['geometry']:
        if point.within(row.geometry):
            count += 1
    stations.loc[index, 'actions'] = count

stations['has_actions'] = stations['actions'] > 0
stations['revenu_rel'] = (stations['revenu_moyen'] - stations['revenu_moyen'].min())/ (stations['revenu_moyen'].max() - stations['revenu_moyen'].min())

array_spatial = np.array(stations[['revenu_rel', 'men_coll_rel']])
tree = spatial.KDTree(array_spatial)
distance_matrix = tree.sparse_distance_matrix(tree, 0.1).todense()

results = {}
for index, row in stations.iterrows():
    # print(index)
    if not row['has_actions']:
        continue
    print(stations.loc[index, 'nomBureauVote'])
    indices = np.nonzero(distance_matrix[index])[1]
    order = np.array(np.argsort(distance_matrix[index, indices])).flatten()
    vote_distances = []
    count = 0
    for ind in indices[order]:
        if stations.loc[ind, 'has_actions']:
            continue
        else:
            vote_distances.append(float(stations.loc[index, 'vote_2024_t2_Gaillard'] - stations.loc[ind, 'vote_2024_t2_Gaillard']))
            count += 1
            if count >= 3:
                break
    results[index] = vote_distances

names = []
average_diff = []
for key, val in results.items():
    if len(val) == 0:
        continue
    names.append(stations.loc[key, 'numeroBureauVote'] + ' ' + stations.loc[key, 'nomBureauVote'] + ' ' + stations.loc[key, 'nomCommune'])
    average_diff.append(np.array(val).mean())

fig = px.scatter(stations, x='men_coll_rel', y='revenu_rel', hover_name='nomBureauVote', color='vote_2024_t2_Gaillard', 
                 hover_data={'nomCommune': True, 'actions': True, 'has_actions':False, 'men_coll_rel':False, 'revenu_rel':False}, 
                 symbol='has_actions', symbol_sequence=['circle', 'cross'], range_color=(30, 80), 
                 labels={'revenu_rel': 'revenu moyen normalisé', 'men_coll_rel': "fraction d'habitat collectif"}
                )
fig.update_traces(showlegend=False)
fig.update_traces(marker_size=14, selector={'marker_symbol':'cross'})
fig.show()
fig.write_html('../docs/distance_bureaux_pap_vote.html', include_plotlyjs='cdn')

fig = px.scatter(stations, x='men_coll_rel', y='revenu_rel', hover_name='nomBureauVote', color='nomCommune',
                 hover_data={'vote_2024_t2_Gaillard':True, 'has_actions':False, 'men_coll_rel':False, 'revenu_rel':False},
                 symbol='has_actions', symbol_sequence=['circle', 'cross'],
                 labels={'revenu_rel': 'revenu moyen normalisé', 'men_coll_rel': "fraction d'habitat collectif"}
                )
fig.update_traces(marker_size=14, showlegend=False, selector={'marker_symbol':'cross'})
fig.show()
fig.write_html('../docs/distance_bureaux_pap_villes.html', include_plotlyjs='cdn')

fig = px.bar(x=names, y=average_diff, labels={'y': 'écart de vote avec <br> bureaux similaires'})
fig.show()
fig.write_html('../docs/ecart_vote_pap.html', include_plotlyjs='cdn')

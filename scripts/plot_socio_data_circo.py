import geopandas as gpd
import plotly.express as px
import re

stations = gpd.read_file('../raw_data/circo_contours_bvnames_filosofi+results.geojson')

labels = {'revenu_moyen': "revenu moyen",
          'men_pauv_rel': "fraction de ménages pauvres",
          'men_fmp_rel': "fraction de familles monoparentales",
          'men_prop_rel': "fraction de propriétaires",
          'men_mais_rel': "fraction de ménages en maison",
          'men_5ind_rel': "fractions de ménages à 5+ individus",}
fig = px.scatter(stations, x='vote_2024_t1_Gaillard', trendline='ols',
                 hover_data=['nomBureauVote', 'nomCommune'], facet_col='variable',
                 facet_col_wrap=3,
                        y=[
                    'revenu_moyen',
                     'men_pauv_rel',
                     'men_fmp_rel',
                     'men_prop_rel',
                     'men_mais_rel',
                     'men_5ind_rel',
                 ],

)
for k in fig.layout:
    if re.search('yaxis[1-9]+', k):
        fig.layout[k].update(matches=None)
for annot in fig.layout.annotations:
    text = annot['text']
    annot['text'] = labels[text.split('=')[-1]]
fig.update_layout(showlegend=False)
for trace in fig.data[::2]:
    trace.hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]}<extra></extra>"
fig.write_html('../docs/scatter_socio_gaillard_t1.html', include_plotlyjs='cdn')

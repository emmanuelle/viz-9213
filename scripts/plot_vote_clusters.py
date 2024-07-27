import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.cluster import KMeans


def format_series(s):
    """
    Replace '35,2%' by 35.2 (type float) to manipulate numbers instead of str
    """
    return float(s[:-1].replace(',', '.'))


df = pd.read_excel('../raw_data/legislatives2024_t2_9213.xlsx')

df['Gaillard'] = df['% Voix/inscrits 1'].map(format_series)
df['Bregeon'] = df['% Voix/inscrits 2'].map(format_series)

X = np.array([df.Bregeon, df.Gaillard]).T
kmeans = KMeans(n_clusters=2, random_state=0, n_init="auto").fit(X)
df['labels'] = kmeans.labels_

fig = px.scatter(df, y='Gaillard', x='Bregeon', color='Libellé commune', symbol='labels',
                 hover_data={'nomBureauVote':True, 'Gaillard':False, 'Bregeon':False, 'Libellé commune':False},
                 color_discrete_sequence=px.colors.qualitative.G10,
                 width=700, height=500,
                 symbol_sequence=['circle', 'star', 'square'],
                 template='presentation'
                )
fig.update_yaxes(
    scaleanchor="x",
    scaleratio=1,
    range=(10, 55)
  )
fig.update_xaxes(
    range=(10, 55)
  )
fig.update_layout(legend_title_text='')
for i in range(8):
    fig.data[i].hovertemplate ='%{customdata[0]}<extra></extra>'
    if i%2:
        fig.data[i].showlegend = False
    else:
        fig.data[i].name = fig.data[i].name[:-3]

fig.write_html('vote_clusters_t2_2024.html')
fig.write_image('vote_clusters_t2_2024.png')
fig.show()

import pandas as pd
import plotly.express as px

df = pd.read_excel('../raw_data/legislatives2024_t1_9213.xlsx')

dimensions = ['Participation', 'Gaillard', 'Bregeon', 'Isnard', 'Yvars']

fig = px.scatter_matrix(df, dimensions=dimensions, height=600, color='Libellé commune',
                        hover_data={'nomBureauVote':True,
                                   },
                        labels={'Libellé commune':'Commune'},
                        color_discrete_sequence=px.colors.qualitative.G10,
                       template="plotly_dark")
fig.update_traces(diagonal_visible=False)
for i in range(4):
    fig.data[i].hovertemplate ='%{customdata[0]}<extra></extra>'
fig.write_html('../figs/scatter_matrix_t1_2024.html', include_plotlyjs='cdn')

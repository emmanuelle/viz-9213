# viz-9213

## Source of data

https://www.data.gouv.fr/fr/datasets/elections-legislatives-des-30-juin-et-7-juillet-2024-resultats-definitifs-du-2nd-tour/


https://www.data.gouv.fr/fr/datasets/proposition-de-contours-des-bureaux-de-vote/

## Data files

``raw_data/circo_contours_bvnames_corrected.geojson``: geojson file with contours of polling stations

``raw_data/circo_contours_bvnames_results.geojson``: geojson file with contours of polling stations and election results as properties

``raw_data/contour_communes.geojson``: geojson file with contours of cities

``raw_data/legislatives2024_t1_9213.xlsx`` and ``raw_data/legislatives2024_t2_9213.xlsx``: election results in 92-13 - legislatives 2024

``raw_data/legislatives2022_t2_9213.xlsx``: election results in 92-13 - legislatives 2022

``raw_data/departementales_2021_t1.xlsx``: election results in 92-13 - departementales 2021

``raw_data/evolution_data.csv``: evolution of election results in 92-13 (europeennes 2024 --> tour 1 legislatives 2024 --> tour 2 legislatives 2024)


## Plotting results

For example (code in ``scripts/plot_data_circo.py``)

```python
import geopandas as gpd
import pandas as pd

df_places = gpd.read_file('../raw_data/circo_contours.geojson')
df = pd.read_excel('../raw_data/legislatives2024_t2_9213.xlsx')

df['id_bv'] = df['Code commune'].astype(str) + '_' + df['Code BV'].astype(str)
merged = gpd.GeoDataFrame(pd.merge(df, df_places, on='id_bv'))

# Plot % of votes for Brice Gaillard
merged.plot(column=merged['% Voix/exprimés 1'].map(lambda x: float(x[:-1].replace(',', '.'))),
        legend=True,
        legend_kwds={'label':'% votes NFP'})

```

![viz-example](https://github.com/user-attachments/assets/6acf7946-52fb-4af3-beed-b891d6f9878c)

## Scripts

``scripts/make_dataframe_evolution_votes.py``: build dataframe/csv with data regarding vote evolution (europeennes 2024 --> tour 1 legislatives 2024 --> tour 2 legislatives 2024). Used to create ``raw_data/evolution_data.csv``
        
``scripts/make_geojson_communes.py``: build contours of cities. Used to create ``raw_data/contour_communes.geojson``
        
``scripts/plot_evolution.py``: plot maps of vote evolution (europeennes 2024 --> tour 1 legislatives 2024 --> tour 2 legislatives 2024)

``scripts/plot_scatter_evolution.py``: plot various scatter plots of vote/vote evolution vs another vote/vote evolution


import geopandas as gpd

carreaux = gpd.read_file('original_data/carreaux_200m_met.gpkg')
carreaux_circo = carreaux[carreaux['lcog_geo'].isin(['92019', '92014', '92071', '92002'])]

carreaux_circo.to_file("carreaux.geojson", driver='GeoJSON')
carreaux_circo.to_file("carreaux.gpkg", driver='GPKG')

import geopandas as gpd


# Original data from https://www.insee.fr/fr/statistiques/7655475?sommaire=7655515

carreaux = gpd.read_file('original_data/carreaux_200m_met.gpkg')
carreaux_circo = carreaux[carreaux['lcog_geo'].isin(['92019', '92014', '92071', '92002'])]

carreaux_circo.to_file("carreaux.geojson", driver='GeoJSON')
carreaux_circo.to_file("carreaux.gpkg", driver='GPKG')

import pyproj

from shapely.geometry import Polygon
from shapely.ops import transform


inCRS = pyproj.CRS('EPSG:2154') # Lambert 93 / RGF 93
outCRS = pyproj.CRS('EPSG:4326') # Latitude longitude

project = pyproj.Transformer.from_crs(inCRS, outCRS, always_xy=True).transform

def transform_poly(poly):
    return transform(project, poly)

carreaux_circo['other_geometry'] = carreaux_circo['geometry'].map(transform_poly)

carreaux_circo['geometry'] = carreaux_circo['other_geometry']
carreaux_circo.drop(columns=['other_geometry']).to_file('carreaux_geo.geojson', driver='GeoJSON')
carreaux_circo.drop(columns=['other_geometry']).to_file('carreaux_geo.gpkg', driver='GPKG')

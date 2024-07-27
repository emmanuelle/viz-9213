import geopandas as gpd


# Original data from https://www.insee.fr/fr/statistiques/7655475?sommaire=7655515

carreaux = gpd.read_file('original_data/carreaux_200m_met.gpkg')
list_communes = [
       '9137792002',
       '9200291377', '92002', '9168992002', '9200291689',
       '913779164592002', '916459137792002', '9164592002', '9200291645',
       '916899403492002', '9200294034', '9403492002', '9164592019',
       '9201991645', '920199200291645', '9200292019', '92019',
       '9201992002', '940349200294038', '920029403894034', '9403892002',
       '9201992071', '9200292071', '9200294038', '9207192019', '92071',
       '9207192002', '9200292014', '9201492002', '940389201492002',
       '9201991064', '920719201492002', '92014', '9201494038',
       '9403892014', '9207192014', '9201492071', '9201992060',
       '9206092019', '9201992023', '920239201992060', '920149401694038',
       '940169403892014', '9207192032', '9201494016',
       '92060920719203292019', '920329207192060', '9203292071',
       '920719203292007', '920719200792032', '9200792071',
       '920149200792071', '9401692014', '9200792014', '9201492007',
       '920149200794016', '920079401692014']
carreaux_circo = carreaux[carreaux['lcog_geo'].isin(list_communes)]
#carreaux_circo = carreaux[carreaux['lcog_geo'].str.contains("92019|92014|92071|92002")]

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

"""
We remove the very small connected components (area <5% of largest connected component,
theshold chosen from visual inspection)
"""


import numpy as np
from shapely.geometry import Polygon
import geojson

with open('circo_contours_bvnames.geojson', 'r') as f:
    data = geojson.load(f)


for i, feat in enumerate(data['features']):
    if feat['geometry']['type'] == 'MultiPolygon':
        if feat['properties']['nomCommune'] == 'Bourg-la-Reine':
            print("skip BLR")
            continue
        areas = []
        for poly in feat['geometry']['coordinates']:
            areas.append(Polygon(poly[0]).area)
        areas = np.array(areas)
        areas /= areas.max()
        indices = np.nonzero(areas > 0.05)[0]
        if len(indices) == 1:
            feat['geometry'] = {'type':'Polygon', 'coordinates':feat['geometry']['coordinates'][indices[0]]}
        elif len(indices) == len(areas):
            continue
        else:
            feat['geometry']['coordinates'] = [feat['geometry']['coordinates'][j] for j in indices]

with open('circo_contours_bvnames_corrected.geojson', 'w') as outfile:
    geojson.dump(data, outfile)


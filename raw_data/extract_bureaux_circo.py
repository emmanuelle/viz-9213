import geojson

with open('contours-france-entiere-latest-v2.geojson', 'r') as f:
    data = geojson.load(f)

features = [x for x in data['features'] 
                if x['properties']['codeCirconscription'] == '9213']

data['features'] = features

with open("circo_contours.geojson", 'w') as outfile:
     geojson.dump(data, outfile)


# df_places = gpd.read_file('circo_contours.geojson')

import geojson

with open('original_data/communes.geojson', 'r') as f:
    data = geojson.load(f)

features = [x for x in data['features'] 
                if x['properties']['nom'] == 'Antony']

data['features'] = features

with open("antony.geojson", 'w') as outfile:
     geojson.dump(data, outfile)


# df_places = gpd.read_file('circo_contours.geojson')

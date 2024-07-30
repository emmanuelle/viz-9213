import geojson

## READ contours of each city

# From contours downloaded from https://polygons.openstreetmap.fr/ : 
# * https://polygons.openstreetmap.fr/?id=57750 for Antony
# * https://polygons.openstreetmap.fr/?id=37041 for Bourg-la-Reine
# * https://polygons.openstreetmap.fr/?id=33914 for Châtenay-Malabry
# * https://polygons.openstreetmap.fr/?id=28069 for Sceaux
# (Generally speaking: use search on https://www.openstreetmap.org to determine relation ID)

DOWNLOAD_DIR = '/home/cazencott/Downloads'

with open(f'{DOWNLOAD_DIR}/antony.geojson') as f:
    gj_anto = geojson.load(f)
with open(f'{DOWNLOAD_DIR}/blr.geojson') as f:
    gj_blr = geojson.load(f)
with open(f'{DOWNLOAD_DIR}/chatenay.geojson') as f:
    gj_chatenay = geojson.load(f)
with open(f'{DOWNLOAD_DIR}/sceaux.geojson') as f:
    gj_sceaux = geojson.load(f)


## COMBINE contours of all cities
circo_coordinates = []
for gj_city in [gj_anto, gj_blr, gj_chatenay, gj_sceaux]:
    circo_coordinates.extend(gj_city['coordinates'][0])
gj_circo = {'type': gj_anto['type'], 'coordinates':[circo_coordinates]}


## WRITE output gejson
with open("../raw_data/contour_communes.geojson", 'w') as outfile:
     geojson.dump(gj_circo, outfile)

from pykml import parser
from rd_convert import *

def parse(src):
	polygons = {'Alpha': [], 'Bravo': [], 'Charlie': [], \
		'Delta': [], 'Echo': [], 'Foxtrot': []}

	with open(src, 'r') as f:
		doc = parser.parse(f)
	root = doc.getroot()

	for folder in root.Document.Folder:
		if folder.name.text == "Deelgebieden":
			for gebied in folder.Placemark:
				for coord in gebied.Polygon.outerBoundaryIs.LinearRing.coordinates.text.split('\n'):
					parts = coord.strip().split(',')
					if parts == ['']:
						continue
					rdc = wgs_to_rd(float(parts[1]), float(parts[0]))
					rdc = (int(round(rdc[0])), int(round(rdc[1])))
					polygons[gebied.name.text].append(rdc)

	return polygons
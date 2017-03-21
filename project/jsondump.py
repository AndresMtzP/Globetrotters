import json
from teleportapi import getContinent, getPopulation, getDetails, getCountry, getLatLng

def infoJSON(loc):
	latlng = getLatLng(loc)
	details = getDetails(loc)
	data = {'Country' : getCountry(loc), 'Continent' : getContinent(loc), 'Population' : getPopulation(loc),
			'Currency' : details[1], 'Language' : details[3], 'Life Expectancy' : details[2],
			'Lat' : latlng[0], 'Lng' : latlng[1], 'Climate' : details[0]}
	with open('info.json', 'w') as outfile:
		json.dump(data, outfile)
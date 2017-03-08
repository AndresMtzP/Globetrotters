# This file contains function definition for gathering data for the Levitating Globe
import wptools
import urllib
import requests

def getImage(loc):
	# grab coords and keyword from google geocode api and user input
	key = "AIzaSyDfANCLdJ72sAANtbIc55BQ2-EAdu5WiOw"
	coords = getLatLng(loc)

	# does a place search to get photo reference id
	payload = {'key' : key, 'location' : coords, 'radius' : '500', 'type' : '(cities)'}
	r = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json", params=payload)

	if r.status_code == 200:
		data = r.json()

	# grab photo reference id for places request
	pref = data['results'][0]['photos'][0]['photo_reference']

	payload = {'key' : key, 'maxwidth' : '400', 'photo_reference' : pref}
	r = requests.get("https://maps.googleapis.com/maps/api/place/photo", params=payload)

	if r.status_code == 200:
		urllib.urlretrieve(r.url,"%s.jpg" % loc)

def getGeneral(loc):
	# relevant information from dictionary after wptools.page('').get_parse()
	# 'population_total', 'coordinates', 'name', 'area_total_km2', area_land_km2', 'area_water_km2'

	# get wikipedia page 
	location = wptools.page(loc, silent=True).get_parse()
	locInfo = location.infobox
	dictKeys = locInfo.keys() # getting list of available keys in info box

	# create dict of keys we're searching for and related string value to display
	labelDict = {'population_total' : 'Population', 
		'name' : 'Location Name', 
		'area_total_km2' : 'Total Area (km2)',
		'area_land_km2' : 'Land Area (km2)', 
		'area_water_km2' : 'Water area (km2)', 
		'coordinates' : 'Region'}
	searchKeys = labelDict.keys()

	# search for the keys in the response because there is no standard format on wiki page
	for key in searchKeys:
		if key in dictKeys:
			if key == 'coordinates':
				coords = locInfo['coordinates']
				coordsList = coords.split('|')
				regionList = filter(lambda x: 'region' in x, coordsList)
				if regionList:
					region = regionList[0].split(':')[1]
					print "Region: %s" % region
			else:
				print "%s: %s" % (labelDict[key], locInfo[key])

def getLatLng(loc):
	key = "AIzaSyDfANCLdJ72sAANtbIc55BQ2-EAdu5WiOw"
	coords = ""

	# geocode api for lat/lng
	payload = {'key' : key, 'address' : loc}
	r = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params = payload)

	# give coords value of lat and lng
	data = r.json()
	if data['results'] and r.status_code == 200:
		lat = str(data['results'][0]['geometry']['location']['lat'])
		lng = str(data['results'][0]['geometry']['location']['lng'])
		coords = lat + "," + lng
	return coords
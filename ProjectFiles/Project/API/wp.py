import requests
import wptools
import re

# relevant information from dictionary after wptools.page('').get_parse()
# 'population_total', 'coordinates', 'name', 'area_total_km2', area_land_km2', 'area_water_km2'

# get wikipedia page 
location = wptools.page('Detroit', silent=True).get_parse()
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
			region = regionList[0].split(':')[1]
			print "Region: %s" % region
		else:
			print "%s: %s" % (labelDict[key], locInfo[key])
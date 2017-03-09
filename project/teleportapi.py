#################################################################################################
# This file is intended to test the functionality of the Teleport API on cities. So currently,
# most of these functions will work with cities until I begin to implement functionality to
# handle countries, continents, states, etc...
#################################################################################################
import requests
import urllib

# Gets the population of the city
def getPopulation(loc):
	payload = {'search': loc}
	r = requests.get("https://api.teleport.org/api/cities", params=payload)
	data = r.json()
	if data['_embedded']['city:search-results']:
		result = data['_embedded']['city:search-results'][0]
		r = requests.get(result['_links']['city:item']['href'])
		data = r.json()
	if 'population' in data.keys():
		return data['population']
	else:
		return None

# Gets the latitude and longitude of the city
def getLatLng(loc):
	payload = {'search': loc}
	r = requests.get("https://api.teleport.org/api/cities", params=payload)
	data = r.json()
	if data['_embedded']['city:search-results']:
		result = data['_embedded']['city:search-results'][0]
		r = requests.get(result['_links']['city:item']['href'])
		data = r.json()
		return (data['location']['latlon']['latitude'], data['location']['latlon']['longitude'])
	else:
		return None

# Gets the fully qualified name of the city (ex: San Diego, California, United States)
def getFullName(loc):
	payload = {'search': loc}
	r = requests.get("https://api.teleport.org/api/cities", params=payload)
	data = r.json()
	if data['_embedded']['city:search-results']:
		result = data['_embedded']['city:search-results'][0]
		return result['matching_full_name'].encode('utf-8')
	else:
		return None

# Gets the country the city is located in
def getCountry(loc):
	payload = {'search': loc}
	r = requests.get("https://api.teleport.org/api/cities", params=payload)
	data = r.json()
	if data['_embedded']['city:search-results']:
		result = data['_embedded']['city:search-results'][0]
		r = requests.get(result['_links']['city:item']['href'])
		data = r.json()
		return data['_links']['city:country']['name'].encode('utf-8')
	else:
		return None

# Gets the continent that the city is located in
def getContinent(loc):
	payload = {'search': loc}
	r = requests.get("https://api.teleport.org/api/cities", params=payload)
	data = r.json()
	if data['_embedded']['city:search-results']:
		result = data['_embedded']['city:search-results'][0]
		r = requests.get(result['_links']['city:item']['href'])
		data = r.json()
		r = requests.get(data['_links']['city:country']['href'])
		data = r.json()
		return data['_links']['country:continent']['name'].encode('utf-8')
	else:
		return None;

# Gets the other results from the response for the city (ex: cities with the same name)
def getSearchResults(loc):
	payload = {'search': loc}
	r = requests.get("https://api.teleport.org/api/cities", params=payload)
	data = r.json()
	for result in data['_embedded']['city:search-results']:
		print result['matching_full_name'].encode('utf-8')

# Gets the image of the urban area the city is located in
def getImage(loc):
	payload = {'search': loc}
	r = requests.get("https://api.teleport.org/api/cities", params=payload)
	data = r.json()
	result = data['_embedded']['city:search-results'][0]
	r = requests.get(result['_links']['city:item']['href'])
	data = r.json()['_links']
	matchKeys = data.keys()
	if 'city:urban_area' in matchKeys:
		r = requests.get(data['city:urban_area']['href'])
		data = r.json()
		r = requests.get(data['_links']['ua:images']['href'])
		data = r.json()
		urllib.urlretrieve(data['photos'][0]['image']['mobile'],"%s.jpg" % loc)

def createCitiesCsv():
	fr = open("allCities.txt", "r")
	fw = open("allCities.csv", "w")
	count = 1
	for loc in fr.readlines():
		print loc
		latlng = getLatLng(loc)
		if latlng is not None:
			lat = latlng[0]
			lng = latlng[1]
		else:
			lat = None;
			lng = None;
		fw.write("%s,%s,%s,%s,%s,%s,%s" % (count, loc.strip(), getPopulation(loc), lat, lng, getCountry(loc), getContinent(loc)))
		count+=1
	fr.close()
	fw.close()

# Writes all the cities that Teleport API references in a file (non-alphabetical)
def writeAllCities():
	f = open('allCities.txt', 'w')
	r = requests.get('https://api.teleport.org/api/countries')
	data = r.json()
	countryList = data['_links']['country:items']
	for country in countryList:
		r = requests.get(country['href'])
		print "Writing cities in %s" % country['name']
		data = r.json()
		r = requests.get(data['_links']['country:admin1_divisions']['href'])
		data = r.json()
		cityList = data['_links']['a1:items']
		for city in cityList:
			if 'name' in city.keys():
				f.write('%s\n' % city['name'].encode('utf-8'))
	f.close()

# Writes all the countries that Teleport API references in a file (alphabetical)
def writeAllCountries():
	f = open('allCountries.txt', 'w')
	r = requests.get('https://api.teleport.org/api/countries')
	data = r.json()
	countryList = data['_links']['country:items']
	for country in countryList:
		f.write('%s\n' % country['name'])
	f.close()


def main():
	'''
	loc = raw_input("Enter a location: ")
	getFullName(loc)
	getPopulation(loc)
	getLatLng(loc)
	getCountry(loc)
	getContinent(loc)
	print "\nList of all results for: %s" % loc
	getSearchResults(loc)
	# getImage(loc)
	# writeAllCountries()
	# writeAllCities()
	'''
	createCitiesCsv()

main()

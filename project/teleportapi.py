#################################################################################################
# This file is intended to test the functionality of the Teleport API on cities. So currently,
# most of these functions will work with cities until I begin to implement functionality to
# handle countries, continents, states, etc...
#################################################################################################
import requests
import urllib

def getAll(loc):
	cityName=population=lat=lng=stateName=countryName=None
	payload = {'search' : loc, 'embed' : 'city:search-results/city:item'}
	r = requests.get("https://api.teleport.org/api/cities", params=payload)
	data = r.json()
	if data['_embedded']['city:search-results']:
		result = data['_embedded']['city:search-results'][0]['_embedded']['city:item']
		infoKeys = result.keys()
		if 'name' in infoKeys:
			cityName = result['name'].encode('utf-8')
		if 'population' in infoKeys:
			population = result['population']
		if 'location' in infoKeys:
			lat = result['location']['latlon']['latitude']
			lng = result['location']['latlon']['longitude']
		if '_links' in infoKeys:
			if 'city:country' in result['_links'].keys():
				countryName = result['_links']['city:country']['name'].encode('utf-8')
		if '_links' in infoKeys:
			if 'city:admin1_division' in result['_links'].keys():
				stateName = result['_links']['city:admin1_division']['name'].encode('utf-8')
	return (cityName,population,lat,lng,stateName,countryName)

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
def getImage(loc, count):
	payload = {'search': loc}
	r = requests.get("https://api.teleport.org/api/cities", params=payload)
	data = r.json()
	if data['_embedded']['city:search-results']:
		result = data['_embedded']['city:search-results'][0]
		r = requests.get(result['_links']['city:item']['href'])
	data = r.json()['_links']
	matchKeys = data.keys()
	if 'city:urban_area' in matchKeys:
		r = requests.get(data['city:urban_area']['href'])
		data = r.json()
		r = requests.get(data['_links']['ua:images']['href'])
		data = r.json()
		urllib.urlretrieve(data['photos'][0]['image']['mobile'],"C:\Users\Brian Pham\Documents\Classes\COMPE 490\Levitating Globe\API\Images\%s.jpg" % count)

# Gets detailed information about certain location
def getDetails(loc):
	weatherType=curr=lifeExpectancy=lang=None

	details = ['CLIMATE', 'ECONOMY', 'INTERNAL', 'LANGUAGE']
	payload = {'search': loc}
	r = requests.get("https://api.teleport.org/api/cities", params=payload)
	data = r.json()
	if data['_embedded']['city:search-results']:
		result = data['_embedded']['city:search-results'][0]
		r = requests.get(result['_links']['city:item']['href'])
	data = r.json()['_links']
	matchKeys = data.keys()
	if 'city:urban_area' in matchKeys:
		r = requests.get(data['city:urban_area']['href'])
		data = r.json()['_links']
		matchKeys = data.keys()
		if 'ua:details' in matchKeys:
			r = requests.get(data['ua:details']['href'])
			data = r.json()['categories']
			for result in data:
				if result['id'] in details:
					ID = result['id']
					if ID == 'CLIMATE':
						climate = result['data']
						for x in climate:
							if x['id'] == 'WEATHER-TYPE':
								weatherType = x['string_value']
								print x['label'] + ": " + weatherType
					elif ID == 'ECONOMY':
						econ = result['data']
						for x in econ:
							if x['id'] == 'CURRENCY-URBAN-AREA':
								curr = x['string_value']
								print x['label'] + ": " + curr
					elif ID == 'INTERNAL':
						internal = result['data']
						for x in internal:
							if x['id'] == 'LIFE-EXPECTANCY':
								lifeExpectancy = str(x['float_value'])
								print x['label'] + ": " + lifeExpectancy
					elif ID == 'LANGUAGE':
						lang = result['data']
						for x in lang:
							if x['id'] == 'SPOKEN-LANGUAGES':
								lang = x['string_value']
								print x['label'] + ": " + lang
	return (weatherType,curr,lifeExpectancy,lang)

def createCitiesCsv():
	fr = open("allCities.txt", "r")
	fw = open("allCities.csv", "w")
	count = 1
	for loc in fr.readlines():
		print loc
		fw.write("%s,%s,%s,%s,%s,%s,%s\n" % ((count,)+getAll(loc)))
		count+=1
	fr.close()
	fw.close()

# Creates CSV containing cities and general information
def createStatesCsv():
	fr = open("allStates.txt", "r")
	fw = open("allStates.csv", "w")
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
		fw.write("%s,%s,%s,%s,%s,%s,%s\n" % (count, loc.strip(), getPopulation(loc), lat, lng, getCountry(loc), getContinent(loc)))
		count+=1
	fr.close()
	fw.close()

# Writes all the cities that Teleport API references in a file (non-alphabetical)
def writeAllCities():
	f = open('allCities.txt', 'w')
	r = requests.get('https://api.teleport.org/api/countries/?embed=country%3Aitems%2Fcountry%3Aadmin1_divisions')
	data = r.json()
	countryList = data['_embedded']['country:items']
	for country in countryList:
		stateList = country['_embedded']['country:admin1_divisions']['_links']['a1:items']
		for state in stateList:
			r = requests.get(state['href'])
			data = r.json()['_links']
			r = requests.get(data['a1:cities']['href'])
			data = r.json()
			if 'name' in state.keys():
				print "Writing cities in %s" % state['name'].encode('utf-8')
				cityList = data['_links']['city:items']
				for city in cityList:
					if 'name' in city.keys():
						f.write('%s,%s\n' % (city['name'].encode('utf-8'),state['name'].encode('utf-8')))
	f.close()


# Writes all the states that Teleport API references in a file (non-alphabetical)
def writeAllStates():
	f = open('allStates.txt', 'w')
	r = requests.get('https://api.teleport.org/api/countries')
	data = r.json()
	countryList = data['_links']['country:items']
	for country in countryList:
		r = requests.get(country['href'])
		print "Writing states in %s" % country['name']
		data = r.json()
		r = requests.get(data['_links']['country:admin1_divisions']['href'])
		data = r.json()
		stateList = data['_links']['a1:items']
		for state in stateList:
			if 'name' in state.keys():
				f.write('%s\n' % state['name'].encode('utf-8'))
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

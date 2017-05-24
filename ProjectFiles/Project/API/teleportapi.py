#################################################################################################
# This file is intended to test the functionality of the Teleport API on cities. So currently,
# most of these functions will work with cities until I begin to implement functionality to
# handle countries, continents, states, etc...
#################################################################################################
import requests
import urllib
import os.path
import json
from trottersDB import *

# Gets all the location information for a location request
def getAll(loc):
	limit = 10
	cityName=population=lat=lng=stateName=countryName=""
	locList = []
	countrySearchDB(loc, locList, limit)
	stateSearchDB(loc, locList, limit)
	payload = {'search' : loc, 'embed' : 'city:search-results/city:item'}
	r = requests.get("https://api.teleport.org/api/cities", params=payload)
	data = r.json()
	cityCount = data['count']
	if data['_embedded']['city:search-results']:
		cities = data['_embedded']['city:search-results']
		for city in cities:
			count = len(locList)
			if count < limit:
				result = city['_embedded']['city:item']
				infoKeys = result.keys()
				if 'full_name' in infoKeys and loc in result['full_name']:
					if 'name' in infoKeys:
						cityName = result['name'].encode('utf-8')
					if 'population' in infoKeys:
						population = result['population']
						population = "{:,}".format(population)
					if 'location' in infoKeys:
						lat = result['location']['latlon']['latitude']
						lng = result['location']['latlon']['longitude']
					if '_links' in infoKeys:
						if 'city:country' in result['_links'].keys():
							countryName = result['_links']['city:country']['name'].encode('utf-8')
						if 'city:admin1_division' in result['_links'].keys():
							if 'name' in result['_links']['city:admin1_division'].keys():
								stateName = result['_links']['city:admin1_division']['name'].encode('utf-8')
					tele_msg = '''{}, has a population of {} people, and is located at {} latitude, and {} longitude'''.format(cityName, population, lat, lng)
					fullname = '''{}, {}, {}'''.format(cityName, stateName, countryName)
					cityDict = {'Name' : cityName, 'Population': population, 'Lat' : lat, 'Lng' : lng, 'State' : stateName, 'Country' : countryName, 'Type' : 'City', 'Message' : tele_msg, 'FullName' : fullname}
					cityDict.update(getDetails(fullname))
					locList.append(cityDict)
	with open('/var/www/html/LocationInfo.json', 'w') as outfile:
		json.dump(locList, outfile, ensure_ascii=False, encoding='utf-8') # Unescape characters
	return locList

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
	if (os.path.isfile("/var/www/html/Images/{}0.jpg".format(loc))):
		print "Trotter: {} images already exists".format(loc)
		return

	print "Trotter: downloading images for {}".format(loc)
	key = "3fe696d991085740dda6a26e7fbd7954"
	payload = {'text':loc + ' travel', 'format':'json', 'api_key':key, 'per_page':3, 'accuracy':11, 'method':'flickr.photos.search', 'nojsoncallback':1,
		'tags':'city, skyline', 'tag_mode':'any'}

	r = requests.get("https://api.flickr.com/services/rest", params=payload)
	data = r.json()
	if data['stat'] == 'ok':
		numPhotos = int(data['photos']['total'])
		count = 0
		while count < 3 and count < numPhotos:
			photo = data['photos']['photo'][count]
			farmid = photo['farm']
			serverid = photo['server']
			photoid = photo['id']
			secret = photo['secret']
			photourl = '''https://farm{}.staticflickr.com/{}/{}_{}_c.jpg'''.format(farmid,serverid,photoid,secret)
			urllib.urlretrieve(photourl,'/var/www/html/Images/{}{}.jpg'.format(loc,count))
			count += 1

# Gets detailed information about certain location
def getDetails(loc):
	weatherType=curr=rate=exchange=lunch=lang=medApart=gunCrime=message=""

	details = ['CLIMATE', 'ECONOMY', 'COST-OF-LIVING', 'LANGUAGE', 'HOUSING', 'SAFETY']
	payload = {'search' : loc, 'embed' : 'city:search-results/city:item/city:urban_area/ua:details'}
	r = requests.get("https://api.teleport.org/api/cities/", params=payload)
	data = r.json()

	try:
		result = data['_embedded']['city:search-results'][0]['_embedded']['city:item']['_embedded']['city:urban_area']['_embedded']['ua:details']['categories']
		for res in result:
				if res['id'] in details:
					ID = res['id']
					if ID == 'CLIMATE':
						climate = res['data']
						for x in climate:
							if x['id'] == 'WEATHER-TYPE':
								weatherType = x['string_value']
								message += ''' This area has a {}.'''.format(weatherType)
					elif ID == 'ECONOMY':
						econ = res['data']
						for x in econ:
							if x['id'] == 'CURRENCY-URBAN-AREA':
								curr = x['string_value']
								message += ''' The currency of this city is {}.'''.format(curr)
							if x['id'] == 'CURRENCY-URBAN-AREA-EXCHANGE-RATE':
								rate = str(x['float_value'])
					elif ID == 'COST-OF-LIVING':
						costOfLiving = res['data']
						for x in costOfLiving:
							if x['id'] == 'COST-RESTAURANT-MEAL':
								lunch = "$" + str(x['currency_dollar_value'])
								message += ''' On average, the price of lunch is around {}.'''.format(lunch)
					elif ID == 'LANGUAGE':
						language = res['data']
						for x in language:
							if x['id'] == 'SPOKEN-LANGUAGES':
								lang = x['string_value']
								message += ''' The spoken languages of this city include {}.'''.format(lang)
					elif ID == 'HOUSING':
						housing = res['data']
						for x in housing:
							if x['id'] == 'APARTMENT-RENT-MEDIUM':
								medApart = "$" + str(x['currency_dollar_value'])
								message += ''' To rent a medium sized apartment in this area, expect to spend around {} a month.'''.format(medApart)
					elif ID == 'SAFETY':
						safety = res['data']
						for x in safety:
							if x['id'] == 'GUN-DEATH-RATE':
								gunCrime = str(x['int_value'])

					if rate != "" and curr != "":
						exchange = '''$1 -> {} {}'''.format(rate,curr)
	except:
		print 'No detailed information for "%s" was found' % loc
		message += '''No detailed information for {} was found.'''.format(loc)
		pass

	return {'Weather' : weatherType, 'ExchangeRate' : exchange, 'Lunch' : lunch, 'Languages' : lang, 'Housing' : medApart, 'GunDeathRate' : gunCrime, 'MoreInfo' : message}



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
	f = open('allCountries.csv', 'w')
	r = requests.get('https://api.teleport.org/api/countries')
	data = r.json()
	countryList = data['_links']['country:items']
	for country in countryList:
		countryName=pop=continent=None;
		if 'name' in country.keys():
			countryName = country['name']
			print countryName
		r = requests.get(country['href'])
		data = r.json()
		if 'population' in data.keys():
			pop = data['population']
		if 'country:continent' in data['_links'].keys():
			continent = data['_links']['country:continent']['name']
		f.write('%s,%s,%s\n' % (countryName, pop, continent))
	f.close()
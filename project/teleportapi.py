import requests
import urllib

def getPopulation(loc):
	payload = {'search': loc}
	r = requests.get("https://api.teleport.org/api/cities", params=payload)
	data = r.json()
	result = data['_embedded']['city:search-results'][0]
	r = requests.get(result['_links']['city:item']['href'])
	data = r.json()
	print data['population']

def getLatLng(loc):
	payload = {'search': loc}
	r = requests.get("https://api.teleport.org/api/cities", params=payload)
	data = r.json()
	result = data['_embedded']['city:search-results'][0]
	r = requests.get(result['_links']['city:item']['href'])
	data = r.json()
	print data['location']['latlon']['latitude']
	print data['location']['latlon']['longitude']

def getFullName(loc):
	payload = {'search': loc}
	r = requests.get("https://api.teleport.org/api/cities", params=payload)
	data = r.json()
	result = data['_embedded']['city:search-results'][0]
	print result['matching_full_name'].encode('utf-8')

def getCountry(loc):
	payload = {'search': loc}
	r = requests.get("https://api.teleport.org/api/cities", params=payload)
	data = r.json()
	result = data['_embedded']['city:search-results'][0]
	r = requests.get(result['_links']['city:item']['href'])
	data = r.json()
	print data['_links']['city:country']['name'].encode('utf-8')

def getContinent(loc):
	payload = {'search': loc}
	r = requests.get("https://api.teleport.org/api/cities", params=payload)
	data = r.json()
	result = data['_embedded']['city:search-results'][0]
	r = requests.get(result['_links']['city:item']['href'])
	data = r.json()
	r = requests.get(data['_links']['city:country']['href'])
	data = r.json()
	print data['_links']['country:continent']['name'].encode('utf-8')

def getSearchResults(loc):
	payload = {'search': loc}
	r = requests.get("https://api.teleport.org/api/cities", params=payload)
	data = r.json()
	for result in data['_embedded']['city:search-results']:
		print result['matching_full_name'].encode('utf-8')

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

def main():
	loc = raw_input("Enter a location: ")
	getFullName(loc)
	getPopulation(loc)
	getLatLng(loc)
	getCountry(loc)
	getContinent(loc)
	print "\nList of all results for: %s" % loc
	getSearchResults(loc)
	getImage(loc)

main()
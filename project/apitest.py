# apitest.py - This is a script to test API calls to various API's to get location specific information
import requests
import MySQLdb
import re

# This function will make a GET request to Wikipedia's endpoint and parse the response
# for the first paragraph of the page
def wikiSum(loc):
	r = requests.get("https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles="+loc)
	data = r.json()
	pageid = data['query']['pages'].keys()[0]
	print data['query']['pages'][pageid]['extract'].encode("utf-8")

# This function will make a GET request to APIXU API to get current weather information.
# This API requires an API key and has a limited # of calls
def weatherInfo(loc, key):
	r = requests.get("http://api.apixu.com/v1/current.json?key="+key+"&q="+loc)
	data = r.json();
	print "After weather get request."
	print "Location Name: %s" % data['location']['name'].encode("utf-8")
	print "Location Region: %s" % data['location']['region'].encode("utf-8")
	print "Location Country: %s" % data['location']['country'].encode("utf-8")
	print "Local Time: %s" % data['location']['localtime'].encode("utf-8")
	print "Temperature(F): %f" % data['current']['temp_f'] # value is a float
	print "Weather: %s" % data['current']['condition']['text']

# This function will make a GET request to rescountries.eu and parse the response
# for various information about a country
def getAllCountries():
	# REST Countries
	r = requests.get("https://restcountries.eu/rest/v1/all")
	data = r.json()
	print '{:50}'.format("Country") + '{:10}'.format("Population")
	for i in range(len(data)):
		print '{:50}'.format(data[i]['name'].encode("utf-8")) + '{:10d}'.format(data[i]['population'])

# This function will make a call to restcountries.eu and populate the Countries table in the RESTCountries database
def createCountriesTable():
	# establish connection to MySQL database
	db = MySQLdb.connect(host='192.168.1.101', user='root', passwd='globetrotters', db='RESTCountries')
	cur = db.cursor()
	print "Connected to MySQL DB"
	
	# delete all existing rows and reset auto increment
	cur.execute("DELETE FROM Countries")
	cur.execute("ALTER TABLE Countries AUTO_INCREMENT = 1")
	print "Reset table rows"

	# get response from restcountries api and place column data in a tuple
	r = requests.get("https://restcountries.eu/rest/v1/all")
	data = r.json()
	cur.execute("SET NAMES utf8;")
	for i in range(len(data)):
		# validate that lat/lng values exist in response for location
		if data[i]['latlng']:
			lat = data[i]['latlng'][0]
			lng =  data[i]['latlng'][1]
		else:
			lat = ""
			lng = ""
		name = data[i]['name'].encode("utf-8")
		pop = data[i]['population']
		capital = data[i]['capital'].encode("utf-8")
		region = data[i]['region'].encode("utf-8")
		subregion = data[i]['subregion'].encode("utf-8")
		cur.execute("INSERT INTO Countries (CountryName, Population, Capital, Region, SubRegion, Lat, Lng) VALUES (%s, %s, %s, %s, %s, %s, %s)", (name, pop, capital, region, subregion, lat, lng))
	print "Populated table"	

	# commit and close connection
	db.commit()
	cur.close()
	db.close()
	print "Closed the connection"


def main():
	# api key values
	weatherKey = "159c5b95dadb4378ba8195926161808"

	# regular expression search strings
	# introRE = "\"extract\":\"(?P<intro>.*)\"}"

	loop = 1
	# takes raw input data from user and formats string to use in request
	while loop == 1:
		print "API Options\n(1) Wiki API\n(2) Weather API\n(3) Get all countries\n(4) Create Countries Table\n(Q) Quit"
		option = raw_input("Select option to test response: ")
		if option == "1":
			# location options
			locSearch = raw_input("Enter a location: ")
			locSearch = locSearch.replace(" ", "%20")

			# obtain wiki summary
			wikiSum(locSearch)
			print "After wiki get request."
		elif option == "2":
			# weather options
			weatherSearch = raw_input("Enter a city, zip code, or lat/long: ")

			# obtain weather info
			weatherInfo(weatherSearch, weatherKey)
			print "After weather get request."
		elif option == "3":
			# REST Countries
			getAllCountries()
		elif option == "4":
			# update DB
			createCountriesTable()			
		elif option == "Q":
			loop = 0
			print "Exiting program"
	#print pageid
	#print r.content

	# parse strings for info
	#intro = re.search(introRE, r.content)
	#print "After string was parsed"
	#print intro.group('intro')

main()

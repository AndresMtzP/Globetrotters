import requests
import re

def wikiSum(loc):
	r = requests.get("https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles="+loc)
	data = r.json()
	pageid = data['query']['pages'].keys()[0]
	print data['query']['pages'][pageid]['extract'].encode("utf-8")

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

def getAllCountries():
	# REST Countries
			r = requests.get("https://restcountries.eu/rest/v1/all")
			data = r.json()
			print '{:40}{:20}{:30}{:20}{:30}{:25}{:25}'.format("Country","Population","Capital","Region",
				"Sub Region", "Lat.", "Long.")
			for i in range(len(data)):
				if data[i]['latlng']:
					lat = data[i]['latlng'][0]
					lng =  data[i]['latlng'][1]
				else:
					lat = ""
					lng = ""
				print '{:40}{:<20}{:<30}{:<20}{:<30}{:<25}{:<25}'.format(data[i]['name'].encode("utf-8"),data[i]['population'],
					data[i]['capital'].encode("utf-8"),data[i]['region'].encode("utf-8"),data[i]['subregion'].encode("utf-8"),
					lat,lng)

def main():
	# api key values
	weatherKey = "159c5b95dadb4378ba8195926161808"

	# regular expression search strings
	# introRE = "\"extract\":\"(?P<intro>.*)\"}"

	# takes raw input data from user and formats string to use in request
	loop = 1
	while loop == 1:
		print "API Options\n(1) Wiki API\n(2) Weather API\n(3) Get all countries\n(Q) Quit"
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
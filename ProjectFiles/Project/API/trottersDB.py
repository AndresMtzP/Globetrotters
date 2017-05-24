import MySQLdb
import json

def continentSearchDB(loc):
	db = MySQLdb.connect(host='localhost', user='root', passwd='globetrotters', db='Globetrotters', charset='utf8', use_unicode=True)
	cur = db.cursor()
	result = {}
	countryList = []

	# return row from database
	cur.execute('SELECT CountryName FROM Countries WHERE Continent = %s', loc)

	rows = cur.fetchall()
	if rows:
		for country in rows:
			countryList.append(country[0].encode('utf-8'))

	cur.close()
	db.close()
	result.update({'Countries' : countryList})
	result.update({'CountryCount' : len(countryList)})
	with open('contTest.json', 'w') as outfile:
		json.dump(result, outfile, ensure_ascii=False, encoding='utf-8') # Unescape characters
	return result

# Search for state in the States table in Globetrotters DB
def stateSearchDB(loc, locList, limit):
	db = MySQLdb.connect(host='localhost', user='root', passwd='globetrotters', db='Globetrotters', charset='utf8', use_unicode=True)
	cur = db.cursor()
	result = {}
	stateList = []
	cityList = []

	# return row from database
	cur.execute('SELECT StateName, Population, Lat, Lng, CountryName, Continent FROM States WHERE StateName = %s', loc)
	rows = cur.fetchall()
	for state in rows:
		count = len(locList)
		if count < limit:
			pop=lat=lng=country=cont=fullname=""
			if state[1] is not None:
				pop = int(state[1])
				pop = "{:,}".format(pop)
			if state[2] is not None:
				lat = state[2]
			if state[3] is not None:
				lng = state[3]
			if state[4] is not None:
				country = state[4]
			if state[5] is not None:
				cont = state[5]
			fullname='''{}, {}'''.format(state[0], country)
			tele_msg = '''{}, has a population of {} people, and is located at {} latitude, and {} longitude'''.format(state[0], pop, lat, lng)
			result = {'Name' : state[0], 'Population' : pop, 'Lat' : lat, 'Lng' : lng, 'Country' : country, 'Continent' : cont, 'Message' : tele_msg, 'Type' : 'State', 'FullName' : fullname}
			cur.execute('SELECT CityName FROM Cities WHERE StateName = %s', loc)
			cityRows = cur.fetchall()
			if cityRows:
				for city in cityRows:
					cityList.append(city[0].encode('utf-8'))
			result.update({'Within' : cityList})
			if len(cityList)>0:
				result.update({'MoreInfo' : '''{} contains a total of {} cities.'''.format(state[0],len(cityList))})
			else:
				result.update({'MoreInfo' : '''No detailed information can be found for {}.'''.format(state[0])})
			locList.append(result)
	cur.close()
	db.close()

# Searches for given country
def countrySearchDB(loc, locList, limit):
	db = MySQLdb.connect(host='localhost', user='root', passwd='globetrotters', db='Globetrotters', charset='utf8', use_unicode=True)
	cur = db.cursor()
	result = {}
	countryList = []
	stateList = []

	# return row from database
	cur.execute('SELECT CountryName, Population, Continent, (SELECT Lat FROM States WHERE CountryName = %s AND Lat IS NOT NULL AND Lng IS NOT NULL ORDER BY StateID LIMIT 1) AS Lat' 
			+ ', (SELECT Lng FROM States WHERE CountryName = %s AND Lat IS NOT NULL and Lng IS NOT NULL ORDER BY StateID LIMIT 1) AS Lng FROM Countries WHERE CountryName = %s', (loc,loc,loc))

	rows = cur.fetchall()
	for country in rows:
		count = len(locList)
		if count < limit:
			pop=cont=lat=lng=""
			if country[1] is not None:
				pop = int(country[1])
				pop = "{:,}".format(pop)
			if country[2] is not None:
				cont = country[2]
			if country[3] is not None:
				lat = country[3]
			if country[4] is not None:
				lng = country[4]
			fullname=country[0]
			tele_msg = '''{}, has a population of {} people.'''.format(country[0], pop)
			result = {'Name' : country[0], 'Population' : pop, 'Continent' : cont, 'Message' : tele_msg, 'Lat' : lat, 'Lng' : lng, 'Type' : 'Country', 'FullName' : fullname}
			cur.execute('SELECT StateName FROM States WHERE CountryName = %s', loc)
			stateRows = cur.fetchall()
			if stateRows:
				for state in stateRows:
					stateList.append(state[0].encode('utf-8'))
			result.update({'Within' : stateList})
			if len(stateList)>0:
				result.update({'MoreInfo' : '''{} contains a total of {} states.'''.format(country[0],len(stateList))})
			else:
				result.update({'MoreInfo' : '''No detailed information can be found for {}.'''.format(country[0])})
			locList.append(result)
	cur.close()
	db.close()
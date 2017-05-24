import requests


r = requests.get('https://api.teleport.org/api/continents/geonames:SA/countries/')
data = r.json()

countryList = data['_links']['country:items']


fw = open("allCountries.csv", "a+")
count = 1
for country in countryList:
	print country
	name=pop=cont=None
	r = requests.get(country['href'])
	data = r.json()
	if 'name' in data.keys():
		name = data['name']
	if 'population' in data.keys():
		pop = data['population']
	if 'country:continent' in data['_links'].keys():
		cont = data['_links']['country:continent']['name']
	fw.write("%s,%s,%s\n" % (name,pop,cont))
	count+=1
fw.close()

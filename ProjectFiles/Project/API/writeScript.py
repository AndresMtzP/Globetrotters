import requests

r = requests.get("https://restcountries.eu/rest/v1/all")
data = r.json()

f = open('countries.txt', 'w')

for i in range(len(data)):
	f.write(data[i]['name'].encode("utf-8")+"\n")

f.close()
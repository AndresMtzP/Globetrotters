import requests
import urllib

# gets image based on the location input
def getImage(loc):
	# grab coords and keyword from database or wiki tools and user input
	key = "AIzaSyDfANCLdJ72sAANtbIc55BQ2-EAdu5WiOw"
	coords = ""

	# geocode api for lat/lng
	payload = {'key' : key, 'address' : loc}
	r = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params = payload)
	#print r.url + "\n"

	# give coords value of lat and lng
	data = r.json()
	if data['results']:
		 # print data['results'][0]['geometry']['location']
		lat = str(data['results'][0]['geometry']['location']['lat'])
		lng = str(data['results'][0]['geometry']['location']['lng'])
		coords = lat + "," + lng
		#print coords

	# does a place search to get photo reference id
	payload = {'key' : key, 'location' : coords, 'radius' : '500', 'type' : '(cities)'}
	r = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json", params=payload)

	#print r.url
	if r.status_code == 200:
		data = r.json()

	# grab photo reference id for places request
	pref = data['results'][0]['photos'][0]['photo_reference']

	payload = {'key' : key, 'maxwidth' : '400', 'photo_reference' : pref}
	r = requests.get("https://maps.googleapis.com/maps/api/place/photo", params=payload)

	#print r.url
	if r.status_code == 200:
		urllib.urlretrieve(r.url,"%s.jpg" % loc)

import requests
import urllib
import os.path
from teleportapi import getLatLng

# gets image based on the lat/lng input
def getImage(loc):
	# grab coords and keyword from database or wiki tools and user input
	if (os.path.isfile("/var/www/html/Images/{}0.jpg".format(loc)) \
		and os.path.isfile("/var/www/html/Images/{}1.jpg".format(loc)) \
		and os.path.isfile("/var/www/html/Images/{}2.jpg".format(loc))):
		print("Trotter: {} images already exists".format(loc))
		return

	print("Trotter: downloading image")
	key = "AIzaSyDfANCLdJ72sAANtbIc55BQ2-EAdu5WiOw"
	latlng = getLatLng(loc)
	print latlng
	if latlng[0] is not None and latlng[1] is not None:
		coords = '{},{}'.format(latlng[0],latlng[1])
	else:
		print("Images could not be found. No lat,lng input.")
		return

	# does a place search to get photo reference id
	payload = {'key' : key, 'location' : coords, 'radius' : '500', 'type' : '(cities)'}
	r = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json", params=payload)

	if r.status_code == 200:
		data = r.json()

	placeid = data['results'][0]['place_id']
	# grab photo reference id for places request
	# pref = data['results'][0]['photos'][0]['photo_reference']

	payload = {'key' : key, 'placeid' : placeid}
	r = requests.get('https://maps.googleapis.com/maps/api/place/details/json',params=payload)

	if r.status_code == 200:
		data = r.json()

	if 'photos' in data['result'].keys():
		count = 0;
		while count < 3 and count < len(data['result']['photos']):
			pref = data['result']['photos'][count]['photo_reference']
			payload = {'key' : key, 'maxwidth' : '400', 'photo_reference' : pref}
			r = requests.get("https://maps.googleapis.com/maps/api/place/photo", params=payload)

			if r.status_code == 200:
				urllib.urlretrieve(r.url,'/var/www/html/Images/{}{}.jpg'.format(loc,count))

			count+= 1
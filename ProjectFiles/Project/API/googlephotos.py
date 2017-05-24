import requests
import urllib

key = "AIzaSyDfANCLdJ72sAANtbIc55BQ2-EAdu5WiOw"

r = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=%s&location=35.0853,-106.6056&radius=500&type=(cities)" % key)

if r.status_code == 200:
  data = r.json()
# print r.content
pref = data['results'][0]['photos'][0]['photo_reference']
print pref
r = requests.get("https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference=%s&key=%s" % (pref,key))

# req = urllib2.Requests(URL)
# res = urllib2.urlopen(req)
# finalURL = res.getURL()
# finalUrl

# print r.url
# URL = "https://lh3.googleusercontent.com/-ZqqwPtW8edE/WApdexmEvpI/AAAAAAAAAC0/t-mVoiKfM0MRKuTAZLcFEflVEvWVzowgACLIB/s1600-w400/"
urllib.urlretrieve(r.url,"Albuquerque.jpg")


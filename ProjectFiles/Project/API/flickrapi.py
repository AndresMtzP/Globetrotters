import requests
import urllib
import os.path

# URL format for images for medium sized images 800 on longest side https://farm{farm-id}.staticflickr.com/{server-id}/{id}_{secret}_c.jpg

def getImage(loc):
	if (os.path.isfile("C:\Python27\Images\{}0.jpg".format(loc)) \
		and os.path.isfile("C:\Python27\Images\{}1.jpg".format(loc)) \
		and os.path.isfile("C:\Python27\Images\{}2.jpg".format(loc))):
		print "Trotter: {} images already exists".format(loc)
		return

	print "Trotter: downloading image"
	key = "3fe696d991085740dda6a26e7fbd7954"
	payload = {'text':loc + ' cityscape', 'format':'json', 'api_key':key, 'per_page':3, 'accuracy':11, 'method':'flickr.photos.search', 'nojsoncallback':1,
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
			urllib.urlretrieve(photourl,'C:\Python27\Images\{}{}.jpg'.format(loc,count))
			count += 1

def main():
	loc = raw_input("Enter a location: ")
	getImage(loc)

main()
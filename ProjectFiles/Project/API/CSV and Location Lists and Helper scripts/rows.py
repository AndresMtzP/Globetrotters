import MySQLdb


# Cities and States
db = MySQLdb.connect(host='192.168.1.101', user='root', passwd='globetrotters', db='Globetrotters')
cur = db.cursor()
print "Connected to MySQL DB"

# delete existing rwows from cities table
cur.execute("DELETE FROM Cities")
cur.execute("ALTER TABLE Cities AUTO_INCREMENT = 1")
print "Reset table rows"

cur.execute("SET NAMES utf8;")
# get city information from text file

f = open("allCities.csv", "r")
for line in f.readlines():
	values = line.strip().split(',')
	name = values[1] if values[1] != 'None' else None
	pop = values[2] if values[2] != 'None' else None
	lat = values[3] if values[3] != 'None' else None
	lng = values[4] if values[4] != 'None' else None
	state = values[5] if values[5] != 'None' else None
	country = values[6] if values[6] != 'None' else None
	row = (name,pop,lat,lng,state,country)
	print row
	cur.execute("INSERT INTO Cities (CityName, Population, Lat, Lng, StateName, CountryName) VALUES (%s, %s, %s, %s, %s, %s)", row)
	f.close()
print "Populated table"	

# commit and close connection
db.commit()
cur.close()
db.close()
print "Closed the connection"


'''
db = MySQLdb.connect(host='192.168.1.101', user='root', passwd='globetrotters', db='Globetrotters')
cur = db.cursor()
print "Connected to MySQL DB"

# delete existing rwows from cities table
cur.execute("DELETE FROM Countries")
cur.execute("ALTER TABLE Countries AUTO_INCREMENT = 1")
print "Reset table rows"

cur.execute("SET NAMES utf8;")
# get city information from text file

f = open("allCountries.csv", "r")
for line in f.readlines():
	values = line.strip().split(',')
	name = values[0] if values[0] != 'None' else None
	pop = values[1] if values[1] != 'None' else None
	cont = values[2] if values[2] != 'None' else None
	row = (name,pop,cont)
	print row
	cur.execute("INSERT INTO Countries (CountryName, Population, Continent) VALUES (%s, %s, %s)", row)
	f.close()
print "Populated table"	

# commit and close connection
db.commit()
cur.close()
db.close()
print "Closed the connection"
'''

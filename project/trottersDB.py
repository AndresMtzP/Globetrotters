import MySQLdb

# Search for city in the Cities table in Globetrotters DB
def citySearch(loc):
	db = MySQLdb.connect(host='192.168.1.101', user='root', passwd='globetrotters', db='Globetrotters')
	cur = db.cursor()

	# return row from database
	cur.execute('SELECT * FROM Cities WHERE CityName = %s', loc)

	rows = cur.fetchall()
	print rows

	cur.close()
	db.close()

# Search for state in the States table in Globetrotters DB
def stateSearch(loc):
	db = MySQLdb.connect(host='192.168.1.101', user='root', passwd='globetrotters', db='Globetrotters')
	cur = db.cursor()

	# return row from database
	cur.execute('SELECT * FROM States WHERE StateName = %s', loc)

	rows = cur.fetchall()
	print rows

	cur.close()
	db.close()

# Searches for given country
def countrySearch(loc):
	db = MySQLdb.connect(host='192.168.1.101', user='root', passwd='globetrotters', db='Globetrotters')
	cur = db.cursor()

	# return row from database
	cur.execute('SELECT * FROM Countries WHERE CountryName = %s', loc)

	rows = cur.fetchall()
	print rows

	cur.close()
	db.close()

def main():
	loc = raw_input("Enter a location: ")
	stateSearch(loc)
	citySearch(loc)
	countrySearch(loc)

main()
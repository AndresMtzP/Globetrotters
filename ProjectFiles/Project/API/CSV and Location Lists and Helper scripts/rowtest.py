
f = open("allCities.csv", "r")
lat = ""
for line in f.readlines():
	values = line.strip().split(',')
	'''
	name = values[1] if values[1] is not None else 'NONE'
	pop = values[2] if values[2] is not None else 'NONE'
	if values[3] is None:
		lat = 'NONE TYPE'
	elif values[3] is 'None':
		lat = 'NONE STRING'
	# lat = values[3] if values[3] is not None else 'NONE'
	lng = values[4] if values[4] is not None else 'NONE'
	country = values[5] if values[5] is not None else 'NONE'
	continent = values[6] if values[6] is not None else 'NONE'
	row = (name,pop,lat,lng,country,continent)
	print "%s,%s,%s,%s,%s,%s" % (name,pop,lat,lng,country,continent)
	'''
	if values[3] == "None":
		print values[3]
f.close()
import csv
# open the csv file using the indicated delimiter and get index of city column
# to find by city
ifile = open('/home/dell/Documents/ECE490/LeonMapData/capitals.csv', "rb")
reader = csv.reader(ifile, delimiter=';')
header = reader.next()
cityIndex = header.index("City (en)")

# city hard coded, planned to have it selected by user request
city = "Baghdad"
lat = 0
long = 0

# begin search in second row after header row
rownum = 2;
for row in reader:
    if city == row[cityIndex]:
        print "Entered city found in row #" + str(rownum) + "\n"
        print "Population is " + str(row[5]) + " people.\n"
        lat = float(row[6])
        long = float(row[7])
        
        # create zoom window 10 units in each direction large
        rect = QgsRectangle(long-10, lat-10, long+10, lat+10)
        # grab the canvas
        canvas = qgis.utils.iface.mapCanvas()
        # set new focus on canvas and refresh the image
        canvas.setExtent(rect)
        canvas.refresh()
    rownum = rownum + 1;
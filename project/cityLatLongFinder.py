import csv
from qgis.core import *
from qgis.gui import *
from PyQt4 import *
from PyQt4.QtCore import QPoint
from qgis.utils import iface
import pyautogui

def zoomLocation():
    # Create a map tip
    mapTip = QgsMapTip()

    # Getting layers (2 different methods of doing so)
    #layer = QgsMapLayerRegistry.instance().mapLayers()
    #for name, layer in layer.iteritems():
    #    print name, layer.type()
    layers = iface.mapCanvas().layers()
    # Bottom line won't work with OpenLayersLayer (Google Maps, etc.)
    #layers[0].setDisplayField('NMG')

    # open the csv file using the indicated delimiter and get index of city column
    # to find by city
    ifile = open('/home/dell/Documents/ECE490/LeonMapData/capitals.csv', "rb")
    reader = csv.reader(ifile, delimiter=';')
    header = reader.next()
    cityIndex = header.index("City (en)")

    # city hard coded, planned to have it selected by user request
    city = "Adamstown"
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
            # Map coordinate
            point = QgsPoint(lat, long)
            # Pixel coordinate (maybe try to land on the center of display)
            qPoint = QPoint(1000, 1000)
            
            # create zoom window 10 units in each direction large
            rect = QgsRectangle(long-1000000, lat-1000000, long+1000000, lat+1000000)
            # grab the canvas
            canvas = iface.mapCanvas()
            # set new focus on canvas and refresh the image
            canvas.setExtent(rect)
            canvas.refresh()
            # Displaying map tip
            mapTip.showMapTip(layers[0], point, qPoint, canvas)
        rownum = rownum + 1;

def moveMouse():
    # moves mouse to the x-y pixel coordinates for a set duration
    # for actual project the coordinates will be the center of the screen
    for i in range(3):
        pyautogui.moveTo(0, 100, duration=2)
        pyautogui.moveTo(100, 100, duration=1)
        
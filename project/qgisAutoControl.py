# This script uses pyautogui to navigate the QGIS application autonomosly
# based on the input Country location
# Pixel coordinate values are based on my laptop screen (1366x768)

import csv
import pyautogui
import time

coordinateBoxX = 510
coordinateBoxY = 752
scaleBoxX = 698
scaleBoxY = 752
middleOfMapX = 742
middleOfMapY = 420

def findLocation(country):
	# open the csv file using the indicated delimiter and get index of country column
    # to find by country
    # CHANGE DIRECTORY IF NECESSARY TO CORRECT LOCATION FOR CSV FILE
	ifile = open('/home/dell/Documents/ECE490/SphereMap/countries.csv', "rb")
	reader = csv.reader(ifile, delimiter=',')
	# header is the first row containing the column names
	header = reader.next()
	countryIndex = header.index("Country")
	lat = 0
	long = 0
	
	# flag
	countryFound = 0;
	
	# begin search in second row after header row
	rownum = 2;
	for row in reader:
		if country == row[countryIndex]:
			countryFound = 1;
			print "Entered city found in row #" + str(rownum) + "\n"
			print "Population is " + str(row[1]) + " people.\n"
			lat = float(row[5])
			long = float(row[6])
		rownum = rownum + 1;
	if countryFound == 0:
		print "Country not found in local table"
	else:
		pyautogui.moveTo(coordinateBoxX, coordinateBoxY)
		#clicks and selects the entire coordinate field text (then delete and enter new one)
		pyautogui.click()
		pyautogui.keyDown('ctrlleft')
		pyautogui.press('a')
		pyautogui.keyUp('ctrlleft')
		pyautogui.typewrite(str(long) + ',' + str(lat))
		pyautogui.press('enter')

		pyautogui.moveTo(scaleBoxX, scaleBoxY)
		#clicks and selects the entire scale field text (then enter new one if required)
		pyautogui.click()
		pyautogui.keyDown('ctrlleft')
		pyautogui.press('a')
		pyautogui.keyUp('ctrlleft')
		pyautogui.press('enter')

		#goes to middle of map to show maptip
		pyautogui.moveTo(middleOfMapX, middleOfMapY)

def main():
	while(1):
		country = raw_input('Enter a country: ')
		if country == 'q':
			break;
		findLocation(country)
		print "Done navigating to location\n"
	print "Exiting"

main()

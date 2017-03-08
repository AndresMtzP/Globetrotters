import urllib
import requests
import wptools
from datafinder import getGeneral, getImage

loc = raw_input("Enter a location: ")

# tries to get population information for location
getGeneral(loc)

# saves image in python folder as loc.jpg
getImage(loc)

# OUTPUT FOR loc=Toronto AFTER RUNNING PROGRAM
# Enter a location: Toronto
# Location Name: Toronto
# Total Area (km2): 630.21
# Region: CA-ON
# Population: 2731571

# OUTPUT FOR loc=San Diego AFTER RUNNING PROGRAM
# Enter a location: San Diego
# Water area (km2): 122.27
# Location Name: San Diego, California
# Total Area (km2): 964.51
# Region: US-CA
# Population: 1394928
# Land Area (km2): 842.23
import requests
import wptools
import re

# coord\|(?P<lat>[0-9]+)|((\|[0-9]+)+)\|(?P<NS>[A-Z])\|(?P<lng>[0-9]+)((\|[0-9]+)+)\|(?P<EW>[A-Z])\|
# relevant information from dictionary after wptools.page('').get_parse()
# 'population_total', 'coordinates'

coordsRE = re.compile(r'(?P<lat>[0-9]+)((\|[0-9]+)+)?\|(?P<NS>[A-Z])\|(?P<lng>[0-9]+)((\|[0-9]+)+)?\|(?P<EW>[A-Z])\|', re.IGNORECASE)
location = wptools.page('San Diego', silent=True).get_parse()
locInfo = location.infobox

coords = locInfo['coordinates']

# location information from infobox
print locInfo['population_total']

regex_matches = re.search(coordsRE, coords)

print regex_matches.group('lat')
print regex_matches.group('NS')
print regex_matches.group('lng')
print regex_matches.group('EW')
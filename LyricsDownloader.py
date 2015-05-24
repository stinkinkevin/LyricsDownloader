import codecs
import json
import sys
import bs4
from bs4 import BeautifulSoup
import urllib, urllib2

ArtistInput = raw_input("Artist: ")
SongInput = raw_input("Song: ")

def Extraction(webpage):
	soup = bs4.BeautifulSoup(webpage)
	result = []
	for tag in soup.find('div', 'lyricbox'):
		if isinstance(tag, bs4.NavigableString):
			if not isinstance(tag, bs4.element.Comment):
				result.append(tag)
		elif tag.name == 'br':
			result.append('\n')
	return "".join(result)


Query = urllib.urlencode(dict(artist=ArtistInput, song=SongInput, fmt="realjson"))
Response = urllib2.urlopen("http://lyrics.wikia.com/api.php?" + Query)
Output = json.load(Response)

if (Output['lyrics'] != 'Not found'):
	# print sneak peek
	#print(data['lyrics'])
	Lyrics = Extraction(urllib2.urlopen(Output['url']))
	print Lyrics
	IsSaveToFile = raw_input("Save to File?(y/n)")
	if (IsSaveToFile == 'y'):
		OutputPath = raw_input("Export to: ")
		OutputPath = "%s//%s - %s.txt" % (OutputPath, Output['artist'], Output['song'])
		with codecs.open(OutputPath, 'w', encoding='utf-8') as output_file:
			output_file.write(Lyrics)
		print("Finished writing '%s'" % OutputPath)
else:
	sys.exit('Lyrics not found')

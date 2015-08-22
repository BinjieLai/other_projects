
from __future__ import division
import numpy as np
import re
import random
import pygmaps
import csv

def ruturnIndex(line):
	counter = 0
	temp1 = 0
	temp2 = 0
	flag1 = False
	flag2 = False
	for i in line:
		if (i == 'victim'):
			if flag1 != True:
			    # this flag to ensure the first 'victim' is registered
			    # in a few cases the word count in one line of the word 'victim'
			    # is more than 1
				temp1 = counter
			flag1 = True
		if i == 'shooting' or i == 'stabbing' or i == 'blunt_force' or i == 'asphyxiation':
			if flag2 !=True:
				temp2 = counter
			flag2 = True
		else:
			counter = counter + 1

	# if the cause of death isn't listed above
	# the cause will be 'unknown'
	if temp1 == 0:
		line.insert(12,'no notes')
		temp1 = 12

	if temp2 == 0:
		line.append('unknown')
		temp2 = len(line)-1

	if temp2 == len(line)-1:
		line.append('no extra notes')

	return line, temp1, temp2
'''
	Description: It creates an address string.
				Based on the location of the zip
				it will join the words between the last name
				and the zip code not inclusive.
	PARAMETER: it takes a list of words

'''
def address(line):
	if re.search("\d\d\d\d\d",line[6]):
		line[4] = str(" ".join(line[4:6]))
		del line[5:6]
	elif re.search("\d\d\d\d\d",line[7]):
		line[4] = str(" ".join(line[4:7]))
		del line[5:7]
	elif re.search("\d\d\d\d\d",line[8]):
		line[4] = str(" ".join(line[4:8]))
		del line[5:8]
	elif re.search("\d\d\d\d\d",line[9]):
		line[4] = str(" ".join(line[4:9]))
		del line[5:9]
	elif re.search("\d\d\d\d\d",line[10]):
		line[4] = str(" ".join(line[4:10]))
		del line[5:10]
	return line


# <.*?>

def CleanData(line):
	line = re.sub("icon_*[\S]*_*[\S]*","",line).lower()
	line = re.sub("\'p\d*\'","",line)
	line = re.sub("href=\"http://+[^\s]*>", "",  line)
	line = re.sub("</*p>","",line)
	line = re.sub(" class=\"popup-note\">",", ",line)
	line = re.sub("<br />",", ",line)
	line = re.sub("<*>", "",line)
	line = re.sub("<*<dd*", "",line)
	line = re.sub(" class=\"address\"",", ",line)
	line = re.sub("</[dtl][dtl]",", ",line)
	line = re.sub("cause: |age: |gender: | race:|read the article","",line)
	line = re.sub("baltimore|md|year*s*|old|jr.|sr.|found on","",line)
	line = re.sub("name not yet released", "unkonwn unknown",line)
	line = re.sub("blunt force","blunt_force",line)
	line = re.sub("\s*,\s*"," ",line)
	line = re.sub("\'lt|\'","",line)
	line = re.sub("\'p\d*\'","",line)
	line = re.sub("</*a|/a", "", line).split()

	# combine the address enteries in a single string
	if (len(line) < 10):
		line = []
	else:
		line = address(line)
		line, t1, t2 = ruturnIndex(line)

		line[t1] = str(" ".join(line[t1:t2]))

		line[t2+1] = str(" ".join(line[t2+1:]))

		del line[t2+2:]
		del line[t1+1:t2]


	return line

def main():
    # reader = csv.reader(open("aqi_china.csv", 'rU'), dialect='excel')
    # for row in reader:
    #     print row

    data = list(open("aqi_china.csv", 'rU'))
    data = data[1:]
    mymap = pygmaps.maps(32, 106, 5)
    color = "#0000FG"
    for item in data:
		item = item.split(',')
		aqi = int(item[3])
		#if (len(item) == 15):
		if aqi <= 50:
			color = "#00FF00" # green
		elif aqi <= 100:
			color = "#FFA500" # orange
		elif aqi > 100:
			color = "#FF0000" # red
		#print color
		mymap.addpoint(float(item[1]), float(item[0]), color)
    mymap.draw('./aqi_map.html')

if __name__ == "__main__":
	main()


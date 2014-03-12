#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import re
import csv
import requests
import os
#from pattern.web import URL
from BeautifulSoup import BeautifulSoup

from time import strptime, strftime
from string import split

#get most recent
#save the pdf off the wesbite:
#####HOW HOW DO I DO THIS?#####
#requests. Get. Fuck. get most recent via Beautiful Soup#

#url = URL(pdf_url)
#f = open('url', 'wb')
#f.write(url.download(cached=False))
#f.close()

#run a quick pdftotext script
#subprocess.call
#or os.system. let's do that. Basically get path of that fucker, and FUCK IT UP.


#but let's work with a test case for now. 
file_path = 'CPD5391.txt'
with open (file_path, "r") as livefile:
	data = livefile.read()

header_pattern = re.compile('\f.*\n.*')
strip_headers = re.sub(header_pattern,'', data)
print strip_headers
#print strip_headers

pattern = re.compile('(?=(\d{5}\s+)((.|\n)*?)(LOCATION: )((.|\n)*?)(OCCURRED: )(.*?)(REPORTED: )((.|\n)*?)(OFFICER: )((.|\n)*?)(SUMMARY: )((.|\n)*?)((PROPERTY: )((.|\n)*?))?(PEOPLE: )((.|\n)*?)((ARRESTS: )((.|\n)*?))?(C13-\d{5}|\Z))')
#with properties.. (nonfunctional)
#(?=(\d{5}\s+)((.|\n)*?)(LOCATION: )((.|\n)*?)(OCCURRED: )(.*?)(REPORTED: )((.|\n)*?)(OFFICER: )((.|\n)*?)(SUMMARY: )((.|\n)*?)((PROPERTY: )((.|\n)*?))?(PEOPLE: )((.|\n)*?)((ARRESTS: )((.|\n)*?))?(C13-\d{5}|\Z))
#no property
#(?=(\d{5}\s+)((.|\n)*?)(LOCATION: )((.|\n)*?)(OCCURRED: )(.*?)(REPORTED: )((.|\n)*?)(OFFICER: )((.|\n)*?)(SUMMARY: )((.|\n)*?)(PEOPLE: )((.|\n)*?)((ARRESTS: )((.|\n)*?))?(C13-\d{5}|\Z))

incidents = pattern.findall(strip_headers)
print incidents

j = 0

for i in incidents:
	j += 1
	print j
	code = i[0].strip()
	print code
	description = i[1].strip()
	print description
	location = i[4].strip()
	print location
	datetime_occurred = i[7].strip()
	print datetime_occurred
	datetime_reported = i[9].strip()
	print datetime_reported
	reporting_officer = i[12].strip()
	print reporting_officer
	summary = i[15].strip()
	print "Summary"
	print summary
	properties = i[19].strip()
	print properties
	people = i[22].strip()
	print people
	arrests = i[26].strip()
	arrests += i[27].strip()
	print arrests

	arrest_pattern = re.compile('(.*)(AGE: )(\d+)\s+(SEX: )(M|F)(\s+)(.*)\n(.*)(CHARGE: )(\w+)\s+(.*)\n(.*)(AT: )(.*)(BY: )(.*)')

	arrests_re = arrest_pattern.findall(arrests)
	x = 0
	for a in arrests_re:
		x = x+1
		print x
		print a


	# (C\d{2}-\d{5}\s+)(.*?)(\s{3,})(.*?)(LOCATION: )(.*?)(\n)

	#(C\d{2}-\d{5}\s+)(.*?)(\s{3,})(.*?)(LOCATION: )(.*?)(\n+)(\s+)(OCCURRED: )(.*?)(REPORTED: )(.*?)(\n+)(\s+)(OFFICER: )(.*?)(\n+)(\s+)(SUMMARY: )

	#

#Pe

#arrests
#(.*)(AGE: )(\d+)\s+(SEX: )(M|F)(\s+)(.*)\n(.*)(CHARGE: )(\w+)\s+(.*)\n(.*)(AT: )(.*)(BY: )(.*)

#how do we parse people?
#have Victim pattern. Repeat as necessary. Victim is mandatory at least once.


#((VICTIM)\s+AGE: (.*)SEX: (M|F)(.*))|(VICTIM|OFFENDER)(.*)

#Have offender hattern

#TODO:
#ARRESTS: (.*)(AGE: )(\d+)\s+(SEX: )(M|F)(\s+)(.*)\n(.*)(CHARGE: )(\w+)\s+(.*)\n(.*)(AT: )(.*)(BY: )(.*)
#PEOPLE: ((VICTIM)\s+AGE: (.*)SEX: (M|F)(.*))|(VICTIM|OFFENDER)(.*)
#PROPERTY: (DAMAGED|BURNED|STOLEN|LOST|NONE)(.*)(\d+)(.*)




'''

(?=
0	(\d{5}\s+)
1	(
2		(.|\n) *?)
3	(LOCATION: )
4	(
5		(.|\n) *?)
6	(OCCURRED: )
7	(.*?)
8	(REPORTED: )
9	(
10		(.|\n)*?)
11	(OFFICER: )
12	(
13		(.|\n)*?)
14	(SUMMARY: )
15	(
16		(.|\n)*?)
17	(
18		(PROPERTY: )
19		(
20			(.|\n)*?) )?
21	(PEOPLE: )
22	(
23		(.|\n)*?)
24	(
25		(ARRESTS: )
26		(
27			(.|\n)*?))?
28	(C13-\d{5}|\Z))?


'''
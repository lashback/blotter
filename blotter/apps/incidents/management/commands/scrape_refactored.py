#!/usr/bin/env python

# coding=utf-8
import re
import csv
import requests
import os
#from pattern.web import URL
import bs4
#import lxml.html, urllib2, urlparse
import glob
#from django import DatabaseError

from time import strptime, strftime
from string import split
from django.core.management.base import BaseCommand
from apps.incidents.models import *
from settings.common import SITE_ROOT

import datetime

#tasks:
	#create list of cities and other locations
	#Use it to identify CH, UR, Champaign, Urbana introduced in REGEX and do beter handling so that it geocodes. 


working_dir = os.path.join(SITE_ROOT, '../data')

class Command(BaseCommand):
	#def parse_crimes(crimes):
#			print crimes_array
	#		return crimes


	def handle(self, *args, **options):
		agencies = ['Champaign', 'Urbana']
		
		for a in agencies:
			pdfs = self.get_pdfs(a)
			texts = self.convert_to_text(a, pdfs)

			self.load_into_db(a, texts)
	
	
	def get_pdfs(self, agency):
		champaign_base = 'http://archive.ci.champaign.il.us/cpd-reports/'
		urbana_base = 'http://www.city.urbana.il.us/_Police_Media_Reports/'
		uipd_base = 'http://www.dps.uiuc.edu/clery/cleryrpts.html'

		if agency == 'Champaign':
			base = champaign_base 
		else:
			base = urbana_base
		
		c = requests.get(base)

		if c.status_code == 200:
			soup = bs4.BeautifulSoup(c.content)
			if agency == 'Champaign':
				links = soup.select('#listing a')
			else:
				links = soup.select('.CellColor5 a')
			pdf_list = []
			print "Scrape: Evaluating %s links" % len(links)
			#$print links
			for link in links:
				#print link
				link_tag = link['href']
				if agency == 'Champaign':
					file_name = link_tag.split('arms/')[1].strip()
				else:
					file_name = link_tag.split('/_Police_Media_Reports/')[1].strip()
				#print "Filename: " + file_name
				if not os.path.exists(working_dir):
					os.makedirs(working_dir)

				if not os.path.exists('%s/pdf/%s/' % (working_dir, agency)):
					os.makedirs('%s/pdf/%s/' % (working_dir, agency))


				if not os.path.exists('%s/pdf/%s/%s' % (working_dir, agency, file_name)):
					if agency == 'Champaign':
						link_url = "http://archive.ci.champaign.il.us/cpd-reports/arms/" + file_name
					else:
						link_url = base + file_name

					r = requests.get(link_url)
					print 'Downloading %s' % file_name

					if r.status_code == 200:
						directory = str('%s/pdf/%s/%s' % (working_dir, agency, file_name))
					#	print directory
						with open(directory, 'wb') as writefile:
							writefile.write(r.content)
						pdf_list.append(directory)

					else:
						print "Failed downloading %s" % file_name


		else:
			print "Doctor Jones Doctor Jones!"
		#print pdf_list
		return pdf_list


	def convert_to_text(self, agency, pdfs):
		#directory = working_dir + '/pdf/%s' % agency
		#pdfs_list = glob.glob(directory + '/*.PDF')
		text_list = []
		for pdf in pdfs:
			print pdf 
			name = pdf.strip('.PDF')
			os.system('pdftotext -enc UTF-8 -layout %s '%pdf)
			path = name + '.txt'
			print path
			text_list.append(path)
		#print text_list
		print text_list
		return text_list

		#first check to see if it has been turned into text


	
	def load_into_db(self, agency, texts):
		directory = working_dir + '/pdf/%s' % agency
		def clean(string):
			line = re.compile('\n')
			excess_spaces = re.compile('\s{2,}')
			string = re.sub(line, "", string)
			string = re.sub(excess_spaces, " ", string)
			string = string.strip()

			return string	
		#make this more complicated
		def parse_address(string, agency):
			
			######################
			#Thing 1: Check for a "slash" that'll show it as an intersection.
			#Thing 2: Check for "block" that'll show it as a block
			#Thing 3: Make this entire fucking smaller, jesus.

			location_pattern = re.compile('(.*)\s{3,}(.*)')
			location_regexed = location_pattern.search(string)
			
			city_pattern = re.compile('(.*)(\s\w+\s+IL)')
			city_regexed = city_pattern.search(string)

			intersection_checker = string.split('/')
			
			print "Raw"	
			print string
			print "Intersection Checker"
			print intersection_checker
			print "City Regex"
			print city_regexed
			print "Location Regex"
			print location_regexed
			
			if len(intersection_checker)>1:
				print clean(string)
				location_import, location_created = Location.objects.get_or_create(
					address = clean(string),
					intersection_indicator = True,
					agency = agency,
					name = None
					)	

			#fuckfuckfuckfuck.
			elif city_regexed:
				location_address = clean(city_regexed.group(1).strip())
				location_city = clean(city_regexed.group(2).strip())
				print location_address
				print location_city

				location_import, location_imported = Location.objects.get_or_create(
					address = location_address,
					city = location_city,
					name = None
					)
			elif location_regexed:
				
				
				location_address = clean(location_regexed.group(1).strip())
				location_name = clean(location_regexed.group(2).strip())
				print "Name found"
				print location_address
				print location_name
				location_import, location_imported = Location.objects.get_or_create(
					address = location_address,
					name = location_name,
					agency = agency
				)

			else:

				location = clean(string) 
				print "No name found"
				print location
				location_import, location_imported = Location.objects.get_or_create(
				address = location,
				name = None,
				agency = agency
				)
			
			
			return location_import

		#print text_files
		for t in texts:
			
			print t
			with open (t, "r") as livefile:
				data = livefile.read()
			#occassionally unicodedecode error
			data = data.decode('utf-8')
			header_pattern = re.compile('\f.*\n.*')
			strip_headers = re.sub(header_pattern,'', data)

			####There's so much that has to be done with this. 
			#	1. Exceptions for when they mention some shit about you know shit and things.
			#	2. The options are making everything super frustrating. Clean it up!
			## oh my fucking god just add a beginning of line character before the final fucker.
			pattern = re.compile('(?=(\d{5}\s+)((.|\n)*?)(LOCATION: )((.|\n)*?)(OCCURRED:)(.*?)(REPORTED:)((.|\n)*?)(OFFICER: )((.|\n)*?)((SUMMARY: )((.|\n)*?))?((PROPERTY: )((.|\n)*?))?(PEOPLE: )((.|\n)*?)((ARRESTS: )((.|\n)*?))?\n(((C|U|W)\d{2}-\d{5})|\Z))')
			
			
			incidents = pattern.findall(strip_headers)
			#print incidents
			count = len(incidents)
			j = 0
			for i in incidents:
				try:
					#print "Here are the things"
					#print i
					j = 0
					#while j<len(i):
				#		
						#print "%s:%s" % (j, i[j])
						#print "Key: %s"%j
						#print "Length: %s" % len(i[j])
						#print "Contents: %s" % i[j]
				#		
				#		if len(i[j]) > 255:
				#			print "YOUR REGEX DONE FUCKED"
				#			print strip_headers
					#	j+=1


					incident_number = clean(i[0].strip())
					#print code
					description = i[1].strip()
					#print description
					location = i[4].strip()

					datetime_occurred = datetime.datetime.strptime(clean(i[7].strip()),'%m/%d/%Y %H:%M')
					#print datetime_occurred
					datetime_reported = datetime.datetime.strptime(clean(i[9].strip()), '%m/%d/%Y %H:%M')
					reporting_officer = clean(i[12].strip())
					summary = clean(i[16].strip())
					properties = i[20].strip()
					people = i[23].strip()
					arrests = i[27].strip()
					arrests += i[28].strip()

					agency_object, agency_created = Agency.objects.get_or_create(
						name = agency
						)

					incident_location = parse_address(location, agency_object)
					
					incident_officer, io_bool = Officer.objects.get_or_create(
						name = reporting_officer
						)
					incident_import, incident_created = Incident.objects.get_or_create(
						agency = agency_object,
						code = incident_number,
						datetime_occurred = datetime_occurred,
						datetime_reported = datetime_reported,			
						summary = summary,
						officer = incident_officer,
						location_occurred = incident_location,
						)

					incident_import.raw_entry = i
					incident_import.save()
					
					crime_list = description.split('\n')
					
					for c in crime_list:
						
						#print c
						#print '\n'

						crime = c.strip()

						crime_pattern = re.compile('(.*)\s+((CPD|UPD|\d{3}).*)')
						crime_parsed = crime_pattern.findall(crime)
					#	print "Parsed: "
					#	print crime_parsed
						if len(crime_parsed) > 0 and len(crime_parsed[0]) > 1:
							name = crime_parsed[0][0].strip()
							code = crime_parsed[0][1].strip()
					#		print "Name: %s" % name.strip()	
					#		print "Code: %s" %code.strip()
							incident_crime, incident_created = Crime.objects.get_or_create(
								name = name,
							)
							incident_crime.code = code.strip()
							incident_crime.save()
						else:
							name = crime
						#	print name
							incident_crime, incident_created = Crime.objects.get_or_create(
							name = name,
							)

						incident_import.crimes.add(incident_crime)
						incident_import.save()

					if incident_import:	
						j+=1
						print "%s imported" % incident_number

					arrest_pattern = re.compile('(.*)(AGE: )(\d+)\s+(SEX: )(M|F)(\s+)(.*)\n(.*)(CHARGE: )(.*)\n(.*)(AT: )(.*)(BY: )(.*)')
					arrests_re = arrest_pattern.findall(arrests)
					total_arrests = 0
					for a in arrests_re:
						total_arrests += 1
						arrestee = 	clean(a[0].strip())
						age = 		clean(a[2].strip())
						sex = 		clean(a[4].strip())
						address = 	a[6].strip()
						charge = 	a[9].strip()
						arrest_location_string = a[12].strip()
						arresting_officer = clean(a[14].strip())			

						print "Arrestee Address:"
						arrestee_address = parse_address(address, agency_object)
						print ""
						arrest_location = parse_address(arrest_location_string, agency_object)
						

						arresting_officer_import, arrest_officier_bool = Officer.objects.get_or_create(
							name = arresting_officer
							)
						print "\n\n\nTHIS IS ARRESTS:"
						print charge
						crime_pattern = re.compile('(.*)\s+((CPD|UPD|\d{3}).*)')
						crime_parsed = crime_pattern.findall(charge)
						print "Parsed: "
						print crime_parsed
						if len(crime_parsed) > 0 and len(crime_parsed[0]) > 1:
							name = crime_parsed[0][0].strip()
							code = crime_parsed[0][1].strip()
							print "Name: %s" % name.strip()	
							print "Code: %s" %code.strip()
							crime_import, crime_imported = Crime.objects.get_or_create(
							name = name
							)
							crime_import.code = code
							crime_import.save()
						else:
							name = charge.strip()
							print name
							crime_import, crime_imported = Crime.objects.get_or_create(
							name = name
							)


						arrestee_import, arrestee_bool = Arrestee.objects.get_or_create(
							name = arrestee,
							age = age,
							sex = sex,
							address = arrestee_address
							)


						arrest_import, arrest_bool = Arrest.objects.get_or_create(
							arrestee = arrestee_import,
							location = arrest_location,
							datetime = datetime_occurred,
							officer = arresting_officer_import

							)

						arrest_import.charges.add(crime_import)
						arrest_import.save()
						incident_import.arrests.add(arrest_import)


						print "Arrests added to %s" %incident_number
					
					print "Total arrests for %s: %s" % (incident_number, total_arrests)
					#this might be useless
					print ("%s successfully imported!" % j)

				except:	
					print ("In %s, %s didn't import! Figure it out, dude!" % (t, incident_number ))
			
			#How well did it perform?
			if count > 0:
				percent_imported = int(100*j/count)
			else:
				percent_imported = 0
			print "In %s, %s percent imported" % (t, percent_imported)

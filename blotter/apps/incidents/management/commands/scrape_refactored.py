#!/usr/bin/env python
# -*- coding: utf-8 -*- 
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

working_dir = os.path.join(SITE_ROOT, '../data')
#directory = os.path.join(working_dir, 'test/archive.ci.chamapign.il.us/cpd-reports/arms/')
#list_date = []
#today = datetime.date.today()
#list_date.append(today)
#directory = os.path.join(working_dir, str(list_date[0]))
#print directory
class Command(BaseCommand):


	def handle(self, *args, **options):
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

	#####HOWSABOUTS we send each function a list of newly-scraped files? Check to see if the directory exists, IF NOT get the file, save it, add it to a list

		#but let's work with a test case for now. 
		#agencies = ['Champaign', 'Urbana']
		agencies = ['Urbana']
		for a in agencies:
			pdfs = self.get_pdfs(a)
			texts = self.convert_to_text(a, pdfs)

			self.load_into_db(a, texts)

	#def get_most_recent_pdf(self):
		#pass

	
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
				print link
				#Okay, so this hates me right now. Why does it hate me??
				link_tag = link['href']

				#print link_tag

				if agency == 'Champaign':
					file_name = link_tag.split('arms/')[1].strip()
				else:
					file_name = link_tag.split('/_Police_Media_Reports/')[1].strip()
				
				print "Filename: " + file_name
				
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
						print directory
						with open(directory, 'wb') as writefile:
							writefile.write(r.content)
						pdf_list.append(directory)

					else:
						print "Failed downloading %s" % file_name


		else:
			print "Oh my god not again"
		print pdf_list
		return pdf_list
		#os.system('wget --random-wait -nd -r -e robots=off -A.PDF -P %s %s' % (directory, champaign_base))
		#maybe this can just be an os.system command
		#make it a date
		# fetch the page
		#res = urllib2.urlopen(champaign_base)

		# parse the response into an xml tree
		#tree = lxml.html.fromstring(res.read())

		# construct a namespace dictionary to pass to the xpath() call
		# this lets us use regular expressions in the xpath
		# iterate over all <a> tags whose href ends in ".pdf" (case-insensitive)
		#for node in tree.xpath('//a[re:test(@href, "\.PDF$", "i")]'):
		    # print the href, joining it to the base_url
		 #   pdf = urlparse.urljoin(base_url, node.attrib['href'])
		  #  os.system('wget -P %s ')
		#r = requests.get(champaign_base)
		#pdf_soup = BeautifulSoup(r.text)

		#maketoday's date 



		###########################################
		##Alternatively, I can set up a function through Soup that will grab the urls
		##DEFINITELY need some way to see whether it's already been crawled. Could bite us in the ass. 
		##


	def convert_to_text(self, agency, pdfs):
		#directory = working_dir + '/pdf/%s' % agency
		#pdfs_list = glob.glob(directory + '/*.PDF')
		text_list = []
		for pdf in pdfs:
			print pdf 
			name = pdf.strip('.PDF')
			os.system('pdftotext -layout %s '%pdf)
			path = name + '.txt'
			print path
			text_list.append(path)
		print text_list
		print "hopefully not in here"
		return text_list

		#first check to see if it has been turned into text

	
	def load_into_db(self, agency, texts):
		directory = working_dir + '/pdf/%s' % agency			
	#	print "i'm in it."
		def clean(string):
			line = re.compile('\n')
			excess_spaces = re.compile('\s{2,}')
			string = re.sub(line, "", string)
			string = re.sub(excess_spaces, " ", string)

			return string
		
	#	print "i'm in something"
		

		#print text_files
		for t in texts:
			#print t
			with open (t, "r") as livefile:
				data = livefile.read()

			header_pattern = re.compile('\f.*\n.*')
			strip_headers = re.sub(header_pattern,'', data)
			pattern = re.compile('(?=(\d{5}\s+)((.|\n)*?)(LOCATION: )((.|\n)*?)(OCCURRED:)(.*?)(REPORTED:)((.|\n)*?)(OFFICER: )((.|\n)*?)(SUMMARY: )((.|\n)*?)((PROPERTY: )((.|\n)*?))?(PEOPLE: )((.|\n)*?)((ARRESTS: )((.|\n)*?))?(C|U\d{2}-\d{5}|\Z))')
			incidents = pattern.findall(strip_headers)
			#print incidents

			j = 0
			#write function that eats extra whitespace characters. 
			print 'still in'
			for i in incidents:
				try:
					j += 1
					code = clean(i[0].strip())
					print code
					description = clean(i[1].strip())
					print description
					location = i[4].strip()

					datetime_occurred = datetime.datetime.strptime(clean(i[7].strip()),'%m/%d/%Y %H:%M')
					print datetime_occurred
					datetime_reported = datetime.datetime.strptime(clean(i[9].strip()), '%m/%d/%Y %H:%M')
					reporting_officer = clean(i[12].strip())
					summary = clean(i[15].strip())
					properties = i[19].strip()
					people = i[22].strip()
					arrests = i[26].strip()
					arrests += i[27].strip()

					agency_object, agency_created = Agency.objects.get_or_create(
						name = agency
						)

					location_pattern = re.compile('(.*)\s{5,}(.*)')
					location_parsed = location_pattern.findall(location)

					print location_parsed
					if len(location_parsed) > 1:
						location_address = clean(location_parsed[0])
						location_name = clean(location_parsed[1])
						
						incident_location, incident_location_bool = Location.objects.get_or_create(
						address = location_address,
						name = location_name,
						agency = agency_object
						)
					else:
						incident_location, incident_location_bool = Location.objects.get_or_create(
						address = location,
						agency = agency_object
						)

					arrest_pattern = re.compile('(.*)(AGE: )(\d+)\s+(SEX: )(M|F)(\s+)(.*)\n(.*)(CHARGE: )(\w+)\s+(.*)\n(.*)(AT: )(.*)(BY: )(.*)')
					arrests_re = arrest_pattern.findall(arrests)
					
					incident_crime, incident_created = Crime.objects.get_or_create(
						name = description
						)

					incident_location, incident_location_bool = Location.objects.get_or_create(
						address = location
						)
					incident_officer, io_bool = Officer.objects.get_or_create(
						name = reporting_officer
						)
					incident_import, incident_created = Incident.objects.get_or_create(
						agency = agency_object,
						code = code,
						datetime_occurred = datetime_occurred,
						datetime_reported = datetime_reported,			
						#datetime_occurred = datetime_occurred.strftime( '%Y-%m-%d %H:%M:%S'),
						#datetime_reported = datetime_reported.strftime('%Y-%m-%d %H:%M:%S'),
						summary = summary,
						officer = incident_officer,
						location_occurred = incident_location,
						)
					incident_import.crimes.add(incident_crime)
					incident_import.save()


					for a in arrests_re:
						arrestee = 	clean(a[0].strip())
						age = 		clean(a[2].strip())
						sex = 		clean(a[4].strip())
						address = 	clean(a[6].strip())
						charge_text=clean(a[9].strip())
						charge_code=clean(a[10].strip())
						arrest_location = clean(a[13].strip())
						arresting_officer = clean(a[15].strip())

						
						crime_import, crime_bool = Crime.objects.get_or_create(
							name = charge_text,
							code = charge_code
							)
						address_import, address_bool = Location.objects.get_or_create(
							address = address
							)

						arrestee_import, arrestee_bool = Arrestee.objects.get_or_create(
							name = arrestee,
							age = age,
							sex = sex,
							address = address_import
							)
						arrest_location_import, arcreated = Location.objects.get_or_create(
							address = arrest_location
							)
						arrest_import, arrest_bool = Arrest.objects.get_or_create(
							arrestee = arrestee_import,
							location = arrest_location_import,
							datetime = datetime_occurred

							)
#						print arrestee_import

						arrest_import.charges.add(crime_import)
						arrest_import.save()
				
					if arrests_re:
						incident_import.arrests.add(arrest_import)
						incident_import.save()
					print ("%s successfully imported!" % code)

				except:
					print ("In %s, %s didn't import! Figure it out, dude!" % (t, code ))
		
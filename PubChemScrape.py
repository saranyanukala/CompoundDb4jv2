#Script to Download Patent Data
#This Script can be used to extract any data from the xml file
#INPUT : MapNotFound.csv
#OUTPUT : FinalData.csv, FinalApplicant.csv,FinalInventor.csv, FinaNotFound.csv

import urllib.request
import xml.etree.ElementTree as ET
from url import *
import time
#patent = input("\nEnter Patent ID: ")

fhand = open ("/sas/vidhya/CompoundDb4jV2/USPTO/data/MapNotFound.csv")
file1 = open ("/sas/vidhya/CompoundDb4jV2/USPTO/data/scrape/FinalData.csv","a")
file2 = open ("/sas/vidhya/CompoundDb4jV2/USPTO/data/scrape/FinalApplicant.csv","a")
file3 = open ("/sas/vidhya/CompoundDb4jV2/USPTO/data/scrape/FinalInventor.csv","a")
file4 = open ("/sas/vidhya/CompoundDb4jV2/USPTO/data/scrape/FinalNotFound.csv","a")

count = 1
start_time = time.time()
for line in fhand:
	if (count%100 == 0):
		print(count)
	if (count%100000 == 0):
		break
	#print ("Patents Parsed :",count)
	PatN = line.rstrip().split("\t")
	if (len(PatN) > 1):
		syns = PatN[1].split()
		PatN = PatN[0]
	else:
		syns = PatN
		PatN = PatN[0]
	flag = 0
	syns.reverse()
	for patent in syns:
		url_name = url_patent_name(patent)
		url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/patent/"+url_name+"/XML/?response_type=display"
		#url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/patent/"+url_name+"/XML/?response_type=save&amp;response_basename=Patent_"+url_name
		try:
			s = urllib.request.urlopen(url)
			contents = s.read()

			f = open("Patent.xml", 'wb')
			f.write(contents)
			f.close()
		except:
			#print("Error 404  " + patent)
			continue  # 404 Not Found Error 

		#print ("\nDownloaded Patent Data of :",patent,"\n")

		try:
			tree = ET.parse("Patent.xml")
			root = tree.getroot()
		except:
			print("Parse Error  " + patent)
			continue # Parse Error

		flag = 1

		subDate = 'NULL'
		grantDate = 'NULL'
		Title = 'NULL'
		Applicant = []
		Inventor = []
		Title = root.find('{http://pubchem.ncbi.nlm.nih.gov/pug_view}RecordTitle').text
		
		for info in root.iter('{http://pubchem.ncbi.nlm.nih.gov/pug_view}Information'):
			#subD = False
			grantD = False
			title = False
			app = False
			inv = False
	
			for name in info.findall('{http://pubchem.ncbi.nlm.nih.gov/pug_view}Name'):
				if (name.text == 'Patent Submission Date'):
					subD = True
				elif (name.text == 'Grant Date'):
					grantD = True
				elif (name.text == 'Patent Applicant'):
					app = True
				elif (name.text == 'Inventor'):
					inv = True

			i = info.find('{http://pubchem.ncbi.nlm.nih.gov/pug_view}Value')
			for value in i.iter():
				if (app and value.tag == "{http://pubchem.ncbi.nlm.nih.gov/pug_view}String"):
					Applicant.append(value.text)
					
				if (inv and value.tag == "{http://pubchem.ncbi.nlm.nih.gov/pug_view}String"):
					Inventor.append(value.text)

				if (grantD and value.tag == "{http://pubchem.ncbi.nlm.nih.gov/pug_view}DateISO8601"):
					grantDate = value.text

				#if (subD and value.tag == "{http://pubchem.ncbi.nlm.nih.gov/pug_view}DateISO8601"):
				#	subDate = value.text

		record = PatN + "|" + url_name + "|" + grantDate + "|" + Title + "\n"
		
		file1.write(record)
		
		for name in Applicant:
			file2.write(PatN+"|"+name+"\n")
		
		for name in Inventor:
			file3.write(PatN+"|"+name+"\n")

		#print(str(Applicant))
		#print(str(Inventor))
		#print(record)
		if (flag == 1):
			break	
	if (flag == 0):
		#print("Not found")
		file4.write(PatN + "\n")
	count+=1

fhand.close()
file1.close()
file2.close()
file3.close()
file4.close()
print("--- %s seconds ---" % (time.time() - start_time))

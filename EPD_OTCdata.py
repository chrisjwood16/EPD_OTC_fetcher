import os
os.system('cls')
import urllib.request, json, urllib.parse, requests
from bs4 import BeautifulSoup
import pandas
import csv
import json
monthsdict={
	"Jan": "01",
	"Feb": "02",
	"Mar": "03",
	"Apr": "04",
	"May": "05",
	"Jun": "06",
	"Jul": "07",
	"Aug": "08",
	"Sep": "09",
	"Oct": "10",
	"Nov": "11",
	"Dec": "12"
}


urlhttp='https://'
urlbase="opendata.nhsbsa.net/api/3/action/datastore_search_sql?resource_id="
urlselect='&sql=SELECT BNF_DESCRIPTION, CHEMICAL_SUBSTANCE_BNF_DESCR, BNF_CHEMICAL_SUBSTANCE, QUANTITY, ITEMS, TOTAL_QUANTITY, ACTUAL_COST, NIC, YEAR_MONTH, PRACTICE_CODE '
urlfrom='FROM '
urlwhere=' WHERE `PRACTICE_CODE`='
#urlmonth='`EPD_202005`'
#urlpracticecode='"E00000"'

def clear(): os.system('cls') #on Windows System

def page_heading():
	clear()
	print_seperator()
	print ('                                      ')
	print ('  OTC Dispensing data download tool   ')
	print ('                                      ')
	print ('')
	print_seperator()
	
def print_seperator():
	print ('--------------------------------------')

def select_practice_code():
	practicechosen=input("Enter practice code (e.g. E00000): ")
	urlpracticecode='"'+practicechosen+'"'
	return urlpracticecode

def check_available_datasets():
    #Scrape EPD list page to find listed months with data
	availabledata=[]
	page = requests.get('https://opendata.nhsbsa.net/dataset/english-prescribing-data-epd')
	soup = BeautifulSoup(page.content, 'html.parser')
	for el in soup.find_all('a', attrs={'class': 'heading'}):
		listitem=el.get_text().replace('\r', '').replace('\n', '').replace('    English Prescribing Dataset (EPD) - ', '')
		listsplit=listitem.split()
		availabledata.append(str(monthsdict[listsplit[0]])+str(listsplit[1]))
	for monthyear in availabledata:
		print (monthyear)
	print_seperator()
	return availabledata

page_heading()
print ('Loading datasets, please wait...')
available_datasets=check_available_datasets()
chooseendmonth=available_datasets[-1]
choosestartmonth=available_datasets[-12]
print (choosestartmonth)
print (chooseendmonth)
urlpracticecode=select_practice_code()
print (practicename+' selected')
print ('')



choosestartmonth=input("Start month (mmyyyy): ")
    if choosestartmonth not in available_datasets:
        print ('Entered dataset not available - try again')
        choosestartmonth=input("Start month (mmyyyy): ")
	
chooseendmonth=input("End month (mmyyyy): ")
    if chooseendmonth not in available_datasets:
        print ('Entered dataset not available - try again')
        chooseendmonth=input("Start month (mmyyyy): ")

page_heading()
start = available_datasets.index(choosestartmonth)
end = available_datasets.index(chooseendmonth, start + 1) + 1
datasets=[]
for day in available_datasets[start:end]:
	dateformatted=str(day[2])+str(day[3])+str(day[4])+str(day[5])+str(day[0])+str(day[1])
	#datasets.append('`EPD_'+dateformatted+'`')
	datasets.append('EPD_'+dateformatted)

DF_list= list()
if (isinstance(urlpracticecode, str)):
	for ds in datasets:
		print ('Getting ' + ds)
		urlfull=urlbase+ds+urlselect+urlfrom+'`'+ds+'`'+urlwhere+urlpracticecode
		urlencoded=urlfull.replace(" ", "%20")
		urlfinal=urlhttp+urlencoded
		#print (urlfinal)
		with urllib.request.urlopen(urlfinal) as url:
			data = json.loads(url.read().decode())
			#print (data)
			if (data['result']['success']=="true"):
				data=data['result']['result']['records']
				data=json.dumps(data)
				df = pandas.read_json(data)
				df = df[['PRACTICE_CODE', 'BNF_DESCRIPTION', 'CHEMICAL_SUBSTANCE_BNF_DESCR', 'BNF_CHEMICAL_SUBSTANCE', 'YEAR_MONTH', 'ITEMS', 'QUANTITY', 'TOTAL_QUANTITY', 'NIC', 'ACTUAL_COST']]
				DF_list.append(df)
			else:
				print ('Failed: ' + data['result']['message'])

	dfFINAL = pandas.concat(DF_list)
	practice=urlpracticecode.strip('"')
	export_csv = dfFINAL.to_csv (practice+'.csv', index = None, header=True)
else:
	DF_list_full= list()
	for pc in urlpracticecode:
		print ('Getting ' + pc)
		DF_list= list()
		pcformatted='"'+pc+'"'
		for ds in datasets:
			print ('Getting ' + ds)
			urlfull=urlbase+ds+urlselect+urlfrom+'`'+ds+'`'+urlwhere+pcformatted
			urlencoded=urlfull.replace(" ", "%20")
			urlfinal=urlhttp+urlencoded
			with urllib.request.urlopen(urlfinal) as url:
				data = json.loads(url.read().decode())
				if (data['result']['success']=="true"):
					data=data['result']['result']['records']
					data=json.dumps(data)
					df = pandas.read_json(data)
					df = df[['PRACTICE_CODE', 'BNF_DESCRIPTION', 'CHEMICAL_SUBSTANCE_BNF_DESCR', 'YEAR_MONTH', 'ITEMS', 'QUANTITY', 'TOTAL_QUANTITY', 'NIC', 'ACTUAL_COST']]
					DF_list.append(df)
					DF_list_full.append(df)
				else:
					print ('Failed: ' + data['result']['message'])

		dfFINAL = pandas.concat(DF_list)
		export_csv = dfFINAL.to_csv (pc+'.csv', index = None, header=True)
	dfFINAL = pandas.concat(DF_list_full)
	export_csv = dfFINAL.to_csv ('HFP_finance'+'.csv', index = None, header=True)		

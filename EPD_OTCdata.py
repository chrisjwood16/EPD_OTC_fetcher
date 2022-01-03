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

urlbase="https://opendata.nhsbsa.net/api/3/action/datastore_search_sql?resource_id="
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

def dateselector(available_datasets):
    choosestartmonth=''
    chooseendmonth=''
    while choosestartmonth not in available_datasets:
        choosestartmonth=input("Start month (mmyyyy): ")
    while chooseendmonth not in available_datasets:
        chooseendmonth=input("End month (mmyyyy): ")
    start = available_datasets.index(choosestartmonth)
    end = available_datasets.index(chooseendmonth, start + 1) + 1
    EPDmonths=[]
    for day in available_datasets[start:end]:
        dateformatted=str(day[2:6]) + str(day[0:2])
        EPDmonths.append('EPD_' + dateformatted)
    return EPDmonths

def main():
    page_heading()
    print ('Loading datasets, please wait...')
    available_datasets=check_available_datasets()
    EPDmonths=dateselector(available_datasets)
    urlpracticecode=select_practice_code()
    print (urlpracticecode+' selected')



if __name__ == "__main__":
    main()





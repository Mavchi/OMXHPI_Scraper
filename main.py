import requests
from requests.exceptions import HTTPError
import json
import base
import random
import time
import csv
import pandas as pd
#import re
# from bs4 import BeautifulSoup

OMXHPI_StocksUrl = '/porssi/indeksit/OMXHPI'
OMXHPI_StockUrl = '/porssi/porssikurssit/osake'

def getAllStocks():
    headers = {'Host': 'www.kauppalehti.fi',
               'User-Agent': 'Mozilla/5.0 (X11 Ubuntu Linux x86_64 rv: 87.0) Gecko/20100101 Firefox/87.0',
               'Accept': '*/*',
               'Accept-Language': 'en-US, en;q = 0.5',
               'Accept-Encoding': 'gzip, deflate, br',
               'Connection': 'keep-alive',
               'Referer': 'https://www.kauppalehti.fi/porssi/indeksit/OMXHPI',
               'Cookie': 'KLKEY = 9930317a-add7-4c5c-9462-414b7b0d9eb3; 4106 = 14373432; sammio-bsid = e7015c7a-e8c8-450f-a6e0-9711fcf022dc; sammio-init-time = 2021-04-01T18: 22: 40.406Z; TcString = CPD-LIgPD-LIgBUAGAFIBTCsAP_AAH_AAApAF5wGwAFgAQAAqABkADwAIAAZAA0ACIAEcAJ4AVAAtgBzAD8AIIATAA0QBsgEIAIiASIAnYBgQD9AJkAXmBecBQABYAFQAMgAeABAADQAIgATwA5gCYAGiANkAhABEQCLAEiAMCAmQBbIC8wAAAAA.YAAAAAAAAMAA; gravitoData = {"TCString": "CPD-LIgPD-LIgBUAGAFIBTCsAP_AAH_AAApAF5wGwAFgAQAAqABkADwAIAAZAA0ACIAEcAJ4AVAAtgBzAD8AIIATAA0QBsgEIAIiASIAnYBgQD9AJkAXmBecBQABYAFQAMgAeABAADQAIgATwA5gCYAGiANkAhABEQCLAEiAMCAmQBbIC8wAAAAA.YAAAAAAAAMAA", "NonTCFVendors": [{"id": 1, "name": "Facebook", "consent": true}, {"id": 3, "name": "Google", "consent": true}, {"id": 4, "name": "Chartbeat", "consent": true}, { "id": 5, "name": "Giosg", "consent": true}, {"id": 6, "name": "Hotjar", "consent": true}, {"id": 7, "name": "Qualifio", "consent": true}, {"id": 8, "name": "Questback", "consent": true}, {"id": 9, "name": "Twitter", "consent": true}, {"id": 10, "name": "Wordpress", "consent": true}, {"id": 13, "name": "Leadoo", "consent": true}, {"id": 14, "name": "AudienceProject", "consent": true}]}; _ga = GA1.2.142231157.1617275755; _gid = GA1.2.425589749.1617275755; kppid_managed = kppidff_OCQSNqmd; _hjTLDTest = 1; _hjid = 2dfa11fa-6295-4a66-8b2c-c32769af681e; _hjIncludedInSessionSample = 0; stonderApp = 30312e30342e323032312031343a31393a30372e353139303030; ubvt = 86.50.44.931617514668918305; 7795 = UA-53865955-1; _gat_UA-53865955-1 = 1; _hjAbsoluteSessionInProgress = 0; _gat_UA-687304-1 = 1;                ALMA_DATA_PRIVACY_SETTINGS_1 = eyJwZXJtaXNzaW9ucyI6eyJjb29raWVzIjp0cnVlLCJnZW8iOlsiVEFSR0VURURfQ09OVEVOVCIsIkFEUyIsIldFQVRIRVIiXX0sIm1ldGEiOnsidXVpZDEiOiI0NTI5MmY3MC05MzE3LTExZWItYmQ2MC05M2NmODViN2QyYmYiLCJ1dWlkNCI6ImE1NjFhYTllLWU4NjItNDU0YS04NzY4LWVjNTZiMGFiMjIyMCIsImNyZWF0ZWRBdCI6IjIwMjEtMDQtMDFUMTg6MjI6NTEuODc5WiIsInVwZGF0ZWRBdCI6IjIwMjEtMDQtMDFUMTg6MjI6NTEuODc5WiJ9fQ ==',
               'Cache-Control': 'max-age = 0',
               'TE': 'Trailers',
    }
    baseUrl = 'https://www.kauppalehti.fi/api/pages/index/OMXHPI'
    try:
        response = requests.get(baseUrl, headers=headers)
        response.raise_for_status()
    except HTTPError as http_err:
        print('Error downloading, ', baseUrl)
        print(f'HTTP ERROR OCCURED: {http_err}')
    except Exception as err:
        print(f'Other error accured: {err}')
    
    content = response.json()
    with open(base.file_AllStocks, 'w') as file:
        json.dump(content, file)

def getStockData(name: str):
    baseUrl = f'https://www.kauppalehti.fi/api/balance/financialstmts/{name}/5'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11 Ubuntu Linux x86_64 rv: 87.0) Gecko/20100101 Firefox/87.0',
        'Referer': 'https://www.google.fi',
    }
    try:
        response = requests.get(baseUrl, headers=headers)
        response.raise_for_status()
    except HTTPError as http_err:
        print('Error downloading stock-data, ', name)
        print(f'HTTP ERROR OCCURED: {http_err}')
        return []
    except Exception as err:
        print(f'Other error accured: {err}')
        return []

    return response.json()

def scrapAllStocks(omxhpi: dict):
    data = []
    
    for stock in omxhpi['constituents']['shares']:
        time.sleep(random.randint(3,7))
        stock = getStockData(stock['symbol'])
        if len(stock) > 0:
            data.append(stock)
    return data


def updateData():
    getAllStocks()

    data = []
    with open(base.file_AllStocks) as file:
        data = json.load(file)
    with open(base.file_AllStocksData, 'w') as file:
        stocks = scrapAllStocks(data)
        json.dump(stocks, file)


def updatePEValue():
    data = []
    with open(base.file_AllStocksData) as file:
        data = json.load(file)

    with open(base.file_csvData, 'w') as file:
        writer = csv.writer(file, delimiter=';',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(['Company Name', 'P/E-luku'])
        for company in data:
            found = False
            row = [company['companyName']]
            for item in company['groups']:
                if item['name'] == 'Sijoittajan tunnuslukuja' or item['name'] == 'Markkinaperusteiset tunnusluvut':
                    for c in item['items']:
                        if c['name'] == 'P/E-luku':
                            found = True
                            if 'p5' in c:
                                row.append(c['p5'])
                            else:
                                row.append('-2000')

            #print(company['companyName'], company['groups'][0]['items'][6])
            writer.writerow(row)

if __name__ == '__main__':
    rawData = []
    with open(base.file_AllStocks) as file:
        rawData = json.load(file)
        
    companies = []
    for company in rawData['constituents']['shares']:
        newData = {
            'lastUpdated': time.time(),
            'name': company['name'],
            'symbol': company['symbol'],
            'exchange': 'OMXHPI',
            'askPrice': company['askPrice'],
            'bidPrice': company['bidPrice'],
            'isin': company['isin'],
            'tradeCurrency': company['tradeCurrency'],
        }
        companies.append(newData)

    with open(base.file_AllStocksData) as file:
        rawData = json.load(file)
        
        for item in rawData:
            correctCompany = {}
            for company in companies:
                if com
"""
    df = pd.read_csv(base.file_csvData, delimiter=';')
    print(df)
    print('')

    df_temp = df[df['P/E-luku'].astype(float) < 20]
    print(df_temp[df_temp['P/E-luku'].astype(float) > 0])"""

import urllib2
import csv
import json


from itertools import islice

SPLIT = ';'

def incState():
    ds = open('state', 'r+')

    index = getIndexState(ds) + 1

    print index
    setIndexState(ds, index)


def main():
    with open('geoinput.csv') as csvfile:
        file = open('testfile.csv','a')
        state = open('state', 'r+')

        index = getIndexState(state)
        values =  csv.reader(csvfile, delimiter=SPLIT, quotechar='|')

        for row in islice(values, index, None):
            id =  row[0]
            adress=  row[1]

            respone = getUrlResult(index, adress)
            geo = getCoordinates(respone)
          
            index += 1
            setIndexState(state, index)
            file.write(printResult(str(index) + SPLIT + id + SPLIT + adress, geo, SPLIT))
            
          


def getIndexState(ds):
    index = ds.read()
    ds.seek(0)
    if(index == ''):
        return 0
    return int(index)

def setIndexState(ds, index):
    index = str(index)
    ds.write(index)
    ds.seek(0)


def printResult(adress, geoData, split):
    lat =  geoData['lat']
    lng = geoData['lng']
    result = adress +  split + str(lat) + split + str(lng) + "\n"
    return result

# https://api3.geo.admin.ch/1807181420/rest/services/ech/SearchServer?sr=2056&searchText=Bundesgasse&lang=de&type=locations
def getUrlResult(index, adress):
    response = '{"results":[]}'

    if(len(adress.strip()) and len(adress.split(" ")) < 10):

        baseUrl = "https://api3.geo.admin.ch/1807181420/rest/services/ech/SearchServer"
        url =  baseUrl + '?sr=2056&searchText=' + adress + '&lang=de&type=locations' 

        url =  url.replace("#", "")
        url =  url.replace(" ", "%20")

        print str(index) +" URL => " + url

        response = urllib2.urlopen(url).read()
    return json.loads(response)

def getCoordinates(result):
    value = {}
    value['lat'] = ''
    value['lng'] = ''

    if len(result['results']) >= 1:    
        value['lat'] = result['results'][0]['attrs']['lat']
        value['lng'] = result['results'][0]['attrs']['lon']
    return value

def getCoordinatesByGoogle(result):
    if len(result['results']) >= 1:
        return result['results'][0]['geometry']['location']
    value = {}
    value['lat'] = ''
    value['lng'] = ''
    return value

def getUrlGoogle(adress):
    print adress.strip()

    BASE_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
    API_KEY = "ANY"

    url =  BASE_URL + '?address=' + adress + '&key=' + API_KEY
    url =  url.replace(" ", "%20")
    response = urllib2.urlopen(url).read()
    return json.loads(response)

if __name__ == "__main__":
    main()
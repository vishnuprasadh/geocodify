import requests
import pandas as pd
import math
import json


class geogoogleapiwrapper:
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}'
    jsondata = ""

    def getlatandlongforgivenpincode(self, pincode):
        try:
            latlong=[]
            response = requests.get(str(self.url).format(pincode))
            self.jsondata = response.json()
            if response.status_code == 200:
                latlong = (self.jsondata["results"][0]["geometry"]["location"])
                latlong = [latlong["lat"], latlong["lng"]]
            else:
                latlong = [0,0]
            print("Google Api is being used")
            return latlong
        except AttributeError as AError:
            print("{} pin could not be found, find manually!. Exception : {}".format(pincode, AError.message))
            return [0, 0]
        except Exception as GenError:
            print("{} pin could not be found, find manually!. Exception : {}".format(pincode, GenError.message))
            return [0, 0]

    def __init__(self):
        requests.ConnectTimeout = 3
        requests.ReadTimeout=2
        requests.Timeout=2

    def getreverseaddressforgivenlatandlong(self, latitude, longitude):
        try:
            if not latitude == 0 or not longitude == 0:
                address =self.jsondata["results"][0]["formatted_address"]
                return address.encode("utf-8").strip()
            else:
                return "NA"
        except Exception as err:
            print("{},{} address formatting had error : {}".format(longitude, latitude,err.message))
            return "NA"



# Tests
#google = geogoogleapiwrapper()
#lat = google.getlatandlongforgivenpincode("560035")
#print(google.getreverseaddressforgivenlatandlong(lat[0],lat[1]))
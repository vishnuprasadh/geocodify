from geopy import *
from geopy.geocoders import Nominatim

class geopywrapper:
    def getlatandlongforgivenpincode(self, pincode):
        try:
            locator = Nominatim()
            location = locator.geocode(pincode)
            latitude = location.latitude
            longitude = location.longitude
            #print("{},{}".format(location.latitude, location.longitude))
            print("GeoPy Api is being used")
            return [location.latitude, location.longitude]
        except AttributeError as AError:
            print("{} pin could not be found, find manually!. Exception : {}".format(pincode, AError.message))
            return [0, 0]
        except Exception as GenError:
            print("{} pin could not be found, find manually!. Exception : {}".format(pincode, GenError.message))
            return [0, 0]

    def getreverseaddressforgivenlatandlong(self, latitude, longitude):
        try:
            if not latitude == 0 or not longitude == 0:
                locator = Nominatim()
                location = locator.reverse("{},{}".format(latitude, longitude))
                print(location.address)
                return location.address.encode("utf-8").strip()
        except Exception as err:
            print("{},{} had error of {}".format(longitude, latitude, err.message))
            return "NA"




# Tests
#geopywrap = geopywrapper()
#lat = geopywrap.getlatandlongforgivenpincode("560034")
#print(geopywrap.getreverseaddressforgivenlatandlong(lat[0],lat[1]))
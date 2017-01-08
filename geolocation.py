import math
import os
import pandas as pd
import csv
import numpy as np
import geogoogleapiwrapper as googleapi


class geolocation:

    inputfileextension = ".csv"
    inputfolder = 'input/'
    outputfile = 'output/output.csv'
    pincodecolumnname = "pincode"
    inputdf = pd.DataFrame()
    outputdf = pd.DataFrame()
    inputset = set()
    outputset = set()
    differenceset = set()
    GOOGLEAPIPROVIDER = "googleapi"
    GEOPYWRAPPER = "geopywrapper"
    wrappertouse = ""

    """ Initialization will pick any first csv file and proceed
        will read the output.csv in the output folder
    """
    def __init__(self,wrapper="geopywrapper"):
        try:
            self.wrappertouse=wrapper
            files = os.listdir(self.inputfolder)
            for file in files:
                iterate = 1
                #we want to do this only once hence iterate = 1 condition for now.
                if os.path.splitext(file)[1]==self.inputfileextension and iterate == 1:
                    filetoload = str(self.inputfolder) + str(file)
                    self.inputdf = pd.read_csv(filetoload)
                    iterate = iterate + 1
            self.outputdf = pd.read_csv(self.outputfile)
            #print(self.outputdf)
        except Exception as err:
            print('Class initiation failed due to exception : {}'.format(err.message))

    """will create or update outputcsv
       By default it doesnt refresh all pincodes in csv output and limits the # of API calls to 500
    """
    def writelatandlong(self,refreshAllPincodes=False, limit=500):
        dictionarylist = list()
        csvcolumns = ['pincode','latitude','longitude','address']
        print('started')
        #Recapture latitude only for delta fields missing or for all ?
        if not refreshAllPincodes:
           #Get unique pincode from input & ooutput files for which lat & long already generated
            self.inputset = set(np.unique(x for x in self.inputdf[self.pincodecolumnname]))
            self.outputset = set(np.unique(x for x in self.outputdf[self.pincodecolumnname]))
            #create a delta for which we need to rewrite
            self.differenceSet = self.inputset.difference(self.outputset)
            print("set all objects")
        elif refreshAllPincodes:
            self.differenceSet = set(np.unique(x for x in self.inputdf[self.pincodecolumnname]))

        geowrapper = []
        #TODO: FIX THIS BY OOPS CONCEPT
        if self.wrappertouse == self.GOOGLEAPIPROVIDER:
            geowrapper = googleapi.geogoogleapiwrapper()
        elif self.wrappertouse == self.GEOPYWRAPPER:
            geowrapper = geopywrapper.geopywrapper()

        """for each different pincode get lat/long and address
        """
        index = 0
        #TODO: Need to modularize with unit tests
        for pin in self.differenceSet:
            try:
                print("{} is now being processed".format(pin))
                latandlongitude = geowrapper.getlatandlongforgivenpincode(pin)
                print(latandlongitude)
                if not(latandlongitude[0]==0 or latandlongitude[1]==0):
                    address = geowrapper.getreverseaddressforgivenlatandlong(latandlongitude[0],latandlongitude[1])
                    dictionarylist.insert(index,  [pin, latandlongitude[0],latandlongitude[1],address])
                index = index + 1
                if (index > limit):
                    break
            except IndexError as indexerr:
                print ("Exception managed , check for error : {}".format(indexerr.message))
            except Exception as err:
                print ("Exception managed , check for error : {}".format(err.message))
        try:
            if(len(dictionarylist)>0):
                print("About to process {} records.".format(len(dictionarylist)))
                #write the fileoutput for the lat, long & pin which is now in list
                with open(self.outputfile,'wb') as w:
                    owriter = csv.writer(w)
                    owriter.writerow(csvcolumns)
                    for row in dictionarylist:
                        print(row)
                        owriter.writerow(row)
                    w.close()
            else:
                print("No dictionary items to process")
        except Exception as generr:
            print ("Exception managed , check for error : {}".format(generr.message))

"""
Marking this class as the main for the package
"""
#if __name__== "__main__":
#geopy = geolocation("googleapi")
#geopy.writelatandlong(limit=10)

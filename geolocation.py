import math
import os
import pandas as pd
import csv
import numpy as np
import geogoogleapiwrapper as googleapi
import geopywrapper as geopywrap


class geolocation:

    inputfileextension = ".csv"
    inputfolder = 'input/'
    outputfolder = 'output/'
    outputfile = 'output.csv'
    pincodecolumnname = "pincode"
    inputdf = pd.DataFrame()
    outputdf = pd.DataFrame()
    inputset = set()
    outputset = set()
    differenceset = set()
    GOOGLEAPIPROVIDER = "googleapi"
    GEOPYWRAPPER = "geopywrapper"
    wrappertouse = ""
    outfileFound = False

    """ Initialization will pick any first csv file and proceed
        will read the output.csv in the output folder
    """
    def __init__(self,wrapper="googleapi"):
        try:
            self.wrappertouse=wrapper
            files = os.listdir(self.inputfolder)
            for file in files:
                iterate = 1
                """we want to pull the first csv file found hence iterate = 1 condition for now."""
                if os.path.splitext(file)[1]==self.inputfileextension and iterate == 1:
                    print(os.path.splitext(file)[0])
                    filetoload = str(self.inputfolder) + str(file)
                    self.inputdf = pd.read_csv(filetoload)
                    iterate= iterate + 1
            """file doesnt exist or exist ?"""
            if (self.__fileexists(self.outputfolder, self.outputfile)):
                self.outputdf = pd.read_csv(self.outputfolder+ self.outputfile)
                print("output file exists, data loaded")
                self.outfileFound = True
            print("outptut found is : {}".format(self.outfileFound))
        except Exception as err:
            print('Class initiation failed due to exception : {}'.format(err.message))

    def __fileexists(self, filepath, filename):
        files = os.listdir(filepath)
        print("files count is {}".format(len(files)))
        for file in files:
            print("{} is the file now".format(os.path.basename(file)))
            if os.path.basename(file) == filename:
                return True
        return False

    def __dataexists(self):
        filehasContent = False
        """file doesnt exist or exist ?"""
        if self.outfileFound:
            """if exists, read and see if there is any data ?"""
            print ("reading into dataexists method")
            with open(self.outputfolder+ self.outputfile, 'rb') as r:
                oreader = csv.reader(r)
                for row in oreader:
                    if not (row == None):
                        filehasContent = True
                        print("File is not empty, append")
                        break
                r.close()
        return filehasContent

    """update or create the file if it doesnt exist"""
    def __updateorcreatefile(self, folderpath, file, dictionarylist, headercolumns):
        if self.outfileFound:
            with open(folderpath + file, 'a') as w:
                owriter = csv.writer(w)
                if not (self.__dataexists()):
                    owriter.writerow(headercolumns)
                for row in dictionarylist:
                    #print(row)
                    owriter.writerow(row)
                    print("file appended and wrote")
                w.close()
        else:
            with open(folderpath + file, 'wb') as w:
                owriter = csv.writer(w)
                owriter.writerow(headercolumns)
                for row in dictionarylist:
                    owriter.writerow(row)
                    print("file new row added and wrote")
                w.close()

    """will create or update outputcsv
       By default it doesnt refresh all pincodes in csv output and limits the # of API calls to 500
    """
    def writelatandlong(self,refreshAllPincodes=False, limit=500):
        dictionarylist = list()
        csvcolumns = ['pincode','latitude','longitude','address']
        print('started')
        """Recapture latitude only for delta fields missing or for all ?"""
        if not refreshAllPincodes:
            """Get unique pincode from input & ooutput files for which lat & long already generated"""
            self.inputset = set(np.unique(x for x in self.inputdf[self.pincodecolumnname]))
            if self.outfileFound:
                #print("printing input file")
                #print(self.inputdf)
                #print("print output file")
                #print(self.outputdf)
                self.outputset = set(np.unique(x for x in self.outputdf[self.pincodecolumnname]))
                #create a delta for which we need to rewrite
                self.differenceSet = self.inputset.difference(self.outputset)
                print("Difference set to be created,count of {}".format(len(self.differenceSet)))

            else:
                self.differenceSet = self.inputset
                print("Difference set same as input set since no file output found, count of {}".format(len(self.differenceSet)))
        elif refreshAllPincodes:
            print("Refreshing all pinsets")
            self.differenceSet = set(np.unique(x for x in self.inputdf[self.pincodecolumnname]))

        geowrapper = []
        #TODO: FIX THIS BY OOPS CONCEPT
        if self.wrappertouse == self.GOOGLEAPIPROVIDER:
            geowrapper = googleapi.geogoogleapiwrapper()
            print("GoogleApi provider created")
        elif self.wrappertouse == self.GEOPYWRAPPER:
            geowrapper = geopywrap.geopywrapper()
            print("GeoPy provider created")

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
                if (index > limit-1):
                    break
            except IndexError as indexerr:
                print ("Exception managed , check for error : {}".format(indexerr.message))
            except Exception as err:
                print ("Exception managed , check for error : {}".format(err.message))
        try:
            if(len(dictionarylist)>0):
                print("About to process {} records.".format(len(dictionarylist)))
                """write the fileoutput for the lat, long & pin which is now in list"""
                self.__updateorcreatefile(self.outputfolder,self.outputfile,dictionarylist,csvcolumns)
            else:
                print("No dictionary items to process")
        except Exception as generr:
            print ("Exception managed , check for error : {}".format(generr.message))



"""
Marking this class as the main for the package
"""
#if __name__== "__main__":
"""geopy = geolocation("geopywrapper")"""
geopy = geolocation("googleapi")
geopy.writelatandlong(limit=100)


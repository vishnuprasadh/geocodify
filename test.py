#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 21:06:49 2017

@author: vishnuhari
"""

import csv
import os

inputfileextension = ".csv"
inputfolder = 'input/'
outputfolder = 'output/'
outputfile = 'output.csv'
pincodecolumnname = "pincode"
    
def checkcfile():
    with open(outputfile,'a') as w:
        owriter = csv.writer(w)
        owriter.writerow(csvcolumns)
        for row in dictionarylist:
            print(row)
            owriter.writerow(row)
        w.close()

def fileexists(filepath, filename):
    files = os.listdir(filepath)
    for file in files:
        if (os.path.basename(file) == filename):
            print("file {} exists".format(filename))



def checklist(source):
    dest = dict()
    #print (len(source))
    s1 = source[0][0]
    s2 = source[0][1][1]
    #dest[source[0]] = s2
    print (s1)
    print (s2)
    #print(dest[s1])

#fileexists(outputfolder,outputfile)
list = [[560034, [12.9261382,77.6221091]],[[560036], 13.008385,77.696008]]
checklist(list)
import math
import collections

class distancecalculator:

    '''Earth radius in kms '''
    earthradius = 6371
    leastdistance = None
    leastvaluekey = None

    '''Send latitude & latitude as first & second params in source in degrees
    Add list of pincode and lat & long of destination in a list and send the same as destintion points in degrees
    '''
    def getequirectangulardistance(self, source, destinationset):
        try:
            '''set in radians the source lat & long'''
            sourcelat = math.radians(source[0])
            sourcelong = math.radians(source[1])
            distance = dict()
            '''for each destination pincode & lat/long combination iterate'''
            for destination in destinationset:
                '''get lat & longitude'''
                destlat = destination[1][0]
                destlong = destination[1][1]

                '''If the dest latitude is none, dont process - something is wrong, else process'''
                if not (destlat == None):
                    '''convert to radians'''
                    destlat = math.radians(destlat)
                    destlong = math.radians(destlong)
                    '''get distance'''
                    d = self.__getdistancebyequiangularformula(destlong,sourcelong,destlat,sourcelat)
                    print("Distance is {}".format(d))
                    distance[destination[0]] = d
                    self.__setleastKeyandValue(d,destination[0])
                    print("Done")
            print("Least distance Pincode is {} among the set at a distance of {}kms from source.".format(self.leastvaluekey,self.leastdistance))
        except Exception as err:
            print ("Exception occurred : {}".format(err.message))

    '''we will use Equirectangular distance formula
    x = longdiff * cos(latadd)
    y = latdiff
    d = R * squareroot(x2 + y2)
    R = radius
    '''
    def __getdistancebyequiangularformula(self,destlong,sourcelong,destlat,sourcelat):
        '''Find X which is as below'''
        X = (destlong - sourcelong) * math.cos((destlat + sourcelat) / 2)
        Y = destlat - sourcelat
        return self.earthradius * math.sqrt(X * X + Y * Y)

    '''Sets the least distance value and corresponding pincode in a class level variable'''
    def __setleastKeyandValue(self,distance, key):
        if (self.leastdistance == None or distance < self.leastdistance):
            self.leastdistance = distance
            self.leastvaluekey = key

        print (self.leastdistance)


distance = distancecalculator()
distance.getequirectangulardistance([12.9048022,77.6821069], [[560034, [12.9261382,77.6221091]],[560036, [13.008385,77.696008]]])


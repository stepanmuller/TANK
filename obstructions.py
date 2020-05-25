
from PIL import Image
from math import sqrt
import json



class Obstructions:
    def __init__(self):
        imag = Image.open("obstructions.png")
        #Convert the image te RGB if it is a .gif for example
        self.imag = imag.convert ('RGB')
        self.array = self.walk()

    def walk(self):
        array = [[0 for x in range(5000)] for y in range(5000)] 
        for i in range(5000):
            for j in range(5000):
                array[i][j]=self.block(i,j)
        return array
    
    def block(self, i, j):
        overall=0
        overall+=self.isObstructed(j,i)
        if (overall==0):
            return 0
        if (overall<170):
            return 0
        return 1

    
    def isObstructed(self, X, Y):
        pixelRGB = self.imag.getpixel((X,Y))
        R,G,B = pixelRGB
        brightness = sum([R,G,B])/3 ##0 is dark (black) and 255 is bright (white)
        return(brightness)

    def getObstructions(self):
        data = {}
        data['obstruction'] = self.array
        with open('obstruction.txt', 'w') as outfile:
            json.dump(data, outfile)


a=Obstructions()
a.getObstructions()

## Use following code to load data
#import json
#
#with open('obstructions.txt') as json_file:
#    data = json.load(json_file)

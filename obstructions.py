
from PIL import Image
from math import sqrt



class Obstructions:
    def __init__(self):
        imag = Image.open(r"C:\Users\tform\OneDrive\Dokumenty\GitHub\TANK\Map.png")
        #Convert the image te RGB if it is a .gif for example
        self.imag = imag.convert ('RGB')
        self.array = self.walk()

    def walk(self):
        array = [[0 for x in range(500)] for y in range(500)] 
        for i in range(500):
            for j in range(500):
                array[i][j]=self.block(i,j)
        return array
    
    def block(self, i, j):
        xpos=j*10
        ypos=i*10
        overall=0
        for i in range(10):
            for j in range(10):
                overall+=self.isObstructed(xpos+j,ypos+i)
        if (overall==0):
            return True
        if ((overall/100)<170):
            return True
        return False

    
    def isObstructed(self, X, Y):
        pixelRGB = self.imag.getpixel((X,Y))
        R,G,B = pixelRGB
        brightness = sum([R,G,B])/3 ##0 is dark (black) and 255 is bright (white)
        return(brightness)

    def getObstructions(self):
        return(self.walk())
## Needs a function to save array to json. Will be added later.


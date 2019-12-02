import sys
from PIL import Image
from math import pi,sin,cos,tan,acos,atan2,sqrt

def getImage(pano, img, heading, pitch, zoom):
    pano_size = pano.size
    img_size = img.size
    pano_array = pano.load()
    img_array = img.load()

    fov = 180/(2**zoom)
    dis = img_size[0] / 2 / tan(fov/2 / 180 * pi)
    p = pitch / 180 * pi
    h = (180+heading)%360 / 180 * pi

    for i in range(img_size[0]):
        for j in range(img_size[1]):
            x = 1
            y = (i - img_size[0]/2)/dis
            z = (j - img_size[1]/2)/dis

            x1 = cos(p) * x - sin(p) * z
            z1 = sin(p) * x + cos(p) * z
            x = x1
            z = z1

            x1 = cos(h) * x - sin(h) * y
            y1 = sin(h) * x + cos(h) * y
            x = x1
            y = y1

            phi = atan2(y,x)
            theta = acos(z/sqrt(x*x + y*y + z*z))

            i2 = int((phi/pi*180)%360 / 360 * pano_size[0])
            j2 = int((theta/pi*180)%180 / 180 * pano_size[1])
            if i2 == pano_size[0]: i2 -= 1
            if j2 == pano_size[1]: j2 -= 1
            img_array[i,img_size[1]-1-j] = pano_array[i2,j2]

pano = Image.open("image.png")
img = Image.new("RGB",(1200,800),"black")
getImage(pano,img,320,0,1)
img.show()

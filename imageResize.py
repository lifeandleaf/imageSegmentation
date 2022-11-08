import os
import PIL.Image as image
import numpy as np

dir = './images'
for file in os.listdir(dir):
    fp = open(dir + '/' + file, 'rb')
    im = image.open(fp)
    m, n = im.size
    im = im.resize((int(m * 0.2), int(n * 0.2)), image.ANTIALIAS)
    im.save("./miniImage/" + file)
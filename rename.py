import os
import sys
import numpy as np
import PIL.Image as image
# id = 1
# for file in os.listdir('./images'):
#     filepath = './images/' + file
#     os.rename(filepath, "./images/car_{}.jpg".format(id))
#     id += 1


# a = np.array([1, 2, 3])
# print(type(int(a[0] * 2)))

fp = open('./kmeans_res/web_1.jpg', "rb")
im = image.open(fp)
m, n = im.size
for i in range(m):
    for j in range(n):
        print(im.putpixel((i, j), ))
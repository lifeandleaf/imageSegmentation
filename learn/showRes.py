#coding:UTF-8

import PIL.Image as image

f_center = open("center_pp")

center = []
for line in f_center.readlines():
    lines = line.strip().split("\t")
    tmp = []
    for x in lines:
        tmp.append(int(float(x) * 256))
    center.append(tuple(tmp))
print(center)
f_center.close()

fp = open("../miniImage/car_1.jpg", "rb")
im = image.open(fp)
# 新建一个图片
m, n = im.size
pic_new = image.new("RGB", (m, n))

f_sub = open("sub_pp")
i = 0
for line in f_sub.readlines():
    index = float((line.strip().split("\t"))[0])
    index_n = int(index)
    pic_new.putpixel((int(i/n),int(i%n)),(center[index_n]))
    i = i + 1
f_sub.close()

pic_new.save("result.jpg", "JPEG")

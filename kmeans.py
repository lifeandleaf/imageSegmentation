# coding:UTF-8
import PIL.Image as image
import matplotlib.pyplot as plt
import numpy as np
from random import random

def load_data(image_path):
    fp = open(image_path, 'rb')
    im = image.open(fp)
    data = []
    m, n = im.size
    for i in range(m):
        for j in range(n):
            # 以颜色空间为特征向量
            tm = []
            x, y, z = im.getpixel((i, j))
            tm.append(x / 256.0)
            tm.append(y / 256.0)
            tm.append(z / 256.0)
            data.append(tm)
    fp.close()
    return np.mat(data)

def distance(x, y):
    dst = (x - y) * (x - y).T
    return dst[0, 0]

def nearest(point, k_center):
    sz = np.shape(k_center)[0]
    min_dst = distance(point, k_center[0, ])
    for i in range(sz):
        d = distance(point, k_center[i, ])
        if d < min_dst:
            min_dst = d
    return min_dst

def get_center(points, k):
    m, n = np.shape(points)
    center = np.mat(np.zeros((k, n)))
    index = np.random.randint(0, m)
    center[0, ] = np.copy(points[index, ])
    d = [0.0 for _ in range(m)]
    for i in range(1, k):
        sum_all = 0
        for j in range(m):
            d[j] = nearest(points[j, ], center[0:i, ])
            sum_all += d[j]
        sum_all *= random()
        for j, di in enumerate(d):
            sum_all -= di
            if sum_all > 0:
                continue
            center[i] = np.copy(points[j, ])
            break
    return center


def kmeans(points, k, center):
    m, n = np.shape(points)
    subCenter = np.mat(np.zeros((m, 2)))
    change = True
    while change == True:
        change = False
        for i in range(m):
            minDst = np.inf
            minIndex = 0
            for j in range(k):
                dst = distance(points[i, ], center[j, ])
                if dst < minDst:
                    minDst = dst
                    minIndex = j
            if subCenter[i, 0] != minIndex:
                change = True
                subCenter[i, ] = np.mat([minIndex, minDst])
        # 重新计算聚类中心
        for j in range(k):
            sum_all = np.mat(np.zeros((1, n)))
            r = 0
            for i in range(m):
                if subCenter[i, 0] == j:
                    sum_all += points[i, ]
                    r += 1
            for z in range(n):
                try:
                    center[j, z] = sum_all[0, z] / r
                except:
                    print("r is zero")
    return subCenter

def save_result(file_name, source):
    m, n = np.shape(source)
    f = open(file_name, "w")
    for i in range(m):
        tmp = []
        for j in range(n):
            tmp.append(str(source[i, j]))
        f.write("\t".join(tmp) + "\n")
    f.close()

def save_image(subCenter, center, filename):
    cent = []
    for i in range(k):
        tmp = []
        for j in range(3):
            tmp.append(int(float(center[i, j]) * 256))
        cent.append(tuple(tmp))
    print(cent)
    fp = open("./images/" + filename, 'rb')
    data = image.open(fp)
    m, n = data.size
    res = image.new("RGB", (m, n))
    for i in range(len(subCenter)):
        index_n = int(subCenter[i,0])
        res.putpixel((int(i/n), int(i%n)), (cent[index_n]))
    res.save("./kmeans_res/" + filename)
    plt.figure()
    plt.subplot(1, 2, 1)
    plt.imshow(data)
    plt.subplot(1, 2, 2)
    plt.imshow(res)
    plt.show()

if __name__ == '__main__':
    # 聚类中心个数
    k = 2
    # 加载数据
    points = load_data('./images/web_1.jpg')
    center = get_center(points, k)
    print(center)
    subCenter = kmeans(points, k, center)
    save_image(subCenter, center, 'web_1.jpg')
    # save_result('./learn/sub_pp', subCenter)
    # save_result('./learn/center_pp', center)
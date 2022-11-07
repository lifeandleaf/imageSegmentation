# coding:UTF-8
import PIL.Image as image
import matplotlib.pyplot as plt
import numpy as np


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
    cla = 0
    for i in range(sz):
        d = distance(point, k_center[i, ])
        if d < min_dst:
            d = min_dst
            cla = i
    return min_dst

def get_center(points, k):
    n = np.shape(points)[1]
    center = np.mat(np.zeros((k, n)))
    for j in range(n):
        minJ = np.min(points[:, j])
        rangeJ = np.max(points[:, j]) - minJ
        center[:, j] = minJ * np.mat(np.ones((k, 1))) + np.random.rand(k, 1) * rangeJ
    return center

def kmeans(points, k, center):
    m, n = np.shape(points)
    subCenter = np.mat(np.zeros((m, 2)))
    change= True
    while change:
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
        # print(subCenter)
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
    fp = open("./images/" + filename, 'rb')
    data = image.open(fp)
    m, n = data.size
    res = image.new("RGB", (m, n))

    cent = []
    k, n = np.shape(center)
    for i in range(k):
        tmp = []
        for j in range(n):
            print(center[i, j])
            tmp.append(float(center[i, j]))
        cent.append(tuple(tmp))
    for i in range(m):
        for j in range(n):
            id = int(subCenter[i * n + j, 0])
            print(cent[id])
            res.putpixel((i, j), cent[id])
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
    subCenter = kmeans(points, k, center)
    print("show")
    save_image(subCenter, center, 'web_1.jpg')

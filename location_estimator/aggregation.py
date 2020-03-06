import sys
sys.path.append("./location_estimator")
sys.path.append("./location_estimator/py")
import csv
import latlng
import numpy as np
import matplotlib.pyplot as plt

def aggregate(objects):
# threshold_1: radius for calculating density, threshold_2: min dis between stores
    threshold_1 = 2
    threshold_2 = 4

    num = len(objects)
    px = np.zeros(num)
    py = np.zeros(num)
    rho = np.zeros(num)
    alat = np.zeros(num)
    alng = np.zeros(num)
    label = [[objects[i].label] for i in range(num)]
    image = [[objects[i].image] for i in range(num)]
    if num < 1: return []

    for i in range(1,num):
        xy = objects[0].get_xy(objects[i])
        px[i] = xy.x
        py[i] = xy.y

    for i in range(num):
        s = 1
        ave_x = px[i]
        ave_y = py[i]
        for j in range(num):
            if i!=j and (px[i]-px[j])**2 + (py[i]-py[j])**2 < threshold_1 **2:
                s += 1
                ave_x += px[j]
                ave_y += py[j]
                label[i].append(objects[j].label)
                image[i].append(objects[j].image)
        rho[i] = s + np.random.rand()*0.01
        ll = objects[0].get_latlng(ave_x/s, ave_y/s)
        alat[i] = ll.lat
        alng[i] = ll.lng

    dis = np.zeros(num)

    for i in range(num):
        m = 2147483647
        for j in range(num):
            if (rho[j] > rho[i]) and ((px[i]-px[j])**2 + (py[i]-py[j])**2 < m):
                m = (px[i]-px[j])**2 + (py[i]-py[j])**2
        dis[i] = m

    aggregated_objects = []
    for i in range(num):
        if dis[i] > threshold_2**2:
            ll = latlng.LatLng(alat[i],alng[i])
            ll.label = label[i]
            ll.image = image[i]
            aggregated_objects.append(ll)
    return aggregated_objects


if __name__ == "__main__":
    points = []
    np.random.seed(0)
    with open('location_estimator/annotation_new.csv') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                if len(row[14]) > 0:
                    lat = float(row[13])
                    lng = float(row[14])
                    ll = latlng.LatLng(lat,lng)
                    ll.label = int(row[3])
                    ll.image = int(row[2])
                    points.append(ll)
                line_count += 1
    agg_points = aggregate(points)
    print(len(agg_points))
    f = open("location_estimator/annotation_aggregated.csv","w")
    f.write("lat,lng,labels,image_ids\n")
    for p in agg_points:
        f.write(str(p.lat)+","+str(p.lng)+",\""+str(p.label)+"\",\""+str(p.image)+"\"\n")
        # print(p.lat, p.lng, p.label)
    #     plt.scatter(p.lng, p.lat)
    # plt.show()

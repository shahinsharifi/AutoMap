import sys
sys.path.append("./location_estimator")
sys.path.append("./location_estimator/py")
import csv
import latlng
import numpy as np
import matplotlib.pyplot as plt
from buildingmanager import *

def read_csv(file, lat_col, lng_col, city):
    points = []
    with open(file) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                lat = float(row[lat_col])
                lng = float(row[lng_col])
                ll = latlng.LatLng(lat,lng)
                b = city.find_nearest_building(ll)
                points.append([ll,b,line_count,0])
                line_count += 1
    return points

def plot_parcel(nodes):
    ndx = []
    ndy = []
    for nd in nodes:
        ndx.append(nd.lng)
        ndy.append(nd.lat)
    plt.plot(ndx, ndy, 'k:')

def plot_points(points, color):
    for p in points:
        plot_parcel(p[1].nodes)
        plt.scatter(p[0].lng, p[0].lat, c = color)

def compare(points, lat_col, lng_col, city, gt):
    f = open(points.replace(".csv","_new.csv"),"w")
    with open(points) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        line_count = 0
        t = 0
        t2 = 0
        for row in csv_reader:
            if line_count == 0:
                f.write(",".join(row)+",gt\n")
                line_count += 1
            else:
                lat = float(row[lat_col])
                lng = float(row[lng_col])
                ll = latlng.LatLng(lat,lng)
                b = city.find_nearest_building(ll)
                gt_id = "-1"
                min_dis = 999999999
                flag1 = False
                flag2 = False
                for p in gt:
                    if b == p[1]:
                        gt_id = str(p[2])
                        if p[3] == 0:
                            flag1 = True
                            p[3] = 1
                        flag2 = True
                if flag1: t += 1
                if flag2: t2+= 1
                #     min_dis = min(min_dis, ll.get_distance(p[0]))
                # if min_dis < 10: t += 1
                f.write(row[0]+","+row[1]+",\""+row[2]+"\",\""+row[3]+"\","+gt_id+"\n")
                line_count += 1

    print(t,t2,len(gt),line_count-1)
    return {"recall": t/len(gt), "precision": t2/(line_count-1)} #, "error_mean": errors.mean(), "error_std": errors.std()}

if __name__ == "__main__":
    city = BuildingManager("location_estimator/maps/manhattan/buildings_manhattan_exp.xml")
    # gt = read_csv("location_estimator/gt.csv", 3,2,city)
    gt = read_csv("location_estimator/annotation_aggregated.csv", 0,1,city)
    # print(compare("location_estimator/annotation_aggregated_auto.csv",0,1,city,gt))
    print(compare("location_estimator/annotation_new_auto.csv",13,14,city,gt))
    # compare("location_estimator/annotation_auto_aggregated.csv", 0,1,city,gt)
    # plot_points(gt,'k')
    # ps = read_csv("location_estimator/annotation_aggregated_auto.csv", 0,1,city)
    # plot_points(ps,'b')
    # plt.show()

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
                points.append((ll,b,row[0]))
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
                for p in gt:
                    if b == p[1]:
                        gt_id = p[2]
                        break
                f.write(row[0]+","+row[1]+",\""+row[2]+"\",\""+row[3]+"\","+gt_id+"\n")
                line_count += 1

    # return {"recall": t/len(gt), "precision": t/len(points)} #, "error_mean": errors.mean(), "error_std": errors.std()}

if __name__ == "__main__":
    city = BuildingManager("location_estimator/maps/manhattan/buildings_manhattan_exp.xml")
    gt = read_csv("location_estimator/gt.csv", 3,2,city)
    compare("location_estimator/annotation_auto_aggregated.csv",0,1,city,gt)
    # compare("location_estimator/annotation_auto_aggregated.csv", 0,1,city,gt)
    # plot_points(gt,'k')
    # plt.show()

import sys
sys.path.append("./location_estimator")
sys.path.append("./location_estimator/py")
import csv
import latlng
from estimator import *
from buildingmanager import *
import matplotlib.pyplot as plt

class Annotation:

    def __init__(self, user_id, image_id, label_id, top, left, bottom, right, time_effort, token, creation_date, is_validated, is_correct = 1):
        self.user_id        = user_id
        self.image_id       = image_id
        self.label_id       = label_id
        self.top            = min(top, bottom)
        self.left           = min(left, right)
        self.bottom         = max(top, bottom)
        self.right          = max(left, right)
        self.time_effort    = time_effort
        self.token          = token
        self.creation_date  = creation_date
        self.is_validated   = is_validated
        self.is_correct     = is_correct
        self.raycast        = None


class Image:

    def __init__(self, name, x, y, pitch, heading, camera_height, fov, annotations, country, direction, width = 2008, height = 646):
        self.name           = name
        self.lng            = x
        self.lat            = y
        self.pitch          = pitch
        self.heading        = heading
        self.camera_height  = camera_height
        self.fov            = fov
        self.n_annotations  = annotations
        self.annotations    = []
        self.country        = country
        self.direction      = direction
        self.width          = width
        self.height         = height

    def append_annotation(self, annotation):
        annotation.raycast = Raycast(latlng.LatLng(self.lat,self.lng), self.width, self.height, (annotation.left+annotation.right)/2, annotation.top, self.heading, self.height, self.pitch, self.fov)
        self.annotations.append(annotation)


class City:

    def __init__(self, map_file):
        self.buildings = BuildingManager(map_file)

    def locate(self, annotation):
        i = annotation.raycast.intersection(self.buildings)
        if i == None or i["latlng"] == None:
            return None
        return (i["latlng"].lng, i["latlng"].lat)

    def plot(self, annotation):
        plt.figure()
        i = city.locate(annotation)
        list = self.buildings.find_buildings(annotation.raycast.camera_latlng)
        for bb in list:
            ndx = [nd.lng for nd in bb.nodes]
            ndy = [nd.lat for nd in bb.nodes]
            plt.plot(ndx, ndy)
        if i == None:
            annotation.raycast.plot()
        else:
            plt.scatter(annotation.raycast.camera_latlng.lng, annotation.raycast.camera_latlng.lat)
            plt.plot([annotation.raycast.camera_latlng.lng, i[0]],[annotation.raycast.camera_latlng.lat, i[1]])
        plt.show()


if __name__=="__main__":

    images = {}
    annotations = {}

    city = City("location_estimator/maps/manhattan/buildings_manhattan.xml")

    with open('location_estimator/image.csv') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                images[row[0]] = Image(row[1], float(row[2]), float(row[3]), float(row[4]), float(row[5]), 1.979, float(row[7]), int(row[8]), row[9], float(row[10]))

    f = open('location_estimator/annotation_new.csv','w')
    store_count = 0

    with open('location_estimator/annotation.csv') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                f.write(','.join(row)+',est_lat,est_lng\n')
                line_count += 1
            else:
                a = Annotation(row[1], row[2], row[3], int(row[4]), int(row[5]), int(row[6]), int(row[7]), int(row[8]), row[9], row[10], row[11], is_correct = 1)
                annotations[row[0]] = a
                if images[row[2]].country == "us":
                    images[row[2]].append_annotation(a)
                    l = city.locate(a)
                    # if store_count < 20: city.plot(a)
                    if l != None:
                        f.write(','.join(row)+','+str(l[1])+','+str(l[0])+'\n')
                        store_count += 1
                    else:
                        f.write(','.join(row)+',,\n')

    print(store_count)

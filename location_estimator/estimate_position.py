import sys
sys.path.append("./location_estimator")
sys.path.append("./location_estimator/py")
import math
import latlng
from buildingmanager import *
import matplotlib.pyplot as plt

class Segment:

    def __init__(self, end1, end2):
        self.end1 = end1
        self.end2 = end2


class Raycast:

    def __init__(self, camera_latlng, screen_width, screen_height, screen_x, screen_y, heading, camera_height = 2, pitch = 0, fov = 90):
        self.camera_latlng = camera_latlng
        self.heading = heading
        self.pitch = pitch
        self.fov = fov
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen_x = 2.0 * screen_x/screen_width - 1.0
        self.screen_y = 1.0 - 2.0 * screen_y/screen_height
        self.aspect = screen_width / screen_height
        self.camera_height = camera_height

    def get_raycast(self):
        return {"pitch": self.pitch + 0.5 * self.screen_y * self.fov / self.aspect,\
                "heading": self.heading + 0.5 * self.screen_x * self.fov}

    def get_distance(self):
        theta = self.get_raycast()["pitch"]
        if -1 > theta and theta > -89:
            return abs(self.camera_height / math.tan(theta/180.0*math.pi))
        else:
            return None

    def get_latlng(self): # intersection with ground
        heading = ((360 - self.get_raycast()["heading"]) + 90)%360
        distance = self.get_distance()
        if distance is None: return None
        x = distance * math.cos(heading/180.0*math.pi)
        y = distance * math.sin(heading/180.0*math.pi)
        return self.camera_latlng.get_latlng(x,y)

    def get_range(self, segment):
        x3 = self.camera_latlng.get_xy(segment.end1).x
        y3 = self.camera_latlng.get_xy(segment.end1).y
        x4 = self.camera_latlng.get_xy(segment.end2).x
        y4 = self.camera_latlng.get_xy(segment.end2).y
        heading1 = (math.atan2(x3, y3) / math.pi * 180 + 360)%360
        heading2 = (math.atan2(x4, y4) / math.pi * 180 + 360)%360
        heading1 = min(heading1, self.heading + 0.5 * self.fov)
        heading1 = max(heading1, self.heading - 0.5 * self.fov)
        heading2 = min(heading2, self.heading + 0.5 * self.fov)
        heading2 = max(heading2, self.heading - 0.5 * self.fov)
        x1 = (heading1 - self.heading + 0.5 * self.fov) / self.fov * self.screen_width
        x2 = (heading2 - self.heading + 0.5 * self.fov) / self.fov * self.screen_width
        return min(x1,x2), max(x1,x2)

    def intersection2d(self, segment):
        p2 = self.get_latlng()
        x2 = self.camera_latlng.get_xy(p2).x
        y2 = self.camera_latlng.get_xy(p2).y
        x3 = self.camera_latlng.get_xy(segment.end1).x
        y3 = self.camera_latlng.get_xy(segment.end1).y
        x4 = self.camera_latlng.get_xy(segment.end2).x
        y4 = self.camera_latlng.get_xy(segment.end2).y
        if ( x4 * y2 - x3 * y2 - x2 * y4 + x2 * y3 ) == 0 or ( y4 * x2 - y3 * x2 - y2 * x4 + y2 * x3 ) == 0:
            return None
        x = ( y3 * x4 * x2 - y4 * x3 * x2 ) / ( x4 * y2 - x3 * y2 - x2 * y4 + x2 * y3 )
        y = ( -y3 * x4 * y2 + y4 * x3 * y2) / ( y4 * x2 - y3 * x2 - y2 * x4 + y2 * x3 )
        if min(0,x2) <= x and x<= max(0,x2) and min(x3,x4) <= x and x <= max(x3,x4) and \
           min(0,y2) <= y and y<= max(0,y2) and min(y3,y4) <= y and y <= max(y3,y4):
            return self.camera_latlng.get_latlng(x,y)
        return None

    def intersection(self, buidlings):
        list = buidlings.find_buildings(self.camera_latlng)
        mindis = 1e99
        inter_latlng = None
        inter_building = None
        inter_x = None
        inter_seg = None

        for b in list:
            x = 0
            for i in range(len(b.nodes)-1):
                seg = Segment(b.nodes[i],b.nodes[i+1])
                p = self.intersection2d( seg )
                if p is not None:
                    d = self.camera_latlng.get_distance(p)
                    if d < mindis:
                        mindis = d
                        inter_latlng = p
                        inter_building = b
                        inter_seg = seg
                        inter_x = x + b.nodes[i].get_distance(inter_latlng)
                x += b.nodes[i].get_distance(b.nodes[i+1])
        return {"latlng":inter_latlng, "height":mindis/self.get_distance() * self.camera_height, "building":inter_building, "segment":inter_seg, "x":inter_x}
        # x is the length of the edges from beginning point of the building to the intersection
        # this x and the height of the intersection are combined as coordinate (x,y) used for aggregation

    def plot(self):
        p2 = self.get_latlng()
        plt.scatter(self.camera_latlng.lng, self.camera_latlng.lat)
        plt.plot([self.camera_latlng.lng,p2.lng],[self.camera_latlng.lat,p2.lat])


point = latlng.LatLng(42.3580053,-71.0627095)
heading = 275
r = Raycast(point,400,400,200,205,heading)
r.plot()

b = BuildingManager("location_estimator/samples/boston/buildings_boston.xml")
list = b.find_buildings(point)
for bb in list:
    ndx = []
    ndy = []
    for nd in bb.nodes:
        ndx.append(nd.lng)
        ndy.append(nd.lat)
    plt.plot(ndx, ndy)

p = r.intersection(b)
plt.scatter(p["latlng"].lng,p["latlng"].lat)
x1, x2 = r.get_range(p["segment"])
Raycast(point,400,400,x1,205,heading).plot()
Raycast(point,400,400,x2,205,heading).plot()

plt.show()

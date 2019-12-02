from xml.dom.minidom import parse
import xml.dom.minidom
import latlng
import math

class Building:

    def __init__(self, ref, nodes):
        self.ref = ref
        self.nodes = nodes
        self.labels = []


class BuildingManager:

    def __init__(self, xml_filename):
        self.buildings = []

        DOMTree = xml.dom.minidom.parse(xml_filename)
        root = DOMTree.documentElement
        xml_buildings = root.getElementsByTagName("building")
        i = 0
        for xml_building in xml_buildings:
            coords = []
            nodes = xml_building.getElementsByTagName("node")
            for node in nodes:
                coords.append( latlng.LatLng(float(node.getAttribute('lat')),float(node.getAttribute('lng'))) )
            self.buildings.append(Building(i,coords))
        self.create_grid()

    def create_grid(self, interval = 50):
        self.building_grid = []
        self.interval = interval

        max_lat = -999999
        max_lng = -999999
        min_lat = 9999999
        min_lng = 9999999
        for b in self.buildings:
            for nd in b.nodes:
                max_lat = max(max_lat, nd.lat)
                max_lng = max(max_lng, nd.lng)
                min_lat = min(min_lat, nd.lat)
                min_lng = min(min_lng, nd.lng)
        width = abs(latlng.LatLng(min_lat,min_lng).get_xy(latlng.LatLng(max_lat, max_lng)).x)
        height = abs(latlng.LatLng(min_lat,min_lng).get_xy(latlng.LatLng(max_lat, max_lng)).y)
        self.min_lat = min_lat
        self.min_lng = min_lng

        self.nx = int(width / interval) + 3
        self.ny = int(height / interval) + 3

        for i in range(self.nx):
            tmp = []
            for j in range(self.ny):
                tmp.append([])
            self.building_grid.append(tmp)

        for b in self.buildings:
            for nd in b.nodes:
                x = abs(latlng.LatLng(min_lat,min_lng).get_xy(nd).x)
                y = abs(latlng.LatLng(min_lat,min_lng).get_xy(nd).y)
                self.building_grid[int(x/interval) + 1][int(y/interval) + 1].append(b)

    def find_buildings(self, point):
        x = abs(latlng.LatLng(self.min_lat,self.min_lng).get_xy(point).x)
        y = abs(latlng.LatLng(self.min_lat,self.min_lng).get_xy(point).y)
        list = []
        for i in range(-1,2):
            for j in range(-1,2):
                for b in self.building_grid[int(x/self.interval) + i][int(y/self.interval) + j]:
                    if b not in list:
                        list.append(b)
        return list

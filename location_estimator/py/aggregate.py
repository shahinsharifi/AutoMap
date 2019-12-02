import numpy as np
import latlng
from matplotlib import pyplot as plt

class Aggregator:

    def __init__(self, threshold_1 = 2.5, threshold_2 = 5):
    # threshold_1: radius for calculating density, threshold_2: min dis between objects
        self.objects = []
        self.weights = []
        self.aggregated_objects = []
        self.threshold_1 = threshold_1
        self.threshold_2 = threshold_2

    def add_object(self, x, y, weight = 1):
        self.objects.append(latlng.Cartesian(x,y))
        self.weights.append(weight)

    def aggregate(self):
        num = len(self.objects)
        px = np.zeros(num)
        py = np.zeros(num)
        rho = np.zeros(num)
        ax = np.zeros(num)
        ay = np.zeros(num)
        if num < 1: return
        for i in range(1,num):
            xy = self.objects[i]
            px[i] = xy.x
            py[i] = xy.y
        for i in range(num):
            s = self.weights[i]
            ave_x = px[i] * self.weights[i]
            ave_y = py[i] * self.weights[i]
            for j in range(num):
                if i!=j and (px[i]-px[j])**2 + (py[i]-py[j])**2 < self.threshold_1 **2:
                    # something can be done here - for instance, considering the text/width/height of the label
                    s += self.weights[j]
                    ave_x += px[j] * self.weights[j]
                    ave_y += py[j] * self.weights[j]
            rho[i] = s + np.random.rand()*0.01
            ax[i] = ave_x/s
            ay[i] = ave_y/s

        dis = np.zeros(num)

        for i in range(num):
            m = 2147483647
            for j in range(num):
                if (rho[j] > rho[i]) and ((px[i]-px[j])**2 + (py[i]-py[j])**2 < m):
                    m = (px[i]-px[j])**2 + (py[i]-py[j])**2
            dis[i] = m

        self.aggregated_objects = []
        for i in range(num):
            if dis[i] > self.threshold_2**2 and rho[i] >= 1:
                self.aggregated_objects.append(latlng.Cartesian(ax[i],ay[i]))

import requests
import os
import PIL.Image as Image

folder_name = "pano"
key = "AIzaSyA7MIhe-OZEx4An2EQKAmVVwKCR6VMqQQA"

lat = []
lng = []

def download_image(id):
    for i in range(4):
        heading = i * 90
        filename = folder_name+"/"+str(id)+"_"+str(heading)+".png"
        if os.path.exists(filename):
            return
        request = "https://maps.googleapis.com/maps/api/streetview?size=640x640";
        request += "&location=" + str(lat[id])+","+str(lng[id]);
        request += "&heading=" + str(heading);
        request += "&pitch=0&fov=90&key=" + key;
        # print(request)
        r = requests.get(request)
        with open(filename,'wb') as f:
            f.write(r.content)

f = open("points_boston.csv","r")
for line in f:
    latlng = line.split(",")
    lat.append(float(latlng[0]))
    lng.append(float(latlng[1]))


import matplotlib.pyplot as plt

plt.scatter(lng,lat)
plt.show()

#
# for i in range(100):
#     download_image(i)


## Gemeente Amsterdam

request_head = "https://api.data.amsterdam.nl/panorama/opnamelocatie/"

import json

def download_cubic_images(lat,lng):
    request = request_head + "?format=json&lat=" + str(lat) + "&lon=" + str(lng);
    r = requests.get(request)
    j = json.loads(r.content)
    baseurl = j["image_sets"]["cubic"]["baseurl"]
    id = baseurl.split("/")[-3]
    if not os.path.exists("cubic/"+id):
        os.mkdir("cubic/"+id)
        os.mkdir("cubic/"+id+"/sub")
    # f=front, b=back, u=up, d=down, l=left, r=right
    # V = ["f","b","u","d","l","r"]
    V = ["f","b","l","r"]
    z = 3
    for v in V:
        for x in range(z+1):
            for y in range(z+1):
                image_url = baseurl+str(z)+"/"+v+"/"+str(x)+"/"+str(y)+".jpg"
                filename = "cubic/"+id+"/sub/"+str(z)+"_"+v+"_"+str(x)+"_"+str(y)+".jpg"
                if os.path.exists(filename):
                    continue
                r = requests.get(image_url)
                with open(filename,'wb') as f:
                    f.write(r.content)
        combine_images(id,z,v).save("cubic/"+id+"/"+str(z)+"_"+v+".jpg","JPEG")

def combine_images(id,z,v):
    filename = "cubic/"+id+"/sub/"+str(z)+"_"+v+"_0_0.jpg"
    img = Image.open(filename)
    w, h = img.size
    newimg = Image.new('RGB', (h * (z+1) , w * (z+1)))
    for x in range(z+1):
        for y in range(z+1):
            filename = "cubic/"+id+"/sub/"+str(z)+"_"+v+"_"+str(x)+"_"+str(y)+".jpg"
            img = Image.open(filename)
            newimg.paste(img, (y * h, x * w))
    return newimg

download_cubic_images(52.375402011376, 4.89601072076594)

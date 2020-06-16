#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from PIL import Image, ImageDraw, ImageFont
import numpy as np
import pandas as pd
import folium
from folium import plugins
import matplotlib.pyplot as plt
import matplotlib.colors
from matplotlib.colors import LinearSegmentedColormap, rgb_to_hsv, hsv_to_rgb
import scipy.ndimage.filters
import time
import datetime
import os.path
import io

import os
os.environ["PATH"] += os.pathsep + "."

get_ipython().magic('matplotlib inline')


# In[ ]:


from PIL import Image, ImageDraw, ImageFont
import numpy as np
import pandas as pd
import folium
from folium import plugins
import matplotlib.pyplot as plt
import matplotlib.colors
from matplotlib.colors import LinearSegmentedColormap, rgb_to_hsv, hsv_to_rgb
import scipy.ndimage.filters
import time
import datetime


# In[ ]:


import numpy as np
import pandas as pd


# In[ ]:


data_201701 = pd.read_csv('C:/Users/Ja/Desktop/Studia/Python/PD3/201701-citibike-tripdata.csv')


# In[4]:


data_201702 = pd.read_csv('C:/Users/Ja/Desktop/Studia/Python/PD3/201702-citibike-tripdata.csv')
data_201703 = pd.read_csv('C:/Users/Ja/Desktop/Studia/Python/PD3/201703-citibike-tripdata.csv')
data_201704 = pd.read_csv('C:/Users/Ja/Desktop/Studia/Python/PD3/201704-citibike-tripdata.csv')
data_201705 = pd.read_csv('C:/Users/Ja/Desktop/Studia/Python/PD3/201705-citibike-tripdata.csv')
data_201706 = pd.read_csv('C:/Users/Ja/Desktop/Studia/Python/PD3/201706-citibike-tripdata.csv')
data_201707 = pd.read_csv('C:/Users/Ja/Desktop/Studia/Python/PD3/201707-citibike-tripdata.csv')
data_201708 = pd.read_csv('C:/Users/Ja/Desktop/Studia/Python/PD3/201708-citibike-tripdata.csv')
data_201709 = pd.read_csv('C:/Users/Ja/Desktop/Studia/Python/PD3/201709-citibike-tripdata.csv')
data_201710 = pd.read_csv('C:/Users/Ja/Desktop/Studia/Python/PD3/201710-citibike-tripdata.csv')
data_201711 = pd.read_csv('C:/Users/Ja/Desktop/Studia/Python/PD3/201711-citibike-tripdata.csv')
data_201712 = pd.read_csv('C:/Users/Ja/Desktop/Studia/Python/PD3/201712-citibike-tripdata.csv')
data_201801 = pd.read_csv('C:/Users/Ja/Desktop/Studia/Python/PD3/201801-citibike-tripdata.csv')
data_201802 = pd.read_csv('C:/Users/Ja/Desktop/Studia/Python/PD3/201802-citibike-tripdata.csv')
data_201803 = pd.read_csv('C:/Users/Ja/Desktop/Studia/Python/PD3/201803-citibike-tripdata.csv')
data_201804 = pd.read_csv('C:/Users/Ja/Desktop/Studia/Python/PD3/201804-citibike-tripdata.csv')
data_201805 = pd.read_csv('C:/Users/Ja/Desktop/Studia/Python/PD3/201805-citibike-tripdata.csv')
data_201806 = pd.read_csv('C:/Users/Ja/Desktop/Studia/Python/PD3/201806-citibike-tripdata.csv')
data_201807 = pd.read_csv('C:/Users/Ja/Desktop/Studia/Python/PD3/201807-citibike-tripdata.csv')
data_201808 = pd.read_csv('C:/Users/Ja/Desktop/Studia/Python/PD3/201808-citibike-tripdata.csv')
data_201809 = pd.read_csv('C:/Users/Ja/Desktop/Studia/Python/PD3/201809-citibike-tripdata.csv')
data_201810 = pd.read_csv('C:/Users/Ja/Desktop/Studia/Python/PD3/201810-citibike-tripdata.csv')
data_201811 = pd.read_csv('C:/Users/Ja/Desktop/Studia/Python/PD3/201811-citibike-tripdata.csv')
data_201812 = pd.read_csv('C:/Users/Ja/Desktop/Studia/Python/PD3/201812-citibike-tripdata.csv')


# In[51]:


data_201812


# Cool! Locations that have positive net departures in the morning have net arrivals in the evening. We can see the heartbeat of the city. This could be the starting point for further analysis, perhaps an algorithm to predict arrivals to help the system operator manage the system, or predict bike availability for users looking for a bike.

#  we already noticed some bike migration: at 9am, some regions have more bike departures and different regions have more bike arrivals. In this tutorial we will show which paths people take. We will put particular emphasis on creating a customized visual appearance. 

# we will: \
# 1.customize the effect of overlapping paths to show traffic density, and \
# 2.we will add a glow effect to draw attention to high density areas.
# To achieve these effects we will use a raster layer (i.e. an image overlay) to draw our own pixels instead of using the built-in objects in folium to draw the paths (e.g. using PolyLine)

# In[104]:


def add_lines(image_array, xys, width=1, weights=None):
    """
    Add a set of lines (xys) to an existing image_array
    width: width of lines
    weights: [], optional list of multipliers for lines. 
    """
    
    for i, xy in enumerate(xys):  # loop over lines
        # create a new gray scale image
        image = Image.new("L",(image_array.shape[1], image_array.shape[0]))
        
        # draw the line
        ImageDraw.Draw(image).line(xy, 200, width=width)
        
        #convert to array
        new_image_array = np.asarray(image, dtype=np.uint8).astype(float)
        
        # apply weights if provided
        if weights is not None:
            new_image_array *= weights[i]
            
        # add to existing array
        image_array += new_image_array

    # convolve image
    new_image_array = scipy.ndimage.filters.convolve(image_array, get_kernel(width*4)) 
    return new_image_array


# In[105]:


def get_kernel(kernel_size, blur=1/20, halo=.001):
    """
    Create an (n*2+1)x(n*2+1) numpy array.
    Output can be used as the kernel for convolution.
    """
    
    # generate x and y grids
    x, y = np.mgrid[0:kernel_size*2+1, 0:kernel_size*2+1]
    
    center = kernel_size + 1  # center pixel
    r = np.sqrt((x - center)**2 + (y - center)**2)  # distance from center
    
    # now compute the kernel. This function is a bit arbitrary. 
    # adjust this to get the effect you want.
    kernel = np.exp(-r/kernel_size/blur) + (1 - r/r[center,0]).clip(0)*halo
    return kernel


# In[106]:


def to_image(array, hue=.62):
    """converts an array of floats to an array of RGB values using a colormap"""
    
    # apply saturation function
    image_data = np.log(array + 1)
    
    # create colormap, change these values to adjust to look of your plot
    saturation_values = [[0, 0], [1, .68], [.78, .87], [0, 1]]
    colors = [hsv_to_rgb([hue, x, y]) for x, y in saturation_values]
    cmap = LinearSegmentedColormap.from_list("my_colormap", colors)
    
    # apply colormap
    out = cmap(image_data/image_data.max())
    
    # convert to 8-bit unsigned integer
    out = (out*255).astype(np.uint8)
    return out


# In[107]:


min_lat = data_201812["start station latitude"].min()
max_lat = data_201812["start station latitude"].max()
max_lon = data_201812["start station longitude"].max()
min_lon = data_201812["start station longitude"].min()

def latlon_to_pixel(lat, lon, image_shape):
    # longitude to pixel conversion (fit data to image)
    delta_x = image_shape[1]/(max_lon-min_lon)
    
    # latitude to pixel conversion (maintain aspect ratio)
    delta_y = delta_x/np.cos(lat/360*np.pi*2)
    pixel_y = (max_lat-lat)*delta_y
    pixel_x = (lon-min_lon)*delta_x
    return (pixel_y,pixel_x)


# In[108]:


def row_to_pixel(row,image_shape):
    """
    convert a row (1 trip) to pixel coordinates
    of start and end point
    """
    start_y, start_x = latlon_to_pixel(row["start station latitude"], 
                                       row["start station longitude"], image_shape)
    end_y, end_x = latlon_to_pixel(row["end station latitude"], 
                                   row["end station longitude"], image_shape)
    xy = (start_x, start_y, end_x, end_y)
    return xy


# In[109]:


paths = data_201812[data_201812.hour==9]
paths = paths.iloc[:3000,:]
# generate empty pixel array, choose your resolution
image_data = np.zeros((900,400))
# generate pixel coordinates of starting points and end points
xys = [row_to_pixel(row, image_data.shape) for i, row in paths.iterrows()]
# draw the lines
image_data = add_lines(image_data, xys, weights=None, width = 1)
Image.fromarray(to_image(image_data*10)[:,:,:3],mode="RGB")


# In[110]:


def add_alpha(image_data):
    """
    Uses the Value in HSV as an alpha channel. 
    This creates an image that blends nicely with a black background.
    """
    
    # get hsv image
    hsv = rgb_to_hsv(image_data[:,:,:3].astype(float)/255)
    
    # create new image and set alpha channel
    new_image_data = np.zeros(image_data.shape)
    new_image_data[:,:,3] = hsv[:,:,2]
    
    # set value of hsv image to either 0 or 1.
    hsv[:,:,2] = np.where(hsv[:,:,2]>0, 1, 0)
    
    # combine alpha and new rgb
    new_image_data[:,:,:3] = hsv_to_rgb(hsv)
    return new_image_data


# In[115]:


# make a list of locations (latitude longitude) for each station id
locations = data_201812.groupby("start station id").mean()
locations = locations.loc[:,["start station latitude", "start station longitude"]]

# group by each unique pair of (start-station, end-station) and count the number of trips
data_201812["path_id"] = [(id1,id2) for id1,id2 in zip(data_201812["start station id"], 
                                                     data_201812["end station id"])]
paths = data_201812[data_201812["hour"]==9].groupby("path_id").count().iloc[:,[1]] 
paths.columns = ["Trip Count"]

# select only paths with more than X trips
paths = paths[paths["Trip Count"]>5]
paths["start station id"] = paths.index.map(lambda x:x[0])
paths["end station id"] = paths.index.map(lambda x:x[1])
paths = paths[paths["start station id"]!=paths["end station id"]]

# join latitude/longitude into new table
paths = paths.join(locations,on="start station id")
locations.columns = ["end station latitude","end station longitude"]
paths = paths.join(locations,on="end station id")
paths.index = range(len(paths))

paths.shape


# In[116]:


def get_image_data(paths, min_count=0, max_count=None):
    # generate empty pixel array
    image_data = np.zeros((900*2,400*2))
    
    # generate pixel coordinates of starting points and end points
    if max_count is None:
        max_count = paths["Trip Count"].max()+1
    selector = (paths["Trip Count"]>= min_count) & (paths["Trip Count"]< max_count)
    xys = [row_to_pixel(row, image_data.shape) for i, row in paths[selector].iterrows()]

    # draw the lines
    image_data = add_lines(image_data, xys, weights=paths["Trip Count"], width = 1)
    return image_data


# In[117]:


# create the map
folium_map = folium.Map(location=[40.738, -73.98],
                        zoom_start=13,
                        tiles="CartoDB dark_matter",
                        width='50%')

# create the overlay
map_overlay = add_alpha(to_image(image_data*10))

# compute extent of image in lat/lon
aspect_ratio = map_overlay.shape[1]/map_overlay.shape[0]
delta_lat = (max_lon-min_lon)/aspect_ratio*np.cos(min_lat/360*2*np.pi)

# add the image to the map
img = folium.raster_layers.ImageOverlay(map_overlay,
                           bounds = [(max_lat-delta_lat,min_lon),(max_lat,max_lon)],
                           opacity = 1,
                           name = "Paths")

img.add_to(folium_map)
folium.LayerControl().add_to(folium_map)

# show the map
folium_map


# In[118]:


folium_map = folium.Map(location=[40.738, -73.98],
                        zoom_start=13,
                        tiles="CartoDB dark_matter",
                        width='50%')

thresholds = [5,15,25]

for i,t in enumerate(thresholds):
    upper = thresholds[i+1] if i<len(thresholds)-1 else None
    image_data = get_image_data(paths, t, upper)
    name = "{} < Num. Trips < {}".format(t,"max" if upper is None else upper)

    map_overlay = add_alpha(to_image(image_data*10))
    delta_lat = (max_lon-min_lon)/map_overlay.shape[1]*map_overlay.shape[0]*np.cos(min_lat/360*2*np.pi)
    img = folium.raster_layers.ImageOverlay(map_overlay,
                               bounds = [(max_lat-delta_lat,min_lon),(max_lat,max_lon)],
                               name = name)

    img.add_to(folium_map)

lc = folium.LayerControl().add_to(folium_map)

folium_map


# To help the user explore the data in more detail, we can add multiple layers and use this LayerControl to toggle between different layers. For example, we can make separate layers for frequently used paths and for infrequently used paths. \
# It’s a bit hard to make out individual trips when there are many on the map, using multiple layers helps with this. We can see how most trips happen in Midtown and are fairly short.

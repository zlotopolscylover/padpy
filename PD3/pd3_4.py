#!/usr/bin/env python
# coding: utf-8

# In[172]:


import pandas as pd
import matplotlib.pyplot as plt


# In[123]:


from mpl_toolkits.basemap import Basemap


# In[118]:


import os
os.environ['PROJ_LIB'] = 'C:/Users/Ja/Anaconda3/Library/share'


# In[122]:


#conda install -c conda-forge basemap-data-hires


# In[174]:


import geopy


# In[173]:


from geopy.distance import vincenty
from geopy.distance import distance


# In[175]:


import itertools


# In[176]:


data_201707 = pd.read_csv('C:/Users/Ja/Desktop/Studia/Python/PD3/201707-citibike-tripdata.csv')
#data_201707


# In[158]:


data_201707.columns


# In[78]:


t1 = data_201707[['start station id', 'start station name', 'start station latitude', 'start station longitude']]             .drop_duplicates().rename(columns = {'start station id':'station id',                                                  'start station name':'station name',                                                  'start station latitude':'station latitude', 
                                                 'start station longitude': 'station longitude'})
t2 = data_201707[['end station id', 'end station name', 'end station latitude', 'end station longitude']]         .drop_duplicates().rename(columns = {'end station id':'station id',                                              'end station name':'station name',                                              'end station latitude':'station latitude',                                              'end station longitude': 'station longitude'})
df_loc = pd.concat([t1, t2]).drop_duplicates()


# In[124]:


# Initialize plots
fig, ax = plt.subplots(figsize=(15,15))

# determine range to print based on min, max lat and lon of the data
lat = list(df_loc['station latitude'])
lon = list(df_loc['station longitude'])
text = list(df_loc['station id'])
margin = 0.01 # buffer to add to the range
lat_min = min(lat) - margin
lat_max = max(lat) + margin
lon_min = min(lon) - margin
lon_max = max(lon) + margin

# create map using BASEMAP
m = Basemap(llcrnrlon=lon_min,
            llcrnrlat=lat_min,
            urcrnrlon=lon_max,
            urcrnrlat=lat_max,
            lat_0=(lat_max - lat_min)/2,
            lon_0=(lon_max - lon_min)/2,
            projection='lcc',
            resolution = 'f',)

m.drawcoastlines()
m.fillcontinents(lake_color='aqua')
m.drawmapboundary(fill_color='aqua')
m.drawrivers()

# convert lat and lon to map projection coordinates
lons, lats = m(lon, lat)

# plot points as red dots
ax.scatter(lons, lats, marker = 'o', color='r', zorder=5, alpha=0.6)
for i in range(df_loc.shape[0]):
    plt.text(lons[i], lats[i], text[i])
plt.show()


# In[79]:


# format example: 2017-07-01 00:00:00
data_201707['starttime'] = pd.to_datetime(data_201707['starttime'], format='%Y-%m-%d %H:%M:%S')
data_201707['stoptime'] =pd.to_datetime(data_201707['stoptime'], format='%Y-%m-%d %H:%M:%S')
data_201707.info()


# In[80]:


def gen_time_segment(dt):
    if dt.minute < 30:
        minute = "%02d" % 0
    else:
        minute = "%02d" % 30
    return "{}-{}-{} {}:{}".format(dt.year, dt.month, dt.day, dt.hour, minute)

data_201707['start_seg'] = [gen_time_segment(dt) for dt in data_201707['starttime']]
data_201707['stop_seg'] = [gen_time_segment(dt) for dt in data_201707['stoptime']]


# In[82]:


data_201707[['start station id', 'starttime', 'start_seg', 'end station id', 'stoptime', 'stop_seg']].head()


# In[83]:


inflow = data_201707[['end station id', 'stop_seg']]             .groupby(['end station id', 'stop_seg'])             .size().reset_index(name='counts')             .rename(columns={'end station id':'station id','stop_seg':'time', 'counts':'in_flow_count'})


# In[84]:


outflow = data_201707[['start station id', 'start_seg']]             .groupby(['start station id', 'start_seg'])             .size().reset_index(name='counts')             .rename(columns={'start station id':'station id','start_seg':'time', 'counts':'out_flow_count'})


# In[85]:


station_id_list = list(df_loc['station id'])

# Create combinations of time series and station ids
time_seg_list = list(pd.date_range("2017-07-01 00:00:00", "2017-07-31 23:30:00", freq="30min"))
template = pd.DataFrame(list(itertools.product(station_id_list, time_seg_list)),                         columns=["station id", "time"])

# Merge in/out flow information & Add zeros to missing data according to every time segment
dat = pd.merge(inflow, outflow, on=['station id', 'time'], how='outer')
dat['time'] = pd.to_datetime(dat['time'], format='%Y-%m-%d %H:%M')
dat = dat.merge(template, on=["station id", "time"], how="right").fillna(0)
dat.head()


# # How many stations are there in this dataset,and what is the average distance between them?

# In[86]:


print("{} stations are found in this dataset.".format(len(station_id_list)))


# In[100]:


# Create dictionaries for station latitude/longitude
lat_dic = {}
lon_dic = {}
for index, row in df_loc.iterrows():
    lat_dic[row['station id']] = row['station latitude']
    lon_dic[row['station id']] = row['station longitude']

# Generate combinations of pairs of station
c = itertools.combinations(station_id_list, 2)

# Calculate the averge distance of pairs of stations
dist = 0
count = 0
for stn1, stn2 in c:
        dist += distance((lat_dic[stn1], lon_dic[stn1]), (lat_dic[stn2], lon_dic[stn2])).meters
        count += 1
print("The average distance between different stations is {} (meters)".format(dist/count))


# Jest większa ta odległość bo nie wyrzuciliśmy tej jednej stacji jak ten koeś na stronie.

# # What are the top 3 frequent stations pairs (start station, end station) in weekdays, how about in weekends?

# In[101]:


# Split the dataframe into weekdays information & weekends information
df_weekdays = data_201707[data_201707['starttime'].dt.dayofweek < 5]
df_weekends = data_201707[data_201707['starttime'].dt.dayofweek >= 5]

# Count and sort station pair frequencies
stn_pair_weekdays = df_weekdays[['start station id', 'end station id']]                     .groupby(['start station id', 'end station id'])                     .size().reset_index(name='counts')                     .set_index(['start station id', 'end station id'])                     .sort_values(by='counts', ascending=False)
stn_pair_weekends = df_weekends[['start station id', 'end station id']]                     .groupby(['start station id', 'end station id'])                     .size().reset_index(name='counts')                     .set_index(['start station id', 'end station id'])                     .sort_values(by='counts', ascending=False)
            
# Find the top 3 station pairs for weekday & weekend
top_weekday_pair = list(stn_pair_weekdays.head(3).index)
top_weekend_pair = list(stn_pair_weekends.head(3).index)

# Print out the result
print("The top 3 frequent stations pairs in weekdays are: {}, {}, and {}.".format(*top_weekday_pair))
print("The top 3 frequent stations pairs in weekends are: {}, {}, and {}.".format(*top_weekend_pair))


# Tutaj znajdź co to konkretnie za stacje i może pokaż na mapie

# # Find the top 3 stations with highest average out-flow, and top 3 highest average in-flow

# In[102]:


# Sort the average in/out flow count of each station
average_inflow = dat[['station id', 'in_flow_count']]                 .groupby(['station id'])                 .mean()                 .sort_values(by='in_flow_count', ascending=False)
average_outflow = dat[['station id', 'out_flow_count']]                 .groupby(['station id'])                 .mean()                 .sort_values(by='out_flow_count', ascending=False)
            
# List the top 3 stations
top_inflow = list(average_inflow.head(3).index)
top_outflow = list(average_outflow.head(3).index)

# Print out the result
print("The top 3 stations with highest outflow are: {}, {}, and {}".format(*top_outflow))
print("The top 3 stations with highest inflow are: {}, {}, and {}".format(*top_inflow))


# # What is the most popular station(highest average inflow+outflow)?

# In[103]:


# Sum up in/out flow at each time station
dat['flow_count'] = dat['in_flow_count'] + dat['out_flow_count']

# Calculate and sort the average flow count for each station
average_flow = dat[['station id', 'flow_count']]                 .groupby(['station id'])                 .mean()                 .sort_values(by='flow_count', ascending=False)
            
# Find the top 1 station
top_flow = list(average_inflow.head(1).index)

# Print out the result
print("The most popular station is: {}".format(*top_outflow))


# ## a. Draw the in-flow(A) and out-flow(B) for that station in a line chart

# In[104]:


# Select station & add information in missing time
small_df = dat[dat['station id'] == 519].sort_values(by='time')
small_df = small_df.sort_values(by='time')

# Plot line chart
small_df.plot(x='time', y=['in_flow_count', 'out_flow_count'], kind='line', figsize=(15,15))
plt.show()


# # Visualize the flows of citibikes over time

# In[105]:


def gen_time_group(dt):
    if dt.day <= 10:
        return "Early-July"
    elif dt.day <= 20:
        return "Mid-July"
    else:
        return "Late-July"


# In[106]:


# Calculate and sort the average flow count for each station
flow = dat[['station id', 'time', 'flow_count']] 

# Create time group
flow['time_group'] = [gen_time_group(dt) for dt in flow['time']]

# Summarise flow count according to time group
flow = flow.groupby(["station id", "time_group"], as_index=False)             .agg({'flow_count': 'sum'})

# Add latitude/logitude columns
flow['latitude'] = [lat_dic[x] for x in flow['station id']]
flow['longitude'] = [lon_dic[x] for x in flow['station id']]

flow.head()


# Then plot every popular stations on map.

# In[107]:


def plot_stations_map(ax, stns, noText=False):
    # determine range to print based on min, max lat and lon of the data
    lat = list(stns['latitude'])
    lon = list(stns['longitude'])
    siz = [(2)**(x/1000) for x in stns['flow_count']]
    margin = 0.01 # buffer to add to the range
    lat_min = min(lat) - margin
    lat_max = max(lat) + margin
    lon_min = min(lon) - margin
    lon_max = max(lon) + margin

    # create map using BASEMAP
    m = Basemap(llcrnrlon=lon_min,
                llcrnrlat=lat_min,
                urcrnrlon=lon_max,
                urcrnrlat=lat_max,
                lat_0=(lat_max - lat_min)/2,
                lon_0=(lon_max - lon_min)/2,
                projection='lcc',
                resolution = 'f',)

    m.drawcoastlines()
    m.fillcontinents(lake_color='aqua')
    m.drawmapboundary(fill_color='aqua')
    m.drawrivers()

    # convert lat and lon to map projection coordinates
    lons, lats = m(lon, lat)

    # plot points as red dots
    if noText:
        ax.scatter(lons, lats, marker = 'o', color='r', zorder=5, alpha=0.6, s=1)
        return
    else:
        ax.scatter(lons, lats, marker = 'o', color='r', zorder=5, alpha=0.3, s=siz)
    
    # annotate popular stations
    for i in range(len(siz)):
        if siz[i] >= 2**6:
            plt.text(lons[i], lats[i], text[i])


# In[125]:


pop_flow = flow[flow['flow_count'] > 2000]
fig, axes = plt.subplots(nrows=1, ncols=4, figsize=(15,15))
ax = plt.subplot(1, 4, 1)
ax.set_title("All Stations")
plot_stations_map(ax, flow, noText=True)
ax = plt.subplot(1, 4, 2)
ax.set_title("Popular Stations in Early July")
plot_stations_map(ax, pop_flow[pop_flow['time_group'] == "Early-July"])
ax = plt.subplot(1, 4, 3)
ax.set_title("Popular Stations in Mid July")
plot_stations_map(ax, pop_flow[pop_flow['time_group'] == "Mid-July"])
ax = plt.subplot(1, 4, 4)
ax.set_title("Popular Stations in Late July")
plot_stations_map(ax, pop_flow[pop_flow['time_group'] == "Late-July"])


# Here are my observations:
# 
# 1.Few people ride citibikes in Jersey City and Brooklyn, that is, the main flow of citibike concentrates in Manhattan.
# 
# 2.The poular stations in Brooklyn are nearly the same across the whole month.
# 
# 3.Although the top popular regions (locations with large red circle) look similar, the top popular stations are not the same across the whole month. (Check station id carefully you’ll see they are not the same.) 
# 
# 4.For popular regions, more and more people ride citibikes in Mid July and Late July.

# # Who is riding Citi Bike?

# In[170]:


average_age_df = data_201812            .groupby("birth year")             .size()            .reset_index(name="Count")            .sort_values("Count", ascending=False)            .head()
average_age_df
#tu dorobić hitogram


# In[171]:


gender_df = data_201812            .groupby("gender")             .size()            .reset_index(name="Count")            .sort_values("Count", ascending=False)            .head()
gender_df
#podział ze względu na płeć!


# In[ ]:





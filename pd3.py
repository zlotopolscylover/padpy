#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[4]:


data_201701 = pd.read_csv('C:/Users/Ja/Desktop/Studia/Python/PD3/201701-citibike-tripdata.csv')


# In[5]:


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


# Z której stacji najczęściej jeździli użytkownicy? - grudzień 2018, można zmienić na zestawienie z każdego miesiąca

# In[49]:


pytanie_1 = data_201812            .groupby("start station name")             .size()            .reset_index(name="Count")            .sort_values("Count", ascending=False)            .head(1)


# In[50]:


pytanie_1


# W którym dniu tygodnia rowerem jeździmy najdłużej?

# W jakich miesiącach ruch rowerowy jest duży?

# In[54]:





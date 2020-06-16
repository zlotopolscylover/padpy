#!/usr/bin/env python
# coding: utf-8

# In[129]:


#Zadanie 1
#import random
#import math

def simulated_annealing(f, N, T0, Tn, a, b):
    """
    Funkcja zwraca argument x, dla którego funkcja f osiaga minimum przy uzyciu algorytmu
    symulowanego wyzarzania.
    Na wejsciu przyjmuje postać funkcji, N - liczbę całkowitą taką, ze N>0, 
    T0, TN - liczby rzeczywiste takie, ze T0 > TN oraz a, b - liczby rzeczywiste takie, ze a < b.
    """
    assert (isinstance(N, int) and N>0), "N nie jest dodatnia całkowita"
    assert ((isinstance(T0, int) or isinstance(T0, float)) and (isinstance(Tn, int) or isinstance(Tn, float)) and T0 >Tn), "T0 nie jest l.rzecz. lub Tn nie jest l.rzecz. lub T0<=Tn"
    assert ((isinstance(a, int) or isinstance(a, float)) and (isinstance(b, int) or isinstance(b, float)) and a < b), "a nie jest l.rzecz. lub b nie jest l.rzecz. lub a >= b"
    x = random.uniform(a,b) #losowanie liczby pseudolowej z przedziału [a, b]
    T= T0
    for k in range(N): #dla el. od 0 do 4
        u1=random.uniform(-1,1) #losowanie liczby pseudolowej z przedziału [-1, 1]
        y=x+u1
        if f(x) > f(y): #jeżeli wartosć funkcji od arg. x > wartosci funkcji od arg. y
            x = y #to x staje się y-kiem
        else:
            u2 = random.uniform(0,1) #losowanie liczby pseudolowej z przedziału [0, 1]
            if math.exp((f(x)-f(y))/T) > u2: 
                x = y
        T=T0 * math.exp(-k/N * math.log(T0/Tn,2))
    return x


# In[13]:


#Przykład 1 


# In[95]:


def f(x):
    t = 0.1
    if x < -4:
        return(x**2 - 10.46)
    elif x <= 4:
        return(t*math.cos(14*x) + (1 - t) * 8*math.sin(x))
    elif x <= 6:
        return(t*math.cos(x) + (1 - t) * 0.5*math.sin(14*x))
    else:
        return(t*math.cos(6) + (1 - t) * 8*math.sin(14*6))


# In[106]:


simulated_annealing(f, 1000, 50, 1, -5, 5)


# In[109]:


#Przykład 2
simulated_annealing(lambda x: math.sin(x**2) + abs(x), 100, 50, 1, -5, 5)


# In[110]:


#Przykład 3 własny

def f(x):
    t = 0.1
    if x < -2:
        return(x**2 - 10.46)
    elif x <= 2:
        return(t*math.tan(14*x))
    elif x <= 4:
        return(t*math.tan(x))
    else:
        return(t*math.tan(6))


# In[111]:


simulated_annealing(f, 10000, 50, 1, -3, 3)


# In[121]:


#Przykład 4 własny

simulated_annealing(lambda x: -(x**2) + abs(x), 1000, 60, 1, -1, 1)


# In[124]:


#Testy dla niepoprawnych danych

simulated_annealing(f, 1000.5, 50, 1, -5, 5)


# In[126]:


simulated_annealing(f, -1000, 50, 1, -5, 5)


# In[130]:


simulated_annealing(f, 1000, 1, 50, -5, 5)


# In[131]:


simulated_annealing(f, 1000.5, 50, 1, 5, -5)


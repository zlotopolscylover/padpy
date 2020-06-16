#!/usr/bin/env python
# coding: utf-8

# In[2]:


#import numpy as np

#Zadanie 2

def from_adjacency_matrix(M):
    """
    Funkcja, która na podstawie macierzy sasiedztwa M (na wejściu) wyznaczy i zwróci 
    liste krotek postaci: (i, j, w_i,j), gdzie i, j oznaczaja wierzchołki grafu, zas w_i,j wage
    łaczacej ich krawedzi.
    """
    lista = [] #pusta lista
    for i in range(1, len(M)):
        for j in range(i): #tylko dla i <j
            lista.append((j, i, np.array(M)[i, j])) #dołączam do pustej listy krotki 3 elementowe (indeks j, indeks i, wartość w itym wierszu jtej kolumnie)
    return lista

def to_adjacency_matrix(x):
    """
    Funkcja, która na podstawie reprezentacji grafu w postaci listy krotek zwróci
    macierz sasiedztwa, czyli listę list.
    """
    n = max([sublist[1] for sublist in x]) + 1 #chcę wymiaru macierzy, a więc biorę maksymalną wartosć spośród drugiej pozycji 
                                                #(w pythonie pozycja 1) krotek w liście i dodaję jedynkę, bo numeracja jest od 0
    Matrix = np.zeros((n,n)) #tworzę macierz zer nxn
    for el in x:
        Matrix[el[0], el[1]] = el[2] #uzupełniam macierz, która jest symetryczna, a na diagonali pozostawiam zera, tak jak w naszym grafie
        Matrix[el[1], el[0]] = el[2]
    return Matrix 

#pip install disjoint-set
from disjoint_set import DisjointSet #https://pypi.org/project/disjoint-set/

def Kruskal(M):
    """
    Funkcja, która przy uzyciu algorytmu Kruskala wyznaczy i zwróci minimalne drzewo rozpinajace.
    Funkcja przyjmuje na wejściu graf pełny, ważony w postaci macierzy (listy podlist, które 
    są tej samej długości, a ich el. są liczbami).
    W funkcji użyto funckji pomocniczej from_adjacency_matrix() w celu przedstawienia macierz(listy podlist) 
    w formie listy krotek dla i<j.
    Na wyjściu funkcja zwraca minimalne drzewo rozpinajace w postaci listy podlist 
    (za pomocą f. pomocniczej to_adjacency_matrix()).
    """
    assert (type(M) == list), "Macierz musi byćpodana w formie listy list"
    assert all((type(el) == list) for el in M) , "Elementy listy muszą być listami"
    if not all(len(l) == len(next(iter(M))) for l in iter(M)):
        raise ValueError('Podlisty w liście M muszą być tej samej długosci')   
    assert all((type(el) == int or type(el) == float) for sublist in M for el in sublist), "Elementy podlist listy muszą być liczbami"
    n = len(M) #wymiar macierzy M, a dokładnie ilość list w liście
    T = [] #deklaruję pustą listę 
    x = from_adjacency_matrix(M) #pomocnicza funkcja
    y = sorted(x, key=lambda el: el[2])
    #y = x.sort( key=lambda el: el[2])
    ds = DisjointSet() #https://pypi.org/project/disjoint-set/
    for i in y: #dla krotek z listy
        if ds.find(i[0]) != ds.find(i[1]): #jeżeli w krotce wartość pozycji 0 jest rózna od wart. pozycji 1
            b=T.append((i)) #to rozszerz pustą listę o tą krotkę
            ds.union(i[0], i[1]) #połącz dwa wierzchołki
    return to_adjacency_matrix(T)          


# In[3]:


#Przykład 1

M = [[
0, 10.95, 13.98, 18.28, 10.49 ],
[ 10.95, 0, 9.3, 9.68, 4.23 ],
[ 13.98, 9.3, 0, 6.15, 5.31 ],
[ 18.28, 9.68, 6.15, 0, 7.83 ],
[ 10.49, 4.23, 5.31, 7.83, 0 ]
]


# In[4]:


print(from_adjacency_matrix(M))
[
(1, 4, 4.23), (2, 4, 5.31), (2, 3, 6.15), (3, 4, 7.83), (1, 2, 9.3),
(1, 3, 9.68), (0, 4, 10.49), (0, 1, 10.95), (0, 2, 13.98), (0, 3, 18.28)
]


# In[6]:


to_adjacency_matrix(from_adjacency_matrix(M))
[[0, 10.95, 13.98, 18.28, 10.49],
[10.95, 0, 9.3, 9.68, 4.23],
[13.98, 9.3, 0, 6.15, 5.31],
[18.28, 9.68, 6.15, 0, 7.83],
[10.49, 4.23, 5.31, 7.83, 0]]


# In[9]:


mst = Kruskal(M)
print(mst)


# In[10]:


#Przykład 2
M = [
[ 0, 1.3, 4.12, 0.96, 1.87, 3.23, 0.98, 2.3, 2.28, 3.51 ],
[ 1.3, 0, 2.86, 1.57, 2.63, 4.19, 1.92, 1.6, 2.67, 2.55 ],
[ 4.12, 2.86, 0, 4.02, 4.84, 6.41, 4.75, 2.49, 4.45, 1.72 ],
[ 0.96, 1.57, 4.02, 0, 1.07, 2.62, 1.91, 1.76, 1.32, 3.03 ],
[ 1.87, 2.63, 4.84, 1.07, 0, 1.6, 2.66, 2.38, 0.76, 3.57 ],
[ 3.23, 4.19, 6.41, 2.62, 1.6, 0, 3.74, 3.93, 2.02, 5.03 ],
[ 0.98, 1.92, 4.75, 1.91, 2.66, 3.74, 0, 3.23, 3.18, 4.38 ],
[ 2.3, 1.6, 2.49, 1.76, 2.38, 3.93, 3.23, 0, 1.95, 1.27 ],
[ 2.28, 2.67, 4.45, 1.32, 0.76, 2.02, 3.18, 1.95, 0, 3.02 ],
[ 3.51, 2.55, 1.72, 3.03, 3.57, 5.03, 4.38, 1.27, 3.02, 0 ]
]
mst = Kruskal(M)
print(mst)


# In[11]:


#Przykład 3 własny
M = [[
0, 1, 5, 7, 8 ],
[ 1, 0, 2, 4, 12 ],
[ 5, 2, 0, 3, 17 ],
[ 7, 4, 3, 0, 6 ],
[ 8, 12, 17, 6, 0 ]
]
mst=Kruskal(M)
print(mst)


# In[16]:


#Przykład 4 własny
M = [[
0, 10, 13, 18, 10 ],
[ 10, 0, 9, 9, 4 ],
[ 13, 9, 0, 6, 5],
[ 18, 9, 6, 0, 7 ],
[ 10, 4, 5, 7, 0 ]
]
mst=Kruskal(M)
print(mst)


# In[18]:


# test dla niepoprawnych danych -  metoda Kruskal(M)
M = [
0, 10, 13, 18, 10 ],
[ 10, 0, 9, 9, 4 ],
[ 13, 9, 0, 6, 5],
[ 18, 9, 6, 0, 7 ],
[ 10, 4, 5, 7, 0 ]


Kruskal(M)


# In[24]:


M =[5,
[ 10, 0, 9, 9, 4 ],
[ 13, 9, 0, 6, 5],
[ 18, 9, 6, 0, 7 ],
[ 10, 4, 5, 7, 0 ]]

Kruskal(M)


# In[25]:


M = [[
0, 10, 13, 18 ],
[ 10, 0, 9, 9, 4 ],
[ 13, 9, 0, 6, 5],
[ 18, 9, 6, 0, 7 ],
[ 10, 4, 5, 7, 0 ]
]
Kruskal(M)


# In[29]:


M = [[0, 10, 13, 18, "a" ],
[ 10, 0, 9, 9, 4 ],
[ 13, 9, 0, 6, 5],
[ 18, 9, 6, 0, 7 ],
[ 10, 4, 5, 7, 0 ]
]

Kruskal(M)


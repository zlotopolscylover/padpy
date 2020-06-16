#!/usr/bin/env python
# coding: utf-8

# In[133]:


#import numpy as np

#Zadanie 3

class Multizbior:
    
    def __init__(self, x):
        """
        Metoda specjalna - konstruktor,automatycznie wywoływana podczas tworzenia instancji danej 
        klasy, który przyjmuje argumenty self i x, gdzie x jest listą o elementach całkowitych 
        nieujemnych okreslajacych liczbe wystapien elementów w multizbiorze.
        Inicjuje pole zbior, w którym znajdują się pary: element:liczba_wystąpień.
        """
        assert (type(x) == list), "Argument x musi być listą"
        assert all(el >= 0 for el in x), "Lista musi być wypełniona elementami nieujemnymi"
        self.x = x 
        self.zbior = {key: i for key, i in enumerate(x) if i!=0} #pole, będące słownikiem 
                                                                #tj. {pozycja wektora wejściowego(jaka liczba):
                                                                #     wartość wektora wejściowego na danej pozycji(ile razy)}
        
    def __str__(self):
        """
        Metoda, która umożliwia estetyczne wypisanie multizbioru.
        Przyjmuje argument self.
        """
        x = np.zeros(max(self.zbior.keys()) + 1, dtype = int) #tworzę wektor zer o długości = max wartości klucza +1 
                                                            #ze względu na to, ze w Pythonie od 0,1,...
        for i in range(len(x)): #dla elementów w zakresie od 0 długości x poniejszonej 
                                #oczywiście o 1 (tak działa range), czyli do 4
            try: 
                x[i] = self.zbior[i]
            except:
                pass
        return '{' + ' '.join(map(str, np.repeat(range(0, len(x)), np.array(x)))) + '}' #zwracam multizbiór w postaci napisu z nawiasami {}
    
    def usun(self,liczba):
        """
        Metoda pozwalająca na usunięcie elementu z multizbioru.
        Na wejściu metoda otrzymuje liczbę całkowitą nieujemną.
        Na wyjściu dostajemy nasz multizbiór pomniejszony o 1 element zgodnie z 
        liczbą, a jeśli danej liczby nie ma w multizbiorze, dostaniemy komunikat.
        """
        #assert (type(liczba) == int and liczba >=0), "Liczba musi być liczbą całkowitą nieujemną"
        try:
            self.zbior[liczba] -= 1 #to pomniejsz ilość tego elementu o 1
            if self.zbior[liczba] == 0: self.zbior.pop(liczba, None) # i jezeli w związku z odjeciem elementu teraz ten nasz 
                                                                    #element występuj 0 razy, to wyrzucamy go ze słownika
        except: print("Tej liczby nie ma w naszym multizbiorze")
        
    def dodaj(self,liczba):
        """
        Metoda pozwalająca na dodanie elementu do multizbioru.
        Na wejściu metoda otrzymuje liczbę całkowitą nieujemną.
        Na wyjściu dostajemy nasz multizbiór powiększony o 1 element zgodny z liczbą.
        """
        assert (type(liczba) == int and liczba >=0), "Liczba musi być liczbą całkowitą nieujemną"
        if liczba in self.zbior.keys(): #jeżeli liczba jest w kluczach słownika, czyli jest wartością (którą mamy ileś tam razy)
            self.zbior[liczba] += 1 #to powiększ ilość tego elementu o 1
        else:
            self.zbior.update({liczba: 1}) #a jeżeli nie to dodaj so słownika liczbę: 1 raz 
    
    def intersect(self, drugi_multizbior):
        """
        Metoda, która wyznacza i zwraca przeciecie dwóch multizbiorów.
        Na wejściu dostaje multizbiór.
        """
        przeciecie= {}
        for i in self.zbior.keys():
            try:
                przeciecie[i] = min(self.zbior[i], drugi_multizbior.zbior[i]) #minimum klucza z obu multizbiorów przy danej wartosci
            except:
                pass
        x = np.zeros(max(przeciecie.keys()) + 1, dtype = int) #tworzę wektor zer o długości = max wartości klucza +1 
                                                            #ze względu na to, ze w Pythonie od 0,1,...
        for i in range(len(x)): #dla elementów w zakresie od 0 długości x poniejszonej 
                                #oczywiście o 1 (tak działa range), czyli do 4
            try: 
                x[i] = przeciecie[i]
            except:
                pass
        return '{' + ' '.join(map(str, np.repeat(range(0, len(x)), np.array(x)))) + '}'


# In[123]:


#Przykład 1
A = Multizbior([0, 1, 2, 0, 3])
print(A)


# In[124]:


print(A.zbior)


# In[125]:


A.usun(1)
print(A)


# In[126]:


print(A.zbior)


# In[127]:


A.dodaj(0)
print(A)


# In[128]:


print(A.zbior)


# In[129]:


B = Multizbior([0, 2, 1, 7, 2, 1, 0, 5])
print(B)


# In[130]:


print(A.intersect(B))


# In[79]:


#Przykład 2
A = Multizbior([0, 3, 0, 3])
print(A)


# In[80]:


print(A.zbior)


# In[81]:


try:
    A.usun(2)
except Exception as e:
    print(e)


# In[82]:


print(A)


# In[83]:


print(A.zbior)


# In[84]:


A.dodaj(3)
print(A)


# In[85]:


B = Multizbior([1, 2, 2, 4])
print(B)


# In[86]:


print(B.intersect(A))


# In[95]:


#Przykład 3 własny
A = Multizbior([0, 0, 4, 1, 2])
print(A)


# In[96]:


print(A.zbior)


# In[97]:


A.usun(1)
print(A)


# In[98]:


print(A.zbior)


# In[99]:


A.dodaj(5)
print(A)


# In[100]:


print(A.zbior)


# In[101]:


B = Multizbior([0, 1,2,3,4,5])
print(B)


# In[102]:


print(A.intersect(B))


# In[103]:


#Przykład 4 własny
A = Multizbior([0, 2,0])
print(A)


# In[104]:


print(A.zbior)


# In[105]:


try:
    A.usun(3)
except Exception as e:
    print(e)


# In[106]:


print(A)


# In[107]:


print(A.zbior)


# In[108]:


A.dodaj(10)
print(A)


# In[109]:


B = Multizbior([3,3,3])
print(B)


# In[110]:


print(B.intersect(A))


# In[112]:


#testy

A=Multizbior(True)


# In[113]:


#testy

A=Multizbior([1,-1,-7])


# In[115]:


A=Multizbior([1,2,3])
A.dodaj(-10)


# In[116]:


try:
    A.usun(25)
except Exception as e:
    print(e)


# In[ ]:





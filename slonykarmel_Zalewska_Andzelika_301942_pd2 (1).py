#!/usr/bin/env python
# coding: utf-8

# In[187]:


import pandas as pd
import numpy as np


# In[199]:


Users = pd.read_csv('C:/Users/Ja/Desktop/Python/PD2/Users.csv',
                      error_bad_lines=False,
                      comment="#")
Badges = pd.read_csv('C:/Users/Ja/Desktop/Python/PD2/Badges.csv',
                      error_bad_lines=False,
                      comment="#")
Comments = pd.read_csv('C:/Users/Ja/Desktop/Python/PD2/Comments.csv',
                      error_bad_lines=False,
                      comment="#")
PostLinks = pd.read_csv('C:/Users/Ja/Desktop/Python/PD2/PostLinks.csv,
                      error_bad_lines=False,
                      comment="#")
Posts = pd.read_csv('C:/Users/Ja/Desktop/Python/PD2/Posts.csv',
                      error_bad_lines=False,
                      comment="#")
Tags = pd.read_csv('C:/Users/Ja/Desktop/Python/PD2/Tags.csv',
                      error_bad_lines=False,
                      comment="#")
Votes = pd.read_csv('C:/Users/Ja/Desktop/Python/PD2/Votes.csv',
                      error_bad_lines=False,
                      comment="#")


# In[189]:


import tempfile
import os
baza = os.path.join(tempfile.mkdtemp(), "baza.db")

if os.path.isfile(baza):
    os.remove(baza)

import sqlite3
conn = sqlite3.connect(baza)


# In[191]:


Badges.to_sql("Badges", conn, index=False)
Comments.to_sql("Comments", conn,index=False)
PostLinks.to_sql("PostLinks", conn,index=False)
Posts.to_sql("Posts", conn,index=False)
Tags.to_sql("Tags", conn,index=False)
Users.to_sql("Users", conn,index=False)
Votes.to_sql("Votes", conn,index=False)


# # Zadanie 1

# Interpretacja: Z tablicy z głosami zliczamy, ile głosów typu 2 ("UpMod") otrzymał każdy post.

# In[192]:


df_sql_1 = pd.read_sql_query("""
SELECT PostId, COUNT(*) AS UpVotes 
FROM Votes 
WHERE VoteTypeId=2 
GROUP BY PostId""", conn)


# In[202]:


df_pd_1 = Votes.loc[(Votes.VoteTypeId==2)]             .groupby("PostId")             .size()             .reset_index(name = "UpVotes")
df_pd_1


# In[212]:


df_sql_1.__class__


# In[211]:


df_pd_1.__class__


# Wyniki są klasy DataFrame.

# In[194]:


df_pd_1.equals(df_sql_1)


# Tabele przedstawiające dwie metody implementacji są sobie równe.

# # Zadanie 2

# Interpretacja: W tym zapytaniu otrzymujemy informację o tytule postu z pytaniem (PostTypeId=1), jego wyniku (Score), liczbie odsłon (ViewCount) oraz o tym, ile osób oznaczyło go jako "ulubiony" (FavoriteCount), ale tylko jeśli post takich odznaczeń miał conajmniej 25, a odsłon conajmniej 10000.

# In[200]:


df_sql_2 = pd.read_sql_query("""
SELECT Title, Score, ViewCount, FavoriteCount 
FROM Posts 
WHERE PostTypeId=1 AND FavoriteCount >= 25 AND ViewCount>=10000""", conn)


# In[208]:


df_pd_2 = Posts.loc[(Posts.PostTypeId==1) & (Posts.FavoriteCount>=25) & (Posts.ViewCount>=10000), ["Title","Score","ViewCount","FavoriteCount"]].reset_index(drop=True)
df_pd_2


# In[210]:


df_pd_2.__class__


# Wyniki są klasy DataFrame.

# In[16]:


df_pd_2.equals(df_sql_2)


# Tabele przedstawiające dwie metody implementacji są sobie równe.

# # Zadanie 3

# Interpretacja: Tabelę z tagami łączymy z tabelą postów i użytkowników. Wybieramy z nich informacje dotyczące nazwy tagu, 
# ilości jego wystąpienia, użytkownika - twórcy danego tagu, pochodzeniu użytkownika oraz jego nicku. Wybieramy tylko posty tych użytkowników, których OwnerUserId jest różne od -1, co prawdopodobnie dotyczy użytkowników nieznanych. Dodatkowo sortujemy po ilości wystąpienia tagu (Count), co daje nam ranking tagów z dodatkową informacją o użytkowniku, który go stworzył, pochodzeniu użytkownika i jego nicku. 

# In[209]:


df_sql_3 = pd.read_sql_query("""SELECT Tags.TagName, Tags.Count, Posts.OwnerUserId,Users.Location, Users.DisplayName 
FROM Tags
JOIN Posts ON Posts.Id=Tags.WikiPostId
JOIN Users ON Users.AccountId=Posts.OwnerUserId
WHERE OwnerUserId != -1
ORDER BY Count DESC""", conn)


# In[214]:


tmp = pd.merge(pd.merge(Tags, Posts, left_on = 'WikiPostId', right_on = 'Id', how='inner'),Users, left_on = 'OwnerUserId', right_on='AccountId', how='inner')
df_pd_3 = tmp.loc[(tmp.OwnerUserId != -1) ,["TagName","Count","OwnerUserId","Location","DisplayName"]]             .sort_values("Count", ascending=False)             .reset_index(drop=True)
df_pd_3


# In[216]:


df_pd_3.__class__


# Wyniki są klasy DataFrame.

# In[215]:


df_pd_3.equals(df_sql_3)


# Tabele przedstawiające dwie metody implementacji są sobie równe.

# # Zadanie 4

# Interpretacja: Dla postów z pytaniami otrzymujemy informację na temat tytułu postu oraz liczbie innych postów z nim połączonych. Sortujemy malejąco po liczbie postów połaczonych z danym postem, dzięki czemu otrzymujemy informację na temat popularności postu.

# In[217]:


df_sql_4 = pd.read_sql_query("""SELECT Posts.Title, RelatedTab.NumLinks 
FROM
(SELECT RelatedPostId AS PostId, COUNT(*) AS NumLinks
FROM PostLinks GROUP BY RelatedPostId) AS RelatedTab
JOIN Posts ON RelatedTab.PostId=Posts.Id
WHERE Posts.PostTypeId=1
ORDER BY NumLinks DESC""", conn)


# In[221]:


df_pd_4 = pd.merge(PostLinks.groupby("RelatedPostId").size().reset_index(name="NumLinks").rename(columns={"RelatedPostId": "PostId"}),Posts.loc[(Posts.PostTypeId==1)], left_on='PostId', right_on ='Id', how='inner')[["Title", "NumLinks"]].sort_values("NumLinks", ascending=False).reset_index(drop=True)
df_pd_4


# In[218]:


df_pd_4.__class__


# Wyniki są klasy DataFrame.

# In[219]:


df_pd_4.sort_values("Title").reset_index(drop=True).equals(df_sql_4.sort_values("Title").reset_index(drop=True))


# Tabele przedstawiające dwie metody implementacji są sobie równe z dokładnością do permutacji wierszy wynikowych ramek danych. Możliwość takiego porównania uzyskujemy dzięki posortowaniu tabel po unikalnej kolumnie, czyli w tym przypadku po tytule.

# # Zadanie 5

# Interpretacja: Tutaj zmieniamy informację otrzymaną w pierwszym zapytaniu, dodając informację o tytule postu oraz biorąc jedynie posty z pytaniami. Dodatkowo sortujemy malejąco po kolumnie UpVotes, dzięki czemu otrzymujemy ranking tytułów pytań pod kątem "kliknięć w górę".

# In[220]:


df_sql_5 = pd.read_sql_query("""SELECT UpVotesTab.*, Posts.Title FROM
(SELECT PostId, COUNT(*) AS UpVotes FROM Votes WHERE VoteTypeId=2 GROUP BY PostId) AS UpVotesTab
JOIN Posts ON UpVotesTab.PostId=Posts.Id
WHERE Posts.PostTypeId=1
ORDER BY UpVotesTab.UpVotes DESC""", conn)


# In[166]:


UpVotesTab = Votes.loc[(Votes.VoteTypeId == 2)].groupby("PostId").size().reset_index(name="UpVotes")
df_pd_5 = pd.merge(UpVotesTab,Posts.loc[(Posts.PostTypeId==1)], left_on='PostId',right_on='Id')[["PostId","UpVotes","Title"]].sort_values("UpVotes", ascending=False).reset_index(drop=True)
df_pd_5


# In[222]:


df_pd_5.__class__


# Wyniki są klasy DataFrame.

# In[223]:


df_pd_5.sort_values("Title").reset_index(drop=True).equals(df_sql_5.sort_values("Title").reset_index(drop=True))


# Tabele przedstawiające dwie metody implementacji są sobie równe z dokładnością do permutacji wierszy wynikowych ramek danych. Możliwość takiego porównania uzyskujemy dzięki posortowaniu tabel po unikalnej kolumnie, czyli w tym przypadku po tytule.

# # Zadanie 6

# Komentarz:
# Złączenie typu LEFT JOIN pozwala nam na uwzględnienie w wyniku danych, które nie posiadają swoich odpowiedników w złączanych tabelach. Oznacza to, że jeśli w pierwszej tabeli pojawiają się wiersze, które nie posiadają odpowiedników w drugiej tabeli to zostaną wzięte pod uwagę podczas złączenia ale puste kolumny zostaną wypełnione wartościami NULL (lub NaN).
# 
# Interpretacja: Do tabeli z zadania pierwszego dołączamy tabelę, która zlicza DownVotes, czyli zlicza dla danego postu ilość "kliknięć w dół" (VoteTypeId=3).
# 
# W kolumnie DownVotes wartości NaN pojawiły się prawdopodobnie ze względu na to, że dany post nie miał żadnych "kliknięć w dół", wobec tego uzupełniamy kolumnę DownVotes wartością 0. 
# 
# Uzyskujemy zatem informację o tym, ile dany post miał "kliknięć w górę", a ile "kliknięć w dół".

# In[224]:


df_sql_6 = pd.read_sql_query("""SELECT UpVotesTab.PostId, UpVotesTab.UpVotes, IFNULL(DownVotesTab.DownVotes, 0) AS DownVotes
FROM
(SELECT PostId, COUNT(*) AS UpVotes FROM Votes
WHERE VoteTypeId=2 GROUP BY PostId) AS UpVotesTab
LEFT JOIN
(SELECT PostId, COUNT(*) AS DownVotes FROM Votes
WHERE VoteTypeId=3 GROUP BY PostId) AS DownVotesTab
ON UpVotesTab.PostId=DownVotesTab.PostId""", conn)


# In[225]:


UpVotesTab = Votes.loc[(Votes.VoteTypeId == 2)].groupby("PostId").size().reset_index(name = "UpVotes")
DownVotesTab = Votes.loc[(Votes.VoteTypeId == 3)].groupby("PostId").size().reset_index(name = "DownVotes")
df_pd_6 = pd.merge(UpVotesTab, DownVotesTab, on = "PostId", how = "left")
df_pd_6["DownVotes"] = df_pd_6["DownVotes"].fillna(value =0).astype('int64')
df_pd_6


# In[226]:


df_pd_6.__class__


# Wyniki są klasy DataFrame.

# In[113]:


df_sql_6.equals(df_pd_6)


# Tabele przedstawiające dwie metody implementacji są sobie równe.

# # Zadanie 7

# Komentarz: Złączenie typu RIGHT JOIN działa analogicznie do LEFT JOIN, ale w tabeli wynikowej uwzględnia wiersze z drugiej tabeli, które nie posiadają odpowiedników w pierwszej.
# 
# Interpretacja: Łączymy poziomo (UNION) tabelę z zadania 6. z podobną tabelą, z tym że ta druga różni się w zapytaniu tylko tym, że tak naprawdę wykonujemy teraz RIGHT JOIN w miejscu LEFT JOIN.
# 
# Wobec tego nasz wynik z zadania 6. zostaje poszerzony o posty, które nie miały "kliknięć w górę", ale miały "klknięcia w dół". 
# Finalnie wynik przedstawiamy w postaci dwóch kolumn: Id posta oraz Votes, która jest różnicą "kliknięć w górę" i "kliknięć w dół", wobec czego otrzymujemy informację, czy post jest bardziej lubiany lub nielubiany.

# In[227]:


df_sql_7 = pd.read_sql_query("""SELECT PostId, UpVotes-DownVotes AS Votes FROM (
SELECT UpVotesTab.PostId, UpVotesTab.UpVotes, IFNULL(DownVotesTab.DownVotes, 0) AS DownVotes
FROM
(SELECT PostId, COUNT(*) AS UpVotes FROM Votes
WHERE VoteTypeId=2 GROUP BY PostId) AS UpVotesTab
LEFT JOIN
(SELECT PostId, COUNT(*) AS DownVotes
FROM Votes WHERE VoteTypeId=3 GROUP BY PostId) AS DownVotesTab
ON UpVotesTab.PostId=DownVotesTab.PostId
UNION
SELECT DownVotesTab.PostId, IFNULL(UpVotesTab.UpVotes, 0) AS UpVotes, DownVotesTab.DownVotes
FROM
(SELECT PostId, COUNT(*) AS DownVotes FROM Votes
WHERE VoteTypeId=3 GROUP BY PostId) AS DownVotesTab
LEFT JOIN
(SELECT PostId, COUNT(*) AS UpVotes FROM Votes
WHERE VoteTypeId=2 GROUP BY PostId) AS UpVotesTab
ON DownVotesTab.PostId=UpVotesTab.PostId
)""", conn)


# In[228]:


df_pd_6_1 = pd.merge(UpVotesTab, DownVotesTab, on = "PostId", how = "right")
df_pd_6_1["UpVotes"] = df_pd_6_1["UpVotes"].fillna(0).astype(int)
df = pd.concat([df_pd_6, df_pd_6_1], ignore_index = True)
df['Votes'] = df['UpVotes'] - df['DownVotes']
df_pd_7 = df[["PostId", "Votes"]].drop_duplicates().sort_values("PostId").reset_index(drop = True)
df_pd_7


# In[229]:


df_pd_7.__class__


# Wyniki są klasy DataFrame.

# In[230]:


df_pd_7.equals(df_sql_7)


# Tabele przedstawiające dwie metody implementacji są sobie równe.

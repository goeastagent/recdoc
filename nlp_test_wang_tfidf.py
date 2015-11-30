from __future__ import division, unicode_literals
import math
from textblob import TextBlob as tb
import nltk
#from nltk.stem.lancaster import LancasterStemmer   # stemer st = LancasterStemmer() st.stem('saying')
#from nltk.stem.porter import *  # poster stemmer
#from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

from collections import Counter
from nltk import cluster

import os
from os import listdir
from os.path import isfile, join

import time


def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)

def idf(word, bloblist):
    return math.log(len(bloblist) / (n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

def buildVector(iterable1, iterable2):
    counter1= dict((k[0],k[1]) for k in iterable1)
    counter2= dict((k[0],k[1]) for k in iterable2)
    all_items = list(set(counter1.keys()).union( set(counter2.keys()) ))
    
    vector1=[]
    vector2=[]
    for k in all_items:
        if k in counter1:
            vector1.append(counter1[k])
        else:
            vector1.append(0)
        if k in counter2:
            vector2.append(counter2[k])
        else:
            vector2.append(0)
        
    #print vector1
    #print vector2
    return vector1, vector2

def cosine_sim(v1,v2):
    return (1-cluster.util.cosine_distance(v1,v2))

cachedStopWords = stopwords.words("english")

def stemming(doc):

    d = toker.tokenize(doc)
    d = [k for k in d if k not in cachedStopWords]
    for i in range(0,len(d)):
        d[i]=lemma.lemmatize(d[i])
    return tb(" ".join(d))    



def filestring(f):
    title = u""
    abstract = u""
    body = u""
    while(1):
        line=f.readline().decode('utf-8')
        if line=="":
            break
        #print line
        #title=title+" "+line
        title = u' '.join([title, line])

    while(1):
        line=f.readline().decode('utf-8')
        if line=="":
            break
        #print line
        #abstract=abstract+" "+line
        abstract = u' '.join([abstract, line])

    while(1):
        line=f.readline().decode('utf-8')
        if not line: break
        #print line
        #body=body+" "+line
        body = u' '.join([body, line])

    return title, abstract, body


threshold = 0.00


####################################################################################

lemma = nltk.wordnet.WordNetLemmatizer()    # stemming

toker = RegexpTokenizer(r'((?<=[^\w\s])\w(?=[^\w\s])|(\W))+', gaps=True)   #punctuation




files0_dir='./0/'
files1_dir='./1/'
files2_dir='./2/'
files0 = [f for f in os.listdir(files0_dir)]
files1 = [f for f in os.listdir(files1_dir)]
files2 = [f for f in os.listdir(files2_dir)]

print "start !!!!"
fileList = []
#print files0
for j,i in enumerate(files0):
    #if j%100==0:
    #    print "file0 : " + str(j)
    if i[-3:]=="txt":
        fileList.append(files0_dir+i)

#print fileList

for j,i in enumerate(files1):
    #if j%100==0:
    #    print "file1 : " + str(j)
    if i[-3:]=="txt":
        fileList.append(files1_dir+i)

for j,i in enumerate(files2):
    #if j%100==0:
    #    print "file2 : " + str(j)
    if i[-3:]=="txt":
        fileList.append(files2_dir+i)


######################################################



#############################################################################################
document_list=[]

for j,i in enumerate(fileList):
    if j%100==0:
        print "read stemmed : " + str(j)
    #f = open("testtest"+str(i)+".txt",'r')
    f = open("./s/"+i[4:-4]+".txt",'r')
    #line = fcontrol.readline()
    #if not line: break
    line=f.readline().decode('utf-8')
    document_list.append(tb(line))
    f.close()



#bloblist = [document1, document2, document3]

#listlist = tfidf_list(document_list)

wordList={}



totallength = len(document_list)

#blob.words.count(word) / len(blob.words)
########
bloblistidf = [set(b.words) for b in document_list]
#print bloblistidf

for k, blob in enumerate(bloblistidf):
    if k%100==0:
        print "make dict : " + str(k)
    for word in blob:
        if not word in wordList:
            wordList[word]=math.log(totallength / n_containing(word, bloblistidf))
            #wordList_name.append(word)
            #wordList_num.append(math.log(totallength / n_containing(word, bloblistidf)))    

#print wordList
del(bloblistidf)


#listlist = []
for i, blob in enumerate(document_list):
    #if i%2==0:
    #    print "iter : "+str(i)
    #    time.sleep(0.1)
    
    bloblength = len(blob.words)
    

    print("Top words in document {}".format(i + 1))
    #scores = {word: ((blob.words.count(word) / bloblength)   * wordList_num[wordList_name.index(word)]  ) for word in blob.words}
    scores = {word: ((blob.words.count(word) / bloblength)   * wordList[word]  ) for word in blob.words if word[0] != '\ufeff'}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    #if i==2:
    #    print sorted_words 


    f2 = open("./tfidf/"+fileList[i][4:-4]+".txt","w")
    for k in sorted_words:
        #print str(k[1])
        f2.write(k[0].encode('utf-8'))
        f2.write(" : ")
        f2.write(str(k[1]))
        f2.write("\n")
    f2.close()

        #listlist.append(sorted_words)

        #for word, score in sorted_words[:5]:
        #    print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
    #return listlist



del(document_list)

"""
for j,i in enumerate(fileList):
    f2 = open("./tfidf/"+i[4:-4]+".txt","w")
    for k in listlist[j]:
        #print str(k[1])
        f2.write(k[0].encode('utf-8'))
        f2.write(" : ")
        f2.write(str(k[1]))
        f2.write("\n")
    f2.close()
"""


# cosine sim

#v1,v2= buildVector(listlist[2], listlist[0])
#print cosine_sim(v1,v2)


#network

"""
for i, blob1 in enumerate(listlist):
    for j, blob2 in enumerate(listlist[i+1:]):
        blob1_v,blob2_v= buildVector(blob1, blob2)
        temp_cos = cosine_sim(blob1_v,blob2_v)        
        #print temp_cos
        if temp_cos >= threshold:
            print i , j+i+1 , temp_cos

"""



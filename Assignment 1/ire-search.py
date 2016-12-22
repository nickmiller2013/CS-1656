# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 12:53:40 2016

@author: Nick
Date: Sun Sept 25, 2016
Class: CS 1656
"""

import math
import os
import json
import nltk

direct = os.getcwd() + '/input'


f = open('inverted-index.json','rb')
words = {}
words = json.load(f)
f.close()
documents = []

stemmedWords = []
weight = {}

keywords = open("keywords.txt").readlines()


#This loop goes through, refixes the keywords and gathers the weights from the algorithm
for file_in in os.listdir(direct):
     if not file_in.startswith('.'):

#        print(file_in)
        for i in keywords:
#            print(i)
            
            phrase = i.split(' ')
            for j in phrase :
                
                a = j.lower()
                
                
                punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
                    
                    
                no_punct = ""
                for char in a:
                   if char not in punctuations:
                       no_punct = no_punct + char
                
                # display the unpunctuated string
                
                no_dig = ''.join([i for i in no_punct if not i.isdigit()])
                
                mysentencetokens = nltk.word_tokenize(no_dig)
                #Stemming
                porter = nltk.PorterStemmer()
                for token in mysentencetokens:
                        mysentencetokens = porter.stem(token)

                if mysentencetokens not in stemmedWords:
                    
                    if mysentencetokens in words:
                        if file_in in words[mysentencetokens]:
                            n = words[mysentencetokens]['count']
                            N = words[mysentencetokens]['total']
                            freq = words[mysentencetokens][file_in]
#                            print n
#                            print N
#                            print freq

                            weightMath = ((1+math.log(float(freq),2))*math.log(float(N)/n,2))
#                            print 'weight'
#                            print weightMath
                            
                            if j not in weight:
                                weight[j] = {file_in:weightMath}
                            else:
                                weight[j][file_in] = weightMath
                    
#print weight
weightT = {}

#This loop is used to sum the weights of different documents if the keywords are more than 1
for i in keywords:
    #print(i)
    
    phrase = i.split(' ')
    for j in phrase :
        for file_in in os.listdir(direct):
            if not file_in.startswith('.'):

                #print(file_in)
                if j in weight:
                    if file_in in weight[j]:
                        if i not in weightT:
                            weightT[i] = {file_in:weight[j][file_in]}
                        else:
                            if file_in not in weightT[i]:
                                weightT[i][file_in] = weight[j][file_in]
                            else:
                                weightT[i][file_in] = weightT[i][file_in] + weight[j][file_in]
                    
#print weightT


# This loop is used to print the output of the program 
for i in keywords:
    
    print('------------------------------------------------------------')
    print "\nKeywords =",i
    prev = -1
    count = 0
    for k in (weightT[i]):
        remove = (max(weightT[i], key=weightT[i].get))
        
        #print weightT[i][remove]
        #print prev
        if prev != weightT[i][remove]:
            count = count + 1
            prev = weightT[i][remove]
        
        #print count
        
        
        print "\n[%d]  File=%s  score=%.6f" % (count,remove,weightT[i][remove])


        weightT[i][remove] = 0
        
        phrase = i.split(' ')
        for j in phrase:
            stripped = j.strip("\n")
            if remove in weight[j]:
                print "weight(%s): %.6f" % (stripped, weight[j][remove])
            else:
                print "weight(%s): %.6f" % (stripped, 0.0)

                
                
                
                
                    
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 15:09:42 2016

@author: Nick
Date: Sun Sept 25, 2016
Class: CS 1656
"""


import os
import json
import nltk


t = 1
count = 1;
direct = os.getcwd() + '/input'
words = {}
documents = []
for file_in in os.listdir(direct):
     if not file_in.startswith('.'):
        if file_in in documents:
            print('This document has already meen entered');
        else:
            #print(file_in)
            
            #The first couple parts of this code fix the words to get them to basic form 
            documents.append(file_in)
            count= count+1
        
            with open(os.path.join(direct, file_in) ,"r+") as f:
                #print f.tell()
            ################# READING FROM A FILE #################
                #  Option 1: use f.read()
                a = f.read()
            
            a = a.lower()
            
            punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
            
            
            no_punct = ""
            for char in a:
               if char not in punctuations:
                   no_punct = no_punct + char
            
            # display the unpunctuated string
            #print(no_punct)
            
            no_dig = ''.join([i for i in no_punct if not i.isdigit()])
            #print(no_dig)
            
            mysentencetokens = nltk.word_tokenize(no_dig)
            #Stemming
            porter = nltk.PorterStemmer()
            looper = 0
            for token in mysentencetokens:
                    mysentencetokens[looper] = porter.stem(token)
                    looper += 1
            #print "Stemmed -->"
            #print mysentencetokens
            
            looper = 0
            add = 1;
            
            #This loop puts them in a dictionary 
            for token in mysentencetokens:
                    if mysentencetokens[looper] in words:
                        if file_in in words[mysentencetokens[looper]]:
                            words[mysentencetokens[looper]][file_in] = words[mysentencetokens[looper]][file_in]+1
                        else:
                            words[mysentencetokens[looper]][file_in] = 1
                            words[mysentencetokens[looper]]['count'] = words[mysentencetokens[looper]]['count'] +1
                            words[mysentencetokens[looper]]['total'] = len(os.listdir(direct))
    
                        
                        
                    if mysentencetokens[looper] not in words:
                        
                        words[mysentencetokens[looper]] = {file_in: 1, 'count':1, 'total':(len(os.listdir(direct)))}
            
                        
                    looper += 1
        #print(words)

#Outputs them to inverted-index.json
f = open('inverted-index.json','wb')
json.dump(words,f)
f.close()


import pandas as pd
import numpy as np
from os import system
import sys
import itertools
import os.path

#Nick Miller
#CS 1656 Assignment 3
#10/26/16

#These are all used as global variables
#originalLine is the original format -- all the strings doesn't change
originalLine = ''
#Number is the column header over our actual set of computed numbers
number = ''
reRun = ''

#evaluate gets the arguments for the correct functions going to the right place
#takes in the argument as str, our splitDim which is an indexer for my use, df which is current dataframe, and df_split which is dictionary of dataframes
# Returns the updated dataframe, the updated (if needed) df_split, and updated splitDim
def evaluate(args, df, splitDim, df_split):
    
    #passes to laod function
    if args[0] == 'load':
        
        df, df_split = load(args[1], splitDim)
    #passes to format function
    elif args[0] == 'format':
        
        splitDim = format(args[1])
    #passes to rollup function
    elif args[0] == 'rollup':
        df, df_split, splitDim = rollup(args[1], splitDim, df, df_split)
        #reformats the current dataframe
        df = reformat(df)
        
    #passes to drilldown function
    elif args[0] == 'drilldown':
        df, df_split, splitDim = drilldown(args[1], splitDim, df, df_split)
        #reformats the current dataframe
        df = reformat(df)
    #passes to the save function
    elif args[0] == 'save':
        save(df)
    #passes to the slice function
    elif args[0] == 'slice' :
        df = slice(args[1], df, splitDim)
        #Resets the index of the current dataframe then reformats
        df = df.reset_index()
        df = reformat(df)

    return df, splitDim, df_split
        
#reformat formats the dataframe to be in the right order, just in case there is a weird
#moving of columns. --Takes in current dataframe, returns updated dataframe
def reformat(df):
    ref = originalLine
    if len(originalLine) is 2:
        df = df[[ref[0],ref[1]]]
    elif len(originalLine) is 3:
        df = df[[ref[0],ref[1],ref[2]]]
    elif len(originalLine) is 4:
        df = df[[ref[0],ref[1],ref[2],ref[3]]]
    elif len(originalLine) is 5:
        df = df[[ref[0],ref[1],ref[2],ref[3], ref[4]]]
    elif len(originalLine) is 6:
        df = df[[ref[0],ref[1],ref[2],ref[3], ref[4], ref[5]]]
    
    return df
    
#Rollup function -- takes in the argument as str, our splitDim which is an indexer for my use, df which is current dataframe, and df_split which is dictionary of dataframes
# Returns the updated dataframe, the updated (if needed) df_split, and updated splitDim
def rollup(str, splitDim, df, df_split):
    #Checks whether or not the rollup function can be performed
    if str in splitDim:
        global number
        
        
        #Removes the string from splitDim -- splitDim acts as a checking system
        splitDim.remove(str)
        
        
        #This will be the case if just a single row
        if len(splitDim) is 0:
        
            
            #Get the df we are looking for
            #reRun is a global variable used for this specialcase
            df = df_split[reRun]
            
            #Sum the df
            df = df.sum()
            df = df.reset_index()
            
            #Properly align the columns
            df.columns = np.where(df.columns==0, number,df.columns)
            #
        elif len(splitDim) is 1:
            
            #The rest of these elifs are for dataframes greater than being just 0
            #They will get the correct dataframe from the df_split, and then group it by
            #the remaining values in splitDim, then it will properly format the dataframe 
            #to make things easier.
            
            x = splitDim[0]
            
            df = df_split[x]
            
            df = df.groupby([x]).sum()
            df = df.reset_index()
            df.columns = np.where(df.columns==0, number,df.columns)
    
        elif len(splitDim) is 2:
            df = df_split[splitDim[0],splitDim[1]]
            df = df.groupby([splitDim[0],splitDim[1]]).sum()
            df = df.reset_index()
            df.columns = np.where(df.columns==0, number,df.columns)
    
    
    
        elif len(splitDim) is 3:
            df = df_split[splitDim[0],splitDim[1],splitDim[2]]
            df = df.groupby([splitDim[0],splitDim[1], splitDim[2]]).sum()
            df = df.reset_index()
            df.columns = np.where(df.columns==0, number,df.columns)
    
            
    
    
        elif len(splitDim) is 4:
            df = df_split[splitDim[0],splitDim[1],splitDim[2],splitDim[3]]
            df = df.groupby([splitDim[0],splitDim[1], splitDim[2], splitDim[3]]).sum()
            df = df.reset_index()
            df.columns = np.where(df.columns==0, number,df.columns)
    
    
    
        elif len(splitDim) is 5:
            df = df_split[splitDim[0],splitDim[1],splitDim[2],splitDim[3], splitDim[4]]
            df = df.groupby([splitDim[0],splitDim[1], splitDim[2], splitDim[3], splitDim[4]]).sum()
            df = df.reset_index()
            df.columns = np.where(df.columns==0, number,df.columns)    
        
        #This piece of code is used to insert 'all' into the dataframe where it needs to be. 
        global originalLine
        for x in originalLine:
            if x not in df.columns.values:
                df.insert(len(df.columns)-1,x,'all')
        
        #'index' will show up when length of splitDim is 0. This is used to remove it if it exists.         
        if 'index' in df:
            df = df.iloc[[1]]
            del df['index']

    else:
        print 'ERROR: The operation rollup ' + str + ' is not available; dimension not available in current cube '

    return df, df_split, splitDim
            
#Drilldown function -- takes in the argument as str, our splitDim which is an indexer for my use, df which is current dataframe, and df_split which is dictionary of dataframes
# Returns the updated dataframe, the updated (if needed) df_split, and updated splitDim
def drilldown(str, splitDim, df, df_split):

    global originalLine

    global number
    if str not in splitDim:
        splitDim.append(str)
        
        if len(splitDim) is 1:
            #This will be the case if all columns are drilled down. Which means our splitDim just recently
            #got a new string appended to be the only thing in it. 
            
            #Recover our dataframe from the df_split
            df_temp = df_split[str]

            #Reset our dataframe to correct values and columns and remove 'index' and add 
            #all to where it needs to be. 
            df_temp = df_temp.reset_index()
            df_temp.columns = np.where(df_temp.columns==0, number,df_temp.columns)
            del df_temp['index']
            for x in originalLine:
                if x not in df_temp.columns.values:
                    df_temp.insert(len(df_temp.columns)-1,x,'all')

            #Then append our recently customized dataframe to the current dataFrame. 
            df = df_temp.append(df)
            
            #group and reformat the dataframe.
            df = df.groupby(str).sum()
            df = df.reset_index()
            df.columns = np.where(df.columns==0, number,df.columns)            
            
    
        elif len(splitDim) is 2:
            #For all that are greater than 1 the current dataframe will be right away appended onto
            #the dataframe with the values we are looking for. Then it will be reformatted. 
            df_temp = df_split[splitDim[0],splitDim[1]]
            df = df_temp.append(df)
            df = df.groupby([splitDim[0],splitDim[1]]).sum()

            df = df.reset_index()
            df.columns = np.where(df.columns==0, number,df.columns)
    
    
    
        elif len(splitDim) is 3:
            df_temp = df_split[splitDim[0],splitDim[1], splitDim[2]]
            df = df_temp.append(df)
            df = df.groupby([splitDim[0],splitDim[1], splitDim[2]]).sum()

            df = df.reset_index()
            df.columns = np.where(df.columns==0, number,df.columns)
    
    
    
        elif len(splitDim) is 4:
            df_temp = df_split[splitDim[0],splitDim[1], splitDim[2], splitDim[3]]
            df = df_temp.append(df)
            df = df.groupby([splitDim[0],splitDim[1], splitDim[2], splitDim[3]]).sum()

            df = df.reset_index()
            df.columns = np.where(df.columns==0, number,df.columns)
    
        elif len(splitDim) is 5:
            df_temp = df_split[splitDim[0],splitDim[1], splitDim[2], splitDim[3], splitDim[4]]
            df = df_temp.append(df)
            df = df.groupby([splitDim[0],splitDim[1], splitDim[2], splitDim[3], splitDim[4]]).sum()

            df = df.reset_index()
            df.columns = np.where(df.columns==0, number,df.columns)
            
        #This is to add the 'all' to any where it needs to be. 
        for x in originalLine:
            if x not in df.columns.values:
                df.insert(len(df.columns)-1,x,'all')
        
        #Remove index -- like previously
        if 'index' in df:
            df = df.iloc[[1]]
            del df['index']
 
    else:
        print 'ERROR: The operation drilldown ' + str + ' is not available; dimension not available in current cube '

    return df, df_split, splitDim

#Slice functon -- returns updated dataframe, and takes in the slice argument and the current dataframe
def slice(arg, df, splitDim):
    #breaks our argument into 2 different strings to be used in slicing.
    out = arg
    breakStr = arg.split('=')
    
    
    #print splitDim
    
    if breakStr[0] in splitDim:
    
        #Checks if the column of dataframe we are dealing with is int or string -- for comparison sake
        if isinstance(df[breakStr[0]][0],(np.int64,long,float)):
            #If it is an int, set sim to be a boolean value, then use the boolean values as indexs for dataframe
            if df[breakStr[0]][0] is not 'all':
                simp = df[breakStr[0]] == int(breakStr[1])
                df = df[simp]
            else:
                print 'sorry can not perform the operation'
    
        elif isinstance(df[breakStr[0]][0],(str)):
            #If it is an str, set sim to be a boolean value, then use the boolean values as indexs for dataframe
            if df[breakStr[0]][0] is not 'all':
    
                simp = df[breakStr[0]] == str(breakStr[1])
                df = df[simp]
            else:
                print 'sorry can not perform the operation'
        else:
            print 'Sorry not possible'
    else:
        print 'ERROR: The operation slice ' + breakStr[0] + '=' + breakStr[1] + ' is not available; dimension not available in current cube '
    return df
    
#Save function
def save(df):
    #Ensures are output will always be named output1.txt ... outputn.txt
    outputFile = 'output'
    
    #Used to loop through our output paths
    x = 0
    n = 1
    while x == 0:
        #Checks if the output file exists, if so we increment n so we don't run into overwriting files
        if (os.path.isfile(outputFile + str(n) + '.txt')):
            n = n+1
        else:
            #We write to a csv file and remove the header and the index -- for formatting sake
            df.to_csv(outputFile + str(n) + '.txt', header=None, index = False)
            x = 1
    
    return 

#Load function
def load(str,splitDim):
    
    #Global variables
    global number
    global reRun
    
    #Read our input file to the dataframe
    df = pd.read_csv(str,names = splitDim)
    
    #Sets our global variable number and then removes it -- for indexing sake
    number = splitDim[-1]
    del splitDim[-1]

    #Empty dictionary where dataframes will be stored
    df_split = {}
    
    #Loop through all lengths to get our combinations for our df_split
    for L in range(1, len(splitDim) + 1):
        #Gets our actual combinations to loop through
        for subset in itertools.combinations(splitDim,L):
            
            #Goes through for each length and creates a data frame holding the values that are associated with 
            #the input of column headers, each formats pretty much the same, with only a small change when len
            #is equal to 1 because don't have to set a certain amount of subsets. This is made to fit the 5 sets
            #of column headers as instructed.
            if len(subset) is 1:
                x = subset[0]
                reRun = x
                df_split[x] = df[[x,number]]

            elif len(subset) is 2:
                df_temp = df[[subset[0],subset[1],number]]
                df_split[subset] = df_temp

            elif len(subset) is 3:
                df_temp = df[[subset[0],subset[1], subset[2], number]]
                df_split[subset] = df_temp

            elif len(subset) is 4:
                df_temp = df[[subset[0],subset[1], subset[3], number]]
                df_split[subset] = df_temp

            elif len(subset) is 5:
                df_temp = df[[subset[0],subset[1], subset[3], subset[4], number]]
                df_split[subset] = df_temp
    
    return df, df_split
    
#printOut was used for testing purposes
def printOut(df):
    print df
    return
    
#format is used to get our splitDim, which is basically our index checker throughout the program and 
#our global variable originalLine which is used as the original set of columns and never changes. 
#originalLine is used in rollup and drilldown
def format(str):
    splitDim = str.split(',')
    #for x in splitDim:
        #print x
    global originalLine
    originalLine = str.split(',')
        
    return splitDim

            


#instruct = raw_input("Please enter a command file: ")

#These are the assumed command files. Easily changable. 
instruct = 'commands.txt'
inputStr = 'input.csv'

#Open our instruct file. and prepare df, splitDim, and df_split to be passed into function
f = open(instruct, 'r')
df = ""
splitDim = ''
df_split = ''

#Loop through the file line by line. 
for line in f:
    #Check for blank lines our lines begining with #
    if (len(line.split()) != 0):
        if list(line)[0] is not '#':
            #Split up the input line to be evaluated then pass it into evaluate function
            splitLine = line.split()
            df, splitDim, df_split = evaluate(splitLine, df, splitDim, df_split)
            
            

            
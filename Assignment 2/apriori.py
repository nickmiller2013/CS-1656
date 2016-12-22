import sys
import csv
from itertools import combinations
from itertools import permutations
from string import punctuation
import re
import math

#Nick Miller
#CS 1656
#Assignment 2

#Get the command line arguments
input = sys.argv[1]
output = sys.argv[2]
min_support_percentage = sys.argv[3]
min_confidence = sys.argv[4]

# print input
# print output
# print min_support_percentage
# print min_confidence

#Read in line by line

with open(input) as f:
    content = f.readlines()

#Format the series of leetters
result = ''.join(i for i in content if not i.isdigit())
output = re.sub(r'\d+', '', result)
# print output
punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

no_punct = ""
for char in output:
    if char not in punctuations:
        no_punct = no_punct + char
# print no_punct
#  for p in permutations(content):
#     print(p)

letters = []

for c in no_punct:
    if c not in letters:
        letters.insert(len(letters), c)

letters.remove('\n')
# print letters

cfi = []

#Get the different combinations
for i in range(len(letters)):
    if i is not 0:
        for p in combinations(letters, i):
            cfi.insert(len(cfi), p)

versusLine = []

#Insert each no_ounct line in
for line in no_punct.splitlines():
    versusLine.insert(len(versusLine), line)

calculate = {}

against = 0

#loop to check if our set is exisiting and calculate. then put in a list of calculate
for line in versusLine:
    #print line
    sizeLine = len(line)
    # print sizeLine
    for k in cfi:
        against = 0
        sizeK = len(k)
        # print sizeK
        if sizeK <= sizeLine:
            # print k
            for c in k:
                if c in line:
                    # print c
                    against += 1

            if against == sizeK:

                add = "".join([str(c) for c in k])
                #print add

                #print 'next'
                if add not in calculate:
                    calculate[add] = 1
                elif add in calculate:
                    calculate[add] += 1

# print calculate

#Output to .csv file with formatting
outputFile = 'output.sup=%s,conf=%s.csv' % (min_support_percentage, min_confidence)
with open(outputFile, 'w') as csvfile:
    outputwriter = csv.writer(csvfile, quoting=csv.QUOTE_NONE, escapechar=' ')

    vfi = {}
    for i in calculate:
        support_percentage = float(calculate[i] / float(len(versusLine)))
        # print support_percentage
        if support_percentage >= float(min_support_percentage):
            i = sorted(i)


            i = str(i)
            i = i.translate(None, '''!()-[]{};:'"\,<>/?@#$%^&*_~ ''')
            vfi[i] = support_percentage

            (support_percentage) = '%.6f'%(support_percentage)
            #print "Set, %s, %s" % (support_percentage, i)

            y = ",".join(map(str, i))
            #print y

            outputwriter.writerow(['set'] + [str(support_percentage)] + [y])

    catchDouble = []

    #Go through and get our diferent permutations, then check against each case then output to .csv file
    for i in vfi:
        # print i
        # print vfi[i]
        if len(i) > 1:
            for p in permutations(i):
                #print p
                add = "".join([str(c) for c in p])
                # print add

                sizeAdd = len(add)
                partition = math.floor(float(sizeAdd) / 2)
                # print partition
                items1 = (add[0:int(partition)])
                # print 'String1: %s'% items1
                items1 = sorted(items1)
                items2 = (add[int(partition):int(sizeAdd)])
                # print 'String2: %s'% items2
                items2 = sorted(items2)

                items1 = str(items1)
                items1 = items1.translate(None, '''!()-[]{};:'"\,<>/?@#$%^&*_~ ''')

                items2 = str(items2)
                items2 = items2.translate(None, '''!()-[]{};:'"\,<>/?@#$%^&*_~ ''')

                combineItems = items1 + '.' + items2
                combineItems2 = items2 + '.' + items1

                partition2 = math.ceil(float(sizeAdd) / 2)
                # print partition
                items3 = (add[0:int(partition2)])
                # print 'String1: %s'% items1

                items3 = sorted(items3)
                items3 = str(items3)
                items3 = items3.translate(None, '''!()-[]{};:'"\,<>/?@#$%^&*_~ ''')


                items4 = (add[int(partition2):int(sizeAdd)])
                # print 'String2: %s'% items2
                items4 = sorted(items4)
                items4 = str(items4)

                items4 = items4.translate(None, '''!()-[]{};:'"\,<>/?@#$%^&*_~ ''')

                combineItems3 = items3 + '.' + items4
                combineItems4 = items4 + '.' + items3

                #The combine items are to ensure that no sdoubles go into it.

                if items1 in vfi:
                    if items2 in vfi:
                        if i in vfi:
                            if combineItems not in catchDouble:

                                left = vfi[i] / vfi[items1]
                                # print 'The left side: %s divided by %s equals %.6f'%(i,items1,left)
                                if left >= float(min_confidence):
                                    #print '1'
                                    left = '%.6f' % left
                                    (support_percentage) = '%.6f' % (vfi[i])

                                    #print 'rule,%.6f,%.6f,%s,=>,%s' % (vfi[i], left, items1, items2)
                                    x = ",".join(map(str, items1))
                                    y = ",".join(map(str, items2))

                                    outputwriter.writerow(['rule'] + [str(support_percentage)] + [str(left)] + [x] + ['=>'] + [y])

                                catchDouble.append(combineItems)

                            if combineItems2 not in catchDouble:
                                right = vfi[i] / vfi[items2]

                                if right >= float(min_confidence):
                                    #print '2'
                                    right = '%.6f' % right
                                    (support_percentage) = '%.6f' % (vfi[i])
                                    x = ",".join(map(str, items1))
                                    y = ",".join(map(str, items2))

                                    #print 'rule,%.6f,%.6f,%s,=>,%s' % (vfi[i], right, items2, items1)
                                    outputwriter.writerow(['rule'] + [str(support_percentage)] + [str(right)] + [y] + ['=>'] + [x])
                                catchDouble.append(combineItems2)

                            if combineItems3 not in catchDouble:
                                if items3 in vfi:

                                    left2 = vfi[i] / vfi[items3]

                                    # print 'The left side: %s divided by %s equals %.6f'%(i,items1,left)
                                    if left >= float(min_confidence):
                                        #print '3'
                                        left2 = '%.6f' % left2
                                        (support_percentage) = '%.6f' % (vfi[i])
                                        x = ",".join(map(str, items3))
                                        y = ",".join(map(str, items4))

                                        #print 'rule,%.6f,%.6f,%s,=>,%s' % (vfi[i], left2, items3, items4)
                                        outputwriter.writerow(['rule'] + [str(support_percentage)] + [str(left2)] + [x] + ['=>'] + [y])

                                        catchDouble.append(combineItems3)

                            if combineItems4 not in catchDouble:

                                if items4 in vfi:
                                    right2 = vfi[i] / vfi[items4]

                                    if right2 >= float(min_confidence):
                                        #print '4'
                                        (support_percentage) = '%.6f' % (vfi[i])
                                        x = ",".join(map(str, items3))
                                        y = ",".join(map(str, items4))

                                        right2 = '%.6f' % right2
                                        #print 'rule,%.6f,%.6f,%s,=>,%s' % (vfi[i], right, items4, items3)
                                        outputwriter.writerow(['rule'] + [str(support_percentage)] + [str(right2)] + [y] + ['=>'] + [x])
                                        catchDouble.append(combineItems4)
                                # print 'The right side: %s divided by %s equals %.6f' % (add, items2, right)

                                # for k in p:
                                # print k

#print catchDouble
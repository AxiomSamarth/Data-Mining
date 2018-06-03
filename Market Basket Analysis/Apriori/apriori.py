from __future__ import division
import pandas as pd
import numpy as np
from itertools import *
import math

items = []
dataset = open('./Datasets/apriori/example1.csv','r').read().split('\n')
unique_items = []

for data in dataset:
    item = data.split(',')
    for i in range(len(item)):
        item[i] = int(item[i])
    items.append(item)

itemset = {}
for item in items:
    itemset[item[0]] = item[1:]

for item in itemset:
    for i in itemset[item]:
        if i not in unique_items:
            unique_items.append(i)

unique_items.sort()

def find_support(item):

    count = 0
    for key in itemset:
        flag=0
        for i in item:
            if i not in itemset[key]:
                flag=1

        if flag==0:
            count+=1

    return count

minimum_support = 2
candidate_itemset = []
pre_frequent_itemset = []

for iteration in range(1, len(unique_items)+1):

    print "Iteration " + str(iteration)

    items = [list(i) for i in combinations(unique_items, iteration)]
    frequent_itemset = []

    for item in items:
        support = find_support(item)
        candidate_itemset.append([item, support])

    print candidate_itemset

    for item in candidate_itemset:
        if item[1]>=minimum_support:
            frequent_itemset.append(item)

    print str(frequent_itemset) + "\n"+ str(len(frequent_itemset))

    if len(frequent_itemset) == 0:
        pre_frequent_itemset = np.array(pre_frequent_itemset)
        print "The frequent itemset is" + str(pre_frequent_itemset[:,0])
        break

    candidate_itemset = []
    pre_frequent_itemset = frequent_itemset

print "Thanks for using my code for market basket analysis!"

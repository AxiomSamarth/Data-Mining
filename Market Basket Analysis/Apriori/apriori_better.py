from __future__ import division
from itertools import *
import numpy as np

minimum_support = 1200
minimum_confidence = 60

location = "./Datasets/apriori/75000"

dataset = open(location+'/75000-out1.csv', 'r').read().split('\n')
itemset = {}
for data in dataset:
    l = data.split(',')
    l = [int(i) for i in l]
    itemset[l[0]] = l[1:]

# print itemset

unique_itemset = []
for item in itemset:
    for i in itemset[item]:
        if i not in unique_itemset:
            unique_itemset.append(i)

unique_itemset.sort()
# print unique_itemset
previous_itemset = []


def find_support(item_list):

    count = 0
    for key in itemset:
        flag = 0
        for i in item_list:
            if i not in itemset[key]:
                flag = 1
        if flag == 0:
            count += 1

    return count


def find_items(items, iteration):
    combo = [list(i) for i in combinations(items, 2)]
    l = []
    for i in combo:
        m = []
        for j in i:
            for k in j:
                m.append(k)
        m = set(m)
        m = list(m)
        l.append(m)

    unique_list = []
    for i in l:
        i.sort()
        if i not in unique_list and len(i) == iteration:
            unique_list.append(i)

    # print "Unique list :", unique_list
    return unique_list


def rule_generation(itemset):

    print "\nThe rules generated with",minimum_confidence,"percent confidence threshold are as follows:\n"

    for i in itemset:
        print "\nRules for frequent itemset", i
        support = find_support(i)
        combos = []
        for j in range(1,len(i)):
            combos.append(list(combinations(i,j)))
            #print combos[j-1]
            for k in combos[j-1]:
                support_k = find_support(list(k))
                if support_k!=0:
                    if support*100/support_k >= minimum_confidence:
                        #print list(k),"--->",[list(itm) for itm in combos[j-1] if itm != k]
                        print list(k), "--->", [itm for itm in i if itm not in k]
        #print i,support,combos

    return


for iteration in range(1, len(unique_itemset) + 1):

    candidate_itemset = []
    frequent_itemset = []

    # print "Iteration",iteration
    file_ci = open(location + "/candidate_itemset" + str(iteration) + ".txt", 'a')
    file_fi = open(location + "/frequent_itemset" + str(iteration) + ".txt", 'a')

    file_ci.write("[[itemset] , support]" + "\n")
    file_fi.write("[[itemset] , support]" + "\n")

    if iteration == 1:

        # print "Previous itemset", previous_itemset
        items = [list(i) for i in combinations(unique_itemset, 1)]
        for item in items:
            support = find_support(item)
            candidate_itemset.append([item, support])

        for item in candidate_itemset:
            if item[1] >= minimum_support:
                frequent_itemset.append(item)

        for itm in candidate_itemset:
            file_ci.write(str(itm)+"\n")
        for itm in frequent_itemset:
            file_fi.write(str(itm)+"\n")

        previous_itemset = frequent_itemset
        # print "Candidate itemset", candidate_itemset
        # print "Frequent itemset", frequent_itemset

    elif iteration > 1:

        # print "Previous itemset", previous_itemset
        previous_itemset = np.array(previous_itemset)
        previous_itemset = previous_itemset[:, 0]
        previous_itemset = list(previous_itemset)

        items = find_items(previous_itemset, iteration)

        for item in items:
            support = find_support(item)
            candidate_itemset.append([item, support])

        for item in candidate_itemset:
            if item[1] >= minimum_support:
                frequent_itemset.append(item)

        for itm in candidate_itemset:
            file_ci.write(str(itm)+"\n")
        for itm in frequent_itemset:
            file_fi.write(str(itm)+"\n")

        if len(frequent_itemset) == 0:
            print "\nThe frequently bought itemset are", previous_itemset
            rule_generation(previous_itemset)
            print "\nProcess completed in",iteration,"iterations and the intermediate frequent itemsets and candidate itemsets have been logged in the log_files.\n"
            exit(0)
        elif len(frequent_itemset) == 1:
            fi = np.array(frequent_itemset)
            print "\nThe frequently bought itemset are", fi[:,0]
            rule_generation(frequent_itemset)
            print "\nProcess completed in", iteration, "iterations and the intermediate frequent itemsets and candidate itemsets have been logged in the log_files.\n"
            exit(0)

        previous_itemset = frequent_itemset
        #print "Candidate itemset", candidate_itemset
        #print "Frequent itemset", frequent_itemset

        file_ci.close()
        file_fi.close()
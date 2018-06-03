from __future__ import division
import pandas as pd 
import math
import numpy as np 
from scipy.stats import pearsonr
data = pd.read_csv('movies.csv')

#drop data that is unwanted for the analysis
data.drop(['poster','director','running_time','storyline','description','gallery/0','gallery/1','gallery/2','gallery/3','gallery/4','stars/0','stars/1','stars/2','release_date'],1, inplace=True)

file = open('Results.json','a')
file.write("{\n")


#This function is to find the correlation coefficient between the atributes of the movie.
def find_correlation(movie_1, movie_2):
	movie_1 = np.array(movie_1)
	movie_2 = np.array(movie_2)

	movie_1_dashed = np.array([(i - np.mean(movie_1))/np.std(movie_1) for i in movie_1])
	movie_2_dashed = np.array([(i - np.mean(movie_2))/np.std(movie_2) for i in movie_2])

	correlation = np.dot(movie_1_dashed,movie_2_dashed)/len(movie_1)
	return correlation


'''This function takes all the correlation coefficients of 1 movie with remaining 249 movies and sorts them in descending order
and picks the first 10 movies so that they are now arranged in descending order of their similarity. Also this
includes code to write it into the output JSON file'''
def find_similar(correlation_list, movie_dictionary):

	for i in range(len(correlation_list)):
		for j in range(1+i,len(correlation_list)-1):
			if correlation_list[i][2] < correlation_list[j][2]:
				temp = correlation_list[j]
				correlation_list[j] = correlation_list[i]
				correlation_list[i] = temp

	corr_list = correlation_list[:10]
	# for i in corr_list:
	# 	print i
	# print "\n\n"
	line = "\""+movie_dictionary[corr_list[0][0]+1]+"\":["
	file.write(line)
	for i in corr_list:
		line = "\""+movie_dictionary[i[1]+1]+"\"" + ","
		file.write(line)

	file.write("],\n")


#This function is for preprocessing the data
def preprocessing(data):

	df = []

	'''Grab the attributes required for finding the similarity and arrange them in a list of list.
	Where primary list is the movies and secondary or inner list is the significant attributes of each 
	individual movies'''
	for id in range(len(data)):
	    li = []
	    genre = []
	    for i in data:
	        if i not in ['genre/0', 'genre/1', 'genre/2']:
	            if str(data[i][id]) == 'nan':
	                li.append(int(0))
	            else:
	                li.append(data[i][id])

	        if i in ['genre/0','genre/1','genre/2'] and str(data[i][id])!='nan':
	            genre.append(data[i][id])

	    li.append(genre)
	    df.append(li)

	#Create a dictionary of keys being movie_ids and values being the names of movies for future use
	movie_dictionary = {}
	for i in df:
	    movie_dictionary[i[2]] = i[3]

	#Now for each movie, compare it with every other movie for similarity
	for i in range(len(df)):
		correlation = 0		
		correlation_list = []
		for j in range(len(df)):
			if i!=j:
				movie_1 = []
				movie_2 = []
				for index in range(len(df[i])):
					if index not in [2,3]:
						movie_1.append(df[i][index])
						movie_2.append(df[j][index])

				'''This code from line 94 to 115 finds the common genre between the two movies being utilized
				and gives a relative value to it given by (number_of_common_genre_in_both / total number of genre in both). 
				This way, a new feature is generated to serve the purpose'''

				genre = []
				for item in movie_1[-1]:
					genre.append(item)
				for item in movie_2[-1]:
					genre.append(item)
				genre = list(set(genre))

				g_value_1 = 0
				g_value_2 = 0

				for item in genre:
					if item in movie_1[-1]:
						g_value_1 += 1
					if item in movie_2[-1]:
						g_value_2 += 1

				movie_1[3] = int(2017 - int(movie_1[3]))
				movie_2[3] = int(2017 - int(movie_2[3]))

				movie_1[-1] = float(g_value_1/len(genre))
				movie_2[-1] = float(g_value_2/len(genre))
				#print movie_1, movie_2

				#Now find the correlation by calling find_correlation function

				correlation = find_correlation(movie_1,movie_2)
				correlation_list.append([i, j, correlation])

		# for i in correlation_list:
		# 	print i
		#Send the found correlations to be aranged in descending order of similarity and to find the top 10 similar movies
		find_similar(correlation_list, movie_dictionary)
		print i,


preprocessing(data)
# for i in correlation_list:
# 	print i
file.write("}")
file.close()
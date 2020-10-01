"""
This code is the work of Shammi Anand
"""

#----------------------------------------------------------------------
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#----------------------------------------------------------------------

def get_title_from_index(index):
	return df[df.index == index]["title"].values[0]

def get_index_from_title(title):
	return df[df.title == title]["index"].values[0]

def match_name(user_choice):
	exists = False
	for name in df['title']:
		if name == movie_user_likes:
			exists = True
			break
	return exists
#----------------------------------------------------------------------

df = pd.read_csv("movie_dataset.csv")
movie_user_likes = input("Enter the name of movie you like : ")

#----------------------------------------------------------------------

def find_similar_movies(words):
	number = 1
	size = len(words)
	for name in df['title']:
		total = 0
		for word in words:
			counter = 0
			n = len(word)
			for c in name:
				if counter == n:
					break
				if c == ' ':
					continue
				if c == word[counter]:
					counter += 1
			if counter == n:
				total += 1
		if total == size:
			print(f"{number}. {name}")
			number += 1

if match_name(movie_user_likes) == False :
	print("This movie does not exists!")
	words = list(movie_user_likes.split(" "))
	words.sort(key = lambda x:len(x), reverse=True)
	new_words = [word.capitalize() for word in words]
	print("Did you mean : ")
	find_similar_movies(new_words)
	movie_user_likes = input("Enter the name of movie you like : ")
#----------------------------------------------------------------------
features = ['keywords','cast','genres','director']
for feature in features:
	df[feature] = df[feature].fillna('')


def combine_features(row):
	try:
		return row['keywords'] +" "+row['cast']+" "+row["genres"]+" "+row["director"]
	except:
		print("Error:", row)

df["combined_features"] = df.apply(combine_features,axis=1)

cv = CountVectorizer()
count_matrix = cv.fit_transform(df["combined_features"])


cosine_sim = cosine_similarity(count_matrix) 


movie_index = get_index_from_title(movie_user_likes)
similar_movies =  list(enumerate(cosine_sim[movie_index]))
sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)

#----------------------------------------------------------------------

print("Here are the top 10 similar movies we recommend : ")
i=1
for element in sorted_similar_movies:
		print(f"{i}. {get_title_from_index(element[0])}")
		i+=1
		if i>10:
			break
#----------------------------------------------------------------------
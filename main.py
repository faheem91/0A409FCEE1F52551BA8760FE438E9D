

'''
################################################
Alert Management System (AMS) - Scrapper 

*******
AUTHORS
*******
1 - Faheem ud Din 
2 - Ahmad Turab
3 - Syed Mehdi 
4 - Fahad Jabbar 

***************
IMPLEMENTATIONS
***************
1 - Parsing HTML on the URL 
2 - Extracting text from HTML 
3 - Extracting keywords from text 
4 - Defining keywords in Alert categories 
5 - Categorization of Alert via keyword match
6 - Validation of Alert based on fraud score 
7 - Exporting data collected to MySQL DB 

***************
DISCLAIMER
***************
1 - The script implements parsing bots, in this case 
	customized according to usatoday.com 
2 - The alert category keywords are hardcorded, more 
	will be added to increase accuracy 
3 - 
################################################
'''


'''
################################################
IMPORT == Libraries 
################################################
'''
from bs4 import BeautifulSoup
import urllib
import http.client
import os, sys
import fnmatch, glob
import string
import copy
import operator
import math
import fnmatch 
import random
import pygal 
import get_pagerank
import pagerank
from stemming.porter import stem
from urllib.request import urlopen
from pagerank import GetPageRank


'''
################################################
FUNCTION == Extract top keywords from URL 
################################################
'''
def getKeywords(articletext):
	web_links = []
	web_links.extend(["facebook", "twitter", "link", "social", "el", "post", "share", "like", "comment"])
	common = open("common_words.txt").read().split('\n')
	word_dict = {}
	word_list = articletext.lower().split()
	for word in word_list:
		if word not in common and word.isalnum():
			if word not in word_dict:
				word_dict[word] = 1
			if word not in web_links: 
				word_dict[word] += 1
			if word in word_dict:
				word_dict[word] += 1
#	top_words =  sorted(word_dict.items(),key=lambda(k,v):(v,k),reverse=True)[0:50]
	top50 = []
#	for w in top_words:
#		top50.append(w)
	return top50

'''
################################################
DEFINE == Define the URL 
################################################
'''

url_protocol = "http://" 
url_tld = "usatoday.com"
url_link = "/story/weather/2015/10/16/pacific-ocean-typhoon-hurricane-season/74061922/"

url = url_protocol + url_tld + url_link 

htmltext = urllib.request.urlopen(url).read()
soup = BeautifulSoup(htmltext, "lxml")
print(soup)



'''
################################################
EXTRACT == Get text from HTML obtained from URL  
################################################
'''

article = ""
for text in soup.findAll("p"):
	article += str(text.encode("utf-8"))


'''
################################################
DEFINE == Categories of Alerts  
################################################
'''

political_alert = []
political_alert.extend(["government", "conference", "dharna", "protest", "parliment", "committee", "elect", "votes", "minister", "elected", "official", "speech", "prime", "pml", "pti", "party", "justice", "mayor", "resign", "inquiry", "sub", "campaign", "democracy", "leader"])

weather_alert = []
weather_alert.extend(["flood", "rain", "power", "storm", "hail", "crash", "typhoon", "temperature", "hurricane", "snow", "fog", "humidity", "pressure", "air", "hot", "cold", "spring", "winter", "autumn", "breeze"])

traffic_alert = []
traffic_alert.extend(["bus", "car", "bike", "traffic", "truck", "bicycle", "accident", "block", "signal", "jam", "route", "wait", "protocol", "line", "road", "bridge", "close", "toll", "motorway", "side"])

terrorism_alert = []
terrorism_alert.extend(["kill", "death", "die", "blast", "authority", "police", "military", "internal", "affair", "ranger", "terror", "isis", "ttp", "taliban", "suicide", "threat", "radical", "extremist", "eliminate", "wanted", "criminal", "suspect", "custody", "hearing", "judicial", "arrest", "felony", "massacre", "behead", "emergency"])

'''
################################################
CALCULATE == Cosine Similarity of Keywords
################################################
'''


def calculate_cosine_similarity(alert_type):
	cos_numerator_sum = 0
	cos_denominator_local_count = 0 
	cos_denominator_news_count = 0 

	for local_word in alert_type: 
		for news_word in getKeywords(article): 
			if stem(local_word) == stem(news_word[0]):
				cos_numerator_sum = cos_numerator_sum + news_word[1]
				cos_denominator_local_count+=1
				cos_denominator_news_count_temp = news_word[1]*news_word[1]
				cos_denominator_news_count = cos_denominator_news_count + cos_denominator_news_count_temp

	cos_denominator_sum = math.sqrt(cos_denominator_news_count) * math.sqrt(cos_denominator_local_count)

	cos_similarity = 0


	if cos_denominator_sum != 0: 
		cos_similarity = cos_numerator_sum / cos_denominator_sum


	return cos_similarity

'''
################################################
CALCULATE == Alert Classification 
################################################
'''


def classify_cateogry(): 
	
	classify_arr = []	
	classify_arr.append(calculate_cosine_similarity(political_alert))
	classify_arr.append(calculate_cosine_similarity(weather_alert))
	classify_arr.append(calculate_cosine_similarity(traffic_alert))
	classify_arr.append(calculate_cosine_similarity(terrorism_alert))

	closest_cateogry = max(classify_arr)
	

	if closest_cateogry == 0: 
		return "None"


	for i in classify_arr: 
		if classify_arr[0] == closest_cateogry: 
			return "Political"
		if classify_arr[1] == closest_cateogry: 
			return "Weather"
		if classify_arr[2] == closest_cateogry: 
			return "Traffic"
		if classify_arr[3] == closest_cateogry: 
			return "Terrorism"








'''
################################################
CALCULATE == Page Validation Module 
################################################
'''

#def page_validity(): 

#	page_rank = int(get_pagerank.my_func(url_protocol + url_tld))

#	if page_rank < 6: 
#		alert_valid = 0
#	else: 
#		alert_valid = 1

#	if alert_valid == 0: 
#		return "invalid"
#	else: 
#		return "valid"



alert_category_message =  "The URL represents a " + classify_cateogry() + " alert!" 
#alert_valid_message = "The alert appears to be " + page_validity() + "!"

print(alert_category_message)

#print(alert_valid_message)

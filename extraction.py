#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Corpus extraction from different categories.
"""

#################### Libraries ####################
import os
import argparse
# import requests
import json
import nltk
from SPARQLWrapper import SPARQLWrapper , JSON
import wikipedia, wptools
#################### Functions ####################

#################### Test ####################



#########################################################################################
categories = ['Airports', 'Artists', 'Astronauts', 'Building', 'Astronomical_objects', 'City',
'Comics_characters', 'Companies', 'Foods', 'Transport', 'Monuments_and_memorials', 'Politicians', 'Sports_teams',
'Sportspeople', 'Universities_and_colleges', 'Written_communication']
k_art = int(input('please enter the number of articles (k)?'))
n_sent = int(input('please enter the number of sentences (n)?'))
try :
	os.mkdir('./data_info')
except:
	print('directore data_info exist.')
try :
	os.mkdir('./data')
except:
	print('directore data exist.')
################################################################################## from last year
# agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
# gragh_endpoint ='https://query.wikidata.org/sparql'

######################################################################
agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
dataStore = "http://dbpedia.org/sparql/"  # 'https://query.wikidata.org/sparql' 
sparql = SPARQLWrapper(dataStore)
for category in categories :
	query =  """
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dbo: <http://dbpedia.org/ontology/>

SELECT ?page , ?pageID WHERE {
	?page dcterms:subject/skos:broader*  	dbc:""" + category + """;
	  dbo:wikiPageID ?pageID .
	
	 } LIMIT """+ str(k_art)
	
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
# print('hi')
	try: 
		result = sparql.query().convert()
		try:
			os.mkdir('./data/'+ category)
		except:
			print(category , ' directory already exist.')

		try:
			os.mkdir('./data_info/'+ category)
		except:
			print(category , ' directory already exist.')

		f=  open('./data_info/'+ category+'/' + category + '_url.txt' , 'w')
	# f2=  open('./data_info/'+ category+'/' + category + '_pageid.txt' , 'w')
	

		for res in result['results']['bindings']:
			print(res['page']['value'], '------------' , res['pageID']['value'])
			print (res['page']['value'] , ', ' , res['pageID']['value'] , file=f)
			pageid = res['pageID']['value']
			try : 
				page = wikipedia.page(pageid = pageid)
				title = page.title
				title_parts = title.split(' ')
				new_title = '_'.join(title_parts)
				article  = open('./data/'+ category+'/' + new_title + '.txt' , 'w') 
				print(new_title)
				content =  page.content
				# try:
				# 	sents = nltk.sent_tokenize(content)
				# 	print(sents[:])
				# except:
				# 	print('sentence tokenizer does not work.')
				print( page.content , file=article)
				article.close()
			except:
				print('error:  wikipedia tool , page  :' , new_title)
			# page2 = wptools.page(pageid = pageid)
			
			# print(res['pageID']['value'], file=f2)
		f.close()
		





	except:
		print('\n\n\nthere was an eror for category :', category)

	
	
	
	# f2.close()
	
	
	
# print(result)
# for res in result["results"]["bindings"]:
# 	print(res["label"]["value"])
#####################################################################
# page2 = wptools.page(pageid=55238747)
##############################################
# print(results)

# def main():
#     pass

# # main entry point
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Corpus Extractor")
#     parser.add_argument("--n_people", type=int, default=30, help="number of persons to extract for each domain")
#     parser.add_argument("--n_sentences", type=int, default=10, help="number of sentences to extract for each person")
#     parser.add_argument('--verbose', help='print out the logs (default: False)', action='store_true')
#     args = parser.parse_args()
#     main(args.n_sentences, args.n_people, args.verbose)

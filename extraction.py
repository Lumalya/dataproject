#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Corpus extraction from different categories.
"""

#################### Libraries ####################
from bdb import Breakpoint
import os
import argparse
# import requests
import json
import nltk
# import spacy
from SPARQLWrapper import SPARQLWrapper , JSON
import wikipedia, wptools
#################### Functions ####################

#################### Test ####################



#########################################################################################
categories = ['Airports', 'Artists', 'Astronauts', 'Building', 'Astronomical_objects', 'City',
'Comics_characters', 'Companies', 'Foods', 'Transport', 'Monuments_and_memorials', 'Politicians', 'Sports_teams',
'Sportspeople', 'Universities_and_colleges', 'Written_communication']
k_art = int(input('please enter the number of articles per category (k)?'))
n_sent = int(input('please enter the minimum number of sentences (n)?'))
try : os.mkdir('./data_info')
except Exception as e : print(e)
try : os.mkdir('./data')
except Exception as e : print(e)
################################################################################## 
# agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
# gragh_endpoint ='https://query.wikidata.org/sparql'

######################################################################
agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
dataStore = "http://dbpedia.org/sparql/"  # 'https://query.wikidata.org/sparql' 
sparql = SPARQLWrapper(dataStore)
# nlp = spacy.load('en_core_web_sm')

for category in categories :
	query =  """
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dbo: <http://dbpedia.org/ontology/>

SELECT ?page , ?pageID WHERE {
	?page dcterms:subject/skos:broader*  	dbc:""" + category + """ ;
	  dbo:wikiPageID ?pageID .
	
	 } LIMIT """+ str(k_art)
	
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
# print('hi')
	try: 
		result = sparql.query().convert()
		try: os.mkdir('./data/'+ category)
		except Exception as e : print(e)

		try: os.mkdir('./data_info/'+ category)
		except Exception as e : print(e)

		f=  open('./data_info/'+ category+'/' + category + '_url.txt' , 'a')
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
				
				content =  page.content
				'''
				text = nlp(content) 
				i = 0
				for sen in text.sents : 
					i += 1
				if i <  n_sent : continue
				'''
				if len(content) < n_sent * 100 : 
					print('Short article! ' , len(content)/100 )
					continue
				article  = open('./data/'+ category+'/' + new_title + '.txt' , 'w')
				print( page.content , file= article)
				article.close()
				try:
					pageInfo = wptools.page(pageid = pageid, silent = True)
					pageInfo.get()
					infobox = pageInfo.data['infobox']
					print('wptools done!\n' , infobox)
					with open('./data/' + category+ '/' + new_title + '_infobox.json' , 'w') as fjson :
						json.dump(infobox, fjson)
					with open('./data/' + category+ '/' + new_title + '_statements.json' , 'w') as fjson2 :
						json.dump( pageInfo.data['wikidata'] , fjson2)
					# with open('./data/' + category+ '/' + new_title + '_description.json' , 'w') as fjson3 :
					# 	json.dump( pageInfo.data['description'] , fjson3)
					# 	print(pageInfo.data['description'])

				except Exception as e :
					print('\n' , 'error: wptools, page : ' , pageid)
					print(e)
					
			except Exception as e :	
				print( '\n' , 'error:  wikipedia tool, page  :' , pageid)
				print(e)
				

			

			

			
			# page2 = wptools.page(pageid = pageid)
			
			# print(res['pageID']['value'], file=f2)
		f.close()
		





	except Exception as e:
		print('\n\n\nthere was an eror for category :', category)
		print(e)


	
	
	
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SEANG Chea-Jimmy
NIAOURI Dimitra
ROSHANFEKR Ghasem
"""

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
from SPARQLWrapper import SPARQLWrapper, JSON
import wikipedia, wptools
#################### Functions ####################
def toSave(category, new_title, page, pageInfo, result2):
	article = open('./data/' + category + '/' + new_title + '.txt', 'w')
	print(page.content, file=article)
	article.close()
	with open('./data/' + category + '/' + new_title + '_desc.txt', 'w') as fdes:
		if len(result2['results']['bindings']) > 0 :
			print(result2['results']['bindings'][0]['o']['value'], file=fdes)
		else :
			print('...', file=fdes)
	with open('./data/' + category + '/' + new_title + '_infobox.json', 'w') as fjson:
		json.dump(pageInfo.data['infobox'], fjson)
	with open('./data/' + category + '/' + new_title + '_statements.json', 'w') as fjson2:
		json.dump(pageInfo.data['wikidata'], fjson2)





#########################################################################################
categories = [
	'Airports',
	'Artists',
	'Astronauts',
	'Building',
	'Astronomical_objects',
	'City',
	'Comics_characters',
	'Companies',
	'Foods',
	'Transport',
	'Monuments_and_memorials',
	'Politicians',
	'Sports_teams',
	'Sportspeople',
	'Universities_and_colleges',
	'Written_communication'
]
k_art = int(input('please enter the number of articles per category (k)?'))
n_sent = int(input('please enter the minimum number of sentences (n)?'))
try: os.mkdir('./data_info')
except Exception as e: print(e)
try: os.mkdir('./data')
except Exception as e: print(e)
################################################################################## 
# agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
# nlp = spacy.load('en_core_web_sm')
######################################################################
dataStore = "http://dbpedia.org/sparql/"  # endpoint for DBpedia sparql query
sparql = SPARQLWrapper(dataStore)  # Wrapper for DBpedia sparql query
# define a general query for categories to extract from dbpedia ...
query_ = """
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dbo: <http://dbpedia.org/ontology/>

SELECT ?page , ?pageID WHERE {
	?page dcterms:subject/skos:broader*  dbc:<category> ;
	dbo:wikiPageID ?pageID .

	} LIMIT <LIMIT_NUM> """
query0 = query_.replace('<LIMIT_NUM>', str(k_art)) # a place holder for making query for each category

dataStore2 = "https://query.wikidata.org/sparql"
sparql2 = SPARQLWrapper(dataStore2)
# define a general query for wikidata to extract description
query02 = """
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX schema: <http://schema.org/>

SELECT ?o WHERE {
  wd:<Qid> schema:description ?o .
  FILTER ( lang(?o) = "en" )
}
"""
# a place holder for making query for each article description

result = None
for category in categories:
	sparql.setQuery(query0.replace('<category>', category))
	sparql.setReturnFormat(JSON)

	flagError = False
	try:
		result = sparql.query().convert()
		print('\n query don!' , category)
		# if len (result['results']['bindings']) < 4 :
		# 	query_skos = query.replace('/skos:broader*', '')
		# 	sparql.setQuery(query_skos)
		# 	sparql.setReturnFormat(JSON)
		# 	# try:
		# 	# 	result = sparql.query().convert()
		# 	# except Exception as e :
		# 	# 	print(e)
	except Exception as e:
		flagError = True
		print('\n\n\n  there was an error for category :', category)
		print(e)
		print('trying with new query:')

		try:
			# query_skos =
			sparql.setQuery(query0.replace('<category>', category).replace('/skos:broader*', ''))
			sparql.setReturnFormat(JSON)
			# try:
			result = sparql.query().convert()
			print('\n query don!', category)
		except Exception as e :
			print('\n\n\n Again, there was an error for category :', category)
			print(e)


		# raise
	if result != None and len(result['results']['bindings']) > 0 :
		try: 	os.mkdir('./data/' + category)
		except Exception as e: 	print(e)
		try: os.mkdir('./data_info/' + category)
		except Exception as e: 	print(e)
		for res in result['results']['bindings']:
			print(res['page']['value'], '------------', res['pageID']['value'])
			# print (res['page']['value'] , ', ' , res['pageID']['value'] , file=f)
			pageid = res['pageID']['value']
			# print(res['page']['value'], ', ', res['pageID']['value'], ', ', Qid, file=f)

			try:
				page = wikipedia.page(pageid=pageid)
				title = page.title
				title_parts = title.split(' ')
				new_title = '_'.join(title_parts)

				content = page.content
				'''
				text = nlp(content) 
				i = 0
				for sen in text.sents : 
					i += 1
				if i <  n_sent : continue
				'''
				if len(content) < n_sent * 100:
					print('Short article! ', len(content) / 100)
					flagError = True
					# raise Exception
					continue

				try:
					pageInfo = wptools.page(pageid=pageid, silent=True)
					pageInfo.get()
					infobox = pageInfo.data['infobox']
					print('\n\nwptools done!', infobox)
					Qid = pageInfo.data["wikibase"]

					query2 = query02.replace('<Qid>', Qid)
					sparql2.setQuery(query2)
					sparql2.setReturnFormat(JSON)
					result2 = None
					try:
						result2 = sparql2.query().convert()
						print('\n res2 done')
					except Exception as e:
						print('\n fail res2')
						print(e)
						# raise e
					toSave(category=category, new_title=new_title, page=page, pageInfo=pageInfo, result2=result2)
					# article = open('./data/' + category + '/' + new_title + '.txt', 'w')
					# print(page.content, file=article)
					# article.close()
					print('save done!')

				# with open('./data/' + category+ '/' + new_title + '_description.json' , 'w') as fjson3 :
				# 	json.dump( pageInfo.data['description'] , fjson3)
				# 	print(pageInfo.data['description'])

				except Exception as e:
					flagError = True
					print('\n', 'error: wptools, page : ', pageid)
					print(e)

			except Exception as e:
				flagError = True
				print('\n', 'error:  wikipedia tool, page  :', pageid)
				print(e)
			if not flagError: pass
		# f.close()


# print(result)
# for res in result["results"]["bindings"]:
# 	print(res["label"]["value"])
#####################################################################
# page2 = wptools.page(pageid=55238747)
##############################################
# print(results)

def main(n_sentences, n_people, verbose):
    print(n_sentences, n_people, verbose)

# main entry point
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Corpus Extractor")
#     parser.add_argument("--n_people", type=int, default=30, help="number of persons to extract for each domain")
#     parser.add_argument("--n_sentences", type=int, default=10, help="number of sentences to extract for each person")
#     parser.add_argument('--verbose', help='print out the logs (default: False)', action='store_true')
#     args = parser.parse_args()
#     main(args.n_sentences, args.n_people, args.verbose)

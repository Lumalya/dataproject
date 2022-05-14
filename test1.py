import os
import argparse
# import requests
import json
import nltk
# import spacy
from SPARQLWrapper import SPARQLWrapper, JSON
import wikipedia, wptools


dataStore2 = "https://query.wikidata.org/sparql"
sparql2 = SPARQLWrapper(dataStore2)
query2 = """
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX schema: <http://schema.org/>

SELECT ?o WHERE {
  wd:<Qid> schema:description ?o .
  FILTER ( lang(?o) = "en" )
}
"""
query22 = query2.replace('<Qid>', 'Q76')
sparql2.setQuery(query22)
sparql2.setReturnFormat(JSON)
try:
    result2 = sparql2.query().convert()
except Exception as e:
    print(e)
    raise

print(result2['results']['bindings'][0]['o']['value'])
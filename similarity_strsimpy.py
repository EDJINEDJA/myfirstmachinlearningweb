
def nlp(text1,text2):
   import spacy

   nlp = spacy.load("en_core_web_sm")
   doc1 = nlp(text1)
   doc2 = nlp(text2)
   
   return doc1, doc2


def Levenshtein_(text1,text2):
   doc1, doc2=nlp(text1,text2)
   from  strsimpy.levenshtein import Levenshtein
   levenshtein=Levenshtein()
   return levenshtein.distance(doc1,doc2)
    
    
def normalized_Levenshtein_(text1,text2):
   doc1, doc2=nlp(text1,text2)
   from  strsimpy.normalized_levenshtein import  NormalizedLevenshtein
   levenshtein= NormalizedLevenshtein()
   return levenshtein.distance(doc1,doc2)
    
    
def jarowinkler_(text1,text2):
   doc1, doc2=nlp(text1,text2)
   from strsimpy.jaro_winkler import JaroWinkler

   jarowinkler = JaroWinkler()
   
   return jarowinkler.similarity(doc1,doc2)


def nGramSimilarity_(text1,text2,numberNgram):
   doc1, doc2=nlp(text1,text2)
   from strsimpy.ngram import NGram

   twogram = NGram(numberNgram)
   return twogram.distance(doc1, doc2)

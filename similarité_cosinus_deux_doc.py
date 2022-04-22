def similarity_cosine(text1,text2):

  import spacy

  nlp = spacy.load("en_core_web_sm")
  doc1 = nlp(text1)
  doc2 = nlp(text2)
  
  return doc1.similarity(doc2)






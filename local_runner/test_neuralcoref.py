import spacy
import neuralcoref

nlp = spacy.load('en') # this is the line where it crashes
neuralcoref.add_to_pipe(nlp)

doc1 = nlp(u'My sister has a dog. She loves him. My mother has a cat. She loves him')
print(doc1._.coref_clusters)
print (doc1._.has_coref)
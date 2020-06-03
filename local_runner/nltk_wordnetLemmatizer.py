import nltk

print (nltk.stem.WordNetLemmatizer().lemmatize('loving', 'v'))


text = nltk.word_tokenize("I am loving you")
print (nltk.pos_tag(text))
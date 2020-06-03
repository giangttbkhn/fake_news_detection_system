from pycorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP('http://localhost:9000')
text = "'Tom is 42 years old, he is a teacher'"
output = nlp.annotate(text, properties={
    'annotators': 'tokenize, ssplit, pos, depparse, parse, openie',
    'outputFormat': 'json'
    })

for item in output:
    for item2 in output[item]:
        print (item2)

print (output['sentences'][0])

for item in output['sentences'][0]:
    print (item)

print (output['sentences'][0]['openie'])

#[{'subject': 'he', 'subjectSpan': [7, 8], 'relation': 'is', 'relationSpan': [8, 9], 'object': 'teacher', 'objectSpan': [10, 11]}, {'subject': 'Tom', 'subjectSpan': [1, 2], 'relation': 'is old', 'relationSpan': [2, 3], 'object': '42 years', 'objectSpan': [3, 5]}]
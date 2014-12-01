from nltk.tokenize import sent_tokenize
from nltk.parse import malt
from nltk.parse.dependencygraph import DependencyGraph
import os
from textblob import TextBlob
from textblob_aptagger import PerceptronTagger

path = './examples'
files = [os.path.join(path, fname) for fname in os.listdir(path) if fname.endswith('.edus')]
tagger = PerceptronTagger()
m = malt.MaltParser()
trainingFile= open('english_train.conll','r')
m.train_from_file(trainingFile,verbose=False)

for fname in files[:1]:
	f = open(fname, 'r')
	text = f.read()
	for sent in sent_tokenize(text):
		blob = TextBlob(sent, pos_tagger=tagger)
		print blob.tags
		
		print m.raw_parse(sent)
		print '...'


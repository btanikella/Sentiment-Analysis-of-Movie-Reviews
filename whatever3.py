from nltk.tokenize import sent_tokenize, word_tokenize
import os
from pprint import pprint
import re

path = './RSTParser/train_data'
files = [os.path.join(path, fname) for fname in os.listdir(path) if fname.endswith('.out')]

for fname in files[:1]:
	f= open(fname,'r')
	lines = f.readlines()
	f.close()
	out = open(fname.replace('out', 'processed'), 'w')

	wordToken=[]
	sentences=[]
	for l in lines:
		if 'Sentence #' in l:
			val =[]
			yo=[]
			nextIndex= lines.index(l)+1
			while not '[Text=' in lines[nextIndex]:
				value = lines[nextIndex]
				if '    ' in value:
					value = value.replace('    ','')
				val.append(value.split('\n')[0])
				yo.append(word_tokenize(value.split('\n')[0]))
				nextIndex+=1
			wordToken.append(yo)
			sentences.append(val)
	# pprint(sentences)

	parsesD=[]
	for l in lines:
		if 'Sentence #' in l:
			parses=[]
			nextIndex = lines.index(l)+2
			while not 'ROOT' in lines[nextIndex]:
				nextIndex+=1
			while not lines[nextIndex]=='\n':
				value = lines[nextIndex]
				parses.append(value.split('\n')[0])
				nextIndex+=1
			parsesD.append(parses)
	# pprint(parsesD)

	#Get tokens
	def process_token(token):
		o = {}
		for tok in token.split():
			k,v = tok.split('=')
			o[k] = v
		return o


	tokensD = []
	for l in lines:
		if 'Text=' in l:
			tokens = re.findall(r'\[([^]]*)\]', l)
			processed_toks = [ process_token(t) for t in tokens ]
			tokensD.append( processed_toks )
	# pprint(tokensD)

	# for i in range(len(tokensD)):
	# 	print len( tokensD[i]), len(word_tokenize(' '.join(sentences[i])) ) 
	print word_tokenize('This is (U.S.A.).')
	
	for sent_edus in sentences:
		range_to_edu = { }
		i = 0
		for edu in sent_edus:
			pass

		head_words = { i:[] for i in range(len(sent_edus) ) }




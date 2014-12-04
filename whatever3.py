from nltk.tokenize import sent_tokenize, word_tokenize
import os
from pprint import pprint
import re
import string
import nltk

path = './RSTParser/examples'
files = [os.path.join(path, fname) for fname in os.listdir(path) if fname.endswith('.out')]

for fname in files:
	f= open(fname,'r')
	lines = f.readlines()
	f.close()

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
			k,v = tok.split('=', 1)
			o[k] = v
		return o


	tokensD = []
	for l in lines:
		if 'Text=' in l:
			tokens = re.findall(r'\[([^]]*)\]', l)
			processed_toks = [ process_token(t) for t in tokens ]
			tokensD.append( processed_toks )
	# pprint(tokensD)

	
	edu_tokens = [] # list of sentences where each sentence is a list of edus broken into tokens
	pos_tags = []
	head_words = []

	for i,sent_edus in enumerate(sentences):
		# sent_edus [edu, edu, edu]
		
		processed_edus = [ [] for e in sent_edus ]
		range_to_edu = {}
		x = 0
		for j,edu in enumerate(sent_edus):
			r = ( x, min( x + len(word_tokenize(edu)), len(tokensD[i]) ) - 1 )
			x += len(word_tokenize(edu))
			range_to_edu[r] = j
		for r in range_to_edu:
			# pprint( sent_edus[range_to_edu[r]] )
			# pprint( tokensD[i][r[0]:r[1]] )
			processed_edus[range_to_edu[r]] = tokensD[i][r[0]:r[1]+1]
		edu_tokens.append(processed_edus)
		
		# find pos tags for sentence and chunk it into edus
		pos = []
		for edu in processed_edus:
			pos.append([ e['PartOfSpeech'] for e in edu ])
		pos_tags.append(pos)

		# pprint(processed_edus)
		# pprint(pos)

		# Find headwords in each edu
		heads = [ [] for e in sent_edus ]

		# pprint(parsesD[i])
		def get_range(idx, ranges):
			for r in ranges:
				# print idx, r[0], 'greater?',idx > r[0]
				# print idx, r[1], 'less?', idx < r[1]
				if idx >= r[0] and idx <= r[1] + 1:
					return r
					# print "returning ", r, 'for index', idx
				elif idx > max([x[1] for x in ranges]):
					# print '\nreturning ', max([x[1] for x in ranges]), idx
					return get_range(max([x[1] for x in ranges]), ranges)
			print 'failing for ', idx, ranges
			return 'fail'

		
		for p in parsesD[i]: #parsesD[i] is the parse of the sentence
			parse = p[p.find("(")+1:p.rfind(")")]
			a, b = parse.split(', ')
			parent, parent_index = a.rsplit('-',1)[0], int(a.rsplit('-',1)[1])
			word, word_index = b.rsplit('-',1)[0], int(b.rsplit('-',1)[1])
			# print parent, range_to_edu[get_range(parent_index, range_to_edu.keys())], word, range_to_edu[get_range(word_index, range_to_edu.keys())]

			if parent == 'ROOT' or get_range(word_index, range_to_edu.keys()) != get_range(parent_index, range_to_edu.keys()):
				if not( word in set(string.punctuation) or parent in set(string.punctuation) ):
					# print 'adding ...', word, parent
					heads[ range_to_edu[get_range(word_index, range_to_edu.keys())] ].append(word)
			
		# pprint(heads)
		head_words.append(heads)



	# Write data to files
	print "Writing POS and headwords for", fname
	posfile = open(fname.replace('.edus.out', '.pos'), 'w')
	for p in pos_tags:
		if len(p) == 0:
			posfile.write(' \n')
		for pe in p:
			posfile.write(' '.join(pe)
				.replace('.', '')
				.replace(',', '')
				.replace('``', '')
				.replace("''", '')
				.strip()+'\n')
	posfile.close()

	headfile = open(fname.replace('.edus.out', '.headwords'), 'w')
	for h in head_words:
		for he in h:
			headfile.write(' '.join(he).strip()+'\n')
	headfile.close()

	# posfile = open(fname.replace('.edus.out', '.pos2'), 'w')
	# for s in sentences:
	# 	for edu in s:
	# 		print edu
	# 		print nltk.pos_tag(edu)
	# 		pos = [t[1] for t in nltk.pos_tag(edu)]
	# 		# print pos
	# 		posfile.write(' '.join(pos)+'\n')
	# posfile.close()








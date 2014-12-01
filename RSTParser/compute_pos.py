from nltk.tokenize import sent_tokenize, word_tokenize
import os
from textblob import TextBlob
from textblob_aptagger import PerceptronTagger
import re
import pdb

path = './train_data'
files = [os.path.join(path, fname) for fname in os.listdir(path) if fname.endswith('.edus')]
tagger = PerceptronTagger()

for fname in files:
	f = open(fname, 'r')
	lines = f.readlines()
	text = ' '.join(lines)
	f.close()
	out = open(fname.replace('edus', 'pos'), 'w')

	for sent in sent_tokenize(text):
		blob = TextBlob(sent, pos_tagger=tagger)
		
		# clean sentence of extra spaces
		s = ' \n '.join(' '.join(line.split()) for line in sent.split('\n')).rstrip().split(' ')
		new_lines = [i for i, x in enumerate(s) if x == "\n"]
		
		if len(new_lines):
			chunks = [0] # indices for where to break the tag list
			for n in new_lines:
				start = n - 4 - len( new_lines[:new_lines.index(n)]) # start searching from this index in the sentence
				
				# find which word to compare it against. ignore non alpha numeric strings
				word = re.sub(r'\W+', '', s[n-1])
				k = 2
				while word == '':
					word = re.sub(r'\W+', '', s[n-k])
					k += 1

				# figure index at which to break the tag list
				for i in range(start, start + 8):
					if i >= 0 and i < len(blob.tags) and blob.tags[i][0] == word:
						chunks.append(i+1)
						break
					elif i >= 0 and i < len(blob.tags) and blob.tags[i][0] == s[n-1]:
						chunks.append(i+1)
						break
					else:
						print i, len(blob.tags), word, blob.tags[i][0], '... mismatch!'
			
			# print taglist chunks (or pos for edus)
			for i in range(len(chunks)):
				if i == len(chunks)-1:
					out.write( ' '.join( [t[1] for t in blob.tags[chunks[i]:]] ) + '\n' )
				else:
					out.write( ' '.join( [t[1] for t in blob.tags[ chunks[i]:chunks[i+1] ]] ) + '\n' )

		else: # No newlines, so no edus
			out.write( ' '.join(t[1] for t in blob.tags) + '\n' )
	
	out.close()
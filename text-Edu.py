from nltk.tokenize import sent_tokenize, word_tokenize
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

path = './sentiment-analysis/aclImdb/train/pos'

files = [os.path.join(path, fname) for fname in os.listdir(path) if fname.endswith('.txt')]

for fname in files:
	f = open(fname, 'r')
	lines = f.readlines()
	text = ' '.join(lines)
	f.close()
	out = open(fname.replace('txt', 'edu'), 'w')

	for sent in sent_tokenize(text):
		sentence = unicode(sent, errors='ignore')
		sentence = str(sentence)
		out.write('    '+sentence+'\n')

	out.close()




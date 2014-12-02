import os
import random

DATA_DIR = 'aclImdb/'
SAMPLE_DIR = 'data_sample/'

def generate_train_sample():
	data_files = {	'pos': [DATA_DIR + 'train/pos/' + f for f in os.listdir(DATA_DIR+'train/pos/') if 'edu' in f], 
					'neg': [DATA_DIR + 'train/neg/' + f for f in os.listdir(DATA_DIR+'train/neg/') if 'edu' in f]}
	random.shuffle(data_files['pos'])
	random.shuffle(data_files['neg'])
	train_sample = data_files['pos'][:10] + data_files['neg'][:10]
	test_sample = data_files['neg'][100:110] + data_files['pos'][100:110]
	for filename in (train_sample):
		label = 'pos' if 'pos' in filename else 'neg'
		f = open(filename, 'r')
		w = open(SAMPLE_DIR + 'train/' + label + filename[filename.rfind('/'):] + 's', 'w')
		text = f.read()
		w.write(text)
		f.close()
		w.close()
		print "Created training sample"
	for filename in (test_sample):
		label = 'pos' if 'pos' in filename else 'neg'
		f = open(filename, 'r')
		w = open(SAMPLE_DIR + 'test/' + label + filename[filename.rfind('/'):] + 's', 'w')
		text = f.read()
		w.write(text)
		f.close()
		w.close()
		print "Created test sample"

generate_train_sample()

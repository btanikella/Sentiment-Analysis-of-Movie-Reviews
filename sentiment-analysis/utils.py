import os
import random
import shutil
from HTMLParser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

stripper = MLStripper() # ;)

DATA_DIR = './aclImdb/'
SAMPLE_DIR = './data_sample/'

def generate_train_sample(numtrain, numtest):
	#remove existing dataset and create new dirs
	shutil.rmtree(SAMPLE_DIR + 'test/neg/')
	shutil.rmtree(SAMPLE_DIR + 'test/pos/')
	shutil.rmtree(SAMPLE_DIR + 'train/neg/')
	shutil.rmtree(SAMPLE_DIR + 'train/pos/')

	os.mkdir( SAMPLE_DIR + 'test/neg' )
	os.mkdir( SAMPLE_DIR + 'test/pos' )
	os.mkdir( SAMPLE_DIR + 'train/neg' )
	os.mkdir( SAMPLE_DIR + 'train/pos' )

	# locate large dataset to sample from
	train_files = {	'pos': [DATA_DIR + 'train/pos/' + f for f in os.listdir(DATA_DIR+'train/pos/') if 'edu' in f], 
					'neg': [DATA_DIR + 'train/neg/' + f for f in os.listdir(DATA_DIR+'train/neg/') if 'edu' in f]}

	test_files = {	'pos': [DATA_DIR + 'test/pos/' + f for f in os.listdir(DATA_DIR+'test/pos/') if 'edu' in f], 
					'neg': [DATA_DIR + 'test/neg/' + f for f in os.listdir(DATA_DIR+'test/neg/') if 'edu' in f]}

	random.shuffle(train_files['pos'])
	random.shuffle(train_files['neg'])
	random.shuffle(test_files['pos'])
	random.shuffle(test_files['neg'])

	# sample training and test data files
	train_sample = train_files['pos'][:numtrain/2] + train_files['neg'][:numtrain/2]
	test_sample = test_files['neg'][:numtest/2] + test_files['pos'][:numtest/2]

	# create data from data files
	def copy_data(sample, destination):
		for filename in sample:
			label = 'pos' if 'pos' in filename else 'neg'
			f = open(filename, 'r')
			w = open(destination + label + filename[filename.rfind('/'):] + 's', 'w')
			text = f.read()
			w.write(text)
			f.close()
			w.close()
		print "Wrote", len(sample), "files to ", destination

	copy_data(train_sample, SAMPLE_DIR + 'train/')
	copy_data(test_sample, SAMPLE_DIR + 'test/')


def clean_text(html):
	stripper.feed(html)
	return stripper.get_data()

if __name__ == '__main__':
	num_train = 4000
	#generate_train_sample(num_train, int(0.1*num_train))

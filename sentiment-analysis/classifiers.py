from collections import defaultdict
import operator

class Perceptron():

	def __init__(self, labels):
		self.weights = defaultdict(float)
		self.labels = labels


	def classify(self, instance):
		argmax = lambda x : max(x.iteritems(),key=operator.itemgetter(1))[0]
		scores = {l:0 for l in self.labels}
		for y in self.labels:
			for f in instance:
				scores[y] += instance[f] * self.weights[(y, f)]
		# return the highest-scoring label, and the scores for all labels
		return argmax(scores)


	def predict(self, instance, weights, labels):
		argmax = lambda x : max(x.iteritems(),key=operator.itemgetter(1))[0]
		scores = {l:0 for l in labels}
		for y in labels:

			for f in instance:
				scores[y] += instance[f] * weights[(y, f)]
		# return the highest-scoring label, and the scores for all labels
		return argmax(scores), scores


	def oneItAvgPerceptron(self,inst_generator, weights, wsum, labels, t=0):
	    tr_err = 0
	    for i,(counts,label) in enumerate(inst_generator):
	        # your code here
	        prediction, s = self.predict(counts, weights, labels)
	        if prediction != label:
	            tr_err += 1
	            for word in counts:
	                wsum[ (label, word) ] += (t+i)*counts[word]
	                wsum[ (prediction, word) ] -= (t+i)*counts[word]
	                weights[ (label, word) ] += counts[word]
	                weights[ (prediction, word) ] -= counts[word]
	    return weights, wsum, tr_err, i

	
	def train(self, N_its, inst_generator, labels):
	    tr_acc = [None]*N_its
	    wsum = defaultdict(float)
	    delta_t = defaultdict(float)
	    T = 0.0
	    for i in xrange(N_its):
	        # You will define oneItAvgPerceptron below. Call it here.
	        self.weights,wsum,tr_err,tr_tot = self.oneItAvgPerceptron(inst_generator,self.weights,wsum,labels,T)
	        T += tr_tot
	        # When you are done with this training pass, compute the averaged weights, as shown above.
	        avg_weights = defaultdict(float)
	        for w in self.weights:
	            avg_weights[w] = self.weights[w] - wsum[w]/T
	        
	        tr_acc[i] = 1. - tr_err/float(tr_tot)
	        print i, 'train:',tr_acc[i]
	    return self.weights, tr_acc

	




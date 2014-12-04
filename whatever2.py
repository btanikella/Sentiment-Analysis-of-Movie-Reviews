from nltk.tokenize import sent_tokenize, word_tokenize
import os


path = './RSTParser/train_data'
files = [os.path.join(path, fname) for fname in os.listdir(path) if fname.endswith('.out')]


for fname in files:
	f= open(fname,'r')
	lines = f.readlines()
	f.close()
	out = open(fname.replace('out', 'processed'), 'w')

	sentenceList=[]
	for l in lines:
		if '[Text=' not in l:
			val = ()
			if 'Sentence #' in l:
				sentenceList.append(lines[lines.index(l)+1].split('\n')[0])
			if '    ' in l:
				sentenceList.append(l.split('\n')[0])


	wordToken=[]
	helloWorld=[]
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
			helloWorld.append(val)


	def makeWord(val):
		word=''
		for i in list(val):
			if i == '-':
				break;
			else: 
				word= word+i
		return word


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

	headWords=[]
	for i in range(len(helloWorld)):
		parse = parsesD[i]
		for edu in helloWorld[i]:
			headWord=''
			for value in parse:
				if 'ROOT' in value:
					word = word_tokenize(value)[4]
					if word in edu:
						headWord=word
						break;
				if headWord=='':
					for word in word_tokenize(edu):
						if len(word_tokenize(edu))==1:
							headWord=word
						else:
							if not 'ROOT' in (word_tokenize(value)[2]):
								if makeWord(word_tokenize(value)[2]) not in edu and word ==makeWord(word_tokenize(value)[4]):
									if not word ==',':
										headWord= word
			if headWord == '':
				headWord = 'a'
		
			headWords.append(headWord)

	for value in headWords:
		out.write( '    '+value + '\n' )

	out.close()

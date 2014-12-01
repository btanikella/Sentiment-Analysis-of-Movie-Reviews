from nltk.tokenize import sent_tokenize, word_tokenize

fname = 'RSTParser/examples/wsj_0600.out.edus.out.header'

f= open(fname,'r')
lines = f.readlines()
f.close()

sentenceList=[]
for l in lines:
	if '[Text=' not in l:
		val = ()
		if 'Sentence #' in l:
			val
			sentenceList.append(lines[lines.index(l)+1].split('\n')[0])
		if '    ' in l:
			sentenceList.append(l.split('\n')[0])

helloWorld=[]
for l in lines:
	if 'Sentence #' in l:
		val =[]
		nextIndex= lines.index(l)+1
		while not '[Text=' in lines[nextIndex]:
			value = lines[nextIndex]
			if '    ' in value:
				value = value.replace('    ','')
			val.append(value.split('\n')[0])
			nextIndex+=1
		helloWorld.append(val)

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

print len(parsesD)

parentLess=[]
words=[]

j=0
for j in range(len(parsesD)):
	parentList=[]
	for edu in helloWorld[j]:
		for val in parsesD[j]:
			if 'ROOT' not in val:
				parentList.append(word_tokenize(val)[2])
		for val in parentList:
			valss=[]
			word=''
			for i in list(val):
				if i == '-':
					break;
				else: 
					word= word+i
			for values in parsesD[j]:

				if word not in edu and word_tokenize(values)[2]==val:
					a=''
					for ik in list(word_tokenize(values)[4]):
						if ik == '-':
							break;
						else: 
							a= a+ik
					valss.append(a)
	words.append(valss)
	j+=1

print words
rootValues=[]
for l in lines:
	if 'ROOT' in l:
		rootValues.append(word_tokenize(l)[4])


value=[]
for val in rootValues:
	temp=[]
	for l in lines:
		if val in l and word_tokenize(l)[2]==val:
			temp.append(word_tokenize(l)[4])
	value.append(temp)

print value


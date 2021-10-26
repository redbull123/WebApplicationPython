def enumPair(outPut,keyWord,keyWord2,num):
	outCC = "@"
	aux = ""
	proc = "0"
	aux2 = ""
	for line in outPut.split("@"):
		for word in line.split():
			if aux == keyWord:
				if word != "=":
					aux = "."
					if word == num:
						proc = "1"
			elif proc == "1":
				if aux2 == keyWord2:
					if word != "=":
						outCC = outCC + word + "@"
						proc = "0"
						aux2 = "."
				elif word == keyWord2:
					aux2 = word
			elif word == keyWord:
				aux = word
	return outCC
def enumPairSC(outPut,keyWord,keyWord2,num,num2):
	outCCAux = "@Cause code"
	outCC = "@"
	aux = ""
	proc = "0"
	aux2 = ""
	aux3 = ""
	for line in outPut.split("@"):
		for word in line.split():
			if aux == keyWord:
				if word != "=":
					if word == num:
						aux = "."
						proc = "1"
			elif proc == "1":
				if aux2 == "cause_code":
					if word != "=":
						outCCAux = word + "@"
						aux2 = "."
				if aux3 == keyWord2:
					if word != "=":
						if word == num2:
							outCC = outCC + outCCAux + "@"
							aux3 = "."
							proc = "0"
				elif word == "cause_code":
					aux2 = word
				elif word == keyWord2:
					aux3 = word
			elif word == keyWord:
				aux = word
	return outCC
def enumCC(outPut,keyWord):
	outCC = "@"
	aux = ""
	for line in outPut.split("@"):
		for word in line.split():
			if aux == keyWord:
				if word != "=":
					outCC = outCC +word + "@"
					aux = "."
			elif word == keyWord:
				aux = word
	return outCC

def alreadyCounter(palabras,word):
	outP = "nc"
	for ep in palabras.split("@"):
		if ep == word:
			outP = "c"
			break
	return outP

def contarCC(numberCC,keyWord):
	cantCC = "@"
	palabras = "@"
	for word in numberCC.split("@"):
		counter = 0
		outP = alreadyCounter(palabras, word)
		if  outP == "nc":
			for word2 in numberCC.split("@"):
				if word == word2:
					counter = counter + 1
				else : 
					continue
			palabras = palabras +"@" + word
			cantCC = cantCC + keyWord+ " "+ word + " cantidad : "+str(counter)+"@"
		elif outP == "c":
			continue
	return cantCC

def deleteEqual(cantCC):
	paragraph = "@"
	for word in cantCC.split("@"):
		addCC = "0"
		for word2 in paragraph.split("@"):
			if word == word2:
				addCC = "0"
				break
			else:
				addCC = "1"
		if addCC == "1" :
			paragraph = paragraph + word + "@"
	return paragraph

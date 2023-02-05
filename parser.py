import sys
import nltk
import re

gr = nltk.data.load(sys.argv[1])

fileName = sys.argv[2]
sentences = open(fileName, 'r')

#retrieve all productions in grammar with given rhs values
def getLHS(rhs1, rhs2):
	prods = []
	for p in gr.productions():
		if p.rhs()[0] == rhs1 and p.rhs()[1] == rhs2:
			prods.append(p)
	return(prods)

for line in sentences:
	line = line.strip()
	print(line) #print line to output
	#separate out any ? . , into its own token
	line = line.replace('?', ' ? ').replace('.', ' . ').replace(',', ' , ')
	line = re.sub(' +', ' ', line)
	line = line.strip()
	
	#split on spaced to get tokens in sentence
	words = line.split(' ')

	#matrix for building the parses
	matrix = [[[] for i in range(len(words) + 1)] for j in range(len(words) + 1)]
	
	#parse the sentence according to CKY algorithm
	for j in range(1, len(words) + 1):
		lex = gr.productions(rhs=words[j-1]) #get all nonterminals for the current word
		nts = []
		for p in lex:
			nts.append([p.lhs(), words[j-1]]) #build lists of nonterminal and word
		matrix[j-1][j] = nts #store lists in cell
		for i in range(j-2, -1, -1):
			cell = [] #values to add to cell
			for k in range(i+1, j):
				value1 = matrix[i][k] #lists containing possible values of first rhs
				rhs1 = []
				for v1 in value1: 
					rhs1.append(v1[0]) #get possible values of first rhs
				value2 = matrix[k][j] #lists containing possible values of second rhs
				rhs2 = []
				for v2 in value2:
					rhs2.append(v2[0]) #get possible values of second rhs
				prods = []
				for n in range (0, len(rhs1)):
					for m in range (0, len(rhs2)): #look at all possible rhs combinations
						prods = getLHS(rhs1[n], rhs2[m]) #all rules that have this rhs 
						if prods:
							for p in prods:
								parse = [p.lhs()] #build list of new parse starting with lhs
								parse.append(value1[n]) #add first rhs value to parse
								parse.append(value2[m]) #add second rhs value to parse
								cell.append(parse) #add parse to cell list
							
			matrix[i][j] = cell #place cell values in matrix
	
	#format parses for output	
	#because parses are stored in matrix as lists, they are formatted with [] and ' ' when printed as string
	#the string representations of lists are formatted with () instead for the output	
	accepted = []
	for p in matrix[0][len(words)]:
		if p[0] == gr.start() and p not in accepted:
			accepted.append(p) #get all accepted parses
	for parse in accepted:
		parsestr = str(parse) #to format parses
		parsestr = parsestr.replace('\',\'', 'COMMA') #replace all comma tokens in original sentence with placeholder
		parsestr = parsestr.replace('[', '(').replace(']', ')') #replace all square brackets with parenthesis
		parsestr = parsestr.replace('\'', '').replace(',', '') #remove all apostrophes and comma not in original sentence
		parsestr = parsestr.replace('COMMA', ',') #put back comma from original sentence
		print(parsestr) 

	print('Number of parses: ' + str(len(accepted)) + '\n')


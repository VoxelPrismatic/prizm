import nltk
import re
import pprint
import random
import sys
import getopt
import glob

table = {}
lineCount = 0;wordCount = 0;keyLen = 1;maxWordInSentence = 20;genNSentences = 5

arg = {}

def checkargs():
	global keyLen, maxWordInSentence, genNSentences
	if len(sys.argv) < 3:
		print( "Usage: " + sys.argv[0] + " -k <Key lenth> -w <sentence word length> -n <sentences to generate> -f <files>")
		exit(0)
	else:
		arg = {}
		options = getopt.getopt(sys.argv[1:], 'k:w:n:f:')
		for item in options[0]:
			if(item): arg[ item[0] ] = item[1]
		pprint.pprint(arg)

		keyLen = int(arg[ '-k'])
		maxWordInSentence = int(arg[ '-w'])
		genNSentences = int(arg[ '-n' ])
		print(arg['-f'])
def readWestWingFile(filename,  fileEncoding="utf-8"):
	prevword = "";
	fullline = ""
	with  open(filename, "r", encoding=fileEncoding) as file:
		bartletLineActive = False
		for line in file:
			if not line.strip():
				bartletLineActive = False
				if fullline: processSection( re.sub(r"\[.+\]","",fullline ) );fullline = ""
				continue
			elif "BARTLET" in line: bartletLineActive = True; fullline = ""
			elif bartletLineActive:fullline = fullline + " " + line.strip()
		if fullline: processSection( re.sub(r"\[.+\]","",fullline ) )

#Text is just the one person
def readGenericFile(filename, fileEncoding="utf-8"):
	with open(filename, "r", encoding=fileEncoding) as file: processSection(" ".join(file))


def processSection(line ):
	global lineCount, wordCount, table, keyLen
	sent_text = nltk.sent_tokenize(line) # this gives us a list of sentences

	for sentence in sent_text:
		lineCount += 1; cleanStr = sentence
		tokens = cleanStr.split(); keyList = [ ];
		table.setdefault( '#BEGIN#', []).append(tokens[0:keyLen]);
		for item in tokens:
			if len(keyList) < keyLen: keyList.append(item); continue
			table.setdefault( tuple(keyList), []).append(item)
			keyList.pop(0); keyList.append(item)
			wordCount += 1


def generate():
	global table, maxWordInSentence

	key = list(random.choice(  table['#BEGIN#'] ))
	genStr = " ".join( key )
	for _ in range( maxWordInSentence ):
		newKey = table.setdefault( tuple(key), "") 
		if(newKey == ""): break
		newVal = random.choice( newKey )
		genStr = genStr + " " + newVal
		key.pop(0); key.append(newVal)
	print("::"+ genStr)

def main():
	global lineCount, wordCount, genNSentences
	checkargs()
	seasonList = ( [1, 22], [2, 22], [3, 21], [4, 22] )
	for season in seasonList:
		seasonNo = season[0]
		for episodeNo in range(1, season[1]+1): filename = "tww-" + str(seasonNo) + "-" + str(episodeNo).zfill(2) + ".txt"

	fileList = []; fileList = glob.glob("eddie*.txt"); fileList = fileList + glob.glob("Obama*.txt") 
	print(fileList)
	for file in fileList: readGenericFile(file, "utf-8")
	print( "lines: " + str(lineCount),'\n',"total words: " + str(wordCount) )
	
	markovDictFile=open('markovdictfile.txt', 'w')
	pprint.pprint(table,markovDictFile)

	for _ in range( genNSentences ):generate()

if __name__ == "__main__": main()
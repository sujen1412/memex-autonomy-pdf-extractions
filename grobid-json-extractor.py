import xmltodict
import json
import sys
import os
import pprint	

def main(inputPath, outputPath, batchMode):
	if(batchMode):
		if(os.path.isdir(inputPath) == False):
			print("Path %s is not a directory"%(inputPath))
			exit()
		
		else:
			print("Processing directory: %s"%(inputPath))
			for f in os.listdir(inputPath):
				inputFile = inputPath + f
				if "references.tei.xml" in f or ".json" in f or "bak" in f:
					print("Skipping "+inputFile)
					continue
				
				extractJsonFromFile(inputFile)
				print("\n")
	else:
		extractJsonFromFile(inputPath)


def extractJsonFromFile(inputFile):
	print("Processing Header File: %s"%(inputFile))
	jsonObject = convertXmlToJson(inputFile)
	inputFile_ref = inputFile[:inputFile.index('tei.xml')] + 'references' + inputFile[inputFile.index('.tei.xml'):]
	
	extractedJSON = {}
	extractedJSON['abstract'] = getAbstract(jsonObject)
	if extractedJSON['abstract'] == None:
		print("Null abstract")
		return 

	extractedJSON['fileName'] = inputFile[inputFile.rindex("/")+1:inputFile.index('tei.xml')] + "pdf"
	# print(json.dumps(jsonObject, indent=2))
	
	# print("Title: ")
	extractedJSON['title'] = getTitle(jsonObject)
	# print("Authors: ")
	extractedJSON['authors'] = getAuthors(jsonObject)
	# print("Abstract: ")
	
	# print("Publication: ")
	extractedJSON['publication'] = getPublicationDate(jsonObject)
	# print("References: ")
	outputFile = inputFile[:inputFile.index('tei.xml')] + "json"
	# print(json.dumps(extractedJSON, indent=2))
	print("Processing reference file: "+inputFile_ref)
	if(os.path.isfile(inputFile_ref)):
		jsonObject_ref = convertXmlToJson(inputFile_ref)
		extractedJSON['references'] = getReferences(jsonObject_ref)
	else:
		print("Could not find " + inputFile_ref)
	writeToFile(extractedJSON, outputFile)
	
	
	# prettyPrint(extractedJSON)

def writeToFile(jsonObject, outputFile):
	print("Writing to output file " + outputFile)
	f = open(outputFile, 'w')
	f.write(json.dumps(jsonObject, ensure_ascii=False).encode('utf8'))
	f.close()

def convertXmlToJson(inputFile):
	
	try:
		document_file = open(inputFile, "r") # Open a file in read-only mode
		original_doc = document_file.read()
		jsonOutput = xmltodict.parse(original_doc)
		return jsonOutput['TEI']
	except:
		print("Error occured while extracting data")
#returns a string
def getTitle(jsonObject):
	try:
		title = jsonObject['teiHeader']['fileDesc']['titleStmt']['title']
		# print(title)
		return title
	except:
		print("Error occured while extracting title")

#returns a JSON object of authors and affiliations if present  
def getAuthors(jsonObject):
	try:	
		authors = jsonObject['teiHeader']['fileDesc']['sourceDesc']['biblStruct']['analytic']['author']
		# prettyPrint(authors)
		return authors
	except:
		print("Error occured while extracting authors")

def getAbstract(jsonObject):
	try:	
		abstract = jsonObject['teiHeader']['profileDesc']['abstract']['p']
		# prettyPrint(abstract)
		return abstract
	except:
		print("Error occured while extracting abstract")

def getPublicationDate(jsonObject):
	try:		
		publication = jsonObject['teiHeader']['fileDesc']['publicationStmt']
		# prettyPrint(publication)
		return publication
	except:
		print("Error occured while extracting publication info")

def getReferences(jsonObject):
	try:
		references = jsonObject['text']['back']['listBibl']
		# prettyPrint(references)
		return references
	except:
		print("Error extracting references")
	
def printKeys(jsonObject):
	for key in jsonObject:
		# print(jsonObject.keys())
		printKeys(jsonObject[key])

def prettyPrint(obj):
	pp = pprint.PrettyPrinter(indent=1)
	pp.pprint(obj)

if __name__ == '__main__':
	
	arg_len = len(sys.argv)
	if(arg_len<3):
		print("Usage: inputPath outputDir [--options]")
		print("options: \n \t--batchMode = to run the extractor on a directory of files")
		exit()

	inputPath = sys.argv[1]
	outputPath = sys.argv[2]
	options = False
	if(arg_len > 3):
		options = True
	print("Setting input %s output %s, options %s "%(inputPath, outputPath, options))
	main(inputPath, outputPath, options)
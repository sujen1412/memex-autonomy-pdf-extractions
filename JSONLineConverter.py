import sys
import os
import json
import codecs 

def main(input_dir):
	output_file = codecs.open(input_dir+"output.jsonl",'w', 'utf-8')
	for f in os.listdir(input_dir):
		if ".json" in f:
			data_file = codecs.open(input_dir+ f,'r', 'utf-8')
			json_data = data_file.read()
			output_file.write(json_data+"\r\n")
	output_file.close()
			

if __name__ == '__main__':
	if(len(sys.argv)<2):
		print("Usage <input_dir>")
		exit()
	input_dir = sys.argv[1]
	if(os.path.isdir(input_dir) == False):
		print("% is not a directory"%(input_dir))
		exit()

	main(input_dir)
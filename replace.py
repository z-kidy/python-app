import sys

def file_replace(filename,pre,replce):
	input_file = open( filename ,'r').read()
	input_file=  input_file.replace(pre,replce)
	open(filename,"w").write(input_file)

lenth = len(sys.argv)

for i in range(1,lenth-2) :
	print sys.argv[i]
	file_replace( sys.argv[i] , sys.argv[-2] , sys.argv[-1] )


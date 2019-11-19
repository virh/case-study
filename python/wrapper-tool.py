#!/usr/bin/env python
import sys, getopt, os

def main(argv):
	baseDir = ''
	statusFile = ''
	statusCell = ''
	sprintArg = ''
	
	try:
		opts, args = getopt.getopt(argv,":h:f:s:",["dir=","sprint="])
	except getopt.GetoptError:
		print('wrapper-tool.py --dir=<dir> --sprint=<sprint> -f <filename> -s <sheetname>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('wrapper-tool.py --dir=<dir> --sprint=<sprint> -f <filename> -s <sheetname>')
			sys.exit()
		elif opt == '--dir':
			baseDir = arg
		elif opt == '--sprint':
			sprintArg = arg				
		elif opt in ("-f"):
			statusFile = arg
		elif opt in ("-s"):
			statusSheet = arg		
	if (not statusFile) or (not statusSheet):
		print("Usage: wrapper-tool.py --dir=<dir> --sprint=<sprint> -f <filename> -s <sheetname>")
		return
	print('Status file is ', statusFile)
	print('Status sheet is ', statusSheet)			
	print('Sprint arg is ', sprintArg)		
	if not baseDir:
		basepath = '.'
	else:
		basepath = baseDir
	
	print('begin backlog-status-format.py ...')					
	os.system('python backlog-status-format.py --dir="' + basepath + '"')
	print('begin backlog-status-check.py ...')	
	os.system('python backlog-status-check.py --dir="' + basepath + '"')
	print('begin backlog-copy.py ...')		
	os.system('python backlog-copy.py --dir="' + basepath + '"')
	print('begin report-status-calculate.py ...')
	os.system('python report-status-calculate.py --dir="' + basepath + '" --sprint=' + sprintArg + ' -f "' + statusFile + '" -s "' + statusSheet + '"')
	print('finish!')
	return

	
if __name__ == "__main__":
   main(sys.argv[1:])
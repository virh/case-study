#!/usr/bin/env python
import sys, getopt, os
import win32com.client
from win32com.client import Dispatch
import time
from datetime import date

def main(argv):
	baseDir = ''
	currDir = '.'
	logpath = currDir + '/logs/'
	if not os.path.exists(logpath):
		os.makedirs(logpath)	

	try:
		opts, args = getopt.getopt(argv,":h:",["dir="])
	except getopt.GetoptError:
		print('backlog-status-hide.py --dir=<dir>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('backlog-status-hide.py --dir=<dir>')
			sys.exit()
		elif opt == '--dir':
			baseDir = arg

	if not baseDir:
		basepath = '.'
	else:
		basepath = baseDir

	#print('Base dir is ', baseDir)		
	excel = win32com.client.Dispatch('Excel.Application')
	hideCount = 0
	
	f = open(os.path.join(logpath, "backlog-status-hidelog.txt"),"w+")
	try:
		excludeFile = open(os.path.join(currDir, "exclude.txt"))
		excludeContent = excludeFiles(excludeFile)
	except IOError:
		excludeContent = []
			
	log(f, '=========Begin hide files=========')
	for entry in os.listdir(basepath):
		if os.path.isfile(os.path.join(basepath, entry)) and 'xlsx'==os.path.splitext(entry)[1][1:]:
			if entry.startswith('~$'):
				continue			
			if entry in excludeContent:
				log(f, '[' + entry + '] exclude')
				continue			
			#print(entry)
			filename = os.path.join(basepath, entry)
			print(os.path.abspath(filename))
			
			#excel.Visible = True
			wb = excel.Workbooks.Open(os.path.abspath(filename))
			try:
				ws = wb.Worksheets('Team Backlog')		
			except:
				continue
			allData = ws.UsedRange
			
			# Get number of rows used on active sheet
			rowCount = allData.Rows.Count
			#print('Number of rows used in sheet : ',rowCount)

			#Get number of columns used on active sheet
			colCount = allData.Columns.Count
			#print('Number of columns used in sheet : ',colCount)
			
			#print(ws.AutoFilter.Filters(10).On)
			try:
				ws.UsedRange.AutoFilter(10,'=Open')
			except:
				log(f, 'File[' + filename + '] filter format error!')

			wb.Save()
			wb.Close()
			#log(f, 'Hide file[' + filename + '] end...')
			log(f, filename)
			hideCount += 1
	excel.Quit()
	excel = None
	log(f, '=========End check files=========')
	log(f, 'Totally hidden ' + str(hideCount) + ' files!')
	f.close()
	return

def log(file, message):
	file.write('{}'.format(message))
	file.write('\n')
	return	

def excludeFiles(file):
	content = file.readlines()
	content = [x.strip() for x in content] 
	return content
	
if __name__ == "__main__":
   main(sys.argv[1:])
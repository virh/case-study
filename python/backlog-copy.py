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
		print('backlog-copy.py --dir=<dir>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('backlog-copy.py --dir=<dir>')
			sys.exit()
		elif opt == '--dir':
			baseDir = arg

	if not baseDir:
		basepath = '.'
	else:
		basepath = baseDir

	#print('Base dir is ', baseDir)		
	excel = win32com.client.Dispatch('Excel.Application')
	updateCount = 0
	today = date.today()
	currentWeekNumber = today.isocalendar()[1]
	previousWeekNumber = currentWeekNumber-1
	year = today.strftime('%y')
	currentWeek = int(year + str(currentWeekNumber))
	previousWeek = int(year + str(previousWeekNumber))
	#print('Week number ', currentWeek, previousWeek)
	
	f = open(os.path.join(logpath, "updatelog.txt"),"w+")
	try:
		excludeFile = open(os.path.join(currDir, "exclude.txt"))
		excludeContent = excludeFiles(excludeFile)
	except IOError:
		excludeContent = []
			
	log(f, '=========Begin update files=========')
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
			
			writeData = wb.Worksheets('Team Backlog')
			#print('Update file[',filename,'] begin...')
			statusIndex = -1
			taskIndex = -1
			previousWeekIndex = -1
			currentWeekIndex = -1
			for col in range(1, colCount+1):
				if (taskIndex>-1 and statusIndex>-1 and previousWeekIndex>-1 and currentWeekIndex>-1):
					break
				if (taskIndex==-1 and ws.Cells(1, col).value=='Task Description'):
					taskIndex = col		
				if (statusIndex==-1 and ws.Cells(1, col).value=='Status'):
					statusIndex = col
				if (previousWeekIndex==-1 and ws.Cells(3, col).value and int(ws.Cells(3, col).value)==previousWeek):
					previousWeekIndex = col
					#print('previous week index ', previousWeekIndex)	
				if (currentWeekIndex==-1 and ws.Cells(3, col).value and int(ws.Cells(3, col).value)==currentWeek):
					currentWeekIndex = col
					#print('current week index ', currentWeekIndex)
			#print('Week index ', ws.Cells(81, 73).value)	
			for row in range(5, rowCount + 1):
				if(not ws.Cells(row, taskIndex).value):
					break
				#print('row index ', row)
				if(str(ws.Cells(row, statusIndex).value).lower()=='open'):
					tempPreviousIndex = statusIndex+1
					tempPreviousValue = ws.Cells(row, tempPreviousIndex).value
					while (tempPreviousIndex<previousWeekIndex):
						tempPreviousIndex = tempPreviousIndex+2
						currentValue = ws.Cells(row, tempPreviousIndex).value
						if(not currentValue):
							ws.Cells(row, tempPreviousIndex).value = tempPreviousValue
							#print('update row ', row, " week index ", tempPreviousIndex)	
						else:
							tempPreviousValue = currentValue
					previousValue = ws.Cells(row, previousWeekIndex).value
					#print('previousValue value ', previousValue)
					if (previousValue) and (not ws.Cells(row, currentWeekIndex).value):
						ws.Cells(row, currentWeekIndex).value = previousValue
						#print('cell value ', previousValue, ws.Cells(row, currentWeekIndex).value)

			wb.Save()
			wb.Close()
			#log(f, 'Update file[' + filename + '] end...')
			log(f, filename)
			updateCount += 1
	excel.Quit()
	excel = None
	log(f, '=========End update files=========')
	log(f, 'Totally updated ' + str(updateCount) + ' files!')
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
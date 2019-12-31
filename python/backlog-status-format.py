#!/usr/bin/env python
import sys, getopt, os
import win32com.client
from win32com.client import Dispatch
import time
from datetime import date
from datetime import timedelta

def main(argv):
	baseDir = ''
	currDir = '.'
	logpath = currDir + '/logs/'
	if not os.path.exists(logpath):
		os.makedirs(logpath)	

	try:
		opts, args = getopt.getopt(argv,":h:",["dir="])
	except getopt.GetoptError:
		print('backlog-status-format.py --dir=<dir>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('backlog-status-format.py --dir=<dir>')
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
	lastWeekDay = today - timedelta(days=7)
	currentWeekNumber = today.isocalendar()[1]
	previousWeekNumber = lastWeekDay.isocalendar()[1] 
	year = str(today.isocalendar()[0])[-2:]
	lastWeekYear = str(lastWeekDay.isocalendar()[0])[-2:]
	currentWeek = int(year + str(currentWeekNumber).zfill(2))
	previousWeek = int(lastWeekYear + str(previousWeekNumber).zfill(2))
	#print('Week number ', today.isocalendar(), currentWeek, previousWeek)
	
	f = open(os.path.join(logpath, "backlog-status-formatlog.txt"),"w+")
	try:
		excludeFile = open(os.path.join(currDir, "exclude.txt"))
		excludeContent = excludeFiles(excludeFile)
	except IOError:
		excludeContent = []
			
	log(f, '=========Begin format files=========')
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
			targetIndex = -1
			previousWeekIndex = -1
			currentWeekIndex = -1
			for col in range(1, colCount+1):
				if (taskIndex>-1 and targetIndex>-1 and statusIndex>-1 and previousWeekIndex>-1 and currentWeekIndex>-1):
					break
				if (taskIndex==-1 and ws.Cells(1, col).value=='Task Description'):
					taskIndex = col					
				if (targetIndex==-1 and ws.Cells(1, col).value=='Target Sprint'):
					targetIndex = col							
				if (statusIndex==-1 and ws.Cells(1, col).value=='Status'):
					statusIndex = col
				if (previousWeekIndex==-1 and ws.Cells(3, col).value and int(ws.Cells(3, col).value)==previousWeek):
					previousWeekIndex = col
					#print('previous week index ', previousWeekIndex)	
				if (currentWeekIndex==-1 and ws.Cells(3, col).value and int(ws.Cells(3, col).value)==currentWeek):
					currentWeekIndex = col
					#print('current week index ', currentWeekIndex)
			#print('Week index ', ws.Cells(81, 73).value)	
			row = 5
			while row < rowCount + 1:
				if(not ws.Cells(row, taskIndex).value):
					taskRangeCell = 'G' + str(int(row)) + ':G' + str(rowCount)
					if(excel.WorksheetFunction.CountA(ws.Range(taskRangeCell))):
						row = row + excel.WorksheetFunction.Match("*", ws.Range(taskRangeCell), 0) - 1
					else:
						break
				# reset target sprint
				ws.Cells(row, targetIndex).NumberFormat='0'
				ws.Cells(row, targetIndex).HorizontalAlignment=-4152 # right
				ws.Cells(row, targetIndex).VerticalAlignment=-4108 # center
				cellValue = ws.Cells(row, statusIndex).value		
				#print('row index ', row, 'cell value', cellValue)
				if(cellValue and str(cellValue).lower()=='closed'):
					ws.Cells(row, statusIndex).value='Closed'
				elif(cellValue and str(cellValue).lower()=='open'):
					ws.Cells(row, statusIndex).value='Open'
				elif(cellValue):
					ws.Cells(row, statusIndex).value='Open'
					log(f, 'row index ' + str(row) + '[' + cellValue + ']' + ' status format invaild rename to [Open]')
				else:
					ws.Cells(row, statusIndex).value='Open'
					log(f, 'row index ' + str(row) + '[None]' + ' status format invaild rename to [Open]')
				row += 1
				
			wb.Save()
			wb.Close()
			#log(f, 'Update file[' + filename + '] end...')
			log(f, filename)
			updateCount += 1
	excel.Quit()
	excel = None
	log(f, '=========End format files=========')
	log(f, 'Totally formated ' + str(updateCount) + ' files!')
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
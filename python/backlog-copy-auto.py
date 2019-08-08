#!/usr/bin/env python
import sys, getopt, os
import win32com.client
from win32com.client import Dispatch
import time
from datetime import date

def main(argv):
	baseDir = ''

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

	print('Base dir is ', baseDir)		
	excel = win32com.client.Dispatch('Excel.Application')
	updateCount = 0
	today = date.today()
	currentWeekNumber = today.isocalendar()[1]
	previousWeekNumber = currentWeekNumber-1
	year = today.strftime('%y')
	currentWeek = int(year + str(currentWeekNumber))
	previousWeek = int(year + str(previousWeekNumber))
	print('Week number ', currentWeek, previousWeek)
	
	f = open(os.path.join(basepath, "updatelog.txt"),"w+")
	log(f, '=========Begin update files=========')
	for entry in os.listdir(basepath):
		if os.path.isfile(os.path.join(basepath, entry)) and 'xlsx'==os.path.splitext(entry)[1][1:]:
			#print(entry)
			filename = os.path.join(basepath, entry)
			print(os.path.abspath(filename))
			
			#excel.Visible = True
			wb = excel.Workbooks.Open(os.path.abspath(filename))
			#try:
			ws = wb.Worksheets('Team Backlog')		
			#except:
				#continue
			allData = ws.UsedRange
			
			# Get number of rows used on active sheet
			rowCount = allData.Rows.Count
			print('Number of rows used in sheet : ',rowCount)

			#Get number of columns used on active sheet
			colCount = allData.Columns.Count
			print('Number of columns used in sheet : ',colCount)
			
			writeData = wb.Worksheets('Team Backlog')
			print('Update file[',filename,'] begin...')
			statusIndex = -1
			previousWeekIndex = -1
			currentWeekIndex = -1
			for col in range(1, colCount+1):
				if (statusIndex>-1 and previousWeekIndex>-1 and currentWeekIndex>-1):
					break
				if (statusIndex==-1 and ws.Cells(1, col).value=='Status'):
					statusIndex = col
				if (previousWeekIndex==-1 and ws.Cells(3, col).value and int(ws.Cells(3, col).value)==previousWeek):
					previousWeekIndex = col
					print('previous week index ', previousWeekIndex)	
				if (currentWeekIndex==-1 and ws.Cells(3, col).value and int(ws.Cells(3, col).value)==currentWeek):
					currentWeekIndex = col
					print('current week index ', currentWeekIndex)
			print('Week index ', ws.Cells(81, 73).value)	
			for row in range(5, rowCount + 1):
				if(ws.Cells(row, statusIndex).value=='Open'):
					previousValue = ws.Cells(row, previousWeekIndex).value
					if (not previousValue):
						 tempPreviousIndex = previousWeekIndex
						 tempPreviousValue = ws.Cells(row, previousWeekIndex-2).value
						 while (tempPreviousIndex>statusIndex) and (not tempPreviousValue):
								tempPreviousIndex = tempPreviousIndex-2
								tempPreviousValue = ws.Cells(row, tempPreviousIndex).value
						 while (tempPreviousIndex<previousWeekIndex) and tempPreviousValue:
						 		tempPreviousIndex = tempPreviousIndex+2
						 		ws.Cells(row, tempPreviousIndex).value = tempPreviousValue
						 previousValue = ws.Cells(row, previousWeekIndex).value
					print('previousValue value ', previousValue)
					if (previousValue) and (not ws.Cells(row, currentWeekIndex).value):
						ws.Cells(row, currentWeekIndex).value = previousValue
						print('cell value ', previousValue, ws.Cells(row, currentWeekIndex).value)

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
	
if __name__ == "__main__":
   main(sys.argv[1:])
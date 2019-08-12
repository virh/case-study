#!/usr/bin/env python
import sys, getopt, os
import win32com.client
from win32com.client import Dispatch
import time
from datetime import date

def main(argv):
	baseDir = ''
	statusFile = ''
	statusCell = ''

	try:
		opts, args = getopt.getopt(argv,":h:f:s:",["dir="])
	except getopt.GetoptError:
		print('report-status-calculate.py --dir=<dir> -f <filename> -s <sheetname>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('report-status-calculate.py --dir=<dir> -f <filename> -s <sheetname>')
			sys.exit()
		elif opt == '--dir':
			baseDir = arg
		elif opt in ("-f"):
			statusFile = arg
		elif opt in ("-s"):
			statusSheet = arg
	print('Status file is ', statusFile)
	print('Status sheet is ', statusSheet)			
	if (not statusFile) or (not statusSheet):
		print("Usage: report-status-calculate.py --dir=<dir> -f <filename> -s <sheetname>")
		return
			
	if not baseDir:
		basepath = '.'
	else:
		basepath = baseDir

	#print('Base dir is ', baseDir)		
	excel = win32com.client.Dispatch('Excel.Application')
	readCount = 0
	today = date.today()
	currentWeekNumber = today.isocalendar()[1]
	previousWeekNumber = currentWeekNumber-1
	year = today.strftime('%y')
	currentWeek = int(year + str(currentWeekNumber))
	previousWeek = int(year + str(previousWeekNumber))
	#print('Week number ', currentWeek, previousWeek)
	#statusFile = 'update-status.xlsx'
	#statusSheet = 'XFT Velocity'
	updateTeams = []
	
	f = open(os.path.join(basepath, "report-status-log.txt"),"w+")	
	
	log(f, '=========Begin read files=========')
	for entry in os.listdir(basepath):
		if os.path.isfile(os.path.join(basepath, entry)) and 'xlsx'==os.path.splitext(entry)[1][1:]:
			#print(entry, os.path.splitext(entry)[0].split('_')[-1])
			team = os.path.splitext(entry)[0].split('_')[-1]
			filename = os.path.join(basepath, entry)
			print(os.path.abspath(filename))
			
			#excel.Visible = True
			wb = excel.Workbooks.Open(os.path.abspath(filename))
			try:
				ws = wb.Worksheets('Report Status')		
			except:
				wb.Close(False)
				continue
			allData = ws.UsedRange
			
			# Get number of rows used on active sheet
			rowCount = allData.Rows.Count
			#print('Number of rows used in sheet : ',rowCount)

			#Get number of columns used on active sheet
			colCount = allData.Columns.Count
			#print('Number of columns used in sheet : ',colCount)
			
			#print('Update file[',filename,'] begin...')
			previousWeekIndex = -1
			currentWeekIndex = -1
			for col in range(1, colCount+1):
				if (previousWeekIndex>-1 and currentWeekIndex>-1):
					break
				if (previousWeekIndex==-1 and ws.Cells(4, col).value and int(ws.Cells(4, col).value)==previousWeek):
					previousWeekIndex = col
					#print('previous week index ', previousWeekIndex)	
				if (currentWeekIndex==-1 and ws.Cells(4, col).value and int(ws.Cells(4, col).value)==currentWeek):
					currentWeekIndex = col
					#print('current week index ', currentWeekIndex)
			#print('Week index ', ws.Cells(81, 73).value)	
			for row in range(5, rowCount + 1):
				if (ws.Cells(row, 1).value):
					previousValue = ws.Cells(row, previousWeekIndex).value
					if (previousValue==0):
						updateTeams.append(team)
						break		
			wb.Close(False)
			#log(f, 'Update file[' + filename + '] end...')
			log(f, filename)
			readCount += 1
	log(f, '=========End read files=========')
	log(f, 'Totally readed ' + str(readCount) + ' files!')	
	log(f, '=========Begin Status File=========')
	statusWb = excel.Workbooks.Open(os.path.abspath(statusFile))
	try:
		statusWs = statusWb.Worksheets(statusSheet)	
		for i in range(0, len(updateTeams)): 
			team = updateTeams[i]
			origin = decrement(statusWb, statusWs, team)
			log(f, team + ' origin value ' + str(origin))	
	except:
			log(f, 'Sheet name [' + statusSheet + '] invaild!')		
	log(f, '=========End Status File=========')
	statusWb.Close()
	excel.Quit()
	excel = None
	f.close()
	return

def log(file, message):
	file.write('{}'.format(message))
	file.write('\n')
	return	
	
def decrement(wb, ws, team):
	allData = ws.UsedRange
	rowCount = allData.Rows.Count
	colCount = allData.Columns.Count
	teamIndex = -1
	origin = -1
	for row in range(1, rowCount + 1):
		if (ws.Cells(row, 1).value and str(ws.Cells(row, 1).value).lower()==str(team).lower()):
			teamIndex = row
			print(team, ' rowIndex ', row)	
			break
	if (teamIndex>-1):
		for col in range(3, colCount + 1):
			scoreIndex = teamIndex+5
			origin = ws.Cells(teamIndex+5, col).value
			if (origin):
				ws.Cells(teamIndex+5, col).value = origin-1
				wb.Save()
				break
	return origin	
	
if __name__ == "__main__":
   main(sys.argv[1:])
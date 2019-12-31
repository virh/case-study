#!/usr/bin/env python
import sys, getopt, os
import win32com.client
from win32com.client import Dispatch
import time
from datetime import date
from datetime import timedelta

def main(argv):
	baseDir = ''
	statusFile = ''
	statusCell = ''
	currDir = '.'
	logpath = currDir + '/logs/'
	if not os.path.exists(logpath):
		os.makedirs(logpath)

	try:
		opts, args = getopt.getopt(argv,":h:f:s:",["dir="])
	except getopt.GetoptError:
		print('backlog-integrity-calculate.py --dir=<dir> -f <filename> -s <sheetname>')
		sys.exit(2)
	#print(opts)
	for opt, arg in opts:
		if opt == '-h':
			print('backlog-integrity-calculate.py --dir=<dir> -f <filename> -s <sheetname>')
			sys.exit()
		elif opt == '--dir':
			baseDir = arg		
		elif opt in ("-f"):
			statusFile = arg
		elif opt in ("-s"):
			statusSheet = arg		
	if (not statusFile) or (not statusSheet):
		print("Usage: backlog-integrity-calculate.py --dir=<dir> -f <filename> -s <sheetname>")
		return
	print('Status file is ', statusFile)
	print('Status sheet is ', statusSheet)	
	if not baseDir:
		basepath = '.'
	else:
		basepath = baseDir

	#print('Base dir is ', baseDir)		
	excel = win32com.client.Dispatch('Excel.Application')
	#excel = win32com.client.gencache.EnsureDispatch('Excel.Application')
	readCount = 0
	today = date.today()
	lastWeekDay = today - timedelta(days=7)
	currentWeekNumber = today.isocalendar()[1]
	previousWeekNumber = lastWeekDay.isocalendar()[1] 
	year = str(today.isocalendar()[0])[-2:]
	lastWeekYear = str(lastWeekDay.isocalendar()[0])[-2:]
	currentWeek = int(year + str(currentWeekNumber).zfill(2))
	previousWeek = int(lastWeekYear + str(previousWeekNumber).zfill(2))
	#print('Week number ', today.isocalendar(), currentWeek, previousWeek)
	#statusFile = 'update-status.xlsx'
	#statusSheet = 'XFT Velocity'
	updateTeams = []
	capacityTeams = {}
	remainTeams = {}
	
	f = open(os.path.join(logpath, "backlog-integrity-calculate-log.txt"),"w+")	
	try:
		excludeFile = open(os.path.join(currDir, "exclude.txt"))
		excludeContent = excludeFiles(excludeFile)
	except IOError:
		excludeContent = []
	
	log(f, '=========Begin read files=========')
	for entry in os.listdir(basepath):
		if os.path.isfile(os.path.join(basepath, entry)) and 'xlsx'==os.path.splitext(entry)[1][1:]:
			if entry.startswith('~$'):
				continue
			if entry in excludeContent:
				log(f, '[' + entry + '] exclude')
				continue
			#print(entry, os.path.splitext(entry)[0].split('_')[-1])
			#team = os.path.splitext(entry)[0].split('_')[-1]
			filename = os.path.join(basepath, entry)
			print(os.path.abspath(filename))
			
			#excel.Visible = True
			wb = excel.Workbooks.Open(os.path.abspath(filename))
			try:
				ws = wb.Worksheets('Capacity')		
				team = ws.Cells(1, 1).value	
			except:
				wb.Close(False)
				log(f, 'Sheet name [Capacity] invaild!')	
				continue			
			try:
				ws = wb.Worksheets('Report Status')		
			except:
				wb.Close(False)
				log(f, 'Sheet name [Report Status] invaild!')	
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
			for col in range(3, colCount+1):
				if (previousWeekIndex>-1 and currentWeekIndex>-1):
					break
				if (previousWeekIndex==-1 and ws.Cells(4, col).value and int(ws.Cells(4, col).value)==previousWeek):
					previousWeekIndex = col
					#print('previous week index ', previousWeekIndex)	
				if (currentWeekIndex==-1 and ws.Cells(4, col).value and int(ws.Cells(4, col).value)==currentWeek):
					currentWeekIndex = col
					#print('current week index ', currentWeekIndex)
			#previousWeekIndex=24
			step = 0
			while(ws.Cells(3, previousWeekIndex-step).value is None):
				step = step + 1
			sprintIndex = ws.Cells(3, previousWeekIndex-step).value
			sprintIndex = sprintIndex.replace("Sprint", today.strftime('%y'))
			#print(sprintIndex)
			for row in range(5, rowCount + 1):
				if (ws.Cells(row, 1).value):
					#print(ws.Cells(row, 1).value)
					formatColor = ws.Cells(row, previousWeekIndex).DisplayFormat.Interior.Color
					#print(formatColor)
					if (formatColor==255 and str(ws.Cells(row, 2).value).lower()=='active'):
						updateTeams.append(team)
						log(f, team + ' name [' + ws.Cells(row, 1).value + '] found not update backlog. ')	
						break		
			#print(updateTeams)			
						
			wb.Close(False)
			#log(f, 'Update file[' + filename + '] end...')
			log(f, filename)
			readCount += 1
			#return 	
	log(f, '=========End read files=========')
	log(f, 'Totally readed ' + str(readCount) + ' files!')	
	log(f, '=========Begin Status File=========')
	statusWb = excel.Workbooks.Open(os.path.abspath(statusFile))
	try:
		statusWs = statusWb.Worksheets(statusSheet)	
	except:
			log(f, sys.exc_info()[0])
			log(f, 'Sheet name [' + statusSheet + '] invaild!')		
	colIndex = fillDefaultScore(statusWb, statusWs, sprintIndex)
	for i in range(0, len(updateTeams)): 
		team = updateTeams[i]
		origin = decrement(statusWb, statusWs, team, colIndex)
		log(f, team + ' sprint ' + sprintIndex + ' origin value ' + str(origin))	
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
	
def decrement(wb, ws, team, colIndex):
	allData = ws.UsedRange
	rowCount = allData.Rows.Count
	colCount = allData.Columns.Count
	teamIndex = -1
	origin = -1
	for row in range(1, rowCount + 1):
		if (ws.Cells(row, 1).value and str(ws.Cells(row, 1).value).lower()==str(team).lower()):
			teamIndex = row
			#print(team, ' rowIndex ', row)	
			break
		if (ws.Cells(row, 1).value is None and ws.Cells(row, 2).value is None):
			break
	if (teamIndex>-1):
		scoreIndex = teamIndex+7
		origin = ws.Cells(scoreIndex, colIndex).value
		if (int(origin) > 0):
			ws.Cells(scoreIndex, colIndex).value = origin-1
			wb.Save()
	return origin	

def fillDefaultScore(wb, ws, sprintIndex):
	allData = ws.UsedRange
	rowCount = allData.Rows.Count
	colCount = allData.Columns.Count
	colIndex = -1
	for col in range(3, colCount + 1):
		#print(ws.Cells(1, col).value, sprintIndex)
		if (int(ws.Cells(1, col).value)==int(sprintIndex)):
			colIndex = col
			break
	#print(colIndex, sprintIndex)		
	for row in range(1, rowCount + 1):
		if (ws.Cells(row, 1).value):
			if (ws.Cells(row+7, colIndex).value is None):
				ws.Cells(row+7, colIndex).value = 3
		if (ws.Cells(row, 1).value is None and ws.Cells(row, 2).value is None):
			break
	wb.Save()
	return colIndex

def excludeFiles(file):
	content = file.readlines()
	content = [x.strip() for x in content] 
	return content
	
if __name__ == "__main__":
	 main(sys.argv[1:])
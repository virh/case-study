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
	sprintArg = ''
	currDir = '.'
	logpath = currDir + '/logs/'
	if not os.path.exists(logpath):
		os.makedirs(logpath)	

	try:
		opts, args = getopt.getopt(argv,":h:f:s:",["dir=","sprint="])
	except getopt.GetoptError:
		print('report-status-calculate.py --dir=<dir> --sprint=<sprint> -f <filename> -s <sheetname>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('report-status-calculate.py --dir=<dir> --sprint=<sprint> -f <filename> -s <sheetname>')
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
		print("Usage: report-status-calculate.py --dir=<dir> --sprint=<sprint> -f <filename> -s <sheetname>")
		return
	print('Status file is ', statusFile)
	print('Status sheet is ', statusSheet)			
	print('Sprint arg is ', sprintArg)	
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
	capacityTeams = {}
	remainTeams = {}
	
	f = open(os.path.join(logpath, "report-status-calculate-log.txt"),"w+")	
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
			if ( not sprintArg ):
				step = 0
				while(ws.Cells(3, previousWeekIndex-step).value is None):
					step = step + 1
				sprintIndex = ws.Cells(3, previousWeekIndex-step).value
				sprintIndex = sprintIndex.replace("Sprint", today.strftime('%y'))
			else:
				sprintIndex = str(sprintArg)
			#print(sprintIndex)		
			# store Capacity Available and Comitted
			try:
				ws = wb.Worksheets('Capacity')		
			except:
				log(f, 'Sheet name [Capacity] can not open!')	
			#print(ws.Cells(4, 1).NumberFormat)	
			#print(ws.Cells(4, 1).value)
			#ws.Cells(4, 1).NumberFormat='@' | '0_'
			ws.Cells(4, 1).value=sprintIndex
			capacityTeams[team]=["{0:.2f}".format(ws.Cells(19, 7).value),"{0:.2f}".format(ws.Cells(19, 8).value)]
			#ws.Cells(4, 1).value='1910'
			#capacityTeams[team+'back']=["{0:.2f}".format(ws.Cells(19, 7).value),"{0:.2f}".format(ws.Cells(19, 8).value)]
			#print(ws.Cells(19, 7).value)
			#print(ws.Cells(19, 8).value)
			#print(capacityTeams)
			
			# store Remain
			try:
				ws = wb.Worksheets('Team Backlog')		
			except:
				log(f, 'Sheet name [Team Backlog] can not open!')		
			allData = ws.UsedRange
			rowCount = allData.Rows.Count
			colCount = allData.Columns.Count
			statusIndex = -1
			taskIndex = -1
			targetIndex = -1
			sprintColIndex = -1
			sprintIndexStr = sprintIndex.replace(today.strftime('%y'), "Sprint", 1)
			for col in range(1, colCount+1):
				if (taskIndex>-1 and targetIndex>-1 and sprintColIndex>-1):
					break
				if (taskIndex==-1 and ws.Cells(1, col).value=='Task Description'):
					taskIndex = col					
				if (targetIndex==-1 and ws.Cells(1, col).value=='Target Sprint'):
					targetIndex = col		
				if (sprintColIndex==-1 and ws.Cells(2, col).value and str(ws.Cells(2, col).value)==sprintIndexStr):
					sprintColIndex = col
				#print('Spring col ', col, ws.Cells(3, col).value)
			#print('Task index ', taskIndex)		
			#print('Target index ', targetIndex)	
			#print('Sprint col index ', sprintColIndex)	
			
			remainSum = 0
			for row in range(5, rowCount + 1):
				if(not ws.Cells(row, taskIndex).value):
					break				
				if(not ws.Cells(row, sprintColIndex+6).value):
					continue
				if(ws.Cells(row, targetIndex).value and int(ws.Cells(row, targetIndex).value)<=int(sprintIndex)):
					remainSum += int(ws.Cells(row, sprintColIndex+6).value)
			#print('Remain sum is ', remainSum)
			remainTeams[team]=remainSum
			#print(remainTeams)
						
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
	storeCapacity(statusWb, statusWs, capacityTeams, remainTeams, sprintIndex)
	for item in capacityTeams.keys():
		log(f, item + ' capacity, commit and remain update success!')		
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

def storeCapacity(wb, ws, capacityTeams, remainTeams, sprintIndex):
	allData = ws.UsedRange
	rowCount = allData.Rows.Count
	colCount = allData.Columns.Count
	teamIndex = -1
	origin = -1
	for col in range(3, colCount + 1):
		#print(ws.Cells(1, col).value, sprintIndex)
		if (ws.Cells(1, col).value and int(ws.Cells(1, col).value)==int(sprintIndex)):
			sprintCol = col
			break
	for row in range(2, rowCount + 1):
		if (ws.Cells(row, 1).value):
			teamIndex = row
			team = ws.Cells(row, 1).value
			capacityIndex = teamIndex
			commitmentIndex = teamIndex+1
			remainIndex = teamIndex+2
			#print(capacityTeams)
			#print(team)
			#print(capacityTeams.get(team))
			if (capacityTeams.get(team) is not None):
				ws.Cells(capacityIndex, sprintCol).value = capacityTeams[team][0]
				ws.Cells(commitmentIndex, sprintCol).value = capacityTeams[team][1]
				#print(ws.Cells(capacityIndex, sprintCol).value)
				#print(ws.Cells(commitmentIndex, sprintCol).value)
			if (remainTeams.get(team) is not None):
				ws.Cells(remainIndex, sprintCol).value = remainTeams[team]
	wb.Save()
	return 

def excludeFiles(file):
	content = file.readlines()
	content = [x.strip() for x in content] 
	return content
	
if __name__ == "__main__":
	 main(sys.argv[1:])
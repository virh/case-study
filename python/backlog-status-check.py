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
		print('backlog-status-check.py --dir=<dir>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('backlog-status-check.py --dir=<dir>')
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
	
	f = open(os.path.join(logpath, "backlog-status-checklog.txt"),"w+")
	try:
		excludeFile = open(os.path.join(currDir, "exclude.txt"))
		excludeContent = excludeFiles(excludeFile)
	except IOError:
		excludeContent = []
			
	log(f, '=========Begin check files=========')
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
			for row in range(5, rowCount + 1):		
				if(not ws.Cells(row, taskIndex).value):
					break		
				#print('row index ', row)
				if(str(ws.Cells(row, statusIndex).value).lower()=='closed'):
					fillFlag = True
					tempPreviousIndex = statusIndex+1
					tempPreviousValue = ws.Cells(row, tempPreviousIndex).value
					while (tempPreviousIndex<previousWeekIndex):
						tempPreviousIndex = tempPreviousIndex+2
						currentValue = ws.Cells(row, tempPreviousIndex).value
						if(currentValue==0):
							fillFlag = False
							break
					if (fillFlag):
						ws.Cells(row, statusIndex).Interior.color = rgb_to_hex((255, 0, 0))
						ws.Cells(row, statusIndex).value = 'Open'
					else:
						ws.Cells(row, statusIndex).Interior.color = rgb_to_hex((255, 255, 255))

				if(ws.Cells(row, targetIndex).value is None):
					fillFlag = True
					tempPreviousIndex = statusIndex+1
					sprintIndex = ""
					while (tempPreviousIndex<=currentWeekIndex):
						if(ws.Cells(2, tempPreviousIndex).value is not None):
							sprintIndex = ws.Cells(2, tempPreviousIndex).value
						currentValue = ws.Cells(row, tempPreviousIndex).value
						if(currentValue is not None):
							sprintIndex = sprintIndex.replace("Sprint", today.strftime('%y'))
							fillFlag = False
							break
						tempPreviousIndex = tempPreviousIndex+2

					if (fillFlag):
						ws.Cells(row, targetIndex).Interior.color = rgb_to_hex((255, 0, 0))
					else:
						ws.Cells(row, targetIndex).value = sprintIndex
						ws.Cells(row, targetIndex).Interior.color = rgb_to_hex((255, 255, 255))

			wb.Save()
			wb.Close()
			#log(f, 'Update file[' + filename + '] end...')
			log(f, filename)
			updateCount += 1
	excel.Quit()
	excel = None
	log(f, '=========End check files=========')
	log(f, 'Totally checked ' + str(updateCount) + ' files!')
	f.close()
	return

def log(file, message):
	file.write('{}'.format(message))
	file.write('\n')
	return	

def rgb_to_hex(rgb):
    '''
    ws.Cells(1, i).Interior.color uses bgr in hex

    '''
    bgr = (rgb[2], rgb[1], rgb[0])
    strValue = '%02x%02x%02x' % bgr
    # print(strValue)
    iValue = int(strValue, 16)
    return iValue

def excludeFiles(file):
	content = file.readlines()
	content = [x.strip() for x in content] 
	return content
	
if __name__ == "__main__":
   main(sys.argv[1:])
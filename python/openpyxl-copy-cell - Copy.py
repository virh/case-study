#!/usr/bin/env python
import sys, getopt, os
import win32com.client
from win32com.client import Dispatch

def main(argv):
	baseDir = ''
	sourceColumn = ''
	distColumn = ''
	try:
		opts, args = getopt.getopt(argv,"h:s:d:",[])
	except getopt.GetoptError:
		print('backlog-copy.py -dir <dir> -s <sourcecolumn> -d <distcolumn>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('backlog-copy.py -dir <dir> -s <sourcecolumn> -d <distcolumn>')
			sys.exit()
		#elif opt == '-dir':
		#	baseDir = arg
		elif opt in ("-s", "--scolumn"):
			sourceColumn = arg
		elif opt in ("-d", "--dcolumn"):
			distColumn = arg

	print('Base dir is ', baseDir)
	print('Source column is ', sourceColumn)
	print('Dist column is ', distColumn)
	if (not sourceColumn) or (not distColumn):
		print("Usage: backlog-copy.py -dir <dir> -s <sourcecolumn> -d <distcolumn>")
		return
	
	if not baseDir:
		basepath = '.'
	else:
		basepath = baseDir
	excel = win32com.client.Dispatch('Excel.Application')
	for entry in os.listdir(basepath):
		if os.path.isfile(os.path.join(basepath, entry)) and 'xlsx'==os.path.splitext(entry)[1][1:]:
			print(entry)
			filename = os.path.join(basepath, entry)
			print(os.path.abspath(filename))
			
			#excel.Visible = True
			wb = excel.Workbooks.Open(os.path.abspath(filename))
			ws = wb.Worksheets('Team Backlog')		
			if not ws:
				return
			
			allData = ws.UsedRange
			
			# Get number of rows used on active sheet
			rowCount = allData.Rows.Count
			print('Number of rows used in sheet : ',rowCount)

			#Get number of columns used on active sheet
			colCount = allData.Columns.Count
			print('Number of columns used in sheet : ',colCount)

			writeData = wb.Worksheets('Team Backlog')

			for row in range(5, rowCount + 1):
				if not ws.Range(str(distColumn) + str(row)).value:
					cellValue = ws.Range(str(sourceColumn) + str(row)).value
					ws.Range(str(distColumn) + str(row)).value = cellValue

			wb.Save()
			wb.Close()
			print(filename)
	excel.Quit()
	excel = None
	
if __name__ == "__main__":
   main(sys.argv[1:])
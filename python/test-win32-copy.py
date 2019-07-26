#!/usr/bin/env python
import sys, getopt, os
import win32com.client
from win32com.client import Dispatch

def main(argv):
	baseDir = ''
	sourceColumn = 'BT'
	distColumn = 'BV'
	try:
		opts, args = getopt.getopt(argv,"h:s:d:",[])
	except getopt.GetoptError:
		print('copy-cell.py -dir <dir> -s <sourcecolumn> -d <distcolumn>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('copy-cell.py -dir <dir> -s <sourcecolumn> -d <distcolumn>')
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
		print("Usage: copy-cell.py -dir <dir> -s <sourcecolumn> -d <distcolumn>")
		return

	filename = os.path.join(".","test1.xlsx")
	print(os.path.abspath(filename))
	xl = win32com.client.Dispatch('Excel.Application')
	#xl.Visible = True
	wb = xl.Workbooks.Open(os.path.abspath(filename))

	getSheetName = wb.Activesheet.Name
	print('Active sheet name : ',getSheetName)
	
	readData = wb.Worksheets('Team Backlog')
	allData = readData.UsedRange
	
	# Get number of rows used on active sheet
	rowCount = allData.Rows.Count
	print('Number of rows used in sheet : ',rowCount)

	#Get number of columns used on active sheet
	colCount = allData.Columns.Count
	print('Number of columns used in sheet : ',colCount)

	writeData = wb.Worksheets('Team Backlog')

	for row in range(5, rowCount + 1):
		if not xl.Range(str(distColumn) + str(row)).value:
			cellValue = xl.Range(str(sourceColumn) + str(row)).value
			xl.Range(str(distColumn) + str(row)).value = cellValue

	wb.SaveAs(os.path.join("C:\python workspace","test3.xlsx"))
	wb.Close()
	xl.Quit()
	xl = None

if __name__ == "__main__":
   main(sys.argv[1:])
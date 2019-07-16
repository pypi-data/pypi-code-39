"""
Maintained by: Casey Johnson
https://github.com/caseyjohnsonwv/sheetslib

NOTE: Google Sheets are indexed from 1, not 0.
Functions should always return arrays indexed with a +1 offset.
"""


def getMatchingCellsFromList(cells, value, case_sensitive=False):
	"""Internal method - returns list containing indexes of matched values in 'cells' list (indexed from 0)"""
	results = []
	if not case_sensitive:
		value = value.lower()
	for i in range(len(cells)):
		cell_value = cells[i]
		if not case_sensitive:
			cell_value = cell_value.lower()
		if cell_value == value:
			results.append(i)
	return results


class GSheets:

	def __init__(self, sheet):
		"""Creates a GSheets object - usage: <varname> = GSheets(<worksheet object>)"""
		#passed worksheet object
		self.SHEET = sheet
		def initCols(sheet):
			COL_NAMES = self.SHEET.row_values(1)
			COLS = {COL_NAMES[i].lower() : i+1 for i in range(len(COL_NAMES))}
			del COL_NAMES
			return COLS
		self.COLS = initCols(sheet)


	def getCellValue(self, location):
		"""Returns formatted value at Sheets-compliant location=(row,col)"""
		return self.SHEET.cell(location[0],location[1]).value


	def getColumns(self):
		"""Returns dictionary mapping column names (key) to Sheets-compliant index (value)"""
		return self.COLS


	def getColumnNames(self):
		"""Returns column names as a list"""
		return list(self.COLS.keys())


	def getNumColumns(self):
		"""Returns number of columns in the sheet, as determined by row 1"""
		return len(self.COLS.keys())


	def getColumnIndex(self, col_name):
		"""Returns Sheets-compliant index of a column or -1 if not found"""
		return self.COLS.get(col_name.lower(), -1)


	def getAllRecords(self):
		"""Wrapper for gspread's get_all_records() function - returns dictionary"""
		return self.SHEET.get_all_records()


	def getAllValues(self):
		"""Wrapper for gspread's get_all_values() function - returns list"""
		return self.SHEET.get_all_values()


	def getIndexesOf(self, value, col_name='', case_sensitive=False):
		"""Finds all instances of a value in the sheet - returns list of Sheets-compliant (R,C) tuples"""
		if not case_sensitive:
			value = value.lower()
		results = []
		col_num = self.getColumnIndex(col_name)
		if col_num > 0:
			col = self.SHEET.col_values(col_num)
			match_indexes = getMatchingCellsFromList(col, value, case_sensitive)
			results = [(row_num + 1, col_num) for row_num in match_indexes]
		else:
			table = self.SHEET.get_all_values()
			for row_num in range(len(table)):
				match_indexes = getMatchingCellsFromList(table[row_num], value, case_sensitive)
				results.extend([(row_num + 1, col_num + 1) for col_num in match_indexes])
		return results


	def getRowsByPositions(self, location_list=[], return_type='list'):
		"""Return rows containing the (R,C) position tuples passed in location_list - returns list of lists or list of dictionaries"""
		if len(location_list) == 0:
			return None
		if len(return_type) >= 4:
			return_type = return_type.lower()[:4]
		all_data = None
		row_nums = []
		results = []
		if return_type == 'list':
			all_data = self.SHEET.get_all_values()
			row_nums=list(set([pos[0] for pos in location_list]))
		elif return_type == 'dict':
			all_data = self.SHEET.get_all_records()
			row_nums=list(set([pos[0]-1 for pos in location_list]))
		else:
			return None
		for row_num in row_nums:
			try:
				results.append(all_data[row_num])
			except Exception:
				pass
		return results


	def getRowsContaining(self, value, col_name='', case_sensitive=False, return_type='list'):
		"""Finds all rows containing a given value - returns list of lists or list of dictionaries"""
		results = []
		if len(return_type) >= 4:
			return_type = return_type.lower()[:4]
		if return_type not in ['list','dict']:
			return None
		if not case_sensitive:
			value = value.lower()
		table = self.SHEET.get_all_values()
		col_num = self.getColumnIndex(col_name)
		if col_num > 0:
			col = self.SHEET.col_values(col_num)
			match_indexes = getMatchingCellsFromList(col, value, case_sensitive)
			results = [table[row_num] for row_num in match_indexes]
		else:
			for row_num in range(len(table)):
				match_indexes = getMatchingCellsFromList(table[row_num], value, case_sensitive)
				if len(match_indexes) > 0:
					results.append(table[row_num])
		if return_type == 'dict':
			for r in range(len(results)):
				results[r] = {(sorted(self.COLS.items(), key=lambda kv:kv[1]))[i][0] : results[r][i] for i in range(len(results[r]))}
		return results


	def getColumnValues(self, col_name):
		"""Fetches all values in a given column - returns a list"""
		return self.SHEET.col_values(self.COLS[col_name.lower()])[1:]


	def updateCell(self, location, value):
		"""Updates a single cell at Sheets-compliant location=(row,col) - use updateRange for contiguous batch updates"""
		self.SHEET.update_cell(location[0], location[1], value)
		return True


	def updateRange(self, location_list=[], topleft=None, bottomright=None, values=[]):
		"""Updates a Sheets-compliant range of cells by [topleft=(row,col), bottomright=(row,col)] or by list of (row,col) tuples"""
		num_cells = len(location_list) if (topleft is None or bottomright is None) else (bottomright[0]-topleft[0]+1)*(bottomright[1]-topleft[1]+1)
		if num_cells == 0 or num_cells != len(values):
			return False
		elif len(location_list) > 0:
			update_map = {location_list[i] : values[i] for i in range(num_cells)}
			location_list.sort(key=lambda tup: (tup[0],tup[1]))
			cell_list = self.SHEET.range(location_list[0][0],location_list[0][1],location_list[-1][0],location_list[-1][1])
			for cell in cell_list:
				cell.value = update_map[(cell.row, cell.col)]
		else:
			cell_list = self.SHEET.range(topleft[0],topleft[1],bottomright[0],bottomright[1])
			for i in range(num_cells):
				cell_list[i].value = values[i]
		self.SHEET.update_cells(cell_list)
		return True


	def updateWhere(self, update_map, row_values=[], row_map={}, row_num=-1, case_sensitive=False):
		"""Updates a row from {'col_name':'value'}, found by values list, dictionary, or row number"""
		cells = []
		if len(update_map.keys()) == 0:
			return False
		elif row_num > 0:
			cells = self.SHEET.range(row_num, 1, row_num, len(self.COLS.keys()))
		elif len(row_values) == len(self.COLS.keys()):
			if not case_sensitive:
				row_values = [v.lower() for v in row_values]
			table = self.SHEET.get_all_values()
			for row_num in range(len(table)):
				row = table[row_num] if case_sensitive else [v.lower() for v in table[row_num]]
				if row == row_values:
					cells = self.SHEET.range(row_num+1, 1, row_num, len(self.COLS.keys()))
					break
		elif len(row_map.keys()) > 0 and len(row_map.keys()) <= len(self.COLS.keys()):
			if not case_sensitive:
				row_map_items = dict((str(k).lower(), v) for k,v in row_map.items()).items()
			table = self.SHEET.get_all_records()
			for row_num in range(len(table)):
				row_items = table[row_num].items() if case_sensitive else dict((str(k).lower(), str(v).lower()) for k,v in table[row_num].items()).items()
				if row_map_items <= row_items:
					cells = self.SHEET.range(row_num+2, 1, row_num+2, len(self.COLS.keys()))
					break
		else:
			return False
		update_map = dict((str(k).lower(), v) for k,v in update_map.items())
		col_names = list(self.COLS.keys())
		for i in range(len(cells)):
			new_value = update_map.get(col_names[i], None)
			if new_value is not None:
				cells[i].value = new_value
		self.SHEET.update_cells(cells)
		return True

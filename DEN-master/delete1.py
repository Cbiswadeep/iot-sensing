import xlrd

loc = ("/home/biswadeep/Downloads/DEN-master/wifi-access-data.xlsx") 
  
# To open Workbook 
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
  
# For row 0 and column 0 
#sheet.cell_value(0, 0) 
for i in range(sheet.nrows): 
    for j in range(sheet.ncols):
        print(sheet.cell_value(i,j), end =" ")
    print("\n")
from openpyxl import load_workbook

workbook = load_workbook(filename="Locations.xlsx")
sheet = workbook.active

locations = {}

for value in sheet.iter_row(min_row = 1, max_row = 1, min_col = 4, max_col = 7, values_only = True)
    location_id = col[0]
    location = {

    }


    print(value)
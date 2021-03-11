import csv

# Reads the CSV Parser
def read_data(data):
    with open(data, 'r') as f:
        data = [row for row in csv.reader(f.read().splitlines())]
    return data

# Run to see if read_data works
data = "studentData.txt"
read_data(data)

# Prints the file
fields = []
rows = []
with open(data, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)

    # extracting field names through first row
    fields = next(csvreader)

    # extracting each data row one by one
    for row in csvreader:
        rows.append(row)

    print("Number of rows: %d" % (csvreader.line_num))

print('Field names are:' + ', '.join(field for field in fields))

#  Prints entire file
for row in rows:
    # parsing each column of a row
    for col in row:
        print("%10s" % col),
    print('\n')

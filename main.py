import csv

debug = True

symbols = []
rawTimings = []

def printVerbose(str):
    if debug == True:
        print(str)

with open("LabelsDBG/ka-ki-ku-ke-ko-ka-N-ka.txt") as file:
    csvReader = csv.reader(file, delimiter="\t")
    for row in csvReader:
        printVerbose(row)
        symbols.append(row[2])
        rawTimings.append(row[1])

printVerbose(f'symbols: {symbols}\nraw timings: {rawTimings}')

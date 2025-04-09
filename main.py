import csv
import os
import sys
import configparser
import json
from logging import exception

# this varible enables verbose output which gives detailed output of what the script does, it's here mostly for debugging
verboseMode = True

workingFolder = input("Path to your labels: ")
directoryList = os.listdir(workingFolder)
directoryList.remove("config.ini")
folderLoopIndex = 0

rawSymbols = []
rawTimings = []
symbols = []
timingsBeginning = []
timingsStable = []
timingsUnstable2 = []
timingsEnd = []

consonantList = []
vowelList = []
addedPhonemes = []

generateCVPlosive = False
generateCVNonPlosive = False
generateV_CNonPlosive = False
generateV_CPlosive = False

config = configparser.ConfigParser()
config.read(os.path.join(workingFolder, "config.ini"))
consonantList = json.loads(config.get("Symbols", "Consonants"))
vowelList = json.loads(config.get("Symbols", "Vowels"))

if config.get("Generate", "Generate_CV_Plosive") == "1":
    generateCVPlosive = True
if config.get("Generate", "Generate_CV_NonPlosive") == "1":
    generateCVNonPlosive = True
if config.get("Generate", "Generate_V_C_NonPlosive") == "1":
    generateV_CNonPlosive = True
if config.get("Generate", "Generate_V_C_Plosive") == "1":
    generateV_CPlosive = True

index = 0

def printVerbose(printInput):
    if verboseMode == True:
        print(printInput)

#this function will concantinate our oto data and the append it to out file and varible keeping track of added phonemes
def addOtoLine(otoFilename, otoPhonemeName, otoOffset, otoConsonant, otoCutoff, otoPreu, otoOverlap):
    global addedPhonemes
    if addedPhonemes.count(otoPhonemeName) >= 1:
        printVerbose("Phoneme exists, skipping")
        return()
    else:
        otoFilename = otoFilename.replace("txt", "wav")
        otoFilename = otoFilename.replace(workingFolder, "")
        otoFilename = otoFilename.replace("\\", "")
        otoData = f"{otoFilename}={otoPhonemeName},{otoOffset},{otoConsonant},{otoCutoff},{otoPreu},{otoOverlap}\n"
        with open("oto.ini", mode="a") as otofile:
            otofile.write(otoData)
        addedPhonemes.append(otoPhonemeName)
        # with open("oto.ini", mode="r", encoding="utf-8") as otofile:
        #     print(otofile.read())

while folderLoopIndex < len(directoryList):
    index = 0
    rawSymbols = []
    rawTimings = []
    symbols = []
    timingsBeginning = []
    timingsStable = []
    timingsUnstable2 = []
    timingsEnd = []

    currentFile = os.path.join(workingFolder, directoryList[folderLoopIndex])
    print(currentFile)


    # open label file and put it into convinient to work variables, 2nd row is used for timing because vLabler quirk even though it's not supported now
    with open(currentFile, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t')
        for row in spamreader:
            tempvar = 0
            tempvar = round((float(row[1]) * 1000), 2)
            rawTimings.append(tempvar)
            rawSymbols.append(row[2])
            printVerbose(row)
            printVerbose(rawTimings)
            printVerbose(rawSymbols)
    times = 0

    # convert raw variables into a more convenient format
    while index < len(rawSymbols):
        printVerbose(f"index: {index}")
        if rawSymbols[index] == "sil" and index < (len(rawSymbols)) - 1:
            symbols.append(rawSymbols[index])
            timingsBeginning.append(rawTimings[index])
            timingsStable.append(rawTimings[index])
            timingsUnstable2.append(rawTimings[index])
            timingsEnd.append(rawTimings[index])
            index = index + 1
            continue
        elif rawSymbols[index] == "sil" and index >= (len(rawSymbols) - 1):
            symbols.append(rawSymbols[index])
            timingsBeginning.append(rawTimings[index])
            timingsStable.append(rawTimings[index])
            timingsUnstable2.append(rawTimings[index])
            timingsEnd.append(rawTimings[index])
            printVerbose("last sil")
            break
        else:
            timingsBeginning.append(rawTimings[index])
            timingsStable.append(rawTimings[index + 1])
            timingsUnstable2.append(rawTimings[index + 2])
            timingsEnd.append(rawTimings[index + 3])
            symbols.append(rawSymbols[index])
            index = index + 3

    printVerbose(f"Symbols length: {len(symbols)}")
    printVerbose(f"Beggining timings length: {len(timingsBeginning)}")
    printVerbose(f"Stable timings length: {len(timingsStable)}")
    printVerbose(f"Unstable timings length: {len(timingsUnstable2)}")
    printVerbose(f"End timings length: {len(timingsEnd)}")
    printVerbose(symbols)
    printVerbose(timingsBeginning)
    printVerbose(timingsStable)
    printVerbose(timingsUnstable2)
    printVerbose(timingsEnd)

    index = 0

    if generateCVPlosive == True:
        while index < len(symbols):
            if symbols[index] == "sil":
                try:
                    if consonantList.count(symbols[index+1]) >= 1:
                        if vowelList.count(symbols[index+2]) >= 1:
                            phoneme = symbols[index+1] + symbols[index+2]
                            offset = round(timingsBeginning[index+1] - 35, 2)
                            overlap = round(timingsBeginning[index+1] - offset, 2)
                            preu = round(timingsEnd[index+1] - offset, 2)
                            consonant = round(timingsStable[index+2] - offset, 2)
                            cutoff = round(timingsUnstable2[index+2] - offset, 2) / -1
                            addOtoLine(currentFile, phoneme, offset, consonant, cutoff, preu, overlap)
                            printVerbose("-----------------------------------")
                            printVerbose(f"phoneme: {phoneme}")
                            printVerbose(f"offset: {offset}")
                            printVerbose(f"overlap: {overlap}")
                            printVerbose(f"preu: {preu}")
                            printVerbose(f"consonant: {consonant}")
                            printVerbose(f"cutoff: {cutoff}")
                except Exception as error:
                    printVerbose(error)
            index = index + 1
        index = 0

    if generateCVNonPlosive == True:
        while index < len(symbols):
            if consonantList.count(symbols[index]) >=1:
                if vowelList.count(symbols[index+1]) >= 1:
                    printVerbose("CV Found, generating instance")
                    phoneme = f"{symbols[index]}{symbols[index+1]}"
                    offset = timingsBeginning[index]
                    overlap = round((timingsEnd[index] - timingsBeginning[index]) / 2, 2)
                    preu = round(timingsEnd[index] - offset, 2)
                    consonant = round(timingsStable[index+1] - offset, 2)
                    cutoff = round(timingsUnstable2[index+1] - offset, 2) / -1
                    addOtoLine(currentFile, phoneme, offset, consonant, cutoff, preu, overlap)
                    printVerbose("-----------------------------------")
                    printVerbose(f"phoneme: {phoneme}")
                    printVerbose(f"offset: {offset}")
                    printVerbose(f"overlap: {overlap}")
                    printVerbose(f"preu: {preu}")
                    printVerbose(f"consonant: {consonant}")
                    printVerbose(f"cutoff: {cutoff}")
            index = index+1
        index = 0

    if generateV_CNonPlosive == True:
        while index < len(symbols):
            if vowelList.count(symbols[index]) >= 1:
                if consonantList.count(symbols[index+1]) >= 1:
                    printVerbose("V C Found, generating instance")
                    phoneme = f"{symbols[index]} {symbols[index+1]}"
                    offset = timingsStable[index]
                    overlap = round((timingsUnstable2[index] - timingsStable[index]) / 2, 2)
                    preu = round(timingsEnd[index] - offset, 2)
                    consonant = round(timingsStable[index+1] - offset, 2)
                    cutoff = round(timingsUnstable2[index+1] - offset, 2) / -1
                    addOtoLine(currentFile, phoneme, offset, consonant, cutoff, preu, overlap)
                    printVerbose("-----------------------------------")
                    printVerbose(f"phoneme: {phoneme}")
                    printVerbose(f"offset: {offset}")
                    printVerbose(f"overlap: {overlap}")
                    printVerbose(f"preu: {preu}")
                    printVerbose(f"consonant: {consonant}")
                    printVerbose(f"cutoff: {cutoff}")
            index = index+1
        index = 0

    if generateV_CPlosive == True:
        while index < len(symbols):
            if vowelList.count(symbols[index]) >= 1:
                try:
                    if symbols[index+1] == "sil":
                        if consonantList.count(symbols[index+2]) >= 1:
                            printVerbose("V C plosive Found, generating instance")
                            phoneme = f"{symbols[index]} {symbols[index+2]}"
                            offset = timingsStable[index]
                            overlap = round((timingsUnstable2[index] - timingsStable[index]) / 2, 2)
                            preu = round(timingsEnd[index] - offset, 2)
                            # before this had -25 for cutoff and consonant had no addition just in case the changed values give poor results
                            consonant = round((timingsStable[index+1] - offset) + 15, 2)
                            cutoff = round((timingsUnstable2[index+1] - offset) + 45, 2)/ -1
                            addOtoLine(currentFile, phoneme, offset, consonant, cutoff, preu, overlap)
                            printVerbose("-----------------------------------")
                            printVerbose(f"phoneme: {phoneme}")
                            printVerbose(f"offset: {offset}")
                            printVerbose(f"overlap: {overlap}")
                            printVerbose(f"preu: {preu}")
                            printVerbose(f"consonant: {consonant}")
                            printVerbose(f"cutoff: {cutoff}")
                except:
                    printVerbose("out of range")
            index = index+1
        index = 0

    folderLoopIndex = folderLoopIndex + 1

print("Oto has been generated!")
input("Press enter to exit")
from ProcessLine import *
from ProcessCapturing import *


blocks = []


def readFile(filePath,inputTime_first, inputTime_second):
    firstSample = []
    with open(filePath, "r") as f:
        data = f.readlines()

        for line in data:
            if line.__contains__("===="):
                continue
            if line.__contains__("Time:"):
                sampleTime = line.replace("Time:","").replace("\n","")
                if firstSample.__len__() > 0:
                    blocks.append(firstSample)
                    firstSample = []
                continue
            if line.__contains__("pid      name                                     exe  "):
                continue
            tmp = ProcessLine(sampleTime,line,inputTime_first,inputTime_second)
            firstSample.append(tmp)
        blocks.append(firstSample)


def findMinTimeDiff():
    if blocks.__len__() <1:
        return []
    minDiff = []
    minDiff1 = blocks[0][0].timeDiff_first
    minDiff2 = blocks[0][0].timeDiff_second
    for block in blocks:
        if(minDiff1 > block[0].timeDiff_first):
            minDiff1 = block[0].timeDiff_first
        if (minDiff2 > block[0].timeDiff_second):
            minDiff2 = block[0].timeDiff_second
    minDiff.append(minDiff1)
    minDiff.append(minDiff2)
    return minDiff


def getBlocksToCompare():
    blocksToCompare = []
    firstFound = False
    secondFound = False
    minDiffs = findMinTimeDiff()
    for block in blocks:
        if block[0].timeDiff_first == minDiffs[0] and not firstFound:
            blocksToCompare.append(block)
            firstFound = True
        if block[0].timeDiff_second == minDiffs[1] and not secondFound:
            blocksToCompare.append(block)
            secondFound = True
        if firstFound and secondFound:
            break
    return blocksToCompare


def writeBlockToFile(name, procs):
    if procs is None:
        return
    file = open(name, "a")
    file.write("{:<8} {:<40} {:<100} {:<20}\n".format(procs.pid,procs.name,procs.exe,procs.runTime))
    file.close()


def compareTwoBlocks(orig,new):
    for p_orig in orig:
        procExist = False
        for p_new in new:
            if p_orig.name == p_new.name :
                procExist = True
                break

        if not procExist:
            writeBlockToFile('Status_log.txt',p_orig)





def manualScaning(filename, date1, date2):
    # readFile("/home/alex/Desktop/PyCharmWorkspace/Processes.txt","2018-04-26 21:35:33.467608","2018-04-26 21:35:38.510485")
    readFile(filename,date1,date2)
    tmp2 = getBlocksToCompare()
    write_to_file('Status_log.txt','New Processes')
    compareTwoBlocks(tmp2[0],tmp2[1]) #add to file status log the killed processes

    write_to_file('Status_log.txt', 'Killed Processes')
    compareTwoBlocks(tmp2[1], tmp2[0])  # add to file status log the killed processes


from datetime import datetime

class ProcessLine():
    pid = ""
    name = ""
    exe = ""
    runTime = 0
    sampleTime = 0
    timeDiff_first = 0
    timeDiff_second = 0

    def __init__(self,sampleTime,row,inputTime_first, inputTime_second):
        arr = row.split()
        self.pid =arr[0]
        self.name = arr[1]
        self.exe = arr[2]
        self.runTime = arr[3]

        dateSample = datetime.strptime(sampleTime.replace(" ",""), "%Y-%m-%d%H:%M:%S.%f")
        dateInputTime = datetime.strptime(inputTime_first.replace(" ",""), "%Y-%m-%d%H:%M:%S.%f")
        diff = (dateSample - dateInputTime)
        self.timeDiff_first = (diff.days *86400).__abs__()+diff.seconds

        dateInputTime = datetime.strptime(inputTime_second.replace(" ", ""), "%Y-%m-%d%H:%M:%S.%f")
        diff = (dateSample - dateInputTime)
        self.timeDiff_second = (diff.days * 86400).__abs__() + diff.seconds

        self.sampleTime = sampleTime





import time
import datetime
import psutil


_FINISH = False


def create_file(name):
    file = open(name, "a")
    file.write(
        "=============================================================================================================================================================================================\n")
    file.write("Time: %s \n" % datetime.datetime.now())
    file.write("{:<8} {:<40} {:<100} {:<20}\n".format('pid', 'name', 'exe', 'time'))
    file.write("=============================================================================================================================================================================================\n")
    file.close()


def write_data_to_file(name, procs):
    if procs is None:
        return
    file = open(name, "a")
    file.write("{:<8} {:<40} {:<100} {:<20}\n".format(procs['pid'],procs['name'],procs['exe'],procs['create_time']))
    file.close()


def write_to_file(name, msg):
    if msg and name is None:
        return
    file = open(name, "a")
    file.write(msg)
    file.write("\n")
    file.close()


def if_procs_exist(orig,new):
    for p_orig in orig:
        procExist = False
        for p_new in new:
            if p_orig['name'] == p_new['name'] :
                procExist = True
                break

        if not procExist:
            write_data_to_file('Status_log.txt',p_orig)


def scan():
    pInfo_original = []
    global _FINISH
    for proc in psutil.process_iter():
        try:
            pI = proc.as_dict(attrs=['pid', 'name', 'exe', 'create_time'])
        except psutil.NoSuchProcess:
            pass
        else:
            pInfo_original.append(pI)

    while True:
        if _FINISH:
            return
        create_file('Processes.txt')
        create_file('Status_log.txt')

        pInfo = []
        for proc in psutil.process_iter():
            try:
                pI = proc.as_dict(attrs=['pid', 'name', 'exe', 'create_time'])
            except psutil.NoSuchProcess:
                pass
            else:
                pInfo.append(pI)
                write_data_to_file('Processes.txt', pI)

        write_to_file('Status_log.txt','New Processes')
        if_procs_exist(pInfo,pInfo_original) #add to file status log the killed processes

        write_to_file('Status_log.txt', 'Killed Processes')
        if_procs_exist(pInfo_original, pInfo)  # add to file status log the killed processes

        pInfo_original = []
        for proc in psutil.process_iter():
            try:
                pI = proc.as_dict(attrs=['pid', 'name', 'exe', 'create_time'])
            except psutil.NoSuchProcess:
                pass
            else:
                pInfo_original.append(pI)

        time.sleep(5)


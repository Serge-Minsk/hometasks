#It was python 2.7.11 used
import os
import schedule
import psutil
import configparser
import time
import datetime
import json

try:
    config = configparser.ConfigParser()
    config.read('config.ini')
    output = config.get('common','output')
    interval = float(config.get('common','interval'))
except ConfigCorruptedError:
    print("Please, check config.ini file and try again.")

snap_stap = 0


def creates_dict(p):
    '''Creates dictionaries'''
    val = list(p)
    key = p._fields
    result_dict = dict(zip(key, val))
    return result_dict

def trun():
    '''Writes results of monitoring into txt file'''
    global interval
    global snap_stap
try:
    print("Writing info in txt file(SNAPSHOT #{})".format(snap_stap))
#    while(1):
    os.system("clear")
    snap_stap = snap_stap + 1
    with open("monitorapp.txt", "a") as txtfile:
        txtfile.write( "\nSNAPSHOT " + "%s" % snap_stap + ":" + " [%s]" % datetime.datetime.now())
        txtfile.write( "\nNumber of CPUs: " +str(psutil.cpu_count()))
        txtfile.write( "\nNumber of Physical CPUs: " +str(psutil.cpu_count(logical=False)))
        txtfile.write( "\nOverall CPU load: " +str(psutil.cpu_stats()))
        txtfile.write( "\nOverall virtual memory usage: " +str(psutil.virtual_memory()))
        txtfile.write( "\nOverall swap memory usage: " +str(psutil.swap_memory()))
        txtfile.write( "\nIO information: " +str(psutil.disk_io_counters(perdisk=True)))
        txtfile.write( "\nNetwork information: " +str(psutil.net_io_counters()))
        txtfile.close()

 #       time.sleep(interval)
 #   break
except Exception, e:
    raise

def jrun():
    '''Writes results of monitoring into json file'''
    global interval
    global snap_stap
try:
    print "Writing info in json file(SNAPSHOT #{})".format(snap_stap)
#    while (1):
    os.system("clear")
    snap_stap = snap_stap + 1
    with open("monitorapp.json", "a") as jsonfile:
        jsonfile.write("\nSNAPSHOT " + "%s" % snap_stap + ":" + " [%s]" % datetime.datetime.now())
        jsonfile.write("\nNumber of CPUs\n")
        json.dump((psutil.cpu_count()), jsonfile, indent=4)
        jsonfile.write("\nNumber of Physical CPUs\n")
        json.dump((psutil.cpu_count(logical=False)), jsonfile, indent=4)
        jsonfile.write("\nOverall CPU load\n")
        json.dump(creates_dict(psutil.cpu_stats()), jsonfile, indent=4)
        jsonfile.write("\nOverall virtual memory usage\n")
        json.dump(creates_dict(psutil.virtual_memory()), jsonfile, indent=4)
        jsonfile.write("\nOverall swap memory usage\n")
        json.dump(creates_dict(psutil.swap_memory()), jsonfile, indent=4)
        jsonfile.write("\nIO information\n")
        json.dump((psutil.disk_io_counters(perdisk=True)), jsonfile, indent=4)
        jsonfile.write("\nNetwork information\n")
        json.dump(creates_dict(psutil.net_io_counters()), jsonfile, indent=4)
        jsonfile.write("\n\n")
        jsonfile.close()

#    time.sleep(interval)
#    break
except Exception, e:
    raise
if output == "txt":
#    print 'Output file type = ' + output + ' and interval is ' + interval + ' minutes'
    schedule.every(int(interval)).minutes.do(trun)
elif output == "json":
#    print 'Output file type = ' + output + ' and interval is ' + interval + ' minutes'
    schedule.every(int(interval)).minutes.do(jrun)
else:
#    print "Unknown file type set in config file"
    quit()
while True:
   schedule.run_pending()
   time.sleep(15)




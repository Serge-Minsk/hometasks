# It was python 2.7.11 used

import os
import schedule
import psutil
import configparser
import time
import datetime
import json

config = configparser.ConfigParser()
config.read('config.ini')
output = config.get('common','output')
interval = str(config.get('common','interval'))


snap_stap = 1


class parent(object):
    '''Initial class'''

    def creates_dict(self, p):
        val = list(p)
        key = p._fields
        result_dict = dict(zip(key, val))
        return result_dict


class textmake(parent):
    "Common base class for txt"
    def __init__(self):
        super(textmake, self).__init__()
    def trun(self):
        global interval
        global snap_stap
        print("Writing info in txt file(SNAPSHOT #{})".format(snap_stap))
        with open("monitorapp.txt", "a+") as txtfile:
            txtfile.write( "\nSNAPSHOT " + "%s" % snap_stap + ":" + " [%s]" % datetime.datetime.now())
            txtfile.write( "\nNumber of CPUs: " +str(psutil.cpu_count()))
            txtfile.write( "\nNumber of Physical CPUs: " +str(psutil.cpu_count(logical=False)))
            txtfile.write( "\nOverall CPU load: " +str(psutil.cpu_stats()))
            txtfile.write( "\nOverall virtual memory usage: " +str(psutil.virtual_memory()))
            txtfile.write( "\nOverall swap memory usage: " +str(psutil.swap_memory()))
            txtfile.write( "\nIO information: " +str(psutil.disk_io_counters(perdisk=True)))
            txtfile.write( "\nNetwork information: " +str(psutil.net_io_counters()))
            txtfile.close()
            snap_stap = snap_stap + 1



class jcreate(parent):
    """Common base class for json"""

    def __init__(self):
        super(jcreate, self).__init__()
    def jrun(self):
        global interval
        global snap_stap
        print "Writing info in json file(SNAPSHOT #{})".format(snap_stap)
        with open("monitorapp.json", "a+") as jsonfile:
            jsonfile.write("\nSNAPSHOT " + "%s" % snap_stap + ":" + " [%s]" % datetime.datetime.now())
            jsonfile.write("\nNumber of CPUs\n")
            json.dump((psutil.cpu_count()), jsonfile, indent=4)
            jsonfile.write("\nNumber of Physical CPUs\n")
            json.dump((psutil.cpu_count(logical=False)), jsonfile, indent=4)
            jsonfile.write("\nOverall CPU load\n")
            json.dump(super(jcreate, self).creates_dict(psutil.cpu_stats()), jsonfile, indent=4)
            jsonfile.write("\nOverall virtual memory usage\n")
            json.dump(super(jcreate, self).creates_dict(psutil.virtual_memory()), jsonfile, indent=4)
            jsonfile.write("\nOverall swap memory usage\n")
            json.dump(super(jcreate, self).creates_dict(psutil.swap_memory()), jsonfile, indent=4)
            jsonfile.write("\nIO information\n")
            json.dump((psutil.disk_io_counters(perdisk=True)), jsonfile, indent=4)
            jsonfile.write("\nNetwork information\n")
            json.dump(super(jcreate, self).creates_dict(psutil.net_io_counters()), jsonfile, indent=4)
            jsonfile.write("\n\n")
            jsonfile.close()
            snap_stap = snap_stap + 1


j = jcreate()
t = textmake()

def work():
    if output == "txt":
        print 'Output file type = ' + output + ' and interval is ' + interval + ' minutes'
        t.trun()
    elif output == "json":
        print 'Output file type = ' + output + ' and interval is ' + interval + ' minutes'
        j.jrun()
    else:
        print "Unknown file type set in config file"
        quit()


schedule.every(int(interval)).minutes.do(work)
while True:
    schedule.run_pending()
    time.sleep(1)


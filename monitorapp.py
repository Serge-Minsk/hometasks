# It was python 2.7.11 used
try:
    import os
    import schedule
    import psutil
    import configparser
    import time
    import datetime
    import json
    import logging
    import logging.config
except ImportError:
    print("Wow, looks like you don't have all the modules required."
          "Check if you have psutil and schedule and try again.")

try:
    config = configparser.ConfigParser()
    config.read('config.ini')
    output = config.get('common','output')
    interval = str(config.get('common','interval'))
    log_level = config.get('common', 'level')
except FileNotFoundError:
    print("Config file not found. Please, check config file and try again.")

handler = logging.FileHandler('monitorapp.log')
logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(log_level)
logger.info("Logging {} level messages".format(log_level))

snap_stap = 1

def benchmark(func):
    """
    The decorator providing time which has borrowed
    performance of the decorated function.
    """
    import time
    def wrapper(*args, **kwargs):
        t = time.clock()
        res = func(*args, **kwargs)
        print func.__name__, time.clock() - t
        return res
    return wrapper


def calls(func):
    """
   The decorator logging work of a code.
    (removes calls)
    """
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        print func.__name__, args, kwargs
        return res
    return wrapper


def counter(func):
    # type: (object) -> object
    """
    The decorator considering and outputting quantity of calls
    the decorated function.
    """
    def wrapper(*args, **kwargs):
        wrapper.count += 1
        res = func(*args, **kwargs)
        print "{0} has been caused: {1}x".format(func.__name__, wrapper.count)
        return res
    wrapper.count = 0
    return wrapper


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

    @benchmark
    @calls
    @counter
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
            snap_stap += 1



class jcreate(parent):
    """Common base class for json"""
    def __init__(self):
        super(jcreate, self).__init__()

    @benchmark
    @calls
    @counter
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
            snap_stap += 1



try:
    j = jcreate()
    logging.info("Object j created")
except Exception as exc:
    logging.exception("Can't create object, {}".format(exc))

try:
    t = textmake()
    logging.info("Object t created")
except Exception as exc:
    logging.exception("Can't create object, {}".format(exc))

try:
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
except Exception as exc:
    logging.exception("Can't execute run() function {}".format(exc))

try:
    schedule.every(int(interval)).minutes.do(work)
except Exception as exc:
    logging.exception("Can't execute scheduling {}".format(exc))

while True:
    schedule.run_pending()
    time.sleep(1)


"""
    Filename    : VirtualEnvironment.py
    Authors     : Shane Moon, Hannah Sarver
    Last Update : December 11, 2012
    Description : Currently a problem with self.allocation changing for no apparent reason
"""

import random
from random import randrange, choice
import math
import numpy as np
import matplotlib.pyplot as plt

class Reporter:
    def __init__(self, drive_type):
        self.total_num_activity = 0
        self.total_io_time = 0
        self.read_time = 0
        self.write_time = 0
        self.write_durations = []  # amount time required for completion
        self.write_start_times = []  # time io occured at
        self.write_durations_cumulative = [] # cumulative
        self.read_durations  = []
        self.read_durations_cumulative = []
        self.read_start_times  = []
        self.drive_type = drive_type

    def display_results(self):
        print "Displaying the result of drive type: %s" % self.drive_type
        print "total io time: %f" % self.total_io_time
        print "total read time: %f" % self.read_time
        print "total write time: %f" % self.write_time

        fig = plt.figure(figsize=(9,9))
        fig.suptitle(self.drive_type)

        writes = fig.add_subplot(2,1,1)
        writes.set_title("writes")
        writes.set_xlabel("Timestamp (sec)")
        writes.set_ylabel("Cumulative Write Times (sec)")

        reads = fig.add_subplot(2,1,2)
        reads.set_title("reads")
        reads.set_xlabel("Timestamp (sec)")
        reads.set_ylabel("Cumulative Read Times (sec)")

        writes.plot(self.write_start_times, self.write_durations_cumulative)
        reads.plot(self.read_start_times, self.read_durations_cumulative)
        # plt.show()


class VirtualEnvironment:
    def __init__(self):
        self.reporter = Reporter(self.drive_type)

    def HandleActivity(self, activity):
        """
            Takes an <Activity> object as an input,
            parses its operation ( = activity.D), and handles it accordingly.

            'R' for ReadFile()
            'W' for WriteFile()
            etc.

            Caller of this function should be a child of <VirtualEnvironment>
            class, e.g. <HDD>, <SSD>, <PD>, so that ReadFile() and WriteFile()
            can be handled accordingly.
        """
        # Refer to Tracer.py for more info on <Activity> object.

        # Convert micro second to second
        io_start_time = activity.start_time / 1000000.0

        # Handle activity according to their access_type.
        # There are some weird cases where io_start_time is older than the most recent one.
        # We're ignoring such cases.
        if (activity.access_type == 'R') and (len(self.reporter.read_start_times) == 0 or io_start_time > self.reporter.read_start_times[-1]):
            io_duration = self.ReadFile(activity)
            self.reporter.read_time += io_duration
            self.reporter.read_durations.append(io_duration)
            self.reporter.read_durations_cumulative.append(self.reporter.read_time)
            self.reporter.read_start_times.append(io_start_time)
            self.reporter.total_io_time += io_duration
            self.reporter.total_num_activity += 1    

        elif (activity.access_type == 'W') and (len(self.reporter.read_start_times) == 0 or io_start_time > self.reporter.write_start_times[-1]):
            io_duration = self.WriteFile(activity)
            self.reporter.write_time += io_duration
            self.reporter.write_durations.append(io_duration)
            self.reporter.write_durations_cumulative.append(self.reporter.write_time)
            self.reporter.write_start_times.append(io_start_time)
            self.reporter.total_io_time += io_duration
            self.reporter.total_num_activity += 1    
            
        else:
            # NEED TO HANDLE ERROR HERE
            pass

        # For any activity type


    def ReadFile(self, activity):
        pass

    def WriteFile(self, activity):
        pass


class HDD(VirtualEnvironment):
    def __init__(self, size):
        self.drive_type = "HDD"
        self.size = size
        VirtualEnvironment.__init__(self)
        

    
    def ReadFile(self,activity):
        file_size = activity.size
        #print "Read file on the virtual HDD environment"


        # According to wikipedia, average seek time is ~8-12ms
        # However, to dramatize the difference, I'll increase the range
        # to 5~15ms.
        seek_time = randrange(500, 1500) / 100.0 / 1000000 # ends up with units of seconds
        
        # Max read rate for an average HDD is ~ 140 MB/s
        # (we should probably check the numbers somewhat more if we can)
        # so let's put in a range from 80,000 to 140,000 kB/s).
        lookup_rate = randrange(80000,140000) # in kB/s
        file_size_kb = float(file_size) / 1000 #file_size should come in bytes
        read_time = seek_time + file_size_kb / lookup_rate 

        return read_time # in seconds

    def WriteFile(self,activity):
        file_size = activity.size
        #print "Write file on the virtual HDD environment"
        write_rate = randrange(80000,140000) #same range?
        file_size_kb = float(file_size) / 1000 #file_size should come in bytes
        write_time = float(file_size_kb) / write_rate
        return write_time


class SSD(VirtualEnvironment):
    def __init__(self,size):
        self.drive_type = "SSD"
        self.size = size
        VirtualEnvironment.__init__(self)

    
    def ReadFile(self,activity):
        file_size = activity.size
        #print "Read file on the virtual SSD environment"
        # According to wikipedia, data access time is about 0.1ms, and data transfer rate is between 100-600MB/s, let's say 400MB/s is reasonable
        access_time = 0.1 / 1000 #in seconds
        transfer_rate = 400 * 1000000 #in ~bytes/s
        read_time = access_time + file_size / transfer_rate
        return read_time

    
    def WriteFile(self,activity):
        file_size = activity.size
        #print "Write file on the virtual SSD environment"
        access_time = 0.1 / 1000 #in seconds
        transfer_rate = 400 * 1000000 #in ~bytes/s
        write_time = access_time + file_size / transfer_rate
        return write_time
        
'''def Allocator(hdd_size,ssd_size,trace,allocation_type):
    """create allocation based on traces and relative drive sizes"""
    allocation = {}
    total_size = hdd_size + ssd_size    
    if allocation_type == 'random':
        for filename in trace.filename_freq.keys():
            if random.random() < hdd_size / total_size:
                allocation[filename[1]] = 'hdd'
            else:
                allocation[filename[1]] = 'ssd'
    else:
        total_filesizes = sum(trace.filename_sizemap.values())
        prop_ssdsize = float(ssd_size) / total_size * total_filesizes
        filename_by_freq = [ (item[1], item[0]) for item in trace.filename_freq.items() ]
        filename_by_freq.sort(reverse = True)

        buffer_ssd = prop_ssdsize
        for filename in filename_by_freq:
            if buffer_ssd > 0:
                allocation[filename[1]] = 'ssd'
                buffer_ssd -= trace.filename_sizemap[filename[1]]
                #print 'buffer  ', buffer_ssd
            else:
                allocation[filename[1]] = 'hdd'
                #print 'hdd'
        print allocation
        return allocation'''

class PD(VirtualEnvironment):
    def __init__(self, hdd_size, ssd_size, trace, allocation_type):
        self.drive_type = "PD (%s)" % allocation_type
        self.HDD = HDD(hdd_size)
        self.SSD = SSD(ssd_size)
        self.total_size = hdd_size + ssd_size
        self.hdd_size = hdd_size
        self.ssd_size = ssd_size
        #VirtualEnvironment.__init__(self)
        self.trace = trace
        self.allocation_type = allocation_type
        self.Allocator()
        #self.allocation = self.Allocator()
        #print self.allocation
        
        
        """
        allocation is dictionary with keys = filenames (str), values = which drive (str)
        """
        VirtualEnvironment.__init__(self)
    
    def Allocator(self):
        """create allocation based on traces and relative drive sizes"""
        self.allocation = {}        
        if self.allocation_type == 'random':
            for filename in self.trace.filename_freq.keys():
                if random.random() < float(self.hdd_size) / self.total_size:
                    self.allocation[filename] = 'hdd'
                else:
                    self.allocation[filename] = 'ssd'
        else:
            total_filesizes = sum(self.trace.filename_sizemap.values())
            prop_ssdsize = float(self.ssd_size) / self.total_size * total_filesizes
            filename_by_freq = [ (item[1], item[0]) for item in self.trace.filename_freq.items() ]
            filename_by_freq.sort(reverse = True)

            buffer_ssd = prop_ssdsize
            for filename in filename_by_freq:
                if buffer_ssd > 0:
                    self.allocation[filename[1]] = 'ssd'
                    buffer_ssd -= self.trace.filename_sizemap[filename[1]]
                    #print 'buffer  ', buffer_ssd
                else:
                    self.allocation[filename[1]] = 'hdd'
                    #print 'hdd'
            #print self.allocation
        

    def ReadFile(self, activity):
        file_size = activity.size
        #print "Read file on the virtual Phoenix Drive environment"
        
        ## THIS IS WHERE IT SHOWS UP AS NOT HAVING THE RIGHT ALLOCATION...
        #print 'allocation:', self.allocation
        #print 'path:', activity.pathname
        #print self.allocation[activity.pathname]

        try:
            #print activity.pathname
            drive = self.allocation[activity.pathname]
        except TypeError:
            drive = 'ssd'
            #print 'stegosaurus'
        if drive == 'hdd':
            #print 'turtles'
            read_time = self.HDD.ReadFile(activity)
        else :
            read_time = self.SSD.ReadFile(activity)
        return read_time

    def WriteFile(self, activity):
        file_size = activity.size
        #print "Write file on the virtual Phoenix Drive environment"

        ## THIS IS WHERE IT SHOWS UP AS NOT HAVING THE RIGHT ALLOCATION...
        #print 'allocation:', self.allocation
        #print 'path:', activity.pathname
        #print self.allocation[activity.pathname]

        try:
            drive = self.allocation[activity.pathname]
        except:
            drive = 'ssd'
        if drive == 'hdd':
            write_time = self.HDD.WriteFile(activity)
        else :
            write_time = self.SSD.WriteFile(activity)
        return write_time

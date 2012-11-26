"""
    Filename    : VirtualEnvironment.py
    Authors     : Shane Moon, Hannah Sarver
    Last Update : November 12, 2012
    Description : 
"""

import random
import math
import numpy as np
import matplotlib.pyplot as plt

class Reporter:
    def __init__(self, drive_type):
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

        plt.show()


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

        if activity.access_type == 'R':
            io_duration = self.ReadFile(activity.size)
            self.reporter.read_time += io_duration
            self.reporter.total_io_time += io_duration
            self.reporter.read_durations.append(io_duration)
            self.reporter.read_durations_cumulative.append(self.reporter.read_time)
            self.reporter.read_start_times.append(io_start_time)

        elif activity.access_type == 'W':
            io_duration = self.WriteFile(activity.size)
            self.reporter.write_time += io_duration
            self.reporter.total_io_time += io_duration
            self.reporter.write_durations.append(io_duration)
            self.reporter.write_durations_cumulative.append(self.reporter.write_time)
            self.reporter.write_start_times.append(io_start_time)
            
        else:
            # NEED TO HANDLE ERROR HERE
            pass

    def ReadFile(self, file_size):
        pass

    def WriteFile(self, file_size):
        pass


class HDD(VirtualEnvironment):
    def __init__(self):
        self.drive_type = "HDD"
        VirtualEnvironment.__init__(self)
        

    
    def ReadFile(self,file_size):
        #print "Read file on the virtual HDD environment"
        # According to wikipedia, average seek time is ~8-12ms, and max read rate for an average HDD is ~ 140 MB/s (we should probably check the numbers somewhat more if we can), so let's put in a range from 80,000 to 140,000 kB/s).
        seek_time = random.randrange(800, 1200) / 100000.0 # ends up with units of seconds
        lookup_rate = random.randrange(80000,140000) # in kB/s
        file_size_kb = float(file_size) / 1000 #file_size should come in bytes
        read_time = seek_time + file_size_kb / lookup_rate 
        return read_time # in seconds

    def WriteFile(self,file_size):
        #print "Write file on the virtual HDD environment"
        write_rate = random.randrange(80000,125000) #same range?
        write_time = float(file_size) / write_rate
        return write_time


class SSD(VirtualEnvironment):
    def __init__(self):
        self.drive_type = "SSD"
        VirtualEnvironment.__init__(self)

    
    def ReadFile(self,file_size):
        #print "Read file on the virtual SSD environment"
        # According to wikipedia, data access time is about 0.1ms, and data transfer rate is between 100-600MB/s, let's say 400MB/s is reasonable
        access_time = 0.1 / 1000 #in seconds
        transfer_rate = 400 * 1000000 #in ~bytes/s
        read_time = access_time + file_size / transfer_rate
        return read_time

    
    def WriteFile(self,file_size):
        #print "Write file on the virtual SSD environment"
        access_time = 0.1 / 1000 #in seconds
        transfer_rate = 400 * 1000000 #in ~bytes/s
        write_time = access_time + file_size / transfer_rate
        return write_time
        

class PD(VirtualEnvironment):
    def __init__(self):
        self.drive_type = "PD"
        self.HDD = HDD()
        self.SSD = SSD()
        VirtualEnvironment.__init__(self)
        

    def ReadFile(self, file_size):
        #print "Read file on the virtual Phoenix Drive environment"
        #eventually do this based on file extensions and other parameters, for now just choose at random
        drive = random.choice(['hdd', 'ssd'])
        if drive == 'hdd':
            read_time = self.HDD.ReadFile(file_size)
            #temp_hdd = new HDD()
            #read_time = temp_hdd.ReadFile(file_size)
        else :
            read_time = self.SSD.ReadFile(file_size)
        return read_time

    def WriteFile(self, file_size):
        #print "Write file on the virtual Phoenix Drive environment"
        drive = random.choice(['hdd', 'ssd'])
        if drive == 'hdd':
            write_time = self.HDD.WriteFile(file_size)
        else :
            write_time = self.SSD.WriteFile(file_size)
        return write_time

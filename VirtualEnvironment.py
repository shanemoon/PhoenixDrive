"""
    Filename    : VirtualEnvironment.py
    Authors     : Shane Moon, Hannah Sarver
    Last Update : November 12, 2012
    Description : 
"""

import random
import math

class VirtualEnvironment:
    def __init__(self):
        pass

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

        file_size = activity.SIZE
        if activity.D == 'R':
            self.ReadFile(file_size)
        elif activity.D == 'W':
            self.WriteFile(file_size)
        else:
            # NEED TO HANDLE ERROR HERE
            pass

    def ReadFile(self, file_size):
        pass

    def WriteFile(self, file_size):
        pass


class HDD(VirtualEnvironment):
    def __init__(self):
        VirtualEnvironment.__init__(self)

    @classmethod
    def ReadFile(file_size):
        print "Read file on the virtual HDD environment"
        # According to wikipedia, average seek time is ~8-12ms, and max read rate for an average HDD is ~ 140 MB/s (we should probably check the numbers somewhat more if we can), so let's put in a range from 80,000 to 140,000 kB/s).
        seek_time = random.randrange(800, 1200) / 100000.0 # ends up with units of seconds
        lookup_rate = random.randrange(80000,140000) # in kB/s
        file_size_kb = float(file_size) / 1000 #file_size should come in bytes
        read_time = seek_time + file_size_kb / lookup_rate 
        return read_time # in seconds

    @classmethod
    def WriteFile(file_size):
        print "Write file on the virtual HDD environment"
        write_rate = random.randrange(80000,125000) #same range?
        write_time = float(file_size) / write_rate
        return write_time


class SSD(VirtualEnvironment):
    def __init__(self):
        VirtualEnvironment.__init__(self)

    @classmethod
    def ReadFile(file_size):
        print "Read file on the virtual SSD environment"
        # According to wikipedia, data access time is about 0.1ms, and data transfer rate is between 100-600MB/s, let's say 400MB/s is reasonable
        access_time = 0.1 / 1000 #in seconds
        transfer_rate = 400 * 1000000 #in ~bytes/s
        read_time = access_time + file_size / transfer_rate
        return read_time

    @classmethod
    def WriteFile(file_size):
        print "Write file on the virtual SSD environment"
        access_time = 0.1 / 1000 #in seconds
        transfer_rate = 400 * 1000000 #in ~bytes/s
        write_time = access_time + file_size / transfer_rate
        return write_time
        

class PD(VirtualEnvironment):
    def __init__(self):
        VirtualEnvironment.__init__(self)

    def ReadFile(self, file_size):
        print "Read file on the virtual Phoenix Drive environment"
        #eventually do this based on file extensions and other parameters, for now just choose at random
        drive = random.choice(['hdd', 'ssd'])
        if drive == 'hdd':
            read_time = HDD.ReadFile(file_size)
            #temp_hdd = new HDD()
            #read_time = temp_hdd.ReadFile(file_size)
        else :
            read_time = SSD.ReadFile(file_size)
        return read_time

    def WriteFile(self, file_size):
        print "Write file on the virtual Phoenix Drive environment"
        drive = random.choice(['hdd', 'ssd'])
        if drive == 'hdd':
            write_time = HDD.WriteFile(file_size)
        else :
            write_time = SSD.WriteFile(file_size)
        return write_time

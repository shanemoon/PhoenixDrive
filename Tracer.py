"""
    Filename    : Tracer.py
    Authors     : Shane Moon, <YOUR_NAME>
    Last Update : November 11, 2012
    Description : 
"""

class Trace:
    def __init__(self):
        """
            <Trace>
            Parses the results of `isnoop', and saves them into
            a list of <Activity> objects
            
            - activities : <list> of <Activity> objects
        """
        self.activities = []
        self.filename_freq = {}
        self.filename_sizemap = {}

    def Parse(self, filename):
        """
            - filename : <String>
                         filename of the file that contains the iosnoop logs
                         e.g.

                         STIME    TIME     DELTA   UID   PID D    BLOCK   SIZE       COMM PATHNAME
                         6430320  6892892  1201    100 15795 R     3808   8192        tar /usr/bin/eject
                         6503020  6900020  1192    100 15795 R    35904   6144        tar /usr/bin/eject
                         6603034  7030042  4121    100 15795 R    39828   6144        tar /usr/bin/env
                         6663040  7000000  1326    100 15795 R     3872   8192        tar /usr/bin/expr
                                 
            - return type : <void>
        """
        f = open(filename, 'r')
        for i,line in enumerate(f):
            # don't look at the first line, it's the header line
            if i==0:
                continue
            activity = Activity()
            if activity.Parse(line):
                self.activities.append( activity )
                # Improve here by doing try / except instead of going through linearly
                try:
                    self.filename_freq[activity.pathname] += 1
                except  KeyError:
                    self.filename_freq[activity.pathname] = 1
                    self.filename_sizemap[activity.pathname] = activity.size


class Activity:
    def __init__(self):
        """
            <Activity>
            Activity object stores the information of a single activity
            (which includes UID, PID, R/W, etc.)
        """
        pass

    def Parse(self, line):
        """
            Parses the line from the iosnoop logs and saves it into
            object variables.
            
            e.g.
            self.UID   :   0
            self.PID   :   15795
            self.D     :   'R'
            self.BLOCK :   3808
            self.SIZE  :   8192
            selef.PATH :   '/usr/bin/eject'
            
            - line : <String>
                     A line from the iosnoop logs
                     e.g.
                     '100 15795 R     3808   8192        tar /usr/bin/eject'

            - return type : <void>
        """
    
        row = line.split()

        #[user_id, process_id, access_type, Block, size, command, pathname]

        try:
            self.start_time = int(row[0])
            self.end_time = int(row[1])
            self.delta = int(row[2])
            self.user_id = int(row[3])   # Device ID
            self.process_id = int(row[4])   # Process ID
            self.access_type = row[5]     # Read/Write
            self.block = row[6]
            self.size = int(row[7])
            self.command = row[8]
            self.pathname = row[9]
        except Exception, e:
            print "Tracer line inccorrectly formated, parsing failed.  Failure due to error %s" % e
            print "line was:"
            print line
            print "continuing to next line"
            # raise RuntimeError("Tracer line inccorrectly formated, parsing failed.  Failure due to error %s" % e)
            return False
        return True

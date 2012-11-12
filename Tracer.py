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

    def Parse(self, filename):
        """
            - filename : <String>
                         filename of the file that contains the iosnoop logs
                         e.g.
                         UID   PID D    BLOCK   SIZE       COMM PATHNAME
                         100 15795 R     3808   8192        tar /usr/bin/eject
                         100 15795 R    35904   6144        tar /usr/bin/eject
                         100 15795 R    39828   6144        tar /usr/bin/env
                         100 15795 R     3872   8192        tar /usr/bin/expr
                         
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
            self.user_id = int(row[0])   # Device ID
            self.process_id = int(row[1])   # Process ID
            self.access_type = row[2]     # Read/Write
            self.block = row[3]
            self.size = row[4]
            self.command = row[5]
            self.pathname = row[6]
        except Exception, e:
            print "Tracer line inccorrectly formated, parsing failed.  Failure due to error %s" % e
            print "line was:"
            print line
            print "continuing to next line"
            # raise RuntimeError("Tracer line inccorrectly formated, parsing failed.  Failure due to error %s" % e)
            return False
        return True

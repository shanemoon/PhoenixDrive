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
        for line in f:
            activity = Activity()
            activity.Parse(line)
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
        self.UID = row[0]   # Device ID
        self.PID = row[1]   # Process ID
        self.D = row[2]     # Read/Write

        # NEED TO CONTINUE HERE ...
        # NEED TO THROW A PARSE_ERROR WHEN THE INPUT LINE IS NOT
        # FORMATTED CORRECTLY
        pass



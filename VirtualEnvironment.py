"""
    Filename    : VirtualEnvironment.py
    Authors     : Shane Moon, <YOUR_NAME>
    Last Update : November 11, 2012
    Description : 
"""


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

        if activity.access_type == 'R':
            self.ReadFile()
        elif activity.access_type == 'W':
            self.WriteFile()
        else:
            # NEED TO HANDLE ERROR HERE
            pass

    def ReadFile(self):
        pass

    def WriteFile(self):
        pass


class HDD(VirtualEnvironment):
    def __init__(self):
        VirtualEnvironment.__init__(self)

    def ReadFile(self):
        print "Read file on the virtual HDD environment"

    def WriteFile(self):
        print "Write file on the virtual HDD environment"



class SSD(VirtualEnvironment):
    def __init__(self):
        VirtualEnvironment.__init__(self)

    def ReadFile(self):
        print "Read file on the virtual SSD environment"

    def WriteFile(self):
        print "Write file on the virtual SSD environment"

        

class PD(VirtualEnvironment):
    def __init__(self):
        VirtualEnvironment.__init__(self)

    def ReadFile(self):
        print "Read file on the virtual Phoenix Drive environment"

    def WriteFile(self):
        print "Write file on the virtual Phoenix Drive environment"

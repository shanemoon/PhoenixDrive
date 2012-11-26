"""
    Filename    : Simulator.py
    Authors     : Shane Moon, <YOUR_NAME>
    Last Update : November 11, 2012
    Description : 
"""

# Please run ./run.sh to execute the simulation

from Tracer import *
from VirtualEnvironment import *

class Simulator:
    def __init__(self, traces, env):
        """
            <Simulator>
            Given the virtual environment and the traces data,
            it performs the simulation and reports the result.

            - traces : A <list> of <Trace> objects. ** refer to Tracer.py **
                       Each <Trace> object has 'activities', which is a
                       <list> of <Acitivty> objects.
                       
            - env : Class object. It can be either:
                    <HDD>, <SSD>, or <PD> (Phoenix Drive).
        """
        self.traces = traces
        self.env = env

    def Simulate(self):
        for trace in self.traces:
            for activity in trace.activities:
                # Passes the <Activity> object to the given
                # <VirtualEnvironment>, which will handle it accordingly.
                self.env.HandleActivity( activity )

            # -------------------------- TO_DO --------------------------
            # After the corresponding environment handles the activities,
            # it should somehow report the result back to the simulator.
            # This result should be saved in or returned to the <Simulator>,
            # so that <Simulator>.Analyze() can analyze the result.

    def Analyze(self):
        print "Analyzing the result of the simulation"
        self.env.reporter.display_results()
        
    
if __name__ == '__main__':

    # Parse Traces
    trace1 = Trace()
    trace1.Parse('snoop2') 

    trace2 = Trace()
    trace2.Parse('snoop2') 

    traces = [trace1]

    # Initiate Simulators
    hdd_simulator = Simulator( traces, HDD() )
    ssd_simulator = Simulator( traces, SSD() )
    pd_simulator = Simulator( traces, PD() )

    # Run Simulators
    hdd_simulator.Simulate()
    ssd_simulator.Simulate()
    pd_simulator.Simulate()

    hdd_simulator.Analyze()
    ssd_simulator.Analyze()
    pd_simulator.Analyze()

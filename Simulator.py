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

def generate_phoenix_curve_plot(io_time,ssd_sizes):
    fig = plt.figure(figsize=(9,9))
    fig.suptitle("Phoenix Curve")
    io_time_plot = fig.add_subplot(2,1,1)
    io_time_plot.set_title("Total i/o vs. ssd buffer size")
    io_time_plot.set_xlabel("ssd sixe (Gb)")
    io_time_plot.set_ylabel("Cumulative i/o Times (sec)")
    print(len(io_time) )
    print(len(ssd_sizes) )
    io_time_plot.plot(ssd_sizes,io_time)
    plt.savefig("phoenix_curve.png")


def Compare(filename, reporters):

        fig = plt.figure(figsize=(9,9))
        fig.suptitle("Comparision Result")

        writes = fig.add_subplot(2,1,1)
        writes.set_title("Writes")
        writes.set_xlabel("Timestamp (sec)")
        writes.set_ylabel("Cumulative Write Times (sec)")

        reads = fig.add_subplot(2,1,2)
        reads.set_title("Reads")
        reads.set_xlabel("Timestamp (sec)")
        reads.set_ylabel("Cumulative Read Times (sec)")

        writes.hold(True)
        reads.hold(True)
        for reporter in reporters:
            writes.plot(reporter.write_start_times, reporter.write_durations_cumulative, label=reporter.drive_type)
            reads.plot(reporter.read_start_times, reporter.read_durations_cumulative, label=reporter.drive_type)

        writes.legend()
        reads.legend()
        plt.savefig(filename)

def phoenix_curve_study(traces):
    pd_io_times = []   
    # Initiate Simulators
    ssd_max_size = 128
    hdd_max_size = 1024
    ssd_sizes = range(0,ssd_max_size,10) + [ssd_max_size]
    print(ssd_sizes)
    hdd_step = float(hdd_max_size)/ssd_max_size    
    for ssd_size in ssd_sizes:
        hdd_size = hdd_max_size - (ssd_size*hdd_step)
        print("initializing simulators")
        pd_simulator = Simulator( traces, PD(hdd_size,ssd_size) )
        print("running pd")
        pd_simulator.Simulate()
        print("saving results")
        pd_io_times.append(pd_simulator.env.reporter.total_io_time)
    print(len(pd_io_times) )
    print(len(ssd_sizes) )
    generate_phoenix_curve_plot(pd_io_times,ssd_sizes)

def drive_type_comparitive_study(traces):
     # Initiate Simulators
    hdd_simulator = Simulator( traces, HDD(1024) )
    ssd_simulator = Simulator( traces, SSD(128) )
    pd_simulator = Simulator( traces, PD(300,64) )

    # Run Simulators
    hdd_simulator.Simulate()
    ssd_simulator.Simulate()
    pd_simulator.Simulate()

    # Analyze and Compare the Results
    Compare('comparison.png',
            [hdd_simulator.env.reporter,
             ssd_simulator.env.reporter,
             pd_simulator.env.reporter])
    
if __name__ == '__main__':

    # Parse Traces
    print("parsing the snoop")
    trace1 = Trace()
    trace1.Parse('snoop2') 

    # trace2 = Trace()
    # trace2.Parse('snoop2') 

    traces = [trace1]

    drive_type_comparitive_study(traces)
    # phoenix_curve_study(traces)

    
    
    

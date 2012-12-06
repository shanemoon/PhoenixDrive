"""
    Filename    : Simulator.py
    Authors     : Shane Moon, <YOUR_NAME>
    Last Update : November 11, 2012
    Description : 
"""

# Please run ./run.sh to execute the simulation

from Tracer import *
from VirtualEnvironment import *

   
class PhoenixConfiguration:
    def __init__(self, budget, sizes):
        """
            budget : dollar amount for this configuration
            sizes : <List> of <Tuple>s of HDD_SIZE and SSD_SIZE
                e.g. sizes = [ ( 0, 128), (1024, 0), ... ]
        """
        self.budget = budget
        self.sizes = sizes

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

def generate_phoenix_curve_plot(io_time, ssd_sizes):
    fig = plt.figure(figsize=(9,9))
    fig.suptitle("Phoenix Curve")
    io_time_plot = fig.add_subplot(2,1,1)
    io_time_plot.set_title("Total I/O vs. ssd buffer size")
    io_time_plot.set_xlabel("ssd size (GB)")
    io_time_plot.set_ylabel("Cumulative I/O Times (sec)")
    print(len(io_time) )
    print(len(ssd_sizes) )
    io_time_plot.plot(ssd_sizes,io_time)
    plt.savefig("phoenix_curve.png")

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


def generate_phoenix_curve_plot_with_real_data(list_io_speeds, pcs):
    """
        pd_io_speeds : <List> of <io_speeds>
        pc : An instance of <PhoenixConfiguration>
    """
    
    filename = 'PhoenixCurve_RealData.png'

    fig = plt.figure(figsize=(9,6))
    fig.suptitle("Phoenix Curve with Real Data (given David's Traces)")

    io_time_plot = fig.add_subplot(1,1,1)
    io_time_plot.set_title("Average I/O Speed vs. Total Disk Size (SSD + HDD)")
    io_time_plot.set_xlabel("Disk Size (SSD + HDD) (GB)")
    io_time_plot.set_ylabel("Average I/O Speed (# of I/O Operations per ms)")
    io_time_plot.hold(True)
    
    for i in range(len(pcs)):
        pc = pcs[i]
        pd_io_speeds = list_io_speeds[i]
        total_sizes = [pc_size[0] + pc_size[1] for pc_size in pc.sizes]
        
        print("Length of io_time array:", len(pd_io_speeds) )
        print("Length of total_sizes array:", len(total_sizes) )
        io_time_plot.plot( total_sizes, pd_io_speeds, label="Budget: $%s" % pc.budget )
    io_time_plot.legend()
    plt.savefig(filename)

def phoenix_curve_study_with_real_data(traces):
    """
        phoenix_configurations : <List> of <PhoenixConfigration>s
        * Please refer to the <PhoenixConfiguration> class definition above.
    """
    pc1 = PhoenixConfiguration(100, [ (0, 128), (300, 64), (1024, 0) ])
    pc2 = PhoenixConfiguration(300, [ (0, 160), (1024, 240), (3000, 0) ])
    pc3 = PhoenixConfiguration(500, [ (0, 480), (2000, 160), (4000, 0) ])
    pcs = [pc1, pc2, pc3]
    list_io_speeds = []

    for pc in pcs:
        pd_io_speeds = []
        print("Running for Phoneix Configuration with Budget %s" % pc.budget)
        for size in pc.sizes:
            hdd_size = size[0]
            ssd_size = size[1]
            print("Initializing simulators")
            pd_simulator = Simulator( traces, PD(hdd_size, ssd_size) )
            print("Running Phoenix Drive")
            pd_simulator.Simulate()
            print("Saving Results")

            # Average Speed = (# of i/o Operations) / (# of Total Cumulative I/O Time in miliseconds)
            speed = pd_simulator.env.reporter.total_num_activity / float(pd_simulator.env.reporter.total_io_time) / 1000.0
            pd_io_speeds.append(speed)
        print(len(pd_io_speeds) )
        print(len(pc.sizes) )
        list_io_speeds.append( pd_io_speeds )
        
    generate_phoenix_curve_plot_with_real_data(list_io_speeds, pcs)
    
    
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

    # drive_type_comparitive_study(traces)
    # phoenix_curve_study(traces)
    phoenix_curve_study_with_real_data(traces)

    
    
    

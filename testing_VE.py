import Tracer
import VirtualEnvironment
t = Tracer.Trace()
t.Parse("snoop2")
hdd = VirtualEnvironment.HDD()
for activity in t.activities:
	hdd.HandleActivity(activity)	

hdd.reporter.display_results()



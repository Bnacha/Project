import os, sys



if 'SUMO_HOME' in os.environ:
	tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
	sys.path.append(tools)
else:   
	sys.exit("please declare environment variable 'SUMO_HOME'")

sumo_tools = r"/home/phop/work/sumo-0.32.0/tools"

sys.path.append(sumo_tools)

sumoBinary = "/usr/bin/sumo-gui"
sumoCmd = [sumoBinary, "-c", "/home/phop/work/Project/map/map.sumo.cfg"]


import traci

print 'START TRACI...'
traci.start(sumoCmd)


step = 0
while step < 1000:
	traci.simulationStep()
	offset = 20
	if(step%(offset*4)==(offset*0)):
		print "STATE 1"
		traci.trafficlights.setRedYellowGreenState("gneJ1", "GGGGrrrrGGGGrrrr")
	if(step%(offset*4)==(offset*1)):
		print "STATE 2"
		traci.trafficlights.setRedYellowGreenState("gneJ1", "rrrrGGGGrrrrGGGG")
	if(step%(offset*4)==(offset*2)):
		print "STATE 3"
		traci.trafficlights.setRedYellowGreenState("gneJ1", "GGGGrrrrGGGGrrrr")
	if(step%(offset*4)==(offset*3)):
		print "STATE 4"
		traci.trafficlights.setRedYellowGreenState("gneJ1", "rrrrGGGGrrrrGGGG")
	step += 1

traci.close()
print 'FINISH'

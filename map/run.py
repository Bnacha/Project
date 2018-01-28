import os, sys

if 'SUMO_HOME' in os.environ:
	tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
	sys.path.append(tools)
else:   
	sys.exit("please declare environment variable 'SUMO_HOME'")

sumo_tools = r"/home/phop/work/sumo-0.31.0/tools"

sys.path.append(sumo_tools)

sumoBinary = "/usr/bin/sumo-gui"
sumoCmd = [sumoBinary, "-c", "/home/phop/work/map/map.sumo.cfg"]


import traci

print '======START====='
traci.start(sumoCmd)


step = 0
while step < 5000:
	
	traci.simulationStep()
	offset = 200
#	if(step%(offset*4)==(offset*0)):
#		print "East Advance Green"
#		traci.trafficlights.setRedYellowGreenState("267870589", "GGggrrrrGGrrrrrr")
#	if(step%(offset*4)==(offset*1)):
#		print "North Advance Green"
#		traci.trafficlights.setRedYellowGreenState("267870589", "rrrrGGggrrrrGGrr")
#	if(step%(offset*4)==(offset*2)):
#		print "West Advance Green"
#		traci.trafficlights.setRedYellowGreenState("267870589", "GGrrrrrrGGggrrrr")
#	if(step%(offset*4)==(offset*3)):
#		print "South Advance Green"
#		traci.trafficlights.setRedYellowGreenState("267870589", "rrrrGGrrrrrrGGgg")

	step += 0.1

traci.close()
print '======FINISH====='

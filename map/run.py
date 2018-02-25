#!/usr/bin/env python
#-*-coding: utf-8 -*-

'''
'''

import os, sys
import numpy as np
from gym import spaces


# Set path
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
    sumoBinary = "/usr/bin/sumo-gui"
    sumoCmd = [sumoBinary, "-c", "/home/phop/work/Project/map/map.sumo.cfg"]
else:   
    sys.exit("please declare environment variable 'SUMO_HOME'")


import traci


class Env(object):
    '''
        This class is the abstract environment class is used by all agents
    '''
    
    sumoBinary = "/usr/bin/sumo"
    sumoCmd = [sumoBinary, "-c", "/home/phop/work/Project/map/map.sumo.cfg"]
    
    
    action_space = None
    observation_space = spaces.Box(low = 0, high = 1000, shape = (1,19), dtype = np.float32)
    reward_range = (-np.inf, np.inf)
    
    TLSID = "3"
    
    possible_actions = ['r', 'g', 'G', 'y']
    edges = []
    
    
    def __init__(self, lanes):
        self.lanes = lanes 
    
    

    def step(self, action):
        '''
            Run one timestep of the environment's dynamics.
            Args:
                action (object): an action provided by the environment
            Returns:
                observation (object): agent's observation of the current environment
                reward (float) : amount of reward returned after previous action
                info (dict): contains auxiliary diagnostic information (helpful for debugging, and sometimes learning)
        '''

        traci.simulationStep()
        
        # read global info
        arrived_vehicles_in_last_step = traci.simulation.getArrivedNumber()
        departed_vehicles_in_last_step = traci.simulation.getDepartedNumber()
        current_simulation_time_ms = traci.simulation.getCurrentTime()
        vehicles_started_to_teleport = traci.simulation.getStartingTeleportNumber()
        vehicles_ended_teleport = traci.simulation.getEndingTeleportNumber()
        vehicles_still_expected = traci.simulation.getMinExpectedNumber()
        observation = [arrived_vehicles_in_last_step, departed_vehicles_in_last_step,
                       current_simulation_time_ms, vehicles_started_to_teleport,
                       vehicles_ended_teleport, vehicles_still_expected]
        
        #traci.trafficlight.setRedYellowGreenState(self.TLSID, action)
        
        reward = 0
        avg_edge_values = np.zeros(8)
        
        for e_id in self.edges:
            edge_values = [
                traci.edge.getWaitingTime(e_id),
                traci.edge.getFuelConsumption(e_id),
                traci.edge.getLastStepMeanSpeed(e_id),
                traci.edge.getLastStepOccupancy(e_id),
                traci.edge.getLastStepLength(e_id),
                traci.edge.getTraveltime(e_id),
                traci.edge.getLastStepVehicleNumber(e_id),
                traci.edge.getLastStepHaltingNumber(e_id)
            ]
            # scale using the amount of vehicles
            if edge_values[6] > 0:
                edge_values[0] /= edge_values[6]
                edge_values[1] /= edge_values[6]   
            avg_edge_values = np.add(avg_edge_values, edge_values)
        
        avg_edge_values /= len(self.edges)

        observation.extend(avg_edge_values)

        waitingFactor = -avg_edge_values[0] / 10
        if waitingFactor == 0:
            waitingFactor += 1
        fuel_factor = -avg_edge_values[1]
        green_factor = 7 * ( action.count("g") + action.count("G") ) / self.lanes
        yellow_factor = -0.5 * action.count("y") / self.lanes
        red_factor= -2 * action.count("r") / self.lanes
        reward += waitingFactor + fuel_factor + green_factor + yellow_factor+red_factor

        info = {'waitingFactor': waitingFactor, 'fuel_factor':fuel_factor, 'green_factor':green_factor, 'yellow_factor':yellow_factor, 'red_factor':red_factor, 'total_reward':reward}
        
        return observation, reward, info
        
    
    def reset(self):
        '''
            Resets the state of the environment and returns an initial observation.
            Returns:
                observation (object): the initial observation of the space. (Initial reward is assumed to be 0.)
        '''
        print 'TRACI START...'
        
        traci.start(self.sumoCmd)
        
        
        lanes = traci.trafficlight.getControlledLanes(self.TLSID)

        for lane in lanes:
            self.edges.append(traci.lane.getEdgeID(lane))
           

       
    def close(self):
        '''
            Ceanup environment
        '''
        print 'TRACI CLOSE...'
        
        traci.close()   


e = Env(16)
e.reset()
text_file = open("output.csv", "w")

for i in range(1, 1000):
    result = e.step('GGGgrrrrGGGgrrrr')
    text_file.write(str(i) + ',' + str(result[2]['total_reward']) + ',\n')
    
e.close()

text_file.close()


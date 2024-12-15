'''
Model of an agent
'''

import numpy as np
from .utils import Angle, Coords

class Agent:
    def __init__(self, id, type, x, y, vx, vy, ax, ay, yaw, dyaw, implied):
        self.id = id
        self.type = type
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay
        self.yaw = yaw
        self.dyaw = dyaw
        self.implied = implied

        # code is the number in the end of the agent id, for "scene-000001-1", the code is "1"
        # it is easier to identify agents with their code in plots
        self.code = id.split('-')[-1]

        # convert cartesian coordinates to polar coordinates and remember them
        self.r, self.rtheta = Coords.polar(x, y)
        self.vr, self.vtheta = Coords.polar(vx, vy)
        self.ar, self.atheta = Coords.polar(ax, ay)

    def fromRawSeries(series, implied):
        return Agent(
            series['TRACK_ID'],
            series['OBJECT_TYPE'],
            series['X'],
            series['Y'],
            series['V_X'],
            series['V_Y'],
            series['A_X'],
            series['A_Y'],
            Angle.normalize(series['YAW']+90),
            series['DYAW'],
            implied,
        )
    
    def copy(self):
        return Agent(self.id, self.type, self.x, self.y, self.vx, self.vy, self.ax, self.ay, self.yaw, self.dyaw, self.implied)

    def distance_to(self, agent):
        dx = self.x - agent.x
        dy = self.y - agent.y
        distance = np.sqrt(dx ** 2 + dy ** 2)
        return distance
    
    def polar_coords_relative_to(self, agent):
        dx = self.x - agent.x
        dy = self.y - agent.y
        distance, angle = Coords.polar(dx, dy)
        angle = Angle.normalize(angle - agent.yaw)
        return distance, angle

    '''Abstract Relations'''

    def front_distance_relative_to(self, agent):
        '''Front is positive and back is negative'''
        distance, angle = self.polar_coords_relative_to(agent)
        return distance * Angle.cos(angle)
    
    def side_distance_relative_to(self, agent):
        '''Right is positive and left is negative'''
        distance, angle = self.polar_coords_relative_to(agent)
        return - distance * Angle.sin(angle)
    
    def front_and_side_distance_relative_to(self, agent):
        '''Front, right is positive; back, left is negative'''
        distance, angle = self.polar_coords_relative_to(agent)
        return distance * Angle.cos(angle), - distance * Angle.sin(angle)
    
    def front_velocity_relative_to(self, agent):
        '''Front is positive and back is negative'''
        angle = Angle.normalize(self.vtheta - agent.yaw)
        return self.vr * Angle.cos(angle)
    
    def front_acceleration_relative_to(self, agent):
        '''Front is positive and back is negative'''
        angle = Angle.normalize(self.atheta - agent.yaw)
        return self.ar * Angle.cos(angle)
    
    def is_very_near(self, agent):
        if self.distance_to(agent) > 4: # prune irrelevant agents
            return False
        
        front_distance, side_distance = self.front_and_side_distance_relative_to(agent)

        return abs(front_distance) < 3.5 and abs(side_distance) < 1.5
    
    # def is_leading(self, agent):
    #     front_distance, side_distance = self.front_and_side_distance_relative_to(agent)

    #     return 0 < front_distance < 5 and abs(side_distance) < 2
    
    def is_in_front_of(self, agent):
        front_distance, side_distance = self.front_and_side_distance_relative_to(agent)

        return front_distance > side_distance ** 2
    
    def is_directly_in_front_of(self, agent):
        front_distance, side_distance = self.front_and_side_distance_relative_to(agent)

        return 0 < front_distance < 15 and front_distance > side_distance ** 2 * 2
    
    def __str__(self):
        return f"[ Agent({self.code}) at ({self.x:.2f}, {self.y:.2f}) ]"
    
    def __repr__(self):
        return self.__str__()
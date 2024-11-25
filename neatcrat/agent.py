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

    def distance(agent1, agent2):
        return np.sqrt((agent1.x-agent2.x) ** 2 + (agent1.y-agent2.y) ** 2)
    
    '''Abstract Relations'''

    def front_distance_relative_to(self, agent):
        '''Front is positive and back is negative'''
        dx = self.x - agent.x
        dy = self.y - agent.y
        distance, angle = Coords.polar(dx, dy)
        angle = Angle.normalize(angle - agent.yaw)
        return distance * Angle.cos(angle)
    
    def side_distance_relative_to(self, agent):
        '''Right is positive and left is negative'''
        dx = self.x - agent.x
        dy = self.y - agent.y
        distance, angle = Coords.polar(dx, dy)
        angle = Angle.normalize(angle - agent.yaw)
        return - distance * Angle.sin(angle)
    
    def is_on_the_face_of(self, agent):
        front_distance = self.front_distance_relative_to(agent)
        side_distance = self.side_distance_relative_to(agent)

        return 0 < front_distance < 2.5 and abs(side_distance) < 1.5
    
    def is_leading(self, agent):
        front_distance = self.front_distance_relative_to(agent)
        side_distance = self.side_distance_relative_to(agent)

        return 0 < front_distance < 5 and abs(side_distance) < 2
    
    def is_in_front_of(self, agent):
        front_distance = self.front_distance_relative_to(agent)
        side_distance = self.side_distance_relative_to(agent)

        return front_distance > side_distance ** 2
    
    def __str__(self):
        return f"[ Agent({self.code}) at ({self.x}, {self.y}) ]"
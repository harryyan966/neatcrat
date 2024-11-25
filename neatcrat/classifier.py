'''
Classifies scene
'''

import numpy as np

from .agent import Agent
from .constants import *
from .scene import Scene

class SceneClassifier:
    def __init__(self, scene: Scene):
        self.scene = scene
        self.agent_finder = AgentFinder(scene)

    def classify_scene(self) -> list[str]:
        '''Returns third class label names of each frame in the scene'''

        result = []

        # for each time stamp
        for ti in range(SCENE_LENGTH):
            second_class = self.scene.second_class[ti]

            # depending on the second class of this frame, use different functions to classify the frame
            if second_class == '1.1 InLane': result.append(self.classify_inlane_frame(ti))
            elif second_class == '2.1 StopAndWait': result.append(self.classify_stop_and_wait_frame(ti))
            elif second_class == '2.4 GoStraight': result.append(self.classify_go_straight_frame(ti))
            elif second_class == '2.5 TurnLeft': result.append(self.classify_turn_left_frame(ti))
            elif second_class == '2.6 TurnRight': result.append(self.classify_turn_right_frame(ti))
            elif second_class == '2.7 UTurn': result.append(self.classify_uturn_frame(ti))
            else: result.append(THIRD_CLASS_NAMES_INVALID)
        
        return result

    ''' Primary Helpers, returns third class label names '''

    def classify_inlane_frame(self, ti):
        options = {
            'leadv0': '1.1.5 LeadVehicleStppoed',
            'leada0': '1.1.1 LeadVehicleConstant',
            'leada-': '1.1.4 LeadVehicleDecelerating',
            'leada+': '1.1.6 LeadVehicleAccelerating',
            'cutout': '1.1.2 LeadVehicleCutOut',
            'cutin': '1.1.3 VehicleCutInAhead',
        }

        leading = AgentFinder.find_nearest_agent_on_ego_trajectory(ti)
        if leading is not None:
            pass # TODO

        
        return 
    
    def classify_stop_and_wait_frame(self, ti):
        return
    
    def classify_go_straight_frame(self, ti):
        return
    
    def classify_turn_left_frame(self, ti):
        return
    
    def classify_turn_right_frame(self, ti):
        return
    
    def classify_uturn_frame(self, ti):
        return
    
    ''' Secondary Helpers '''
    
    def simple_leading(self, traj1, traj2) -> bool:
        return
    
    def trajectory_focused_leading(self, traj1, traj2) -> bool:
        return
    
    def orientation_focused_leading(self, traj1, traj2) -> bool:
        return
    
    def before_left_cutin(self, traj1, traj2) -> bool:
        return
    
    def after_left_cutin(self, traj1, traj2) -> bool:
        return
    
    def before_right_cutin(self, traj1, traj2) -> bool:
        return
    
    def after_right_cutin(self, traj1, traj2) -> bool:
        return
    
    def before_left_cutout(self, traj1, traj2) -> bool:
        return
    
    def after_left_cutout(self, traj1, traj2) -> bool:
        return
    
    def before_right_cutout(self, traj1, traj2) -> bool:
        return

    def after_right_cutout(self, traj1, traj2) -> bool:
        return
    
    def left_turn_leading(self, traj1, traj2) -> bool:
        return
    
    def right_turn_leading(self, traj1, traj2) -> bool:
        return
    
    def left_turn_cutin_before(self, traj1, traj2) -> bool:
        return
    
    def left_turn_cutin_after(self, traj1, traj2) -> bool:
        return
    
    def right_turn_cutin_before(self, traj1, traj2) -> bool:
        return
    
    def right_turn_cutin_after(self, traj1, traj2) -> bool:
        return
    

class AgentFinder:
    def __init__(self, scene: Scene):
        self.scene = scene

    def distance_between(agent1, agent2):
        return np.sqrt((agent1.x - agent2.x) ** 2 + (agent1.y - agent2.y) ** 2)
    
    def find_nearest_agent_on_ego_trajectory(self, ti):
        '''Find the nearest agent on the way of the ego'''

        max_extrapolation = 5

        while ti < max(ti + max_extrapolation, SCENE_LENGTH):

            # get ego at this timestamp
            ego_anchor = self.scene.trajectories['ego'][ti]

            # return any agent that is extremely close to the current agent
            for agent in self.scene.snapshot(ti):
                if agent.id == 'ego':
                    continue
                if agent.is_on_the_face_of(ego_anchor):
                    return agent
            
            ti += 1
        
        return None


class TrajectoryPatternMatcher:
    def lead_constant(t1: list[Agent], t2: list[Agent]):
        '''Old idea, theoretically shouldn't work in some cases, can be removed'''

        if len(t1) != len(t2):
            return False
        
        for i in range(len(t1)):
            a1 = t1[i]; a2 = t2[i]

            if abs(a1.yaw - a2.yaw) > 20:
                return False
            
            # move both trajectories to the origin
            a1 = a1.copy(); a2 = a2.copy()
            a1.x -= t1[0].x; a1.y -= t1[0].y; a2.x -= t2[0].x; a2.y -= t2[0].y

            if Agent.distance(a1, a2) > 2:
                return False
        
        return True
            
        

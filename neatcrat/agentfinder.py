'''
Finds specific agents in a scene
'''

from .constants import SCENE_LENGTH
from .scene import Scene

class AgentFinder:
    TURNING_EXTRAPOLATION_RANGE = 10

    def __init__(self, scene: Scene):
        self.scene = scene
    
    def get_ego(self, ti):
        return self.scene.trajectories['ego'][ti]
    
    def get_front(self, ti, max_extrapolation=40, use_direct_front=True):
        '''Find the nearest agent on the way of the ego'''

        snapshot = self.scene.snapshot(ti)

        ego_ti = ti + 1

        # for a given scene, move ego across the time dimension
        while ego_ti < ti + max_extrapolation:

            # get ego at this future timestamp
            ego_anchor = self.get_ego(ego_ti)

            # ignore agents far from ego
            close_agents = [agent for agent in snapshot if \
                agent.distance_to(ego_anchor) < 5 \
                and agent.id != 'ego' \
            ]

            # sort snapshot from nearest to farthest
            close_agents.sort(key=lambda agent: agent.distance_to(ego_anchor))

            # move from nearest to farthest agent
            for agent in close_agents:

                # return the first agent that's on track
                # TODO?: change to agent.is_in_track_of(ego_anchor, next_ego_anchor): get angle, use angle threshold
                if agent.is_very_near(ego_anchor):
                    return agent
            
            ego_ti += 1
        
        # if nothing is found, find an agent in the direct front
        if use_direct_front:
            ego = self.get_ego(ti)
            snapshot.sort(key=lambda agent: agent.front_distance_relative_to(ego))
            for agent in snapshot:
                if agent.is_directly_in_front_of(ego):
                    return agent
        
        return None
    
    # used for classifying gostraight, turnleft, and turnright
    # high coupling for syntactic sugar
    def get_turning_front(self, ti):
        return self.get_front(ti, max_extrapolation=self.TURNING_EXTRAPOLATION_RANGE, use_direct_front=False)


'''
Classifies scene
'''

import numpy as np

from .agent import Agent
from .agentfinder import AgentFinder
from .constants import *
from .scene import Scene

class SceneClassifier:
    # inlane
    SMALL_VELOCITY_THRESHOLD = 3

    # inlane
    DV_THRESHOLD_FOR_ACCELERATION = 2
    DV_THRESHOLD_FOR_DECELERATION = -2

    # inlane
    CUTOUT_BACKWARD_DELTA = 1
    CUTOUT_FORWARD_DELTA = 2
    CUTIN_BACKWARD_DELTA = 1
    CUTIN_FORWARD_DELTA = 4

    # wait
    PEDESTRIANS_CROSS_BACKWARD_DELTA = 3
    PEDESTRIANS_CROSS_FORWARD_DELTA = 3

    # straight left right
    CROSS_BACKWARD_DELTA = 1
    CROSS_FORWARD_DELTA = 1

    # initialize object with scene
    def __init__(self, scene: Scene):
        self.scene = scene
        self.finder = AgentFinder(scene)

    # "main function"
    def classify_scene(self) -> list[str]:
        '''Returns third class label names of each frame in the scene'''

        labels = []

        # make contiguous sections with the same second-level labels
        sections = []

        prev_second_class = None

        for ti in range(SCENE_LENGTH):
            second_class = self.scene.second_class[ti]

            # if a new section is introduced, create a new section
            if second_class != prev_second_class:
                sections.append((second_class, []))
                prev_second_class = second_class
            
            # append the current timestamp index in the last section
            sections[-1][1].append(ti)

        # for each section
        for second_class, tis in sections:

            # depending on the second class of this section, use different functions to classify the frame
            if second_class == '1.1 InLane': labels += self.classify_inlane_section(tis)
            elif second_class == '2.1 StopAndWait': labels += self.classify_stop_and_wait_section(tis)
            elif second_class == '2.4 GoStraight': labels += self.classify_go_straight_section(tis)
            elif second_class == '2.5 TurnLeft': labels += self.classify_turn_left_section(tis)
            elif second_class == '2.6 TurnRight': labels += self.classify_turn_right_section(tis)
            elif second_class == '2.7 UTurn': labels += self.classify_uturn_section(tis)
            else: labels += [INVALID3] * len(tis)
        
        return labels

    ''' section classifiers for specific second class labels '''

    # inlane section classifier
    def classify_inlane_section(self, tis):
        n = len(tis)
        fronts = [self.finder.get_front(ti) for ti in tis]
        labels = [INVALID3] * n

        # for i from 0 -> n
        i = -1
        while i+1 < n:
            i += 1

            front: Agent = fronts[i]

            # let next front be front if there is no next front, else just let it be next front
            next_front: Agent = front if i == n-1 else fronts[i+1]

            # nothing in front and nothing in next front (nothing ahead)
            if front is None and next_front is None:
                continue

            # same thing in front and next front (leading not changing in the next frame)
            if front is not None and next_front is not None and front.id == next_front.id:
                # (then the next front is irrelevant)
                
                # front has small velocity => stopped
                if abs(front.vr) < self.SMALL_VELOCITY_THRESHOLD:
                    labels[i] = INLANE_LEAD_STOPPED
                    continue
                
                ego: Agent = self.finder.get_ego(tis[i])

                # acceleration and deceleration don't actually depend on acceleration value
                # it instead depends on the difference in velocity between ego and front
                ego_v = ego.front_velocity_relative_to(ego)
                front_v = front.front_velocity_relative_to(ego)
                dv = front_v - ego_v

                # front velocity > ego velocity => accelerating
                if dv > self.DV_THRESHOLD_FOR_ACCELERATION:
                    labels[i] = INLANE_LEAD_ACCELERATE
                    continue
            
                # front velocity < ego velocity => decelerating
                if dv < self.DV_THRESHOLD_FOR_DECELERATION:
                    labels[i] = INLANE_LEAD_DECELERATE
                    continue

                # else (relatively small velocity difference)
                labels[i] = INLANE_LEAD_CONST
            
            # different thing in front and next front
            # front or nextfront = none or front.id != nextfront.id
            else:
                # no lead -> has lead => cutin
                if front is None:
                    cutout = False
                # has lead -> no lead => cutout
                elif next_front is None:
                    cutout = True
                # lead further after lead change => prev lead cutout, vice versa
                else:
                    ego = self.finder.get_ego(tis[i])
                    curr_dist = front.distance_to(ego)

                    next_ego = self.finder.get_ego(tis[i+1])
                    next_dist = next_front.distance_to(next_ego)

                    cutout = next_dist > curr_dist

                if cutout:

                    # set every label from i-mind to i+maxd to cutout
                    mind = -self.CUTOUT_BACKWARD_DELTA
                    maxd = self.CUTOUT_FORWARD_DELTA
                    for di in range(mind, maxd+1):
                        ip = i + di # i_prime = i + delta_i
                        if 0 <= ip < n: # if ip is not out of bounds
                            labels[ip] = INLANE_CUTOUT
                    i += maxd
                
                else: # cutin

                    # set every label from i-mind to i+maxd to cutin
                    mind = -self.CUTIN_BACKWARD_DELTA
                    maxd = self.CUTIN_FORWARD_DELTA
                    for di in range(mind, maxd+1):
                        ip = i + di # i_prime = i + delta_i
                        if 0 <= ip < n: # if ip is not out of bounds
                            labels[ip] = INLANE_CUTIN
                    i += maxd
        
        return labels

    # stop and wait section classifier
    def classify_stop_and_wait_section(self, tis):
        n = len(tis)
        fronts = [self.finder.get_front(ti) for ti in tis]
        labels = [INVALID3] * n

        # for i from 0 -> n
        i = -1
        while i+1 < n:
            i += 1

            front: Agent = fronts[i]

            # nothing in front
            if front is None:
                continue

            # pedestrian or bike in front
            if front.type in [OT_BIKE, OT_PEDESTRIAN]:

                # set everything from i-mind to i-maxd to pedestrians crossing
                mind = -self.PEDESTRIANS_CROSS_BACKWARD_DELTA
                maxd = self.PEDESTRIANS_CROSS_FORWARD_DELTA
                for di in range(mind, maxd+1):
                    ip = i + di # i_prime = i + delta_i
                    if 0 <= ip < n: # if ip is not out of bounds
                        labels[ip] = WAIT_HAS_PEDESTRIANS
                i += maxd
            
            # car in front
            elif front.type == OT_CAR:
                labels[i] = WAIT_HAS_LEAD
                
        return labels
    
    # go straight section classifier
    def classify_go_straight_section(self, tis):
        n = len(tis)
        fronts = [self.finder.get_turning_front(ti) for ti in tis]
        labels = [INVALID3] * n

        # for i from 0 -> n
        i = -1
        while i+1 < n:
            i += 1

            front: Agent = fronts[i]
            next_front: Agent = front if i == n-1 else fronts[i+1]

            # nothing in front (or nothing in front that is crossing with ego)
            if front is None and next_front is None:
                labels[i] = STRAIGHT_NOTHING_AHEAD
                continue

            # same thing in front
            if front is not None and next_front is not None and front.id == next_front.id:
                labels[i] = STRAIGHT_HAS_LEAD
                continue

            # some different agent in front
            # TODO?: check if the different thing is leading or crossing?
            else:
                mind = -self.CROSS_BACKWARD_DELTA
                maxd = self.CROSS_BACKWARD_DELTA
                for di in range(mind, maxd+1):
                    ip = i + di # i_prime = i + delta_i
                    if 0 <= ip < n: # if ip is not out of bounds
                        labels[ip] = STRAIGHT_HAS_CROSS
                i += maxd
        
        return labels
    
    # turn left section classifier
    def classify_turn_left_section(self, tis):
        n = len(tis)
        fronts = [self.finder.get_turning_front(ti) for ti in tis]
        labels = [INVALID3] * n

        for i in range(n):
            front: Agent = fronts[i]
            next_front: Agent = front if i == n-1 else fronts[i+1]

            # nothing in front (or nothing in front that is crossing with ego)
            if front is None and next_front is None:
                labels[i] = LEFT_NOTHING_AHEAD
                continue

            # same thing in front
            if front is not None and next_front is not None and front.id == next_front.id:
                labels[i] = LEFT_HAS_LEAD
                continue
            
            # different thing in front
            # TODO?: check if the different thing is leading or crossing?
            else:
                mind = -self.CROSS_BACKWARD_DELTA
                maxd = self.CROSS_BACKWARD_DELTA
                for di in range(mind, maxd+1):
                    ip = i + di # i_prime = i + delta_i
                    if 0 <= ip < n: # if ip is not out of bounds
                        labels[ip] = LEFT_HAS_CROSS
                i += maxd
        
        return labels
    
    # turn right section classifier
    def classify_turn_right_section(self, tis):
        n = len(tis)
        fronts = [self.finder.get_turning_front(ti) for ti in tis]
        labels = [INVALID3] * n

        for i in range(n):
            front: Agent = fronts[i]
            next_front: Agent = front if i == n-1 else fronts[i+1]

            # nothing in front (or nothing in front that is crossing with ego)
            if front is None and next_front is None:
                labels[i] = RIGHT_NOTHING_AHEAD
                continue

            # same thing in front
            if front is not None and next_front is not None and front.id == next_front.id:
                labels[i] = RIGHT_HAS_LEAD
                continue
            
            # different thing in front
            # TODO?: check if the different thing is leading or crossing?
            else:
                mind = -self.CROSS_BACKWARD_DELTA
                maxd = self.CROSS_BACKWARD_DELTA
                for di in range(mind, maxd+1):
                    ip = i + di # i_prime = i + delta_i
                    if 0 <= ip < n: # if ip is not out of bounds
                        labels[ip] = RIGHT_HAS_CROSS
                i += maxd
        
        return labels
    
    # uturn section classifier
    def classify_uturn_section(self, tis):
        n = len(tis)
        labels = [UTURN_NOTHING_AHEAD] * n
        return labels
    

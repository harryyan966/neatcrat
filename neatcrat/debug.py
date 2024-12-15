'''
To help visualization
'''

from .constants import INVALID3
from .scene import Scene
from .trajectory import Trajectory
from .agent import Agent

class Debug:
    def print_third_class_intervals(scene: Scene):

        # list of label, start, end time
        intervals: list[tuple[str, int, int]] = []
        curr_label = ''
        start = 0

        for ti, third_class in sorted(scene.third_class.items(), key=lambda item: item[0]):

            # a new interval
            if third_class != curr_label:

                # append previous label if it's valid and there IS a previous label
                if curr_label != INVALID3 and ti != 0:
                    intervals.append((curr_label, start, ti))

                # start to record the current label
                start = ti
                curr_label = third_class

        # append last label if it's valid
        if curr_label != INVALID3:
            intervals.append((curr_label, start, len(scene.third_class)))

        # print the intervals
        for label, start, end in intervals:
            if start == end:
                print(f"{label} [{start}]")
            else:
                print(f'{label} [{start} ~ {end}]')
        if len(intervals) == 0:
            print("All Invalid")

    class TranslatedTrajectory:
        def __init__(self, trajectory, dx, dy):
            self.trajectory = trajectory
            self.dx = dx; self.dy = dy

        def __getitem__(self, ti):
            agent = self.trajectory[ti].copy()
            agent.x -= self.dx; agent.y -= self.dy
            return agent
        
    def translate_trajectory(trajectory, dx, dy):
        return Debug.TranslatedTrajectory(trajectory, dx, dy)


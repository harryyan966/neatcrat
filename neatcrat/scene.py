'''
Model of a scene (40-frame long video)
'''

import pandas as pd
from .agent import Agent
from .data import Data
from .trajectory import Trajectory
from .constants import INVALID3, SCENE_LENGTH

class Scene:
    def __init__(self, dfs: list[pd.DataFrame], label_df: pd.DataFrame):

        # "trajectories" maps agent code to its trajectory
        self.trajectories: dict[str, Trajectory] = {}

        # "snapshots" maps timestamp index to a list of agents in that time
        self.snapshots: dict[int, list[Agent]] = {}

        # "...class" maps timestamp index to the classification result
        self.first_class: dict[int, str] = {i: l for i, l in enumerate(label_df['first_class'])}
        self.second_class: dict[int, str] = {i: l for i, l in enumerate(label_df['second_class'])}
        self.third_class: dict[int, str] = {i: l for i, l in enumerate(label_df['third_class'])}

        # make trajectories dictionary from raw dfs
        for ti, df in enumerate(dfs):

            # add all agents at this timestamp to their trajectories
            for _, agent_row in df.iterrows():
                agent: Agent = Agent.fromRawSeries(agent_row, implied=False)
                if agent.code not in self.trajectories:
                    self.trajectories[agent.code] = Trajectory(agent.id, agent.type)
                self.trajectories[agent.code][ti] = agent
        
        # make snapshots from trajectories (currently without interpolation)
        for ti in range(SCENE_LENGTH):
            self.snapshots[ti] = []
            for trajectory in self.trajectories.values():
                # only insert known agents into snapshots
                if ti in trajectory.agents:
                    agent = trajectory[ti]
                    if not agent.implied:
                        self.snapshots[ti].append(trajectory[ti])

            # sort agents from nearest to farthest from ego
            # ego = self.trajectories['ego'][ti]
            # self.snapshots[ti].sort(key=lambda agent: agent.distance_to(ego))

    def from_data(data: Data):
        # init wrapper to convert Data directly to Scene
        return Scene(data.dfs, data.label_df)

    def invalid(self):
        # every scene is invalid
        return all(map(lambda c: c == INVALID3, self.third_class.values()))
    
    def snapshot(self, ti, include_implied=False) -> list[Agent]:
        # gets all agents in this timestamp index

        # # all agents in this timestamp index
        # agents = set()

        # # go over all trajectories
        # for _, trajectory in self.trajectories.items():

        #     # if include implied directly get the agent in this timestamp index
        #     if include_implied:
        #         agents.add(trajectory[ti])
        #     # else if not check if it is in existing agents and decide whether to add it
        #     else:
        #         if ti in trajectory.agents:
        #             agent = trajectory[ti]
        #             if not agent.implied:
        #                 agents.add(agent)
        return self.snapshots[ti]
    
    def __str__(self):
        return str(self.trajectories)
    
    def __repr__(self):
        return self.__str__()

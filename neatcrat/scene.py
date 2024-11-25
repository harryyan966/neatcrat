'''
Model of a scene (40-frame long video)
'''

import pandas as pd
from .agent import Agent
from .data import Data
from .trajectory import Trajectory
from .constants import THIRD_CLASS_NAMES_INVALID

class Scene:
    def __init__(self, dfs: list[pd.DataFrame], label_df: pd.DataFrame):

        # "trajectories" maps agent code to its trajectory
        self.trajectories: dict[str, Trajectory] = {}

        # "...class, ...label" maps timestamp index to the classification result
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

    def from_data(data: Data):
        # init wrapper to convert Data directly to Scene
        return Scene(data.dfs, data.label_df)

    def invalid(self):
        # everything in third_class is invalid
        return all(map(lambda c: c == THIRD_CLASS_NAMES_INVALID, self.third_class.values()))
    
    def snapshot(self, ti, include_implied=False) -> set[Agent]:

        # all agents in this timestamp index
        agents = set()

        # go over all trajectories
        for _, trajectory in self.trajectories.items():

            # if include implied directly get the agent in this timestamp index
            if include_implied:
                agents.add(trajectory[ti])
            # else if not check if it is in existing agents and decide whether to add it
            else:
                if ti in trajectory.agents:
                    agent = trajectory[ti]
                    if not agent.implied:
                        agents.add(agent)

        return agents
    
    def __str__(self):
        return str(self.trajectories)

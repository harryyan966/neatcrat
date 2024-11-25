'''
Model for an agent trajectory

List of ti -> agents, but able to extrapolate

TODO(MID-PRIORITY) ADD RECURSIVE VALIDATION FOR EXTRAPOLATION INSTEAD OF ALLOWING STACK OVERFLOW WHEN THERE IS NOT ENOUGH AGENTS

TODO(MID-PRIORITY) ADD "EXTRAPOLATE WITHIN"

TODO(LOW-PRIORITY) ADD (DETERMINISTIC) NOISE TO EXTRAPOLATION RESULTS TO WEAKEN EXPONENTIAL TRENDS
'''

from .constants import SCENE_LENGTH, SECONDS_PER_FRAME
from .agent import Agent
from .utils import Numbers

class Trajectory:
    EXTRAPOLATION_RANGE = 5

    def __init__(self, id, type, agents=None):
        self.id = id
        self.type = type
        self.agents: dict[int, Agent] = {} if agents is None else agents.copy() # maps timestamp index to agent
    
    def __setitem__(self, ti, agent):
        self.agents[ti] = agent
    
    def __getitem__(self, ti):
        if isinstance(ti, slice):
            return [self[i] for i in range(ti.start, ti.stop)]
        
        elif isinstance(ti, int):
            if ti in self.agents:
                return self.agents[ti]
            if ti < 0:
                extrapolated_agent = self._extrapolate_back(ti)
            elif ti >= SCENE_LENGTH:
                extrapolated_agent = self._extrapolate_front(ti)
            else:
                extrapolated_agent = self._extrapolate_within(ti)
        
            # cache the extrapolated agent
            self.agents[ti] = extrapolated_agent

            return extrapolated_agent
    
    def _extrapolate_back(self, ti):

        # get next agents, closest in the front
        next_agents = [self[temp_ti] for temp_ti in range(ti+1, ti+1+Trajectory.EXTRAPOLATION_RANGE)]
        # self[ti+1 : ti+1+Trajectory.EXTRAPOLATION_RANGE]

        # value = nearest value + backward delta [approx]= nearest value - weighted average of nearest forward deltas
        dyaw = next_agents[0].dyaw - Numbers.weighted_avg(Numbers.deltas(map(lambda agent: agent.dyaw, next_agents)))
        ax = next_agents[0].ax - Numbers.weighted_avg(Numbers.deltas(map(lambda agent: agent.ax, next_agents)))
        ay = next_agents[0].ay - Numbers.weighted_avg(Numbers.deltas(map(lambda agent: agent.ay, next_agents)))

        # yawi = yawf - dyaw * t
        yaw = next_agents[0].yaw - Numbers.weighted_avg([dyaw, next_agents[0].dyaw]) * SECONDS_PER_FRAME

        # vi = vf - a * t
        vx = next_agents[0].vx - Numbers.weighted_avg([ax, next_agents[0].ax]) * SECONDS_PER_FRAME
        vy = next_agents[0].vy - Numbers.weighted_avg([ay, next_agents[0].ay]) * SECONDS_PER_FRAME

        # xi = xf - v * t
        x = next_agents[0].x - Numbers.weighted_avg([vx, next_agents[0].vx]) * SECONDS_PER_FRAME
        y = next_agents[0].y - Numbers.weighted_avg([vy, next_agents[0].vy]) * SECONDS_PER_FRAME

        return Agent(self.id, self.type, x, y, vx, vy, ax, ay, yaw, dyaw, implied=True)

    def _extrapolate_front(self, ti):
        
        # get previous agents, closest in the front
        prev_agents = [self[temp_ti] for temp_ti in range(ti-1, ti-1-Trajectory.EXTRAPOLATION_RANGE, -1)]

        # value = nearest value + forward delta [approx]= nearest value + weighted average of forward deltas
        dyaw = prev_agents[0].dyaw + Numbers.weighted_avg(Numbers.deltas(map(lambda agent: agent.dyaw, prev_agents)))
        ax = prev_agents[0].ax + Numbers.weighted_avg(Numbers.deltas(map(lambda agent: agent.ax, prev_agents)))
        ay = prev_agents[0].ay + Numbers.weighted_avg(Numbers.deltas(map(lambda agent: agent.ay, prev_agents)))

        # yawf = yawi + dyaw * t
        yaw = prev_agents[0].yaw + Numbers.weighted_avg([dyaw, prev_agents[0].dyaw]) * SECONDS_PER_FRAME

        # vf = vi + a * t
        vx = prev_agents[0].vx + Numbers.weighted_avg([ax, prev_agents[0].ax]) * SECONDS_PER_FRAME
        vy = prev_agents[0].vy + Numbers.weighted_avg([ay, prev_agents[0].ay]) * SECONDS_PER_FRAME

        # xf = xi + v * t
        x = prev_agents[0].x + Numbers.weighted_avg([vx, prev_agents[0].vx]) * SECONDS_PER_FRAME
        y = prev_agents[0].y + Numbers.weighted_avg([vy, prev_agents[0].vy]) * SECONDS_PER_FRAME

        return Agent(self.id, self.type, x, y, vx, vy, ax, ay, yaw, dyaw, implied=True)

    def _extrapolate_within(self, ti):
        raise NotImplementedError(f'Had to extrapolate_within for {self.id} at {ti}')
        # print(f'Had to extrapolate_within for {self.id} at {ti}')
        # return Agent(self.id, self.type, 5, 5, 5, 5, 5, 5, 5, 5, implied=True)

    def __str__(self):
        s = 'Trajectory(\n'
        s += f'ID={self.id}\n'
        s += f'TYPE={self.type}\n'
        for ti, agent in self.agents.items():
            s += f'{ti}: {str(agent)}\n'
        s += ')'
        return s
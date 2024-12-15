'''
Example Usage (Use in different blocks): 

p = Plot(-30, 30, -50, 300)

# draw the ego at frame 0
p.draw_agent(scene.trajectories['ego'][0]).show()

# draw the ego trajectory from 0 to 8
p.draw_trajectory(scene.trajectories['ego'], 0, 8).show()

# draw the first frame
p.draw_snapshot(scene.snapshot(0)).show()

# show an interactive video of the scene
p.draw_scene(s)

# show an interactive video of the scene, but only with ego, 62, and 63
p.draw_trajectories_of_scene(s, {'ego', '62', '63'})

# show an inter
'''

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

from .utils import Angle
from .scene import Scene
from .constants import SCENE_LENGTH
from .agentfinder import AgentFinder

class Plot:
    def __init__(self, xmin, xmax, ymin, ymax, sz=6):
        # Create a plot
        fig, ax = plt.subplots(figsize=(sz, sz))

        # save the variables
        self.xmin, self.base_xmin = xmin, xmin
        self.xmax, self.base_xmax = xmax, xmax
        self.ymin, self.base_ymin = ymin, ymin
        self.ymax, self.base_ymax = ymax, ymax
        self.fig = fig
        self.ax = ax

        self.redraw_canvas()


    def redraw_canvas(self):
        ax = self.ax

        ax.clear()

        # Set x and y limits
        ax.set_xlim(self.xmin, self.xmax)
        ax.set_ylim(self.ymin, self.ymax)

        # Maintain x-y 1:1 aspect ratio
        maintain_aspect_ratio = False
        if maintain_aspect_ratio:
            ax.set_aspect('equal', adjustable='box')
        
        # Draw x-y axes
        ax.axhline(0, color='gray', linewidth=0.8)
        ax.axvline(0, color='gray', linewidth=0.8)
        
        # Draw a grid
        ax.grid(visible=True, which='both', linestyle='--', linewidth=0.5, color='lightgray')
        
        # Label x-y axes
        step_size = 10
        ax.set_xticks(range(self.xmin, self.xmax+1, step_size))
        ax.set_yticks(range(self.ymin, self.ymax+1, step_size))

    
    def move_canvas(self, dx, dy):

        # ensure limits are multiples of 10 (for some reason)
        m = 10
        self.xmin = int((self.base_xmin + dx) // m * m)
        self.xmax = int((self.base_xmax + dx) // m * m + m)
        self.ymin = int((self.base_ymin + dy) // m * m)
        self.ymax = int((self.base_ymax + dy) // m * m + m)

        self.redraw_canvas()
    
    
    def draw_agent(self, agent, color='#1960ef'):
        
        # default color for single agent "#1960ef" is dark blue

        # define convenient variable names
        ax = self.ax
        x = agent.x
        y = agent.y

        # do not allow drawings outside the boundary
        if not self.xmin < x < self.xmax:
            return
        if not self.ymin < y < self.ymax:
            return

        # delta x and y, used to draw the arrow
        # dx = agent.vx
        # dy = agent.vy
        dx = 15 * Angle.cos(agent.yaw)
        dy = 15 * Angle.sin(agent.yaw)

        # draw the arrow
        ax.arrow(x, y, dx, dy,
                  head_width=1, head_length=2, 
                  fc=color, 
                  ec=color)
        
        # draw a square agent
        ax.plot(x, y, marker='s', color=color, markerfacecolor='white', markersize=13)

        # mark the agent with its code
        ax.text(x, y, f'{agent.code}', ha='center', va='center', fontsize=8, color=color)

        return self


    def draw_trajectory(self, trajectory, start_ti=0, end_ti=SCENE_LENGTH, color='#44d352'):
        # default color for trajectory "#44d352" is light green

        # for each timestamp index
        for ti in range(start_ti, end_ti):

            # draw the agent with a custom color
            self.draw_agent(trajectory[ti], color)

        return self

    
    def draw_snapshot(self, agents: set):

        # for each agent
        for agent in agents:

            # draw ego as red
            if agent.code == 'ego':
                self.draw_agent(agent, '#f63c5b')

            # draw non-vehicles as gray
            elif agent.type != 'Vehicle':
                self.draw_agent(agent, '#c3d4d9')

            # draw normal vehicles as light blue
            else:
                if agent.is_in_front_of(next(x for x in agents if x.id == 'ego')): # agent is in front of ego
                    self.draw_agent(agent, '#1c99ec')
                else:
                    self.draw_agent(agent, '#2bc793')

            #-yellow: '#fec315'
        
        return self


    def draw_scene(self, scene: Scene, start_ti=0, end_ti=SCENE_LENGTH):

        def update(ti):
            self.redraw_canvas()

            snapshot = scene.snapshot(start_ti+ti)

            self.draw_snapshot(snapshot)
            
        # Create the animation
        ani = FuncAnimation(
            self.fig, update, frames=end_ti-start_ti, interval=200
        )

        return ani
    

    def draw_scene_with_ego_traj(self, scene: Scene, start_ti=0, end_ti=SCENE_LENGTH, traj_length=40, firm_traj_length=0):

        finder = AgentFinder(scene)

        def update(dti):
            self.redraw_canvas()

            ti = start_ti + dti

            snapshot = scene.snapshot(ti)
            
            # draw trajectory from current ego to last known ego anchor
            self.draw_trajectory(scene.trajectories['ego'], ti, min(ti+traj_length, SCENE_LENGTH), color='#37d065')

            # draw trajectory from first unknown ego anchor to last needed anchor
            if ti+traj_length > SCENE_LENGTH:
                self.draw_trajectory(scene.trajectories['ego'], SCENE_LENGTH, ti+traj_length, color='#fd842e')

            # draw trajectory from current ego to last "firm" ego anchor
            self.draw_trajectory(scene.trajectories['ego'], ti, ti+firm_traj_length, color='#447343')

            # draw the other agents
            self.draw_snapshot(snapshot)

            # mark the front agent as purple
            front = finder.get_front(ti)
            if front is not None:
                self.draw_agent(front, color='purple')
            
        # Create the animation
        ani = FuncAnimation(
            self.fig, update, frames=end_ti-start_ti, interval=200
        )

        return ani
    

    def draw_trajectories(self, trajectories, start_ti=0, end_ti=SCENE_LENGTH):

        def update(ti):
            self.redraw_canvas()

            # add everything in this timestamp index to the snapshot
            snapshot = []
            for trajectory in trajectories:
                snapshot.append(trajectory[start_ti+ti])

            self.draw_snapshot(snapshot)
            
        # Create the animation
        ani = FuncAnimation(
            self.fig, update, frames=end_ti-start_ti, interval=100
        )

        return ani
    

    def draw_scene_trajectories(self, scene, codes, start_ti=0, end_ti=SCENE_LENGTH):

        # get all trajectories of agents with the provided codes
        trajectories = {scene.trajectories[code] for code in codes}

        # draw those trajectories
        return self.draw_trajectories(trajectories, start_ti, end_ti)


    def show(self):
        # hacky show, may cause problems
        # we use it because in interactive mode, video functions will display an extra image
        # therefore we close interactive mode and show figures by calling show

        # close all previous irrelevant figures
        for f in plt.get_fignums():
            if f != self.fig.number:
                plt.close(f)
    
        # show the plot
        plt.show()


#@Autor: Eber Jesus Aguilera Zerpa A00829692
#@Tecnologico de Monterrey 
#@Actividad M1 - Aspiradora "Cleaning Robot Agent"

""" Dependencies and libraries """

from mesa import Agent, Model 
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation

from mesa.datacollection import DataCollector
import matplotlib 
import matplotlib.pyplot as plt
import matplotlib.animation as animation 

plt.rcParams["animation.html"] = "jshtml"
matplotlib.rcParams["animation.embed_limit"] = 2**128

import numpy as np
import pandas as pd 

import time 
import datetime 

"""Grid Definition"""

#--Global variables--

grid_width = 10
grid_height = 10
dirt_percentage = 4

agents = 1 #Number of cleaning robots

def get_grid(model): 
    grid = np.zeros((model.grid.width, model.grid.height))
    for cell in model.grid.coord_iter(): 
        cell_content, x, y = cell 
        for content in cell_content: 
            if isinstance(content, CleaningRobotAgent):
                grid[x][y] = 2
            else:
                grid[x][y] = content.live
    
    return grid


class CleaningRobotAgent(Agent): 
    def __init__(self, unique_id, model): 
        super().__init__(unique_id, model)
        self.next_state = None 
        self.type_identifier = 1

    def step(self): 

        
        self.advance()

    def advance(self): 
        
        neighbors = self.model.grid.get_neighbors(
            self.pos, 
            moore = True,
            include_center = False
        )

        new_position = self.random.choice(neighbors)
        self.model.grid.move_agent(self, new_position)

class FloorAgent(Agent): 
    def __init__(self, unique_id, model): 
        super().__init__(unique_id, model)

        self.live = np.random.choice([0,1])
        self.type_identifier = 2


class CleaningRobotModel(Model):
    def __init__(self, width, height): 
        self.num_cells = width * height
        self.grid = MultiGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)

        for (content, x, y) in self.grid.coord_iter():
            a = FloorAgent((x,y), self)
            self.grid.place_agent(a, (x, y))

        #Initialize every agent in the first cell in the grid 
        for i in range(0, agents): 
            a = CleaningRobotAgent((1, 1), self)
            self.grid.place_agent(a, (1,1))
            self.schedule.add(a)

        self.datacollector = DataCollector(
            model_reporters={"Grid" : get_grid}
        )

        def step(self):
            self.datacollector.collect(self)
            self.schedule.step()

Grid_Size = 10 
Num_Iterations = 50

start_time = time.time()
model = CleaningRobotModel(Grid_Size, Grid_Size)

for i in range(Num_Iterations): 
    model.step() 

print('Tiempo de ejecución:', str(datetime.timedelta(seconds=(time.time() - start_time))))

all_grid = model.datacollector.get_model_vars_dataframe()

"""fig, axs = plt.subplots(figsize = (7,7))
axs.set_xticks([])
axs.set_yticks([])
patch = plt.imshow(all_grid.iloc[0][0], cmap=plt.cm.binary)

def animate(i):
    patch.set_data(all_grid.iloc[i][0])

anim = animation.FuncAnimation(fig, animate, frames=Num_Iterations)
anim"""
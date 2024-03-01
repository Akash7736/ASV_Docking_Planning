import numpy as np 
import dockmap 
from utils import point_on_line_segment,is_within_radius



startloc = (-532,461.91)
startloc2 = (-532.0,170.0)
goalloc = [-460.9,207.0]
goalloc2 = [-463,204.0]

class Graphnet:
    def __init__(self) -> None:
        self.startloc = startloc2
        self.goalloc = goalloc2
    def getStartState(self):
        start_state = self.startloc
        return start_state
    def getGoalState(self):
     goal_state =  self.goalloc
     return goal_state
    def isGoalState(self, state):
     if state == self.getGoalState():
         return True
     else:
         return False
    def isObstacle(self, state):
      if point_on_line_segment(state) or is_within_radius(state):
          return True
      else:
          return False
  
    def getStateExpansionCount(self):
      return self.state_expansion_counter

    def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     if enable_plots:
         #Update changes on the plot copy
         if self.map_plot_copy[state[0]][state[1]] == maze_maps.fringe_id:
             self.map_plot_copy[state[0]][state[1]] = maze_maps.expanded_id
     
     successors = []
     self.state_expansion_counter = self.state_expansion_counter + 1
     for action in self.four_neighbor_actions:
         
         #Get individual action
         del_x, del_y = self.four_neighbor_actions.get(action)
         
         #Get successor
         new_successor = [state[0] + del_x , state[1] + del_y]
         new_action = action
         
         # Check for obstacle 
         if self.isObstacle(new_successor):
             continue
          
         
         if enable_plots:
             #Update changes on the plot copy
             if self.map_plot_copy[new_successor[0]][new_successor[1]] == maze_maps.free_space_id1 or self.map_plot_copy[new_successor[0]][new_successor[1]] == maze_maps.free_space_id2:
                 self.map_plot_copy[new_successor[0]][new_successor[1]] = maze_maps.fringe_id
         
         #Check cost
         if self.maze_map.map_data[new_successor[0]][new_successor[1]] == maze_maps.free_space_id2:
             new_cost = maze_maps.free_space_id2_cost
         else:
             new_cost = maze_maps.free_space_id1_cost 
             
         successors.append([new_successor, new_action, new_cost])
         
     if enable_plots:   
         #Plot the changes
         self.plot_map()
     return successors


    
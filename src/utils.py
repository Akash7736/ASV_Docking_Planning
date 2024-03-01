import numpy as np
import heapq

buoys = [(-528,183),(-530,183),(-504,186),(-495,200),(-487,207),(-487,216),(-478,210),(-478,168),(-487,187),(-495,172),(-466,194)]


class PriorityQueue:

  def  __init__(self):  
    self.heap = []
    
  def push(self, item, priority):
      pair = (priority,item)
      heapq.heappush(self.heap,pair)

  def pop(self):
      (priority,item) = heapq.heappop(self.heap)
      return item
  
  def isEmpty(self):
    return len(self.heap) == 0
  
  def replace_cost(self,state, old_cost, new_cost):
        # print(item)
        for i, (priority, item) in enumerate(self.heap):
            # print(item,state)
            if item[0]==state and item[2] == old_cost:
                # print(item[1][0])
                new_item = (item[0],item[1],new_cost)
                self.heap[i] = (priority, new_item)
                heapq.heapify(self.heap)
                # print('replaced')
                return
        raise ValueError("Item not found in the priority queue")

def heuristic_1(problem, state):
    """
    Euclidean distance
    """
    state_vec = np.array(state).flatten()
    goal_vec = np.array(problem.getGoalState())
    eucdist = np.linalg.norm((goal_vec - state_vec)) 
    return eucdist

linesegments = {

    'line1': [(-483, 184), (-479, 190)],
    'line2': [(-483, 184), (-466, 176)],
    'line3': [(-466, 176), (-463, 183)],
    'line4': [(-470, 209), (-467, 215)],
    'line5': [(-467, 215), (-451, 205)],
    'line6': [(-451, 205), (-455, 199.5)]

}

def point_on_line_segment(x, y, x1, y1, x2, y2):
    # Function to calculate distance between a point and a line
    def distance_to_line(x, y, x1, y1, x2, y2):
        numerator = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1)
        denominator = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
        return numerator / denominator

    # Check if the point is within a 1 unit distance of the line segment
    if distance_to_line(x, y, x1, y1, x2, y2) <= 5:
        # Check if the point lies within the bounding box of the line segment
        if min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2):
            return True
    return False



def is_within_radius(point1, point2, radius):
    x1, y1 = point1
    x2, y2 = point2
    distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance <= radius

def connect_points(p1, p2):
    line = np.linspace(p1, p2, num=100)
    for point in line:
        col = False
        for i in linesegments.values():
            if point_on_line_segment(point[0],point[1],i[0][0],i[0][1],i[1][0],i[1][1]):col=True
        for j in buoys:
            if is_within_radius(point,j,5):col=True
        if col :return False
    return True

import matplotlib.pyplot as plt

def plot_lines_from_point(start_point, end_points):
    """
    Plot lines from a single start point to a list of end points.

    Parameters:
        start_point (tuple): Coordinates of the start point (x, y).
        end_points (list of tuples): List of coordinates of end points [(x1, y1), (x2, y2), ...].
    """
    # Unzip start_point coordinates
    start_x, start_y = start_point

    # Unzip end_points coordinates
    end_x, end_y = zip(*end_points)

    # Plot the start point
    # plt.plot(start_x, start_y, 'ro')  # 'ro' means red circle

    # Plot lines from the start point to each end point
    plt.plot([start_x] * len(end_points), [start_y] * len(end_points), 'ro')  # Plot lines from start point to each end point
    for x, y in zip(end_x, end_y):
        plt.plot([start_x, x], [start_y, y], 'black',linewidth=1)  # 'b-' means blue line

    # Set labels and title
    # plt.xlabel('X')
    # plt.ylabel('Y')
    # plt.title('Lines from a Single Point')

    # # Show plot
    # plt.grid(True)
    # plt.show()


def weighted_AStarSearch(problem):
    """
    Pop the node that having the lowest combined cost plus heuristic
    heuristic_ip can be M, E, or a number 
    if heuristic_ip is M use Manhattan distance as the heuristic function
    if heuristic_ip is E use Euclidean distance as the heuristic function
    if heuristic_ip is a number, use weighted A* Search with Euclidean distance as the heuristic function and the integer being the weight
    """
    "*** YOUR CODE HERE ***"
    # if heuristic_ip =='E':
    heuristic = heuristic_1
    weight = 50
    # elif heuristic_ip == 'M':
        # heuristic = heuristic_2
        # weight = 1
    # else: 
        # heuristic = heuristic_1
        # weight = int(heuristic_ip)
    
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    
    pq = PriorityQueue()
    start_state = problem.getStartState()
    pq.push((start_state, [], 0),weight*heuristic(problem,start_state) )
    statecount = 0

    
    visited = []

    while not pq.isEmpty():
        item = pq.pop()
        state , actions, cost = item[0],item[1],item[2]
      
 
        if problem.isGoalState(state):
            return actions

        if state not in visited:
        #   print(state)
          visited.append(state)
          statecount+=1

        
        for successor, action, stepCost in problem.getSuccessors(state):
            if successor not in visited:
                if successor not in [item[1][0] for item in pq.heap]:
                    new_actions = actions + [action]
                    new_cost = cost + stepCost
                    priority = new_cost + weight*heuristic(problem,successor)
                    # print(priority)
                    pq.push((successor, new_actions, new_cost), priority)
                elif successor in [item[1][0] for item in pq.heap]:
                   new_cost = cost + stepCost
                   for suc,ac,cos in [item[1] for item in pq.heap]:
                       if suc==successor:
                           if cos>new_cost:pq.replace_cost(successor,cos,new_cost)
                   


    return []
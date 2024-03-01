import numpy as np 
import matplotlib.pyplot as plt 
from utils import point_on_line_segment,is_within_radius,connect_points,plot_lines_from_point
from sklearn.neighbors import KDTree
import networkx as nx

startloc = (-532,461.91)
startloc2 = (-532.0,170.0)
goalloc = [-460.9,207.0]
goalloc2 = [-463,204.0]
buoys = [(-528,183),(-530,183),(-504,186),(-495,200),(-487,207),(-487,216),(-478,210),(-478,168),(-487,187),(-495,172),(-466,194)]
dock1 = [(-483,184),(-479,190),(-475,180),(-474,188),(-475,180),(-468,185),(-466,176),(-463,183)]
dock2 = [(-470,209),(-467,215),(-465,206),(-459,211),(-460,202.5),(-455,199.5),(-451,205)]

    

dock1lines = {
    'line1' : [(-483,184),(-479,190)],
    'line2' : [(-483,184),(-466,176)],
    'line3' : [(-466,176),(-463,183)]
}

dock2lines = {
    'line1' : [(-470,209),(-467,215)],
    'line2' : [(-467,215),(-451,205)],
    'line3' : [(-451,205),(-455,199.5)]
}
for i in dock1lines.values():
    plt.plot([j[0] for j in i],[j[1] for j in i],linewidth=3,color='r')

for i in dock2lines.values():
    plt.plot([j[0] for j in i],[j[1] for j in i],linewidth=3,color='g')
#*************************************************************************
    linesegments = {

    'line1': [(-483, 184), (-479, 190)],
    'line2': [(-483, 184), (-466, 176)],
    'line3': [(-466, 176), (-463, 183)],
    'line4': [(-470, 209), (-467, 215)],
    'line5': [(-467, 215), (-451, 205)],
    'line6': [(-451, 205), (-455, 199.5)]

}
num_points = 100
min_x, max_x = -530,-450 
min_y, max_y = 170, 210
random_points = np.random.uniform(low=[min_x, min_y], high=[max_x, max_y], size=(num_points, 2))
# random_points = np.concatenate((random_points, np.array(goalloc).reshape(1, -1)), axis=0)
# print(random_points.shape)


# Filter valid points
valid_points = []
for point in random_points:
    col = False
    for i in linesegments.values():
        if point_on_line_segment(point[0],point[1],i[0][0],i[0][1],i[1][0],i[1][1]):col=True
    for j in buoys:
        if is_within_radius(point,j,5):col=True
    if col==False: 
        valid_points.append(point)
valid_points.append(np.array(goalloc))
valid_points.append(np.array(goalloc2))
valid_points.append(np.array(startloc2))

# print(valid_points)
tree=KDTree(valid_points)
# plt.scatter([valid_points[0][0]],[valid_points[0][1]],color='red')
# print([valid_points[0][0]],[valid_points[0][1]])
# print(tree.query([valid_points[-2]],k=50))
graph = {}
for i, point in enumerate(valid_points):
    graph[i] = []
    
   

# Connect points to nearby points in the graph
for i, point in enumerate(valid_points):
    # Find nearby points within a certain radius
    # if np.any(point ==np.array(goalloc)): graph[i].append(goalloc2)
    # if np.any(point ==np.array(goalloc2)): graph[i].append(goalloc)
    _, indices = tree.query([point], k=50)
    
    # Connect the point to its nearby points
    for j in indices[0]:
        if i != j and connect_points(point, valid_points[j]):
            graph[i].append(j)
            graph[j].append(i)
        if i!=j and np.any(point ==np.array(goalloc)):
            g1 = i
        if i!=j and np.any(point ==np.array(goalloc2)):
            g2 = i
            
graph[g1].append(g2)
graph[g2].append(g1) 
    


# print(graph)
plt.scatter([i[0] for i in valid_points],[i[1] for i in valid_points],color='black')
for i,adjlist in graph.items():
    plot_lines_from_point(valid_points[i],[valid_points[k] for k in adjlist])
    # print(i,adjlist)


#***********************************************************************
# plt.scatter(startloc[0],startloc[1],color='y')
plt.scatter(goalloc[0],goalloc[1],color='r')
plt.scatter([i[0] for i in buoys],[i[1] for i in buoys])
plt.scatter([i[0] for i in dock1],[i[1] for i in dock1],color='r')
plt.scatter([i[0] for i in dock2],[i[1] for i in dock2],color='g')
plt.show()
from cprr_experiments_linearlatency import *

# # Two-Edge Parallel Network
# print("\n\n\n ----- \n Parallel \n\n")
# cprr_experiment_linearlatency(road_network='Pigou_bpr')

# # Six-Edge parallel Network
# print("\n\n\n ----- \n Expanded \n\n")
# cprr_experiment_linearlatency(road_network='Pigou_expanded')

# # # Series-Parallel Network
# print("\n\n\n ----- \n Series-Parallel \n\n")
# cprr_experiment_linearlatency(road_network='Series_parallel')

# # Grid Network
print("\n\n\n ----- \n Grid \n\n")
cprr_experiment_linearlatency(road_network='Grid')

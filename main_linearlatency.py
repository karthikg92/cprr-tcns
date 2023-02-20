from cprr_experiments_linearlatency import *
from utils import save_log


# Single OD
log = []
log.append(cprr_experiment_linearlatency(road_network='Pigou_bpr_singleOD'))
log.append(cprr_experiment_linearlatency(road_network='Pigou_expanded_singleOD'))
log.append(cprr_experiment_linearlatency(road_network='Series_parallel_singleOD'))
log.append(cprr_experiment_linearlatency(road_network='Grid_singleOD'))
save_log(log, fname='results_singleOD.csv')

# Multiple OD
log = []
log.append(cprr_experiment_linearlatency(road_network='Pigou_bpr_multipleOD'))
log.append(cprr_experiment_linearlatency(road_network='Pigou_expanded_multipleOD'))
log.append(cprr_experiment_linearlatency(road_network='Series_parallel_multipleOD'))
log.append(cprr_experiment_linearlatency(road_network='Grid_multipleOD')) # taking quite a while, but doable (5 min and 2% gap)
save_log(log, fname='results_multipleOD.csv')

# Variance expts
log = []
log.append(cprr_experiment_linearlatency(road_network='Pigou_bpr_low-var'))
log.append(cprr_experiment_linearlatency(road_network='Pigou_bpr_med-var'))
log.append(cprr_experiment_linearlatency(road_network='Pigou_bpr_high-var'))
log.append(cprr_experiment_linearlatency(road_network='Pigou_bpr_skew-var'))
# save_log(log, fname='results_pigou_var.csv')

# log = []
log.append(cprr_experiment_linearlatency(road_network='Pigou_expanded_low-var'))
log.append(cprr_experiment_linearlatency(road_network='Pigou_expanded_med-var'))
log.append(cprr_experiment_linearlatency(road_network='Pigou_expanded_high-var'))
log.append(cprr_experiment_linearlatency(road_network='Pigou_expanded_skew-var'))
# save_log(log, fname='results_pigou_expanded_var.csv')

# log = []
log.append(cprr_experiment_linearlatency(road_network='Series_parallel_low-var'))
log.append(cprr_experiment_linearlatency(road_network='Series_parallel_med-var'))
log.append(cprr_experiment_linearlatency(road_network='Series_parallel_high-var'))
log.append(cprr_experiment_linearlatency(road_network='Series_parallel_skew-var'))
# save_log(log, fname='results_pigou_expanded_var.csv')

# log = []
log.append(cprr_experiment_linearlatency(road_network='Grid_low-var'))
log.append(cprr_experiment_linearlatency(road_network='Grid_med-var'))
log.append(cprr_experiment_linearlatency(road_network='Grid_high-var'))
log.append(cprr_experiment_linearlatency(road_network='Grid_skew-var'))
# save_log(log, fname='results_pigou_expanded_var.csv')
save_log(log, fname='results_variance.csv')
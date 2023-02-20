from network import Network
from users import Users
from user_equilibrium_with_tolls_linearlatency import *
from optimal_flow_linearlatency import *
import pandas as pd
import numpy as np
from utils import *


def cprr_experiment_linearlatency(road_network):

    output_results = {'experiment':road_network}

    print("---- ", road_network, ' ----')

    PRINT_FLAG = False

    # users for the experiment
    users_exact = Users(road_network, aggregate=False)
    users_aggregate = Users(road_network, aggregate=True)

    # city network for the experiment
    network = Network(road_network)

    # test to see if UE is solved faster
    x_notoll_ue, f_notoll_ue = ue_with_tolls_linearlatency(network, users_exact, np.zeros(network.NumEdges))

    # minimum total system cost with complete information
    x_opt, f_opt = optimal_flow_linearlatency(network, users_exact)
    # print("Solved first optimization")
    edge_tt = bpr_linearlatency(f_opt, network.capacity_array(), network.latency_array(), network.latency_slope)
    min_cost_complete_info = edge_tt @ x_opt @ users_exact.vot_array()


    # sanity check!
    t_derivative = network.latency_slope
    toll_opt = np.zeros(len(f_opt))
    for e in range(len(toll_opt)):
        toll_opt[e] = sum(x_opt[e,i] * users_exact.vot_array()[i] for i in range(users_exact.num_users)) * t_derivative[e]
    x_opt_ue, f_opt_ue = ue_with_tolls_linearlatency(network, users_exact, toll_opt)
    edge_tt_ue = bpr_linearlatency(f_opt_ue, network.capacity_array(), network.latency_array(), network.latency_slope)
    min_cost_complete_info_sanitycheck = edge_tt_ue @ x_opt_ue @ users_exact.vot_array()


    # minimum total system cost with aggregate information
    x_agg, f_agg = optimal_flow_linearlatency(network, users_aggregate)
    

    # compute tolls that would result in f_agg
    t_derivative = network.latency_slope
    toll_agg = np.zeros(len(f_agg))

    for e in range(len(toll_agg)):
        toll_agg[e] = sum(x_agg[e,i] * users_aggregate.vot_array()[i] for i in range(users_aggregate.num_users)) * t_derivative[e]

    # compute flow thats realized corresponding to toll_agg (this should use exact vot)
    x_agg_ue, f_agg_ue = ue_with_tolls_linearlatency(network, users_exact, toll_agg)

    # Cost for realized flow
    edge_tt_ue = bpr_linearlatency(f_agg_ue, network.capacity_array(), network.latency_array(), network.latency_slope)
    min_cost_agg_info = edge_tt_ue @ x_agg_ue @ users_exact.vot_array()

    print("Complete info cost: ", min_cost_complete_info)
    print("Aggregate info cost: ", min_cost_agg_info)

    output_results['complete_info'] = min_cost_complete_info
    output_results['agg_info'] = min_cost_agg_info
    

    if PRINT_FLAG:
        print("Sanity check: ", min_cost_complete_info_sanitycheck)
        print("Optimal flows")
        print(x_opt)
        print(f_opt)
        
        print("Optimal_ue flows")
        print(x_opt_ue)
        print(f_opt_ue)
        
        

        print("Approximate flows")
        print(x_agg)
        print(f_agg)


        print("Approximate_ue flows")
        print(x_agg_ue)
        print(f_agg_ue)

    # C* == min system cost with exact information
    C_star = min_cost_complete_info

    # Compute GC of initial income distribution
    initial_income_exact = users_exact.income_array()
    gc_initial = compute_gini(initial_income_exact)
    print("Initial GC = ", gc_initial)

    output_results['initial_gc'] = gc_initial

    # Compute GC of Incomes of users after they pay a cost to form the UE outcome (with no tolls)
        # compute UE with no tolls (i.e., total system cost as well as flows for each group -- C0)
        # compute cost for every user group (using flows for that group)
        # subtract cost from initial income for every user group to get final UE income
        # compute GC on final UE income
    
    x_notoll_ue, f_notoll_ue = ue_with_tolls_linearlatency(network, users_exact, np.zeros(len(f_opt)))
    edge_tt = bpr_linearlatency(f_notoll_ue, network.capacity_array(), network.latency_array(), network.latency_slope)


    C0 = edge_tt @ x_notoll_ue @ users_exact.vot_array()
    cost_per_group_notoll_ue = np.zeros(x_notoll_ue.shape[1])
    for g in range(len(cost_per_group_notoll_ue)):
        cost_per_group_notoll_ue[g] = sum(edge_tt[e] * x_notoll_ue[e,g] * users_exact.vot_array()[g] for e in range(len(f_opt)))/ users_exact.user_flow_list()[g] 
    
    print("User equilibrium no tolls, complete information cost = ", C0)
    output_results['c0'] = C0

    if PRINT_FLAG:
        print("Cost per group after no toll UE")
        print(cost_per_group_notoll_ue)
        print("Initial income")
        print(initial_income_exact)
    income_after_notoll_ue = initial_income_exact - cost_per_group_notoll_ue
    if PRINT_FLAG:
        print("Income after UE")
        print(income_after_notoll_ue)
    gc_after_ue = compute_gini(income_after_notoll_ue)
    if PRINT_FLAG:
        print("Gini coefficient after UE = ", gc_after_ue)

    # Exact:
        # Implement water filling to compute refunds (C0-C*) -- this water filling happens on final UE income
        # This gives a refunded Income
        # Compute GC on that
    

    # print("Income after tolls UE: ", income_after_toll_ue)
    income_after_refunds = distribute_refunds(income_after_notoll_ue, users_exact.user_flow_list(), C0-C_star)
    # print(income_after_refunds)
    gc_after_refund = compute_gini(income_after_refunds)

    print("GC after exact refunds= ", gc_after_refund )
    output_results['gc_after_exact_refund'] = gc_after_refund

    # Approx:
        # \hat{C}* = min system cost based on approx VOT info
        # \hat{C}0 = min system cost of UE without tolls on approxmate VOT info
        # Implement water filling to compute refunds (\hat{C}0-\hat{C}*) -- this water filling happens on apprximate final UE income
        # compute GC on that (w.r.t true VOT info)

    # print("------- Aggregate approximation ---------")

    initial_income_agg = users_aggregate.income_array()

    x_agg_ue, f_agg_ue = ue_with_tolls_linearlatency(network, users_aggregate, np.zeros(len(f_opt)))
    edge_tt_ue = bpr_linearlatency(f_agg_ue, network.capacity_array(), network.latency_array(), network.latency_slope)
    C0_hat = edge_tt_ue @ x_agg_ue @ users_aggregate.vot_array()

    # print("Edge travel time: ", edge_tt_ue)
    # print("Total flows for C0_hat:", f_agg_ue)

    x_agg, f_agg = optimal_flow_linearlatency(network, users_aggregate)
    edge_tt_agg = bpr_linearlatency(f_agg, network.capacity_array(), network.latency_array(), network.latency_slope)
    C_star_hat = edge_tt_agg @ x_agg @ users_aggregate.vot_array()

    # print("Edge travel time: ", edge_tt_agg)
    # print("Total flows for C_star_hat:", f_agg)

    total_agg_refund_hat = C0_hat - C_star_hat

    # print("total refund = ", total_agg_refund_hat)

    cost_per_group_notoll_ue_agg = np.zeros(x_agg_ue.shape[1])
    for g in range(len(cost_per_group_notoll_ue_agg)):
        cost_per_group_notoll_ue_agg[g] = sum(edge_tt_ue[e] * x_agg_ue[e,g] * users_aggregate.vot_array()[g] for e in range(len(f_opt)))/ users_aggregate.user_flow_list()[g] 
    

    income_after_notoll_ue_agg = initial_income_agg - cost_per_group_notoll_ue_agg

    # print("Income after travelling: ", income_after_notoll_ue_agg)


    income_after_refund_agg = distribute_refunds(income_after_notoll_ue_agg, users_aggregate.user_flow_list(), total_agg_refund_hat)
    refunds_issued_agg = income_after_refund_agg - income_after_notoll_ue_agg

    # convert refund issued agg (which is per person) to refund per user group
    refunds_issued = aggregate_refund_to_exact_refund(refunds_issued_agg, users_aggregate, users_exact)

    true_income_after_refund_agg = refunds_issued + income_after_notoll_ue

    # print("income after refund: ", true_income_after_refund_agg)

    gc_after_refund_agg = compute_gini(true_income_after_refund_agg)

    print("GC after aggregate refunds = ", gc_after_refund_agg )

    output_results['gc_after_agg_refund'] = gc_after_refund_agg

    # print("---- Debug ------")
    # print("C0:", C0)
    # print("C0_hat:", C0_hat)

    # print("C_star:", C_star)
    # print("C_star_hat:", C_star_hat)

    print('\n')

    return output_results
    
def bpr_linearlatency(f, capacity, free_flow_latency, latency_slope):
    """
    :param f: edge flow numpy array
    :param capacity: edge capacity array
    :param free_flow_latency: free flow latency
    :return: numpy array of travel times on edges
    """
    if len(f) != len(capacity):
        print("[bpr-function] Error!")

    edge_tt = np.zeros(len(f))

    for e in range(len(edge_tt)):
            edge_tt[e] = free_flow_latency[e] + latency_slope[e] * f[e]
    return edge_tt


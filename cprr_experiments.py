from network import Network
from users import Users
from user_equilibrium_with_tolls import *
from optimal_flow import *
import pandas as pd
import numpy as np
from utils import *


def cprr_experiment(road_network):

    # users for the experiment
    users_exact = Users(road_network, aggregate=False)
    users_aggregate = Users(road_network, aggregate=True)

    # city network for the experiment
    network = Network(road_network)

    # test to see if UE is solved faster
    x_notoll_ue, f_notoll_ue = ue_with_tolls(network, users_exact, np.zeros(network.NumEdges))

    # minimum total system cost with complete information
    x_opt, f_opt = optimal_flow(network, users_exact)
    print("Solved first optimization")
    edge_tt = bpr(f_opt, network.capacity_array(), network.latency_array())
    min_cost_complete_info = edge_tt @ x_opt @ users_exact.vot_array()


    # sanity check!
    t_derivative = compute_t_derivative(f_opt, network.capacity_array())
    toll_opt = np.zeros(len(f_opt))
    for e in range(len(toll_opt)):
        toll_opt[e] = sum(x_opt[e,i] * users_exact.vot_array()[i] for i in range(users_exact.num_users)) * t_derivative[e]
    x_opt_ue, f_opt_ue = ue_with_tolls(network, users_exact, toll_opt)
    edge_tt_ue = bpr(f_opt_ue, network.capacity_array(), network.latency_array())
    min_cost_complete_info_sanitycheck = edge_tt_ue @ x_opt_ue @ users_exact.vot_array()


    # minimum total system cost with aggregate information
    x_agg, f_agg = optimal_flow(network, users_aggregate)
    

    # compute tolls that would result in f_agg
    t_derivative = compute_t_derivative(f_agg, network.capacity_array())
    toll_agg = np.zeros(len(f_agg))

    for e in range(len(toll_agg)):
        toll_agg[e] = sum(x_agg[e,i] * users_aggregate.vot_array()[i] for i in range(users_aggregate.num_users)) * t_derivative[e]

    # compute flow thats realized corresponding to toll_agg (this should use exact vot)
    x_agg_ue, f_agg_ue = ue_with_tolls(network, users_exact, toll_agg)

    # Cost for realized flow
    edge_tt_ue = bpr(f_agg_ue, network.capacity_array(), network.latency_array())
    min_cost_agg_info = edge_tt_ue @ x_agg_ue @ users_exact.vot_array()

    print("Complete info cost: ", min_cost_complete_info)
    print("Sanity check: ", min_cost_complete_info_sanitycheck)
    print("Aggregate info cost: ", min_cost_agg_info)

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
    initial_income = 1000*users_exact.vot_array()
    gc_initial = compute_gini(initial_income)
    print("Initial GC = ", gc_initial)

    # Compute GC of Incomes of users after they pay a cost to form the UE outcome (with no tolls)
        # compute UE with no tolls (i.e., total system cost as well as flows for each group -- C0)
        # compute cost for every user group (using flows for that group)
        # subtract cost from initial income for every user group to get final UE income
        # compute GC on final UE income
    
    x_notoll_ue, f_notoll_ue = ue_with_tolls(network, users_exact, np.zeros(len(f_opt)))
    edge_tt = bpr(f_notoll_ue, network.capacity_array(), network.latency_array())


    C0 = edge_tt @ x_notoll_ue @ users_exact.vot_array()
    cost_per_group_notoll_ue = np.zeros(x_notoll_ue.shape[1])
    for g in range(len(cost_per_group_notoll_ue)):
        cost_per_group_notoll_ue[g] = sum(edge_tt[e] * x_notoll_ue[e,g] * users_exact.vot_array()[g] for e in range(len(f_opt)))/ users_exact.user_flow_list()[g] 
    print("Cost per group after no toll UE")
    print(cost_per_group_notoll_ue)
    print("Initial income")
    print(initial_income)
    income_after_notoll_ue = initial_income - cost_per_group_notoll_ue
    print("Income after UE")
    print(income_after_notoll_ue)
    gc_after_ue = compute_gini(income_after_notoll_ue)
    print("Gini coefficient after UE = ", gc_after_ue)

    # Exact:
        # Implement water filling to compute refunds (C0-C*) -- this water filling happens on final UE income
        # This gives a refunded Income
        # Compute GC on that

    print("Refund amount = ", C0- C_star)
    # cost_per_group_ue = np.zeros(x_opt.shape[1])
    # for g in range(len(cost_per_group_ue)):
    #     cost_per_group_ue[g] = sum(edge_tt[e] * x_opt[e,g] * users_exact.vot_array()[e] for i in range(len(f_opt))) 
    # income_after_toll_ue = initial_income - cost_per_group_ue


    # print("Income after tolls UE: ", income_after_toll_ue)
    income_after_refunds = distribute_refunds(income_after_notoll_ue, C0-C_star)
    print(income_after_refunds)
    gc_after_refund = compute_gini(income_after_refunds)

    print("GC after refunds= ", gc_after_refund )

    # Approx:
        # \hat{C}* = min system cost based on approx VOT info
        # \hat{C}0 = min system cost of UE without tolls on approxmate VOT info
        # Implement water filling to compute refunds (\hat{C}0-\hat{C}*) -- this water filling happens on apprximate final UE income
        # compute GC on that (w.r.t true VOT info)

    print("------- Aggregate approximation ---------")

    x_agg_ue, f_agg_ue = ue_with_tolls(network, users_aggregate, np.zeros(len(f_opt)))
    edge_tt_ue = bpr(f_agg_ue, network.capacity_array(), network.latency_array())
    C0_hat = edge_tt_ue @ x_agg_ue @ users_aggregate.vot_array()

    print("Edge travel time: ", edge_tt_ue)
    print("Total flows for C0_hat:", f_agg_ue)

    x_agg, f_agg = optimal_flow(network, users_aggregate)
    edge_tt_agg = bpr(f_agg, network.capacity_array(), network.latency_array())
    C_star_hat = edge_tt_agg @ x_agg @ users_aggregate.vot_array()

    print("Edge travel time: ", edge_tt_agg)
    print("Total flows for C_star_hat:", f_agg)

    total_agg_refund_hat = C0_hat - C_star_hat

    print("total refund = ", total_agg_refund_hat)

    cost_per_group_notoll_ue_agg = np.zeros(x_agg_ue.shape[1])
    for g in range(len(cost_per_group_notoll_ue_agg)):
        cost_per_group_notoll_ue_agg[g] = sum(edge_tt_ue[e] * x_agg_ue[e,g] * users_aggregate.vot_array()[g] for e in range(len(f_opt)))/ users_aggregate.user_flow_list()[g] 
    
    income_after_notoll_ue_agg = initial_income - cost_per_group_notoll_ue_agg

    print("Income after travelling: ", income_after_notoll_ue_agg)

    income_after_refund_agg = distribute_refunds(income_after_notoll_ue_agg, total_agg_refund_hat)

    print("income after refund: ", income_after_refund_agg)

    gc_after_refund_agg = compute_gini(income_after_refund_agg)

    print("GC after refunds (aggregate)= ", gc_after_refund_agg )

    print("---- Debug ------")
    print("C0:", C0)
    print("C0_hat:", C0_hat)

    print("C_star:", C_star)
    print("C_star_hat:", C_star_hat)

    return None
    
def bpr(f, capacity, free_flow_latency):
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
        if f[e] < 1.1 * capacity[e]:
            edge_tt[e] = 1.025 * free_flow_latency[e]
        else:
            edge_tt[e] = 1.025 * free_flow_latency[e] + 0.6 * (f[e] - 1.1 * capacity[e])
    return edge_tt


def compute_t_derivative(f, capacity):
    t_derivative = np.zeros(len(f))
    for e in range(len(t_derivative)):
        if f[e] > 1.1 * capacity[e]:
            t_derivative[e] = 0.6
    return t_derivative

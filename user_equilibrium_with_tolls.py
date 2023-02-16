import numpy as np
import gurobipy as gp
from gurobipy import GRB

def ue_with_tolls(network, users, tolls):

    num_edges = network.NumEdges
    num_users = users.num_users

    # Model initialization
    m = gp.Model('VoT')
    m.setParam('OutputFlag', 0)

    # decision variable
    x_eu = m.addVars(num_edges, num_users, lb=0.0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name="x_eu")

    # decision variable: epsilon
    eps = m.addVars(num_edges, lb=0.0, ub=GRB.INFINITY,  vtype=GRB.CONTINUOUS, name="eps")

    # introducing edge flows
    x_e = m.addVars(num_edges, lb=0.0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name="x_e")
    m.addConstrs(x_eu.sum(e, '*') == x_e[e] for e in range(num_edges))

    # demand from origin constraint
    m.addConstrs(
        sum([x_eu[e, u] for e in network.next(node=users.data[u]['orig'])]) == users.data[u]['vol']
        for u in range(num_users))

    m.addConstrs(
        sum([x_eu[e, u] for e in network.prev(node=users.data[u]['orig'])]) == 0
        for u in range(num_users))

    # demand at destination constraint
    m.addConstrs(
        sum([x_eu[e, u] for e in network.prev(node=users.data[u]['dest'])]) ==
        users.data[u]['vol']
        for u in range(num_users))

    m.addConstrs(
        sum([x_eu[e, u] for e in network.next(node=users.data[u]['dest'])]) == 0
        for u in range(num_users))

    # flow conservation
    for u in range(num_users):
        exclude_od_nodes = [n for n in range(network.NumNodes)]
        exclude_od_nodes.remove(users.data[u]['orig'])
        exclude_od_nodes.remove(users.data[u]['dest'])

        m.addConstrs(
            sum(x_eu[g, u] for g in network.prev(node=n)) ==
            sum(x_eu[g, u] for g in network.next(node=n))
            for n in exclude_od_nodes)

    # eps constraints
    for e in range(num_edges):
        m.addConstr(eps[e] >= x_e[e] - 1.1 * network.capacity[e], name='eps_edge' + str(e))

    # set objective
    obj_term1 = 0
    obj_term2 = 0

    for e in range(num_edges):
        obj_term1 += 1.025 * network.edge_latency[e] * x_e[e] + eps[e] * eps[e]/2 * 0.6
        for u in range(num_users):
            obj_term2 += tolls[e] / users.data[u]['vot'] * x_eu[e,u]

    obj = obj_term1 + obj_term2
    m.setObjective(obj)

    # optimize 
    m.optimize()

    # If infeasible, terminate program
    assert m.status != GRB.INFEASIBLE

    # extract the solution flows
    x = np.zeros((num_edges, num_users))
    x_dict = m.getAttr('x', x_eu)
    for e in range(num_edges):
        for u in range(num_users):
            x[e, u] = x_dict[e, u]
    f = np.sum(x, axis=1)

    return x, f

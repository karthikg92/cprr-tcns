import os
import numpy as np
import gurobipy as gp
from gurobipy import GRB 


def vector_to_file(fname, x):
    try:
        os.remove(fname)
    except:
        pass

    with open(fname, 'a') as f:
        for el in x:
            f.write(str(el) + '\n')


def write_row(fname, row):
    with open(fname, 'a') as f:
        for i in range(len(row)):
            if i < (len(row)-1):
                f.write(str(row[i]) + ', ')
            else:
                f.write(str(row[i]) + '\n')


def compute_gini(x):
    total = 0
    for i, xi in enumerate(x[:-1], 1):
        total += np.sum(np.abs(xi - x[i:]))
    return total / (len(x)**2 * np.mean(x))

def distribute_refunds(income, volume, total_refund):
    # waterfall approach for distributing refund to incomes
    m = gp.Model('refund')
    m.setParam('OutputFlag', 0)

    # decision variable
    r = m.addVars(len(income), lb=0.0, ub=total_refund, vtype=GRB.CONTINUOUS, name="r")

    # tracking the lowest value
    l = m.addVar(lb=0.0, ub=GRB.INFINITY, name='l')

    # total refund constraints
    m.addConstr( sum([r[u]* volume[u] for u in range(len(income))]) == total_refund)

    # lowest value constraint
    for u in range(len(income)):
        m.addConstr(income[u]+r[u] >= l)

    # objective function
    m.setObjective(l, GRB.MAXIMIZE)

    m.optimize()

    # If infeasible, terminate program
    assert m.status == GRB.OPTIMAL

    # extract the solution
    new_income = np.zeros(len(income))
    refund_dict = m.getAttr('x', r)
    for u in range(len(income)):
        new_income[u] = income[u] + refund_dict[u]

    return new_income

def aggregate_refund_to_exact_refund(refunds_issued_agg, users_aggregate, users_exact):

    od_exact = []
    for _, val in users_exact.data.items():
        od_exact.append([val['orig'], val['dest']])

    od_aggregate = []
    for _, val in users_aggregate.data.items():
        od_aggregate.append([val['orig'], val['dest']])

 
    refund_exact = []
    for i in range(len(od_exact)):

        # find index in od aggregate that has the same value
        od_exact_index = od_aggregate.index(od_exact[i])
        refund_exact.append(refunds_issued_agg[od_exact_index])

    return refund_exact
    
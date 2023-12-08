from ConstraintFunctions import findallConnectedNodes
from collections import Counter
from AlgorithmComparison import get_ports, NodeGroupConstraintDictBuilder, updateGraphByNGConstraint


def fp_flag(a, b):
    # true positive
    if a == 1 and b == 1:
        return 1
    # false positive
    if a == 0 and b == 1:
        return 0
    # true negative
    if b == 0:
        return 2


def checkandappend(nodeslist, b):
    repeatflag = 0
    for n in nodeslist:
        if Counter(n) == Counter(b):
            repeatflag = 1
            break
    if repeatflag == 0:
        nodeslist.append(b)
    return nodeslist


def Vespa_checker(t, l, flag):
    # true negative for Vespa, because it scanned all the possible graphs
    t = fp_flag(t, l)
    if flag == 1 and t == 2:
        t = 23
    return t, l


# calculate_false_pos([NetxSPLength, AstarLength, VespaLength1, VespaLength2, VespaLength], ConstraintList,
#                                                       [NetxSPControlNodeList, AstarControlNodeList, VespaControlNodeList1, VespaControlNodeList2,
#                                                        VespaControlNodeList], g_c, [flagFalseNegative1, flagFalseNegative2, flagFalseNegative])
def calculate_false_pos(p, cl, c, g_c, flag, g, ur):
    # l means the result of predict value, t means [0-false, 1-true] in the beginning and fp value in the end.
    l = [1] * len(p)
    t = [1] * len(p)
    for i in range(len(p)):
        if p[i] == -1:
            l[i] = 0
    nodeslist = []

    # check leakage in two naive algorithms
    # transfer control protocol list to constraint list by labeling all un-mentioned control ports as type 1 constraint.
    # feed that to NodeGroupConstraintDictBuilder() and updateGraphByNGConstraint(), we can get a residual graph without any edges blocked by the
    # control ports not in the control protocol list.
    # remove all the edges if they are not in the control list, then search the other ports.
    # If find an "other" port can be reached, assign t[i]=0
    ports = get_ports(g)


    # check the constraints again, make sure the target path follow all constraints.
    for cc in cl:
        if cc[0] == 1:
            nodes = findallConnectedNodes([cc[1]], g_c.edges())
            for n in nodes:
                for i in range(len(c)):
                    if n in c[i]:
                        t[i] = 0
            nodeslist = checkandappend(nodeslist, nodes)
        elif cc[0] == 2:
            nodes1 = findallConnectedNodes([cc[1]], g_c.edges())
            nodes2 = findallConnectedNodes([cc[2]], g_c.edges())
            for n in nodes1:
                for nn in nodes2:
                    for i in range(len(c)):
                        if n in c[i] and nn in c[i]:
                            t[i] = 0
            nodeslist = checkandappend(nodeslist, nodes1)
            nodeslist = checkandappend(nodeslist, nodes2)

    # true positive = 1, false positive = 0, true negative = 2, false negative = 3
    t[0] = fp_flag(t[0], l[0])
    t[1] = fp_flag(t[1], l[1])
    for i in range(2, len(p)):
        t[i], l[i] = Vespa_checker(t[i], l[i], flag[i-2])

    # other algorithm can find a path without breaking the constraint, that means Vespa is false negative
    if t[0] == 1 or t[1] == 1:
        for i in range(2, len(p)):
            if t[i] in [23, 2]:
                t[i] = 3
    return l, t, nodeslist
import networkx as nx
from networkx.drawing.nx_agraph import read_dot
from collections import Counter
import random


def createRandomConstraint(ControlNodes, n, VandCOlength):
    # generate a list consists of n constraints
    # 0. If the number of v and co is smaller than 2, cannot support constraint type 2. Directly give type 1
    # 1. Randomly choose the type of constraint
    # 2. If type 1,
    # 2-1. Randomly choose one control component (except control port) involved
    # 3. If type 2,
    # 3-1. Randomly choose two control components (except control port) involved
    ConstraintList = []
    i = 0
    while i < n:
        RepeatFlag = 0
        ConstraintEquation = []
        if VandCOlength < 2:
            ConstraintType = 0
        else:
            ConstraintType = random.randint(0, 1)
        if ConstraintType == 0:
            while 1:
                CtrlComponentNum = random.randint(0, len(ControlNodes) - 1)
                if ControlNodes[CtrlComponentNum][0] == 'v' or ControlNodes[CtrlComponentNum][1] == 'o':
                    break
            ConstraintNode = ControlNodes[CtrlComponentNum]
            ConstraintEquation = [1, ConstraintNode]
        else:
            while 1:
                CtrlComponentNum = random.randint(0, len(ControlNodes) - 1)
                CtrlComponentNum2 = random.randint(0, len(ControlNodes) - 1)
                if ControlNodes[CtrlComponentNum][0] == 'v' or ControlNodes[CtrlComponentNum][1] == 'o':
                    if ControlNodes[CtrlComponentNum2][0] == 'v' or ControlNodes[CtrlComponentNum2][1] == 'o':
                        while 1:
                            CtrlComponentNum2 = random.randint(0, len(ControlNodes) - 1)
                            if ControlNodes[CtrlComponentNum2][0] == 'v' or ControlNodes[CtrlComponentNum2][1] == 'o':
                                break
                        break
            if CtrlComponentNum == CtrlComponentNum2:
                RepeatFlag = 1
            else:
                ConstraintNode = ControlNodes[CtrlComponentNum]
                ConstraintNode2 = ControlNodes[CtrlComponentNum2]
                ConstraintEquation = [2, ConstraintNode, ConstraintNode2]

        if RepeatFlag == 1:
            continue
        for ExistsEdge in ConstraintList:
            if Counter(ConstraintEquation) == Counter(ExistsEdge):
                RepeatFlag = 1
                break
        if RepeatFlag == 1:
            continue
        ConstraintList.append(ConstraintEquation)
        i += 1
    return ConstraintList

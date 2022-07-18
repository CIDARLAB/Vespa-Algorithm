import matplotlib.pyplot as plt
import networkx as nx
import test
from networkx.drawing.nx_pydot import write_dot
from collections import Counter
import os


def createVertexList(nodeinfo, typeinfo):
    Vertexlist = []
    i = 0
    while i < len(nodeinfo):
        j = 1
        while j <= nodeinfo[i]:
            NodeName = f"{typeinfo[i]}{j}"
            Vertexlist.append(NodeName)
            j += 1
        i += 1
    return Vertexlist


def generateRandomNodeInfo(ComplexityUpperBound):
    # randomly choose the total number N of nodes
    N = test.randint(4, int(ComplexityUpperBound / 2) - 1)
    # randomly choose number Nf for flow-layer components, Nv for valves and Nc for control-layer, Nv can be 0
    Nf = test.randint(2, N - 2)
    Nc = N - Nf
    Nv = test.randint(1, Nc - 1)
    # decide number for Nfp, Nfo, Ncp, Nco
    Nfp = test.randint(2, Nf)
    Nfo = Nf - Nfp
    Ncp = test.randint(1, Nc - Nv)
    Nco = Nc - Ncp - Nv
    return [N, Nf, Nc, Nfp, Nfo, Ncp, Nv, Nco]


# generate edges, if the edge not exist in the past edge groups, go to the next enumerate
# exist, generate the edges again
def createFlowEdge(ENf):
    i = 0
    iterate = 1
    flow_edge_list = []
    FlowNodeInfo = CurrentNodeInfo[3:5]
    FPflag = 0
    FOflag = 0
    while i < ENf:
        iterate += 1
        if iterate > 200:
            break

        # each flow port should be one terminal of a connection, so firstly generate the edges include all flow ports
        # then generate the edges include all other flow components
        if FPflag < FlowNodeInfo[0]:
            NodeType1 = "f"
            NodeNum1 = FPflag + 1
        elif FOflag < FlowNodeInfo[1]:
            NodeType1 = "fo"
            NodeNum1 = FOflag + 1
        else:
            NodeType1Num = test.randint(0, len(FlowTypeList) - 1)
            if FlowNodeInfo[NodeType1Num] < 1:
                continue
            NodeType1 = FlowTypeList[NodeType1Num]
            NodeNum1 = test.randint(1, FlowNodeInfo[NodeType1Num])

        NodeType2Num = test.randint(0, len(FlowTypeList) - 1)
        if FlowNodeInfo[NodeType2Num] < 1:
            continue
        NodeType2 = FlowTypeList[NodeType2Num]
        NodeNum2 = test.randint(1, FlowNodeInfo[NodeType2Num])

        Node1 = f"{NodeType1}{NodeNum1}"
        Node2 = f"{NodeType2}{NodeNum2}"
        if Node1 == Node2:
            continue
        weight = 2
        CurrentEdge = [Node1, Node2, weight]
        # check if the edge we generate in this iteration exists in the edge list, if not, add into the list
        RepeatFlag = 0
        for ExistsEdge in flow_edge_list:
            if Counter(CurrentEdge) == Counter(ExistsEdge):
                RepeatFlag = 1
                break
        if RepeatFlag == 1:
            continue
        if FPflag < FlowNodeInfo[0]:
            FPflag += 1
        elif FOflag < FlowNodeInfo[1]:
            FOflag += 1
        flow_edge_list.append(CurrentEdge)
        i += 1
    return flow_edge_list


def createControlEdge(ENc):
    i = 0
    iterate = 1
    control_edge_list = []
    ControlNodeInfo = CurrentNodeInfo[5:]
    Vflag = 0
    COflag = 0
    # show if in this iteration the valve is one terminal necessarily

    while i < ENc:
        Vround = 0
        iterate += 1
        if iterate > 200:
            break
        # each control component should be one node of an edge and the other node is control port in need.
        # one co may connect to many control ports
        if Vflag < ControlNodeInfo[1] or COflag < ControlNodeInfo[2]:
            if Vflag < ControlNodeInfo[1]:
                NodeType1 = "v"
                Vround = 1
                NodeNum1 = Vflag + 1
            else:
                NodeType1 = "co"
                NodeNum1 = COflag + 1
            NodeType2Num = 0

        else:
            NodeType1Num = test.randint(0, len(ControlTypeList) - 1)
            if ControlNodeInfo[NodeType1Num] < 1:
                continue
            NodeType1 = ControlTypeList[NodeType1Num]
            NodeNum1 = test.randint(1, ControlNodeInfo[NodeType1Num])
            # two control ports are not allowed to connect as an edge
            if NodeType1Num == 0:
                NodeType2Num = test.randint(1, len(ControlTypeList) - 1)

        if ControlNodeInfo[NodeType2Num] < 1:
            continue
        NodeType2 = ControlTypeList[NodeType2Num]
        NodeNum2 = test.randint(1, ControlNodeInfo[NodeType2Num])

        Node1 = f"{NodeType1}{NodeNum1}"
        Node2 = f"{NodeType2}{NodeNum2}"
        if Node1 == Node2:
            continue
        weight = 1
        CurrentEdge = [Node1, Node2, weight]
        # check if the edge we generate in this iteration exists in the edge list, if not, add into the list
        RepeatFlag = 0
        for ExistsEdge in control_edge_list:
            if Counter(CurrentEdge) == Counter(ExistsEdge):
                RepeatFlag = 1
                break
        if RepeatFlag == 1:
            continue

        # Check if this is round for building edge with one valve, if not, check if COflag is bigger than its upper
        # bound, if not, add 1 into its value
        if Vround == 1:
            Vflag += 1
        elif COflag < ControlNodeInfo[2]:
            COflag += 1
        control_edge_list.append(CurrentEdge)
        i += 1
    return control_edge_list


def createNumberOfFlowAndControlEdge(EdgeNum):
    ENf = 0
    ENc = 0
    iterate = 0
    while 1:
        iterate += 1
        if iterate > 200:
            break
        ENfUpperBound = min(int(Nf * (Nf - 1) / 2), EdgeNum - Nco - Nv)
        if Nf - 1 >= ENfUpperBound:
            continue
        ENf = test.randint(Nf, ENfUpperBound)
        ENc = EdgeNum - ENf
        if ENc > 0 and ENc in range(Nco + Nv, int(Nc * (Nc - 1) / 2)):
            break
        elif ENc == 0:
            break
    return iterate, ENf, ENc


# plot the random graph, two layer with different color
def plotAndSave(SectionNum, flow_edge_list, control_edge_list, CurrentNodeInfo, CurrentEdgeInfo, edgenum, nodenum):
    g_flow = nx.DiGraph()
    g_control = nx.DiGraph()

    # create a list of node names
    FlowNodeInfo = CurrentNodeInfo[3:5]
    ControlNodeInfo = CurrentNodeInfo[5:]
    flow_node_list = createVertexList(FlowNodeInfo, FlowTypeList)
    control_node_list = createVertexList(ControlNodeInfo, ControlTypeList)

    # add elements into g_flow and g_control
    g_flow.add_nodes_from(flow_node_list)
    g_flow.add_weighted_edges_from(flow_edge_list)
    g_control.add_nodes_from(control_node_list)
    g_control.add_weighted_edges_from(control_edge_list)
    if EdgeGroupNum == 1:
        print("Flow and Control node list:")
        print(flow_node_list)
        print(control_node_list)

    ValveCOLocateList = []
    valve_list = control_node_list[CurrentNodeInfo[5]:CurrentNodeInfo[5]+CurrentNodeInfo[6]]
    co_list = control_node_list[CurrentNodeInfo[5]+CurrentNodeInfo[6]:]
    for i in range(CurrentNodeInfo[6]):
        valve_location = test.randint(0, len(flow_edge_list) - 1)
        valve_relationship = [valve_list[i]] + flow_edge_list[valve_location][0:2]
        ValveCOLocateList.append(valve_relationship)

    for i in range(CurrentNodeInfo[7]):
        co_location = test.randint(0, len(flow_edge_list) - 1)
        co_relationship = [co_list[i]] + flow_edge_list[co_location][0:2]
        ValveCOLocateList.append(co_relationship)

    str1 = '_'.join(str(v) for v in CurrentNodeInfo)
    str2 = '_'.join(str(v) for v in CurrentEdgeInfo)
    folder_path = f"RandomCaseFiles/Section_{SectionNum}/Node{nodenum}_{str1}"
    outpath_v = f"RandomCaseFiles/Section_{SectionNum}/Node{nodenum}_{str1}/Edge{edgenum}|{str2}_valve&co.txt"
    outpath_c = f"RandomCaseFiles/Section_{SectionNum}/Node{nodenum}_{str1}/Edge{edgenum}|{str2}_control.dot"
    outpath_f = f"RandomCaseFiles/Section_{SectionNum}/Node{nodenum}_{str1}/Edge{edgenum}|{str2}_flow.dot"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    write_dot(g_flow, outpath_f)
    write_dot(g_control, outpath_c)
    with open(outpath_v, 'w') as f:
        for vi in ValveCOLocateList:
            vi = str(vi).strip('[').strip(']').replace(',', '').replace('\'', '') + '\n'
            f.writelines(vi)

    # plot control layer graph
    pos = nx.spring_layout(g_control)
    color_list = ['red' for i in range(len(control_node_list))]
    nx.draw_networkx(g_control, pos, nodelist=control_node_list, node_color=color_list)
    plt.show()

    # plot flow layer graph
    pos = nx.spring_layout(g_flow)
    color_list = ['yellow' for i in range(len(flow_node_list))]
    nx.draw_networkx(g_flow, pos, nodelist=flow_node_list, node_color=color_list)
    plt.show()


# complexity bound for each section: [0, 40, 100, 500, inf]
# for section 4, the upperbound of loop var flag and iteration is 4 times bigger than previous ones
if __name__ == '__main__':

    SectionNum = 4
    ComplexityLowerBound, ComplexityUpperBound = 501, 1000
    FlowTypeList = ["f", "fo"]
    ControlTypeList = ["c", "v", "co"]
    NodeGroupNum = 1
    NodeList = []
    while NodeGroupNum <= 25:
        [N, Nf, Nc, Nfp, Nfo, Ncp, Nv, Nco] = generateRandomNodeInfo(ComplexityUpperBound)
        CurrentNodeInfo = [N, Nf, Nc, Nfp, Nfo, Ncp, Nv, Nco]
        if CurrentNodeInfo in NodeList:
            continue
        else:
            NodeList.append(CurrentNodeInfo)

        # creat edges and check if it will go beyond the complexity upper bound for current section
        # randomly choose number of edges for the current node group in a limited range
        # since we divide the chip into two different graphs, we need to have limited edges giving the num of nodes
        EdgeGroupNum = 1
        flag = 0
        EdgeNumInfo = []
        EdgeListAll = []
        flow_edge_listAll = []
        control_edge_listAll = []
        while EdgeGroupNum <= 8:
            flag += 1
            if flag > 2000:
                break
            EdgeNumUpperBound = min(ComplexityUpperBound - N * 2, int(Nf * (Nf - 1) / 2 + Nc * (Nc - 1) / 2))

            # make sure all control components has connection to control port and all flow layer components are connected
            EdgeNumLowerBound = max(ComplexityLowerBound - 2 * N, Nf - 1 + Nv + Nco)
            if EdgeNumUpperBound < EdgeNumLowerBound:
                continue

            # randomly choose number of flow and control edges, and create flow and control edges in detail
            EdgeNum = test.randint(EdgeNumLowerBound, EdgeNumUpperBound)
            iterate, ENf, ENc = createNumberOfFlowAndControlEdge(EdgeNum)
            if iterate > 200:
                continue
            flow_edge_list = createFlowEdge(ENf)
            control_edge_list = createControlEdge(ENc)
            EdgeList = flow_edge_list + control_edge_list

            # number of edges are not be given in a good departure, return back to change the edge number
            if len(EdgeList) < EdgeNum:
                continue
            CurrentEdgeInfo = [EdgeNum, ENf, ENc]
            if CurrentEdgeInfo in EdgeNumInfo:
                continue
            EdgeNumInfo.append(CurrentEdgeInfo)
            EdgeGroupNum += 1
            EdgeListAll.append(EdgeList)
            flow_edge_listAll.append(flow_edge_list)
            control_edge_listAll.append(control_edge_list)

        if flag > 2000:
            NodeList.pop()
            print("Beyond loop upper bound, try a new node group again!")
            continue
        print()
        print(NodeList[-1])
        for i in range(len(EdgeListAll)):
            plotAndSave(SectionNum, flow_edge_listAll[i], control_edge_listAll[i], NodeList[-1], EdgeNumInfo[i], i+1, NodeGroupNum)
            # print(EdgeNumInfo[i])
            # print(EdgeListAll[i])
        print()
        NodeGroupNum += 1

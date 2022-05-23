import json
from typing import Dict, Tuple
import networkx as nx
from parchmint.device import ValveType

from pymint.mintdevice import MINTDevice
from pymint.mintlayer import MINTLayerType
from pymint.minttarget import MINTTarget
import re


def read_valve_map_file(filename: str) -> Dict[str, Tuple[str, str]]:
    """
    Reads the valve map file and returns a dictionary of valve IDs to connection IDs.
    """
    valve_map = {}
    with open(filename, "r") as f:
        for line in f:
            valve_id, sourc_id, sink_id = line.strip().split(" ")
            valve_map[valve_id] = (sourc_id, sink_id)
    return valve_map


def generate_random_graphs(
    flow_vertices, max_ports, max_valves, max_control_ports
) -> Tuple[nx.DiGraph, nx.DiGraph, Dict[str, Tuple[str, str]]]:
    """
    Generates a random graph with the given number of vertices and edges.
    """
    flow_graph = nx.drawing.nx_agraph.read_dot(
        f"../TestCaseFiles/Section_1/Node1_10_7_3_5_2_1_2_0/Edge1|16_14_2_flow.dot")
    control_graph = nx.drawing.nx_agraph.read_dot(
        f"../TestCaseFiles/Section_1/Node1_10_7_3_5_2_1_2_0/Edge1|16_14_2_control.dot")

    # Valve map has the valve id as the key and the tuple for source and sink ids
    # as the value.
    valve_map = read_valve_map_file("../TestCaseFiles/Section_1/Node1_10_7_3_5_2_1_2_0/Edge1|16_14_2_valve&co.txt")

    return nx.DiGraph(flow_graph), nx.DiGraph(control_graph), valve_map


def generate_random_netlists(device_name: str) -> MINTDevice:
    """
    Generates a random netlist.
    """
    flow_graph, control_graph, valve_map = generate_random_graphs(5, 6, 7, 8)

    device = MINTDevice(device_name)
    device.create_mint_layer("FLOW", "0", "0", MINTLayerType.FLOW)
    device.create_mint_layer("CONTROL", "0", "0", MINTLayerType.CONTROL)

    # Loop through the nodes and create new components in the device.
    for node in flow_graph.nodes():

        # TODO - Decide if this is a port or something else
        if re.compile("^f").match(node):
            mint_string = "PORT"
        elif re.compile("^fo").match(node):
            mint_string = "MIXER"
        else:
            print("Not adding node: {}, since type is unknown".format(node))
            continue
        device.create_mint_component(node, mint_string, {}, ["FLOW"])

    # Loop through the edges and create new connections in the device.
    connection_count = 0
    for edge in flow_graph.edges():
        device.create_mint_connection(
            "connection_{}".format(connection_count),
            "CHANNEL",
            {},
            MINTTarget(edge[0], None),
            [MINTTarget(edge[1], None)],
            "FLOW",
        )

        connection_count += 1

    # Go through the dictionary entries and add the valves to the device.
    for valve_id, (source_id, sink_id) in valve_map.items():
        for connection in device.get_connections():
            if (
                connection.source.component == source_id
                and connection.sinks[0].component == sink_id
            ):
                device.create_valve(
                    valve_id,
                    "VALVE3D",
                    {},
                    ["CONTROL"],
                    connection,
                    ValveType.NORMALLY_CLOSED,
                )
                break

    # Insert the rest of the control nodes
    for node in control_graph.nodes():
        if device.component_exists(node):
            continue
        if re.compile("^c").match(node):
            mint_string = "PORT"
        elif re.compile("^co").match(node):
            mint_string = "MIXER"
        else:
            print("Not adding node: {}, since type is unknown".format(node))
            continue

        device.create_mint_component(node, mint_string, {}, ["CONTROL"])

    # Loop through the edges and create new connections in the device.
    connection_count = 0
    for edge in control_graph.edges():
        device.create_mint_connection(
            "control_connection_{}".format(connection_count),
            "CHANNEL",
            {},
            MINTTarget(edge[0], None),
            [MINTTarget(edge[1], None)],
            "CONTROL",
        )

        connection_count += 1

    return device


device = generate_random_netlists("Node1_10_7_3_Edge1|16_14_2")


print(device.to_parchmint_v1_x())

jsonstring = json.dumps(device.to_parchmint_v1_x())

file = open("TestCaseFiles/{}.json".format(device.name), "w")
file.write(jsonstring)
file.close()
print(device.to_MINT())

file = open("TestCaseFiles/{}.mint".format(device.name), "w")
file.write(device.to_MINT())
file.close()

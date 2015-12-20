import json
import sys
from collections import namedtuple

def find_maximum_cycle_from_root(root, dest_list, adj_list, route):
    if not dest_list:
        return -sys.maxsize - 1

    maximum_cost = -sys.maxsize - 1
    best_route_dst = []
    for edge in dest_list:
        route_edge = route
        if edge not in route_edge:
            if edge.dst == root:
                if len(route_edge) >= 4 and edge.value > maximum_cost:
                    maximum_cost = edge.value
                    best_route_dst = [edge]
            elif edge.dst in adj_list:
                route_edge.append(edge)
                cost_route, route_dst = find_maximum_cycle_from_root(root, adj_list[edge.dst], adj_list, route_edge)
                if cost_route > maximum_cost:
                    maximum_cost = cost_route + edge.value
                    best_route_dst = []
                    best_route_dst.extend(route_dst)
                    best_route_dst.append(edge)
    return maximum_cost, best_route_dst

with open('graph.json', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

Edge = namedtuple('Edge', 'src dst value')

adj_list = {}
maximum_cost = -sys.maxsize - 1

for route in json_data:
    for key, value in route.items():
        src, dst = key.split('-')
        edge = Edge(src, dst, value)
        if src not in adj_list:
            adj_list[src] = []
        adj_list[src].append(edge)

for src in adj_list:
    cost_src, route_src = find_maximum_cycle_from_root(src, adj_list[src], adj_list, [])
    if cost_src > maximum_cost:
        best_route = route_src
        maximum_cost = cost_src
        print('Most profitable for Source ' + src + ':' + str(maximum_cost))

print('Most profitable cycle on the graph: ' + str(maximum_cost))
print('The best route: ')
for edge in best_route[::-1]:
    print('Source '+ edge.src + ' to Destination ' + edge.dst + ' - Value: ' + str(edge.value))

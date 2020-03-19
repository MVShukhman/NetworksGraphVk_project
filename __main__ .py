from constants import *
from vk_parser import VkParser
from py2neo import Graph, Node, Relationship


def main():
    parser = VkParser(DRIVER_PATH)
    parser.login(LOGIN, PASSWORD)
    friends_ids = list(parser.get_friends_list(START_ID))
    edges = {START_ID: friends_ids}
    for id in friends_ids:
        edges[id] = []
        for friend_id in parser.get_friends_list(id):
            if friend_id in friends_ids:
                edges[id] += [friend_id]
    nodes = {}
    g = Graph()
    tx = g.begin()
    for id in friends_ids:
    	node = Node("Person", id=id)
    	nodes[id] = node
    for id in friends_ids:
    	for friend in nodes[id]:
    		edge = Relationship(nodes[id], "FRIENDSHIP", nodes[friend])
    		tx.create(edge)
    		tx.commit()


main()
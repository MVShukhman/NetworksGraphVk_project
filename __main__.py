from constants import *
from vk_parser import VkParser


def main():
    parser = VkParser(DRIVER_PATH)
    parser.login(LOGIN, PASSWORD)
    friends_ids = list(parser.get_friends_list(START_ID))
    edges = {START_ID: friends_ids}
    for id in friends_ids:
        edges[id] = list(parser.get_friends_list(id))
    print(edges)


main()
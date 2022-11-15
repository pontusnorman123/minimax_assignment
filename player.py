#!/usr/bin/env python3
import random

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR


class PlayerControllerHuman(PlayerController):
    def player_loop(self):
        """
        Function that generates the loop of the game. In each iteration
        the human plays through the keyboard and send
        this to the game through the sender. Then it receives an
        update of the game through receiver, with this it computes the
        next movement.
        :return:
        """

        while True:
            # send message to game that you are ready
            msg = self.receiver()
            if msg["game_over"]:
                return


class PlayerControllerMinimax(PlayerController):

    def __init__(self):
        super(PlayerControllerMinimax, self).__init__()

    def player_loop(self):
        """
        Main loop for the minimax next move search.
        :return:
        """

        # Generate first message (Do not remove this line!)
        first_msg = self.receiver()

        while True:
            msg = self.receiver()

            # Create the root node of the game tree
            node = Node(message=msg, player=0)

            # Possible next moves: "stay", "left", "right", "up", "down"
            best_move = self.search_best_next_move(initial_tree_node=node)

            # Execute next action
            self.sender({"action": best_move, "search_time": None})

    def search_best_next_move(self, initial_tree_node):
        """
        Use minimax (and extensions) to find best possible next move for player 0 (green boat)
        :param initial_tree_node: Initial game tree node
        :type initial_tree_node: game_tree.Node
            (see the Node class in game_tree.py for more information!)
        :return: either "stay", "left", "right", "up" or "down"
        :rtype: str
        """

        # EDIT THIS METHOD TO RETURN BEST NEXT POSSIBLE MODE USING MINIMAX ###

        # NOTE: Don't forget to initialize the children of the current node
        #       with its compute_and_get_children() method!

        print("fishes: ", initial_tree_node.state.get_fish_positions())
        print("hook:", initial_tree_node.state.get_hook_positions()[0])
        print("min_dis: ", self.create_hueristic(initial_tree_node))

        random_move = random.randrange(5)
        return 1

    def get_hueristic(node, depth):

        node.compute_and_get_children
        if (depth != 1):
            depth = depth - 1

            for c in node.children:
                c.setValue(node.get_hueristic(c, depth))

        else:
            # create hueristic
            return 1  # min/max

    def get_min_distance(self,node):
        p1 = node.state.get_hook_positions()[0]
        fishes = node.state.get_fish_positions()
        p0_x = p1[0]
        p0_y = p1[1]
        min_dis = 999
        closest_fish = 0

        for i in range(len(fishes)):
            x = abs(fishes[i][0] - p0_x)
            y = abs(fishes[i][1] - p0_y)
            if((x+y < min_dis)):
                min_dis = x+y
                closest_fish = i

        return min_dis,closest_fish


    def create_hueristic(self,node):

        min_dis,closest_fish = self.get_min_distance(node)

        print("the fish: ", closest_fish)
        return min_dis


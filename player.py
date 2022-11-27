#!/usr/bin/env python3
import random

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR

hash_table_states = {}


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

        nodes = initial_tree_node.compute_and_get_children()

        alpha = -999999
        beta = 9999
        highScore = -99999
        best_move = 0

        #print(hash_table_states)

        for node in nodes:
            player = node.state.get_player()
            score = self.iter_depth_search(node, alpha, beta, player,highScore,7,0)
            if (score > highScore):
                highScore = score
                best_move = node.move
        return ACTION_TO_STR[best_move]

    def iter_depth_search(self,node,a,b,player, prev_node_value,max_depth,cur_depth):

        cur_depth = cur_depth + 1
        if max_depth == cur_depth or node.compute_and_get_children() == []:
            return self.evaluation(node)

            ##Kollar om state finns i hash tabell
        if (hash(node.state) in hash_table_states.keys()):
            return hash_table_states.get(hash(node.state))

        if player == 0:
            current_node_value = self.evaluation(node)
            v = -99999

            #### Jämför om vi har bättre värde nu än den förra noden och om vi har det behöver vi inte gå djupare så vi returnar istället direkt.
            if(current_node_value <= prev_node_value):
                nodes = node.compute_and_get_children()
                for child in nodes:
                    v = max(v, self.iter_depth_search(child, a, b, 1,current_node_value,max_depth,cur_depth))
                    a = max(a, v)
                    if b <= a:
                        break
                return v
            else:
                return current_node_value
        else:
            current_node_value = self.evaluation_p1(node)
            v = 99999
            nodes = node.compute_and_get_children()
            for child in nodes:
                v = min(v, self.iter_depth_search(child, a, b, 0,current_node_value,max_depth,cur_depth))
                b = min(b, v)
                if a >= b:
                    break
            return v
    def minimax(self, node, depth, a, b, player):
        if depth == 0 or node.compute_and_get_children() == []:
            return self.evaluation(node)

        ##Kollar om state finns i hash tabell
        if(hash(node.state) in hash_table_states.keys()):
            return hash_table_states.get(hash(node.state))

        nodes = node.compute_and_get_children()
        if player == 0:
            v = -99999
            for child in nodes:
                v = max(v, self.minimax(child, depth-1, a, b, 1))
                a = max(a, v)
                if b <= a:
                    break
            return v
        else:
            v = 99999
            for child in nodes:
                v = min(v, self.minimax(child, depth-1, a, b, 0))
                b = min(b, v)
                if a >= b:
                    break
            return v

    def computerBlocks(self, node, fishPos):
        hooks = node.state.get_hook_positions()
        computerPos = hooks[1][0]
        playerPos = hooks[0][0]

        if (min(fishPos, playerPos) <= computerPos <= max(fishPos, playerPos)):
            return True

        return False

    def evaluation(self, node):
        p = abs(node.state.get_player_scores()[0])  # Player points
        c = node.state.get_player_scores()[1]       # Computer points
        heuristic = p-c
        # Difference in points
        if( hash(node.state) not in hash_table_states.keys() and node.state.player == 0):
            self.add_state_to_hash_table(hash(node.state),heuristic + self.decideFish(node)) ## add state with value to hash table
        return heuristic + self.decideFish(node)

    def evaluation_p1(self,node):
        p = abs(node.state.get_player_scores()[0])  # Player points
        c = node.state.get_player_scores()[1]       # Computer points
        heuristic = c-p
        # Difference in points
        self.add_state_to_hash_table(hash(node.state),heuristic + self.decideFish(node)) ## add state with value to hash table
        return heuristic + self.decideFish(node)

    def decideFish(self, node):
        fishes = node.state.get_fish_positions()
        hookPos = node.state.get_hook_positions()[0]
        ratio = 0
        for f in fishes:
            x = abs(hookPos[0]-fishes[f][0])
            if (self.computerBlocks(node, fishes[f][0])):
                x = abs(20-x)
            y = abs(hookPos[1] - fishes[f][1])
            d = x + y
            point = abs(node.state.get_fish_scores()[f]) ##Ska det vara abs om vissa fiskar har negativ poäng
            point = node.state.get_fish_scores()[f] ##Ska det vara abs om vissa fiskar har negativ poäng
            ratio = max(ratio, point/((d*d)+1))
        return ratio


    def add_state_to_hash_table(self,state,value):

        hash_table_states.update({state : value})
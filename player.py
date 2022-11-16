#!/usr/bin/env python3
from math import inf
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

        #print("fishes: ", initial_tree_node.state.get_fish_positions())
        #print("hook:", initial_tree_node.state.get_hook_positions()[0])
        #print("min_dis: ", self.create_hueristic(initial_tree_node))
        random_move = random.randrange(5)
        # print(ACTION_TO_STR[random_move])
        startPlayer = 0
        print(self.get_hueristic(initial_tree_node, 4, 0))

        return self.optimalMove(initial_tree_node)

    def createHeuristic(self, node):
        # Return poängställning
        """
        Input: hookPos, fishesPos, player.scores()
        Function: Beräkna poängställning efter move
        Output: Poängställning
        """
        p = node.state.get_player_scores()[0]
        c = node.state.get_player_scores()[1]
        return p-c

    def get_hueristic(self, node, depth, player):

        node.compute_and_get_children()
        if (depth == 1):
            return self.createHeuristic(node)

        depth = depth - 1

        if (player == 0):
            player = 1
            bestPossible = -inf
            for child in node.children:
                points = self.get_hueristic(child, depth, player)
                bestPossible = max(bestPossible, points)
            return bestPossible
        else:
            bestPossible = inf
            player = 0
            for child in node.children:
                points = self.get_hueristic(child, depth, player)
                bestPossible = min(bestPossible, points)
            return bestPossible

    """
    Rules:
    1. a/b pruning - "poäng skillnaden mellan p och c + poäng/fisk"
    2. getMinDistance

    1. Go for the best fish first
    2. Position hook on same level as fish before moving boat
    3. Move boat closer to fish

    """

    def highestFishScore(self, node):
        fishes = node.state.get_fish_positions()
        highScore = 0
        bestFishes = []
        for fish in fishes:
            tempScore = node.state.get_fish_scores()[fish]
            if tempScore > highScore:
                highScore = tempScore
                bestFishes.append(fish)
        return bestFishes

    def getDistance(self, playerPos, fishPos, movePos):
        x = abs(playerPos[0]-fishPos[0] + movePos[0])
        y = abs(playerPos[1]-fishPos[1] + movePos[1])
        return x + y

    def bestMove(self, node, bestFishes):
        moves = {"left": (-1, 0), "right": (1, 0),
                 "up": (0, 1), "down": (0, -1), "stay": (0, 0)}
        hookPos = node.state.get_hook_positions()[0]
        fishesPos = node.state.get_fish_positions()
        minDistance = 666
        bestMove = "stay"
        for fish in bestFishes:
            for move in moves:
                tempDistance = self.getDistance(
                    hookPos, fishesPos[fish], moves[move])
                #print("HookPos:", hookPos, "   ", "FishPos:", fishesPos[fish])
                #print("distance:", tempDistance, "   ", "move", move)
                if tempDistance < minDistance:
                    minDistance = tempDistance
                    targetFish = fish
                    bestMove = move
        return bestMove

    def optimalMove(self, node):
        # GetHeuristic (skapar träd, kollar alla noder, hittar best outcome)

        # Om det skiter sig (kan inte se tillräckligt långt fram)
        # getMinDistance --> bestMove

        # Return poängställningen i varje state
        moves = {"left": (-1, 0), "right": (1, 0),
                 "up": (0, 1), "down": (0, -1), "stay": (0, 0)}

        min_dis = 666
        bestMove = "stay"
        bestFishes = self.highestFishScore(node)
        #print("TargetedFish:", bestFishes)
        theMove = self.bestMove(node, bestFishes)
        return theMove

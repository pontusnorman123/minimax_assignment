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
        #self.get_hueristic(initial_tree_node, 2, 0)
        # print(initial_tree_node.get_move())

        return self.optimalMove(initial_tree_node, 4)

    def closestFish(self, node, player):
        fishes = node.state.get_fish_positions()
        hookpos = node.state.get_hook_positions()[player]
        minDistance = 666
        for fish in fishes:
            x = abs(hookpos[0]-fishes[fish][0])
            y = abs(hookpos[1]-fishes[fish][1])
            if ((x+y) < minDistance):
                minDistance = x+y
        return (1/(minDistance+1))

    def evaluation(self, node):
        # Return poängställning
        """
        Input: hookPos, fishesPos, player.scores()
        Function: Beräkna poängställning efter move
        Output: Poängställning
        """

        p = node.state.get_player_scores()[0]
        c = node.state.get_player_scores()[1]
        heuristic = p-c
        player = node.state.player
        #print(node.move, "  ", node.state.player_caught)
        # min
        if (player):
            return heuristic - self.closestFish(node, player)
        return heuristic + self.closestFish(node, player)

    def minmax(self, node, depth, player):
        #print("Depth:", depth, "   Player:", player)
        if (depth == 0):
            #print(ACTION_TO_STR[node.move], node.state.get_fish_positions(), node.state.get_hook_positions()[0])
            return self.evaluation(node)

        node.compute_and_get_children()  # Populate node with children

        depth = depth - 1

        if (player == 0):
            player = 1
            bestPossible = -inf
            for child in node.children:
                points = self.minmax(child, depth, player)
                bestPossible = max(bestPossible, points)
                #print(ACTION_TO_STR[child.move], points, "   ", end="")
            #print("Depth:", node.depth, "   Player:", "0.   ", bestPossible)
            return bestPossible
        else:
            bestPossible = inf
            player = 0
            for child in node.children:
                points = self.minmax(child, depth, player)
                #print("Move:", child.get_move(), "    Points:", points)
                bestPossible = min(bestPossible, points)
            #print("BestPossible:", bestPossible)
            # print("----")
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

    def bestMove(self, node):
        moves = {
            "up": (0, 1), "down": (0, -1), "stay": (0, 0)}
        hookPos = node.state.get_hook_positions()[0]
        fishesPos = node.state.get_fish_positions()
        minDistance = 666
        bestMove = "stay"
        for fish in fishesPos:
            for move in moves:
                tempDistance = self.getDistance(
                    hookPos, fishesPos[fish], moves[move])
                #print("HookPos:", hookPos, "   ", "FishPos:", fishesPos[fish])
                #print("distance:", tempDistance, "   ", "move", move)
                if tempDistance < minDistance:
                    minDistance = tempDistance
                    targetFish = fish
                    bestMove = move
        return bestMove, minDistance

    def minmaxMove(self, node, depth):
        children = node.compute_and_get_children()
        bestScore = -inf
        bestMoves = 0
        print("")
        print(" --- Possible Scores ---")
        for child in children:
            # print(child.move)
            score = self.minmax(child, depth-1, 0)
            print(ACTION_TO_STR[child.move], score, "   ", end="")
            if (score > bestScore):
                bestScore = score
                bestMoves = child.move
        print("")
        print("BestMove:", ACTION_TO_STR[bestMoves],
              "    BestScore:", bestScore)
        return ACTION_TO_STR[bestMoves]

    def optimalMove(self, node, depth):
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
        moveCloser, distance = self.bestMove(node)
        smartMove = self.minmaxMove(node, depth)
        print("Distance:", distance)
        print("Closer", moveCloser, "   Smart", smartMove)
        if (distance > depth/2):
            return moveCloser

        return smartMove

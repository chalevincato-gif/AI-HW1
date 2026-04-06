import math
import random
import copy
from dlgo.gotypes import Player, Point
from dlgo.goboard import GameState, Move

__all__ = ["MCTSAgent"]

class MCTSNode:
    def __init__(self, game_state, parent=None, prior=1.0):
        self.game_state = game_state
        self.parent = parent
        self.children = []
        self.visit_count = 0
        self.value_sum = 0
        self.prior = prior
        self.move = None  

    @property
    def value(self):
        if self.visit_count == 0:
            return 0.0
        return self.value_sum / self.visit_count

    def is_leaf(self):
        return len(self.children) == 0

    def is_terminal(self):
        return self.game_state.is_over()

    def best_child(self, c=1.414):
        if not self.children:
            return self

        best_score = -float('inf')
        best_node = self.children[0]
        
        for child in self.children:
            if child.visit_count == 0:
                return child
            
            exploitation = child.value
            exploration = c * math.sqrt(math.log(self.visit_count) / child.visit_count)
            score = exploitation + exploration
            
            if score > best_score:
                best_score = score
                best_node = child
                
        return best_node

    def expand(self):
        if len(self.children) > 0:
            return self.children

        for move in self.game_state.legal_moves():
            next_state = self.game_state.apply_move(move)
            new_node = MCTSNode(game_state=next_state, parent=self)
            new_node.move = move  
            self.children.append(new_node)
            
        return self.children

    def backup(self, value):
        self.visit_count += 1
        self.value_sum += value
        
        # Perspective flip: What is good for me is bad for my opponent
        if self.parent is not None:
            self.parent.backup(1.0 - value)


class MCTSAgent:
    def __init__(self, num_rounds=1000, temperature=1.0):
        self.num_rounds = num_rounds
        self.temperature = temperature

    def select_move(self, game_state: GameState) -> Move:
        legal_moves = game_state.legal_moves()
        if not legal_moves:
            return Move.pass_turn()

        root = MCTSNode(game_state)

        for _ in range(self.num_rounds):
            node = root
            
            # 1. Selection
            while (not node.is_leaf()) and (not node.is_terminal()):
                node = node.best_child()
            
            # 2. Expansion
            if not node.is_terminal():
                children = node.expand()
                if children:
                    node = random.choice(children)
            
            # 3. Simulation
            value = self._simulate(node.game_state)
            
            # 4. Backpropagation
            node.backup(value)
            
        best_move = self._select_best_move(root)
        
        # Fallback if MCTS somehow fails to pick a move
        if best_move is None:
            return random.choice(legal_moves)
            
        return best_move

    def _simulate(self, game_state):
        current_state = copy.deepcopy(game_state)
        
        depth = 0
        max_depth = 30
        
        while (not current_state.is_over()) and (depth < max_depth):
            possible_moves = current_state.legal_moves()
            if not possible_moves:
                break
            move = random.choice(possible_moves)
            current_state = current_state.apply_move(move)
            depth += 1
            
        winner = current_state.winner()
        if winner is None:
            return 0.5  
            
        # Determine who just moved to cause this state
        player_who_just_moved = Player.black if game_state.next_player == Player.white else Player.white
        
        if winner == player_who_just_moved:
            return 1.0 
        else:
            return 0.0 

    def _select_best_move(self, root):
        best_move = None
        best_visits = -1
        
        for child in root.children:
            if child.visit_count > best_visits:
                best_visits = child.visit_count
                best_move = child.move
                
        return best_move
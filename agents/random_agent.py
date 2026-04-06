import random
from dlgo import GameState, Move

__all__ = ["RandomAgent"]


class RandomAgent:
    def __init__(self):
        pass

    def select_move(self, game_state: GameState) -> Move:
        legal_moves = game_state.legal_moves()

        chosen_move = random.choice(legal_moves)

        return chosen_move

def random_agent(game_state: GameState) -> Move:
    agent = RandomAgent()
    return agent.select_move(game_state)
"""
第一小问（必做）：随机 AI

基于随机落子（但需满足规则）的基础围棋 AI
用于验证规则调用和基础设施正常工作。
"""

import random
from dlgo import GameState, Move

__all__ = ["RandomAgent"]


class RandomAgent:
    """
    随机落子智能体 - 第一小问实现

    从所有合法棋步中均匀随机选择，包括：
    - 正常落子
    - 停一手 (pass)
    - 认输 (resign)
    """

    def __init__(self):
        pass

    def select_move(self, game_state: GameState) -> Move:
        # 1. Ask the game engine for a list of all legal moves right now
        legal_moves = game_state.legal_moves()
        
        # 2. Randomly pick one move from that list
        chosen_move = random.choice(legal_moves)
        
        # 3. Return the move so the game can play it
        return chosen_move


# 便捷函数（向后兼容 play.py）
def random_agent(game_state: GameState) -> Move:
    """函数接口，兼容 play.py 的调用方式"""
    agent = RandomAgent()
    return agent.select_move(game_state)
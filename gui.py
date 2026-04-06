import tkinter as tk
from dlgo.goboard import GameState, Move
from dlgo.gotypes import Player, Point
from agents.mcts_agent import MCTSAgent

BOARD_SIZE = 5
CELL_SIZE = 60
MARGIN = 40
CANVAS_SIZE = (BOARD_SIZE - 1) * CELL_SIZE + 2 * MARGIN

class GoGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("5x5 Go AI (Human vs MCTS)")
        
        # Setup the canvas
        self.canvas = tk.Canvas(master, width=CANVAS_SIZE, height=CANVAS_SIZE, bg="#DCB35C")
        self.canvas.pack()
        
        # Bind left mouse click to our handler
        self.canvas.bind("<Button-1>", self.handle_click)
        
        # Initialize the engine and your AI
        self.game_state = GameState.new_game(BOARD_SIZE)
        self.agent = MCTSAgent(num_rounds=1000, temperature=1.0)
        
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        
        # Draw grid lines
        for i in range(BOARD_SIZE):
            x = MARGIN + i * CELL_SIZE
            self.canvas.create_line(x, MARGIN, x, CANVAS_SIZE - MARGIN, width=2)
            y = MARGIN + i * CELL_SIZE
            self.canvas.create_line(MARGIN, y, CANVAS_SIZE - MARGIN, y, width=2)
            
        # Draw stones based on the dlgo internal board state
        for r in range(1, BOARD_SIZE + 1):
            for c in range(1, BOARD_SIZE + 1):
                stone = self.game_state.board.get(Point(row=r, col=c))
                if stone is not None:
                    # Math to convert grid (row, col) back to pixels (x, y)
                    y = MARGIN + (BOARD_SIZE - r) * CELL_SIZE
                    x = MARGIN + (c - 1) * CELL_SIZE
                    
                    color = "black" if stone == Player.black else "white"
                    radius = CELL_SIZE * 0.4
                    self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)

    def handle_click(self, event):
        if self.game_state.is_over():
            print("Game Over!")
            return
            
        # 1. Translate pixel click to grid intersection
        c = round((event.x - MARGIN) / CELL_SIZE) + 1
        r = BOARD_SIZE - round((event.y - MARGIN) / CELL_SIZE)
        
        # Ignore clicks that are outside the board boundaries
        if not (1 <= r <= BOARD_SIZE and 1 <= c <= BOARD_SIZE):
            return
            
        move = Move.play(Point(row=r, col=c))
        
        # 2. Check if the human's move is legal
        if self.game_state.is_valid_move(move):
            # Human plays
            self.game_state = self.game_state.apply_move(move)
            self.draw_board()
            self.master.update()  # Force the window to draw the human stone immediately
            
            if self.game_state.is_over():
                print("Game Over!")
                return
                
            # 3. AI takes its turn
            print("AI is thinking...")
            ai_move = self.agent.select_move(self.game_state)
            self.game_state = self.game_state.apply_move(ai_move)
            self.draw_board()
            
            if self.game_state.is_over():
                print("Game Over!")
        else:
            print("Invalid move! Try again.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GoGUI(root)
    root.mainloop()
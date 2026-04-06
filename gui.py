import tkinter as tk
from tkinter import messagebox
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
        
        self.canvas = tk.Canvas(master, width=CANVAS_SIZE, height=CANVAS_SIZE, bg="#DCB35C")
        self.canvas.pack()
        
        self.pass_btn = tk.Button(master, text="Pass Turn (Human)", command=self.human_pass, font=("Arial", 12))
        self.pass_btn.pack(pady=10)
        
        self.canvas.bind("<Button-1>", self.handle_click)
        
        self.game_state = GameState.new_game(BOARD_SIZE)
        self.agent = MCTSAgent(num_rounds=1000, temperature=1.0)
        
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        
        for i in range(BOARD_SIZE):
            x = MARGIN + i * CELL_SIZE
            self.canvas.create_line(x, MARGIN, x, CANVAS_SIZE - MARGIN, width=2)
            y = MARGIN + i * CELL_SIZE
            self.canvas.create_line(MARGIN, y, CANVAS_SIZE - MARGIN, y, width=2)

        for r in range(1, BOARD_SIZE + 1):
            for c in range(1, BOARD_SIZE + 1):
                stone = self.game_state.board.get(Point(row=r, col=c))
                if stone is not None:
                    y = MARGIN + (BOARD_SIZE - r) * CELL_SIZE
                    x = MARGIN + (c - 1) * CELL_SIZE
                    
                    color = "black" if stone == Player.black else "white"
                    radius = CELL_SIZE * 0.4
                    self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)

    def check_game_over(self):
        if self.game_state.is_over():
            winner = self.game_state.winner()
            if winner == Player.black:
                result = "Black (Human) Wins!"
            elif winner == Player.white:
                result = "White (AI) Wins!"
            else:
                result = "It's a Draw!"
            
            messagebox.showinfo("Game Over", f"The game has ended.\nResult: {result}", parent=self.master)
            return True
        return False

    def trigger_ai(self):
        self.master.update() 
        print("AI is thinking...")
        
        ai_move = self.agent.select_move(self.game_state)
        
        # Check if the AI decided to pass
        if ai_move.is_pass:
            print("\n" + "="*40)
            print(">>> ALERT: White (AI) just passed a turn! <<<")
            print("="*40 + "\n")
            
        self.game_state = self.game_state.apply_move(ai_move)
        self.draw_board()
        self.check_game_over()

    def human_pass(self):
        if self.game_state.is_over():
            return
            
        print("Human passes.")
        move = Move.pass_turn()
        self.game_state = self.game_state.apply_move(move)
        self.draw_board()
        
        if not self.check_game_over():
            self.trigger_ai()

    def handle_click(self, event):
        if self.game_state.is_over():
            return
            
        c = round((event.x - MARGIN) / CELL_SIZE) + 1
        r = BOARD_SIZE - round((event.y - MARGIN) / CELL_SIZE)
        
        if not (1 <= r <= BOARD_SIZE and 1 <= c <= BOARD_SIZE):
            return
            
        move = Move.play(Point(row=r, col=c))
        
        if self.game_state.is_valid_move(move):
            self.game_state = self.game_state.apply_move(move)
            self.draw_board()
            
            if not self.check_game_over():
                self.trigger_ai()
        else:
            print("Invalid move! Try again.")
            messagebox.showwarning(
                "Illegal Move", 
                "You cannot place a stone here.", 
                parent=self.master
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = GoGUI(root)
    root.mainloop()
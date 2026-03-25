import tkinter as tk
import math
import random

ROWS = 6
COLS = 7
PLAYER = 1
AI = 2
EMPTY = 0
WINDOW_LENGTH = 4
DEPTH = 4
CELL_SIZE = 100

class Connect4:
    def __init__(self):
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def is_valid_location(self, col):
        return self.board[0][col] == 0

    def get_next_open_row(self, col):
        for r in range(ROWS-1, -1, -1):
            if self.board[r][col] == 0:
                return r

    def print_board(self):
        for row in self.board:
            print(row)

    def winning_move(self, piece):
        for c in range(COLS-3):
            for r in range(ROWS):
                if all(self.board[r][c+i] == piece for i in range(4)):
                    return True

        for c in range(COLS):
            for r in range(ROWS-3):
                if all(self.board[r+i][c] == piece for i in range(4)):
                    return True

        for c in range(COLS-3):
            for r in range(ROWS-3):
                if all(self.board[r+i][c+i] == piece for i in range(4)):
                    return True

        for c in range(COLS-3):
            for r in range(3, ROWS):
                if all(self.board[r-i][c+i] == piece for i in range(4)):
                    return True
        return False

    def get_valid_locations(self):
        return [c for c in range(COLS) if self.is_valid_location(c)]

    def is_terminal_node(self):
        return self.winning_move(PLAYER) or self.winning_move(AI) or len(self.get_valid_locations()) == 0

    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = PLAYER if piece == AI else AI

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 2
        if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
            score -= 4
        return score

    def score_position(self, piece):
        score = 0
        center_array = [self.board[i][COLS//2] for i in range(ROWS)]
        score += center_array.count(piece) * 3

        for r in range(ROWS):
            row_array = self.board[r]
            for c in range(COLS-3):
                window = row_array[c:c+WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        for c in range(COLS):
            col_array = [self.board[r][c] for r in range(ROWS)]
            for r in range(ROWS-3):
                window = col_array[r:r+WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        for r in range(ROWS-3):
            for c in range(COLS-3):
                window = [self.board[r+i][c+i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        for r in range(3, ROWS):
            for c in range(COLS-3):
                window = [self.board[r-i][c+i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        return score

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = self.get_valid_locations()
        is_terminal = self.is_terminal_node()
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.winning_move(AI):
                    return (None, 1000000000000)
                elif self.winning_move(PLAYER):
                    return (None, -10000000000000)
                else:
                    return (None, 0)
            else:
                return (None, self.score_position(AI))

        if maximizingPlayer:
            value = -math.inf
            best_col = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(col)
                temp_board = [r.copy() for r in self.board]
                self.drop_piece(row, col, AI)
                new_score = self.minimax(self.board, depth-1, alpha, beta, False)[1]
                self.board = [r.copy() for r in temp_board]
                if new_score > value:
                    value = new_score
                    best_col = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return best_col, value

        else:
            value = math.inf
            best_col = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(col)
                temp_board = [r.copy() for r in self.board]
                self.drop_piece(row, col, PLAYER)
                new_score = self.minimax(self.board, depth-1, alpha, beta, True)[1]
                self.board = [r.copy() for r in temp_board]
                if new_score < value:
                    value = new_score
                    best_col = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return best_col, value
class Connect4GUI:
    def __init__(self, game):
        self.game = game
        self.current_turn = None  # None until selected
        self.window = tk.Tk()
        self.window.title("Connect 4 with Minimax")
        self.turn_count = 0

        self.canvas = tk.Canvas(self.window, width=COLS*CELL_SIZE, height=(ROWS)*CELL_SIZE, bg="blue")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.click_event)
        self.draw_board()
        self.botton_frame = tk.Frame(self.window)
        self.botton_frame.pack(pady=10)

        self.start_button = tk.Button(self.botton_frame, text="Start : player",font="30", command=self.start_player)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.start_ai_button = tk.Button(self.botton_frame, text="Start : AI",font="30", command=self.start_ai)
        self.start_ai_button.pack(side=tk.LEFT, padx=10)

        self.restart_button = tk.Button(self.botton_frame, text="Restart game",font="30", command=self.restart_game)
        self.restart_button.pack(side=tk.LEFT, padx=10)
        self.player_score = 0
        self.ai_score = 0

        # show score
        self.score_label = tk.Label(self.window, text=f"Player: {self.player_score}   AI: {self.ai_score}", font= "30", fg="purple")
        self.score_label.pack(pady=5)
        self.window.mainloop()

    def draw_board(self):
        self.canvas.delete("all")
        for c in range(COLS):
            for r in range(ROWS):
                x0 = c * CELL_SIZE
                y0 = (r) * CELL_SIZE
                x1 = x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE
                color = "white"
                if self.game.board[r][c] == PLAYER:
                    color = "red"
                elif self.game.board[r][c] == AI:
                    color = "yellow"
                self.canvas.create_oval(x0+5, y0+5, x1-5, y1-5, fill=color)
        
    def click_event(self, event):
        if self.current_turn != PLAYER:
            return  # Ignore the pressure if it's not the player's turn

        col = event.x // CELL_SIZE
        if self.game.is_valid_location(col):
            row = self.game.get_next_open_row(col)
            self.game.drop_piece(row, col, PLAYER)
            if self.game.winning_move(PLAYER):
             self.player_score += 1
             self.update_score_label()
             self.draw_board()
             self.canvas.create_text(COLS*CELL_SIZE//2, CELL_SIZE//2, text="Player wins!", font="30", fill="green")
             self.canvas.unbind("<Button-1>")
             return
            self.draw_board()
            self.current_turn = AI
            self.window.after(500, self.ai_move)  # A small delay to make the transition natural.

    def ai_move(self):
        ai_col, _ = self.game.minimax(self.game.board, DEPTH, -math.inf, math.inf, True)
        if ai_col is not None and self.game.is_valid_location(ai_col):
            ai_row = self.game.get_next_open_row(ai_col)
            self.game.drop_piece(ai_row, ai_col, AI)
            if self.game.winning_move(AI):
             self.ai_score += 1
             self.update_score_label()
             self.draw_board()
             self.canvas.create_text(COLS*CELL_SIZE//2, CELL_SIZE//2, text="AI wins!", font="50", fill="orange")
             self.canvas.unbind("<Button-1>")
             return
            self.draw_board()
            self.current_turn = PLAYER   
           

    def update_score_label(self):
        self.score_label.config(text=f"Player: {self.player_score}   AI: {self.ai_score}")   

    def start_player(self):
        self.restart_game()
        self.current_turn = PLAYER

    def start_ai(self):
        self.restart_game()
        self.current_turn = AI
        self.window.after(500, self.ai_move)  # The AI ​​starts immediately

    def restart_game(self):
        self.game = Connect4()
        self.canvas.bind("<Button-1>", self.click_event)
        self.draw_board()
if __name__ == "__main__":
    game = Connect4()
    Connect4GUI(game)

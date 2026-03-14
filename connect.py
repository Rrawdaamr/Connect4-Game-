import tkinter as tk
import random

ROWS = 6
COLS = 7
SIZE = 80

player = "red"
mode = "pvp"

player1_score = 0
player2_score = 0

board = [["" for _ in range(COLS)] for _ in range(ROWS)]

def reset_board(clear_score=False):
    global board, player, player1_score, player2_score
    board = [["" for _ in range(COLS)] for _ in range(ROWS)]
    player = "red"
    draw_board()
    result_label.config(text="") 

    if clear_score:
        player1_score = 0
        player2_score = 0
        score_label.config(text=f"Player1: {player1_score}    Player2/Computer: {player2_score}")

def draw_board():
    canvas.delete("all")
    for r in range(ROWS):
        for c in range(COLS):
            x1 = c * SIZE
            y1 = r * SIZE
            x2 = x1 + SIZE
            y2 = y1 + SIZE

            canvas.create_rectangle(x1, y1, x2, y2, fill="blue")

            color = "white"
            if board[r][c] == "red":
                color = "red"
            elif board[r][c] == "yellow":
                color = "yellow"

            canvas.create_oval(x1+10, y1+10, x2-10, y2-10, fill=color)

def check_win(p):
    for r in range(ROWS):
        for c in range(COLS-3):
            if board[r][c]==p and board[r][c+1]==p and board[r][c+2]==p and board[r][c+3]==p:
                return True
    for r in range(ROWS-3):
        for c in range(COLS):
            if board[r][c]==p and board[r+1][c]==p and board[r+2][c]==p and board[r+3][c]==p:
                return True
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if board[r][c]==p and board[r+1][c+1]==p and board[r+2][c+2]==p and board[r+3][c+3]==p:
                return True
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if board[r][c]==p and board[r-1][c+1]==p and board[r-2][c+2]==p and board[r-3][c+3]==p:
                return True
    return False

def drop_piece(col):
    global player, player1_score, player2_score

    for r in reversed(range(ROWS)):
        if board[r][col] == "":
            board[r][col] = player
            break
    else:
        return 

    draw_board()

    if check_win(player):
        if player == "red":
            player1_score += 1
        else:
            player2_score += 1

        score_label.config(
            text=f"Player1: {player1_score}    Player2/Computer: {player2_score}"
        )

        result_label.config(text=f"{player} wins!")
        return

    player = "yellow" if player == "red" else "red"

    if mode == "pvc" and player == "yellow":
        root.after(500, computer_move)  

def computer_move():
    col = random.randint(0, COLS-1)
    drop_piece(col)

def click(event):
    col = event.x // SIZE
    drop_piece(col)

def set_pvp():
    global mode
    mode = "pvp"

def set_pvc():
    global mode
    mode = "pvc"

root = tk.Tk()
root.title("Connect 4")

canvas = tk.Canvas(root, width=COLS*SIZE, height=ROWS*SIZE)
canvas.pack()
canvas.bind("<Button-1>", click)

btn_frame = tk.Frame(root)
btn_frame.pack()

tk.Button(btn_frame, text="Player vs Player", command=set_pvp).pack(side="left")
tk.Button(btn_frame, text="Player vs Computer", command=set_pvc).pack(side="left")
tk.Button(btn_frame, text="Restart Game", command=reset_board).pack(side="left")

score_label = tk.Label(root, text="Player1: 0    Player2/Computer: 0", font=("Arial",14))
score_label.pack()

result_label = tk.Label(root, text="", font=("Arial",16))
result_label.pack()

draw_board()

root.mainloop()


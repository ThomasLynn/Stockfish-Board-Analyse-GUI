import chess
import chess.engine
import os

#here we assume the engine file is in same folder as our python script
path = os.getcwd()
#Let's try our code with the starting position of chess:
fen = "8/3b4/2rP3p/prP1k1p1/2R1N1p1/P3P3/5P1P/3R2K1 w - a6 0 33"
board = chess.Board(fen)
#Now make sure you give the correct location for your stockfish engine file
#...in the line that follows by correctly defining path
engine = chess.engine.SimpleEngine.popen_uci("./stockfish/stockfish_13_win_x64_bmi2.exe")
engine.options["Hash"] = 1000
engine.options["Threads"] = 12
info = engine.analyse(board, chess.engine.Limit(time=5), multipv =5)
for w in info:
    moves = w['pv']
    string = ""
    for i,j in enumerate(moves):
        string += board.san(j)
        board.push(j)
        if i<len(moves)-1:
            string += ", "
    board.set_fen(fen)
    print(board.san(w['pv'][0]),w['score'],string)
engine.quit()
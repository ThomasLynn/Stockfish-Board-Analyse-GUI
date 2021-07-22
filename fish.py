import chess
import chess.engine
import psutil
import gui

multipv = 10

fen = "r1bq1rk1/1p2bppp/p1nppn2/2p5/P1B1P3/2NP1N2/1PP1QPPP/R1B2RK1 w - - 1 9"
board = chess.Board(fen)

engine = chess.engine.SimpleEngine.popen_uci("./stockfish/stockfish_13_win_x64_bmi2.exe")
engine.configure({"Threads": psutil.cpu_count()})

mem = psutil.virtual_memory()
ram_size = mem.total//2**20
ram_avaliable = mem.available//2**20

hash_size = ram_size//2
if ram_avaliable - 2**10 < hash_size:
    hash_size =  - 2**10
if hash_size<10:
    hash_size = 10
if hash_size>1_000: # this should be overridable for people who want more
    hash_size = 1_000
print("hash size",hash_size)

engine.configure({"Hash": hash_size})


gui.analysis_board = board
gui.run_ui(fen)


with engine.analysis(board, multipv =multipv) as analysis:
    #print("\ninfo",info,"\n")
    for info in analysis:
        gui.update_moves(info)
            
        gui.run_ui(fen)
        if gui.should_terminate:
            gui.quit_program()
            break

engine.quit()
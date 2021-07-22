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
print("hash size",hash_size)

engine.configure({"Hash": hash_size})


gui.start(fen)


with engine.analysis(board, multipv =multipv) as analysis:
    for info in analysis:
        #print("\ninfo",info,"\n")
        moves = info.get('pv')
        if moves!=None:
            moves = info.get('pv')[:10]
            string = ""
            for i,j in enumerate(moves):
                string += board.san(j)
                board.push(j)
                if i<len(moves)-1:
                    string += ", "
            board.set_fen(fen)
            if info.get('multipv') == 1:
                print()
            print(info.get('multipv'),board.san(info.get('pv')[0]),info.get('score'), info.get('hashfull'),string)
            
        gui.start(fen)
        if gui.should_terminate:
            gui.quit_program()
            break
        #if info.get("seldepth", 0) > 50:
        #    break

engine.quit()
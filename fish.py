import chess
import chess.engine
import psutil
import gui

multipv = 10

fen = "rnbq1rk1/pp1pp1bp/2p2np1/5p2/2PP4/2NBPN2/PP3PPP/R1BQK2R w KQ - 0 7"
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
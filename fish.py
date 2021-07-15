import chess
import chess.engine
import psutil

multipv = 5

fen = "8/3b4/2rP3p/prP1k1p1/2R1N1p1/P3P3/5P1P/3R2K1 w - a6 0 33"
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
        #if info.get("seldepth", 0) > 50:
        #    break

engine.quit()
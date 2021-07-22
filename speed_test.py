import chess
import chess.engine
import time
import psutil

# run a speed test with a specified hash size.
# prints output in a csv format for importing into spreadsheets

hash_sizes = [2,4,8,16,32,64,128,256,512]
#hash_sizes = [2,4,8]
depths = range(1,36)

data = {}

engine = chess.engine.SimpleEngine.popen_uci("./stockfish/stockfish_13_win_x64_bmi2.exe")
engine.configure({"Threads": psutil.cpu_count()})

for hash_size in hash_sizes:
    print("testing hash size",hash_size)
    engine.configure({"Hash": hash_size})
    engine.configure({"Clear Hash": ""})


    board = chess.Board("r1bq1rk1/1p2bppp/p1nppn2/2p5/P1B1P3/2NP1N2/1PP1QPPP/R1B2RK1 w - - 1 9")
    
    new_data = []
    for i in depths:
        timer = time.time()
        info = engine.analyse(board, chess.engine.Limit(depth=i))
        #print(info)
        #print(str(i)+","+str(time.time()-timer))
        new_data.append(str(time.time()-timer))
        engine.configure({"Clear Hash": ""})
        
    data[str(hash_size)+"MB"]=new_data


engine.quit()
    
print("Threads",psutil.cpu_count())
string = "Depth,"
for i,w in enumerate(hash_sizes):
    string+=str(w)+"MB"
    if i!=len(hash_sizes)-1:
        string+=","
print(string)

for i in range(len(depths)):
    string = str(depths[i])+","
    for j,w in enumerate(data):
        string+=str(data[w][i])
        if j!=len(data)-1:
            string+=","
    print(string)
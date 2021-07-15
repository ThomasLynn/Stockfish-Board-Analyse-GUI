import chess
import chess.engine

class Move:

    def __init__(self, engine, board, move):
        self.score = None
        self.white_score = None
        self.engine = engine
        self.board = board
        self.move = move
        
    def calculate_score(self, time):
        info = self.engine.analyse(self.board, chess.engine.Limit(time=time), root_moves=[self.move],multipv =5)
        self.score = info["score"].relative
        self.white_score = info["score"].white()
        
    def get_score(self):
        return self.score
        
    def get_white_score(self):
        return self.white_score
    
    def __lt__(self, other):
        return self.get_score() < other.get_score()
    
    def __eq__(self, other):
        return self.get_score() == other.get_score()
        
    def __str__(self):
        return str(self.board.san(self.move))+" "+str(self.white_score)
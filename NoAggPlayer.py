import AlphBeta
import Eval
MAX_D = AlphBeta.MAX_D



class Player():
  def __init__(self,pieces):
    if pieces[0].color == 'W':
      self.player = 0
    else:
      self.player = 1
    self.pieces = pieces

  def GetMove(self,BOARD,p_t):
    move = AlphBeta.alphabeta(BOARD,MAX_D,-10000,10000,self.player,self.player,Eval.NoAggEval,p_t)
    return (move[0],(move[1],move[2]))

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

  '''  def Eval(self, color, num_moves):
    if num_moves == 0:
      dummy_piece = self.GetWhiteAlive()[0]
      if self.Check(dummy_piece, color,
                     (dummy_piece.row,dummy_piece.col)):
        return 0
      return .5
    else:
      #EVAL FUNCTION!!!
      return 1./num_moves
  '''

  def GetMove(self,BOARD,p_t):
    move = AlphBeta.alphabeta(BOARD,MAX_D,-10000,10000,self.player,self.player,Eval.BaseEval,p_t)
    return (move[0],(move[1],move[2]))


import ChessBoard
#import HumanPlayer
import BasePlayer
import NoAggPlayer
import AggPlayer
import sys

old_out = sys.stdout

class dummyStream:
	''' dummyStream behaves like a stream but does nothing. '''
	def __init__(self): pass
	def write(self,data): pass
	def read(self,data): pass
	def flush(self): pass
	def close(self): pass

def PlayGame(Init,p1,p2):
  BOARD = Init()
  position_tracker = {}
  #player1 = HumanPlayer.Player(BOARD.GetWhite())
  player1 = p1(BOARD.GetWhite())
  player2 = p2(BOARD.GetBlack())
  W_PAWNS = BOARD.GetWhite()[8:]
  B_PAWNS = BOARD.GetBlack()[8:]
  print BOARD
  #print BasePlayer.Eval.Eval(BOARD)[:4]
  #print BasePlayer.Eval.Eval(BOARD)[4:]

  player = 1
  color = 'W'
  for z in xrange(250):
    board_str = str(BOARD)
    position_tracker[board_str] = position_tracker.setdefault(board_str,0) + 1
    if position_tracker[board_str] == 4:
      return .5
      print "IT'S A DRAW"
      break
    if player == 1:
      curr_player = player1
      pieces = BOARD.GetWhiteAlive()
      color = 'W'
      for pawn in W_PAWNS:
        pawn.en_passantable = False
    else:
      curr_player = player2
      pieces = BOARD.GetBlackAlive()
      color = 'B'
      for pawn in B_PAWNS:
        pawn.en_passantable = False
    #print BasePlayer.Eval.BaseEval(BOARD, color, 1)
    #print BasePlayer.Eval.Eval(BOARD)[:4]
    #print BasePlayer.Eval.Eval(BOARD)[4:]
    moves_left = {}
    for piece in pieces:
      moves = piece.MoveChoices()
      if moves:
        moves_left[piece] = moves
    #print len(moves_left),moves_left
    if len(moves_left) == 0:
      dummy_piece = pieces[0]
      if BOARD.Check(dummy_piece, color,
                     (dummy_piece.row,dummy_piece.col)):
        if color == 'W':
          return 0
        else:
          return 1
        print "GAME OVER, %s LOSES" % color
      else:
        return .5
        print "IT'S A DRAW"
      break

    sys.stdout = dummyStream()
    move = curr_player.GetMove(BOARD, position_tracker)
    sys.stdout = old_out
    piece = move[0]
    loc = move[1]

    if piece in moves_left and loc in moves_left[piece]:
      if len(move) > 2:
        piece.Move(loc[0],loc[1],move[2])
      else:
        piece.Move(loc[0],loc[1])
    else:
      try:
        print moves_left[piece],loc
      except:
        "No possible moves"
      print "INVALID MOVE", move[1]
      return -.5
      continue
    player = 3 - player
    #print BOARD
  return .5
  print BOARD

if __name__ == '__main__':
  results_file_name = sys.argv[1]
  f = open(results_file_name,'w')
  score_w = 0
  score_b = 0
  for InitPos in [ChessBoard.Game1,ChessBoard.Game2,ChessBoard.Game3,
                  ChessBoard.Game4,ChessBoard.Game5,ChessBoard.Game6]:
    try:
      score_w += PlayGame(InitPos,AggPlayer.Player,BasePlayer.Player)
    except:
      sys.stdout = old_out
      print "FAILED GAME"
    print score_w
  for InitPos in [ChessBoard.Game1,ChessBoard.Game2,ChessBoard.Game3,
                  ChessBoard.Game4,ChessBoard.Game5,ChessBoard.Game6]:
    try:
      score_b += 1-PlayGame(InitPos,BasePlayer.Player,AggPlayer.Player)
    except:
      sys.stdout = old_out      
      print "FAILED GAME"
    print score_b
  f.write(str(score_w) + ' ' + str(score_b) + ' ' + str(score_w + score_b) + '\n')

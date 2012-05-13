import sys
import ChessBoard
import Eval

PieceClassDict = {'N': ChessBoard.Knight,
                  'R': ChessBoard.Rook,
                  'K': ChessBoard.King,
                  'Q': ChessBoard.Queen,
                  'B': ChessBoard.Bishop}

def StringFormat(result,num_turns,data):
  if result == 2:
    return ''
  if result == 1:
    sgn = '-'
  else:
    sgn = ''
  out_str = ''
  for half_turns, datum in enumerate(data):
    out_str += sgn + str(1+half_turns/2) + '/' + str(num_turns)
    for curr_set in datum:
      str_set = [str(point) for point in curr_set]
      out_str += ' ' + ' '.join(str_set)
    out_str += '\n'
  return out_str

def GetMove(BOARD,move_str,player):
  if player == 0:
    piece_list = BOARD.GetWhite()
  else:
    piece_list = BOARD.GetBlack()
  if '=' in move_str:
    prom = move_str[move_str.find('=')+1]
  else:
    prom = ''
  if move_str[0] == 'O':
    King = piece_list[0]
    if len(move_str) >= 5 and move_str[:5] == 'O-O-O':
      return King,(King.row,King.col-2)
    return King,(King.row,King.col+2)
  if move_str[0] in PieceClassDict:
    pieceType = PieceClassDict[move_str[0]]
    start_char = 1
  else:
    pieceType = ChessBoard.Pawn
    start_char = 0
  info = ''
  for i in xrange(start_char,len(move_str)-1):
    if move_str[i] == 'x':
      continue
    if move_str[i+1].isdigit():
      targ_str = move_str[i:i+2]
      break
    info += move_str[i]
  if len(info) > 1:
    print info
    assert False
  targ_col = 1+ord(targ_str[0])-ord('a')
  targ_row = int(targ_str[1])
  for piece in piece_list:
    if piece.__class__ == pieceType and piece.alive:
      moves = piece.MoveChoices()
      if (targ_row,targ_col) in moves:
        if info == '' or piece.col == (1+ord(info)-ord('a')) or \
          (info.isdigit() and piece.row == int(info)):
          if prom:
            return piece,(targ_row,targ_col),prom
          return piece,(targ_row,targ_col)
  BISHOP = BOARD.GetWhite()[5]
#  print BISHOP.MoveChoices()
  print pieceType,targ_row,targ_col, info
#  print info == '', (targ_row,targ_col) in BISHOP.MoveChoices(),BISHOP.alive,BISHOP.__class__ == pieceType
  print BOARD
  print move_str
  assert False




def PlayGame(game_str):
  out_data = []
  game_str = game_str.replace('  ',' ')
  BOARD = ChessBoard.InitBoard()
  movepairs = game_str.split('.')
  num_turns = 0
  for move in movepairs[1:]:
    num_turns += 1
    indmoves = move.split(' ')
    while not indmoves[0]:
      indmoves = indmoves[1:]
    move1 = GetMove(BOARD,indmoves[0],0)
    piece = move1[0]
    loc = move1[1]
    if len(move1) == 2:
      piece.Move(loc[0],loc[1])
    else:
      piece.Move(loc[0],loc[1],PieceClassDict[move1[2]])
    out_data.append(Eval.Eval(BOARD))
#    print BOARD
#    s = raw_input()
    if len(indmoves[1]) > 1 and not indmoves[1][0].isdigit():
      move2 = GetMove(BOARD,indmoves[1],1)
      piece = move2[0]
      loc = move2[1]
      if len(move2) == 2:
        piece.Move(loc[0],loc[1])
      else:
        piece.Move(loc[0],loc[1],PieceClassDict[move2[2]])
      out_data.append(Eval.Eval(BOARD))
#      print BOARD
#      s = raw_input()
#  print game_str[-1]
  out_str = StringFormat(int(game_str[-1]),num_turns,out_data)
  out_f.write(out_str)

file_name = sys.argv[1]
f = open(file_name,'r')
out_file_name = sys.argv[2]
out_f = open(out_file_name,'w')
lines = f.read().split('\n')
InGame = False
game_str = ''
num_games = 0
for i,line in enumerate(lines):
  if line == '\r':
    if InGame:
      num_games += 1
      if num_games%49 == 1:
        PlayGame(game_str)
      game_str = ''
    else:
      print "LINE:", i
    InGame = not InGame
    continue
  if InGame:
    game_str += ' ' + line[:-1]
print num_games

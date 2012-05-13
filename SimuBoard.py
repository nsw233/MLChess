import ChessBoard

class SimuBoard(object):
  def __init__(self,board):
    self.board = board
    self.pos_to_piece = [row[:] for row in board.GetPTP()]
    self.translate_pieces = {}

  def RefreshPTP(self,PTP):
    self.board.RefreshPTP(PTP)

  def GetPTP(self):
    return self.board.GetPTP()

  def GetWhiteAlive(self):
    return self.board.GetWhiteAlive()

  def GetBlackAlive(self):
    return self.board.GetBlackAlive()

  def GetWhite(self):
    return self.board.GetWhite()

  def GetBlack(self):
    return self.board.GetBlack()

  def Check(self, piece, color, move):
    return self.board.Check(piece, color, move)

  def RefreshAlive(self):
    return self.board.RefreshAlive()

  def __str__(self):
    return str(self.board)

  def UpdateSimuBoard(self,piece,row,col):
    updates = piece.Affected(row,col)
    o_piece_copy = None
    PTP = self.board.GetPTP()
    for piece in updates:
      if piece.color == 'W':
        piece_list = self.GetWhite()
        p_la = self.GetWhiteAlive()
      else:
        piece_list = self.GetBlack()
        p_la = self.GetBlackAlive()
      if o_piece_copy and o_piece_copy.__class__ == ChessBoard.King and \
        o_piece_copy.color == piece.color:
        piece_copy = piece.Copy(True)
      else:
        piece_copy = piece.Copy()
      if o_piece_copy == None:
        o_piece_copy = piece_copy
      self.translate_pieces[piece_copy] = piece
      try:
        piece_list[piece_list.index(piece)] = piece_copy
      except:
        print piece, o_piece_copy
        print row, col
        print self.board
        piece_list[piece_list.index(piece)] = piece_copy
      try:
        p_la[p_la.index(piece)] = piece_copy
      except:
        print piece, o_piece_copy
        print row,col
        print self.board
        p_la[p_la.index(piece)] = piece_copy
      PTP[piece.row][piece.col] = piece_copy
    self.board.RefreshPTP(PTP)
    o_piece_copy.Move(row,col)
    return self.translate_pieces

  def UpdateBoard(self, piece, row, col):
    self.board.UpdateBoard(piece, row, col)
    #return (move[0],(move[1],move[2]))

def GetMoveList(b_state, player):
  if player == 0:
    piece_list = b_state.GetWhite()
  else:
    piece_list = b_state.GetBlack()
  moves = []
  for piece in piece_list:
    if piece.alive:
      moves.append((piece,piece.MoveChoices()))
  moves_f = []
  for move in moves:
    for row,col in move[1]:
      moves_f.append((move[0],row,col))
  return moves_f
'''
    Make a copy of each piece that is affected:
      Keep track of pos_to_piece
      alive_white, alive_back, all_white, all_black
      Keep a dictionary of modified pieces (from new ones to old ones?)
    This way I can use all the built-in functions :)
'''

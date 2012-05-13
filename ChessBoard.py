class Board(object):
  def __init__(self):
    self.pos_to_piece = [[None]*9 for i in xrange(9)]
    self.alive_white = []
    self.alive_black = []
    self.all_white = []
    self.all_black = []
    pass

  def GetWhiteAlive(self):
    return self.alive_white

  def GetBlackAlive(self):
    return self.alive_black

  def GetWhite(self):
    return self.all_white

  def GetBlack(self):
    return self.all_black

  def RefreshAlive(self):
    self.alive_white = []
    for piece in self.all_white:
      if piece.alive:
        self.alive_white.append(piece)
    self.alive_black = []
    for piece in self.all_black:
      if piece.alive:
        self.alive_black.append(piece)

  def Check(self, piece, color, move):
    if color == 'W':
      op_pieces = self.GetBlackAlive()
      KING = self.GetWhite()[0]
    else:
      op_pieces = self.GetWhiteAlive()
      KING = self.GetBlack()[0]
    if piece == KING:
      targ_row = move[0]
      targ_col = move[1]
    else:
      targ_row = KING.row
      targ_col = KING.col
    for op_piece in op_pieces:
      if op_piece.row == move[0] and op_piece.col == move[1]:
        continue
      moves = op_piece.GetCheckMoveList()
      for move_set in moves:
        for op_move in move_set:
          if self.Ally(op_piece.color,op_move[0],op_move[1]) and \
            not (op_move[0] == move[0] and op_move[1] == move[1]):
            break
          if (self.pos_to_piece[op_move[0]][op_move[1]] and \
             self.pos_to_piece[op_move[0]][op_move[1]].color == color and\
             not self.pos_to_piece[op_move[0]][op_move[1]] == piece) or \
             (op_move[0] == move[0] and op_move[1] == move[1]):
            if op_move[0] == targ_row and op_move[1] == targ_col:
              return True
            break
          if op_move[0] == targ_row and op_move[1] == targ_col:
            return True
    return False

  def EPCheck(self, piece, color, move):
    if not (move[0] == piece.row + piece.direction and abs(move[1]-piece.col) == 1):
      return True
    if color == 'W':
      op_pieces = self.GetBlackAlive()
      KING = self.GetWhite()[0]
    else:
      op_pieces = self.GetWhiteAlive()
      KING = self.GetBlack()[0]
    if piece == KING:
      targ_row = move[0]
      targ_col = move[1]
    else:
      targ_row = KING.row
      targ_col = KING.col
    for op_piece in op_pieces:
      if op_piece.row == piece.row and op_piece.col == move[1]:
        continue
      moves = op_piece.GetCheckMoveList()
      for move_set in moves:
        for op_move in move_set:
          if self.Ally(op_piece.color,op_move[0],op_move[1]) and \
            not (op_move[0] == move[0] and op_move[1] == move[1]) and \
            not (op_move[0] == piece.row and op_move[1] == move[1]):
            break
          if (self.pos_to_piece[op_move[0]][op_move[1]] and \
             self.pos_to_piece[op_move[0]][op_move[1]].color == color and\
             not self.pos_to_piece[op_move[0]][op_move[1]] == piece) or \
             (op_move[0] == move[0] and op_move[1] == move[1]):
            if op_move[0] == targ_row and op_move[1] == targ_col:
              return True
            break
          if op_move[0] == targ_row and op_move[1] == targ_col:
            return True
    return False

  def OnBoard(self, move):
    return move[0] > 0 and move[0] < 9 and move[1] > 0 and move[1] < 9

  def Ally(self,color,row,col):
    return self.pos_to_piece[row][col] and \
           self.pos_to_piece[row][col].color == color

  def Take(self,color,row,col):
    return self.pos_to_piece[row][col] and \
           self.pos_to_piece[row][col].color != color

  def EnPassant(self,color,row,col):
    return self.pos_to_piece[row][col] and \
           self.pos_to_piece[row][col].color != color and \
           self.pos_to_piece[row][col].__class__ == Pawn and \
           self.pos_to_piece[row][col].en_passantable

  def UpdateBoard(self,piece,row,col):
    if self.pos_to_piece[row][col]:
      taken = self.pos_to_piece[row][col]
      taken.alive = False
      taken.row = 0
      taken.col = 0
      if taken.color == 'W':
#        print 'w',taken, taken.row, taken.col
#        print self.alive_black
#        print self
        del self.alive_white[self.alive_white.index(taken)]
      else:
        del self.alive_black[self.alive_black.index(taken)]
    #print piece.row, piece.col
    self.pos_to_piece[piece.row][piece.col] = None
    self.pos_to_piece[row][col] = piece

  def Place(self,piece):
    self.pos_to_piece[piece.row][piece.col] = piece
    if piece.color == 'W':
      self.alive_white.append(piece)
      self.all_white.append(piece)
    else:
      self.alive_black.append(piece)
      self.all_black.append(piece)

  def RefreshPTP(self,PTP):
    self.pos_to_piece = [row[:] for row in PTP]

  def GetPTP(self):
    return self.pos_to_piece

  def __str__(self):
    out_str = ""
    Piece_to_let = {
                    Pawn: 'P',
                    Bishop: 'B',
                    Rook: 'R',
                    Knight: 'N',
                    Queen: 'Q',
                    King: 'K'}
    for row in xrange(8,0,-1):
      for col in xrange(1,9):
        if self.pos_to_piece[row][col]:
          piece = self.pos_to_piece[row][col]
          out_str += Piece_to_let[piece.__class__] + piece.color
        else:
          out_str += '||'
      out_str += '\n'
    return out_str

class Piece(object):
  def __init__(self,init_row,init_col,color,board):
    self.row = init_row
    self.col = init_col
    self.color = color
    self.board = board
    self.alive = True

  def MoveChoices(self):
    moves = self.GetMoveList()
    possible_moves = []
    for move_set in moves:
      for move in move_set:
        if self.board.Ally(self.color,move[0],move[1]):
          break
        if self.board.Take(self.color,move[0],move[1]):
          if not self.board.Check(self,self.color,move):
            possible_moves.append(move)
          break
        if not self.board.Check(self,self.color,move):
          possible_moves.append(move)
        elif self.__class__ == Pawn:
          if not self.board.EPCheck(self,self.color,move):
            possible_moves.append(move)
    return possible_moves


  def GetCheckMoveList(self):
    return self.GetMoveList()

  def Affected(self,row,col):
    affected = [self]
    if self.board.pos_to_piece[row][col]:
      affected.append(self.board.pos_to_piece[row][col])
    return affected

  def __str__(self):
    return str(self.__class__) + " " + str(self.col) + " " + str(self.row)

class Bishop(Piece):
  def __init__(self,init_row,init_col,color,board):
    Piece.__init__(self,init_row,init_col,color,board)
    self.score = 3

  def GetMoveList(self,new_piece=None,new_pos=None):
    dirs = [[1,1],[1,-1],[-1,1],[-1,-1]]
    move_list = []
    for dirr in dirs:
      move_dir = []
      curr_row = self.row + dirr[0]
      curr_col = self.col + dirr[1]
      while self.board.OnBoard((curr_row,curr_col)):
        move_dir.append((curr_row,curr_col))
        curr_row += dirr[0]
        curr_col += dirr[1]
      move_list.append(move_dir)
    return move_list

  def Move(self,row,col):
    self.board.UpdateBoard(self,row,col)
    self.row = row
    self.col = col

  def Copy(self,kin=False):
    return Bishop(self.row,self.col,self.color,self.board)

class Rook(Piece):
  def __init__(self,init_row,init_col,color,board):
    self.moved = False
    Piece.__init__(self,init_row,init_col,color,board)
    self.score = 5

  def GetMoveList(self):
    dirs = [[0,1],[0,-1],[1,0],[-1,0]]
    move_list = []
    for dirr in dirs:
      move_dir = []
      curr_row = self.row + dirr[0]
      curr_col = self.col + dirr[1]
      while self.board.OnBoard((curr_row,curr_col)):
        move_dir.append((curr_row,curr_col))
        curr_row += dirr[0]
        curr_col += dirr[1]
      move_list.append(move_dir)
    return move_list

  def Move(self,row,col):
    self.moved = True
    self.board.UpdateBoard(self,row,col)
    self.row = row
    self.col = col

  def Copy(self,kin = False):
    piece = Rook(self.row,self.col,self.color,self.board)
    if kin:
      if self.col == 1:
        if self.color == 'W':
          King = self.board.all_white[0]
        else:
          King = self.board.all_black[0]
        King.l_rook = piece
      if self.col == 8:
        if self.color == 'W':
          King = self.board.all_white[0]
        else:
          King = self.board.all_black[0]
        King.r_rook = piece
    piece.moved = self.moved
    return piece

class Knight(Piece):
  def __init__(self,init_row,init_col,color,board):
    Piece.__init__(self,init_row,init_col,color,board)
    self.score = 3

  def GetMoveList(self):
    poss_moves = [[1,2],[2,1],[-1,2],[-2,1],[1,-2],[2,-1],[-1,-2],[-2,-1]]
    move_list = []
    for poss_move in poss_moves:
      new_row = self.row + poss_move[0]
      new_col = self.col + poss_move[1]
      if self.board.OnBoard((new_row,new_col)):
        move_list.append([(new_row,new_col)])
    return move_list

  def Move(self,row,col):
    self.board.UpdateBoard(self,row,col)
    self.row = row
    self.col = col

  def Copy(self,kin=False):
    return Knight(self.row,self.col,self.color,self.board)

class Queen(Piece):
  def __init__(self,init_row,init_col,color,board):
    Piece.__init__(self,init_row,init_col,color,board)
    self.score = 9

  def GetMoveList(self):
    dirs = [[0,1],[0,-1],[1,0],[-1,0],[1,1],[1,-1],[-1,1],[-1,-1]]
    move_list = []
    for dirr in dirs:
      move_dir = []
      curr_row = self.row + dirr[0]
      curr_col = self.col + dirr[1]
      while self.board.OnBoard((curr_row,curr_col)):
        move_dir.append((curr_row,curr_col))
        curr_row += dirr[0]
        curr_col += dirr[1]
      move_list.append(move_dir)
    return move_list

  def Move(self,row,col):
    self.board.UpdateBoard(self,row,col)
    self.row = row
    self.col = col

  def Copy(self,kin=False):
    return Queen(self.row,self.col,self.color,self.board)

class King(Piece):
  def __init__(self,init_row,init_col,color,board,l_rook,r_rook):
    self.l_rook = l_rook
    self.r_rook = r_rook
    self.moved = False
    self.castle = False
    Piece.__init__(self,init_row,init_col,color,board)
    self.score = 0

  def GetCheckMoveList(self):
    poss_moves = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
    move_list = []
    for poss_move in poss_moves:
      new_row = self.row + poss_move[0]
      new_col = self.col + poss_move[1]
      if self.board.OnBoard((new_row,new_col)):
        move_list.append([(new_row,new_col)])
    return move_list

  def GetMoveList(self):
    poss_moves = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
    move_list = []
    for poss_move in poss_moves:
      new_row = self.row + poss_move[0]
      new_col = self.col + poss_move[1]
      if self.board.OnBoard((new_row,new_col)):
        move_list.append([(new_row,new_col)])
    if self.moved == False and self.l_rook.moved == False and self.l_rook.alive and\
       self.board.pos_to_piece[self.row][6] == None and \
       self.board.pos_to_piece[self.row][7] == None and \
       not self.board.Check(self,self.color,(self.row,5)) and \
       not self.board.Check(self,self.color,(self.row,6)):
      move_list.append([(self.row,7)])
    if self.moved == False and self.r_rook.moved == False and self.r_rook.alive and\
       self.board.pos_to_piece[self.row][2] == None and \
       self.board.pos_to_piece[self.row][3] == None and \
       self.board.pos_to_piece[self.row][4] == None and \
       not self.board.Check(self,self.color,(self.row,4)) and \
       not self.board.Check(self,self.color,(self.row,5)):
      move_list.append([(self.row,3)])
    return move_list

  def Affected(self,row,col):
    affected = [self]
    if self.col - col == 2:
      affected.append(self.l_rook)
    elif self.col - col == -2:
      affected.append(self.r_rook)
    if self.board.pos_to_piece[row][col]:
      affected.append(self.board.pos_to_piece[row][col])
    return affected


  def Move(self,row,col):
    if self.col - col == 2:
      self.board.UpdateBoard(self.l_rook,row,4)
      self.l_rook.moved = True
      self.l_rook.col = 4
      self.castle = True
    elif self.col - col == -2:
      self.board.UpdateBoard(self.r_rook,row,6)
      self.r_rook.moved = True
      self.r_rook.col = 6
      self.castle = True
    self.moved = True
    self.board.UpdateBoard(self,row,col)
    self.row = row
    self.col = col

  def Copy(self,kin=False):
    piece = King(self.row,self.col,self.color,self.board,self.l_rook,self.r_rook)
    piece.moved = self.moved
    return piece

class Pawn(Piece):
  def __init__(self,init_row,init_col,color,board):
    if color == 'W':
      self.home_row = 2
      self.direction = 1
    else:
      self.home_row = 7
      self.direction = -1
    self.en_passantable = False
    self.score = 1
    Piece.__init__(self,init_row,init_col,color,board)

  def GetMoveList(self):
    move_list = []
    if self.row == self.home_row:
      if not self.board.pos_to_piece[self.row+self.direction][self.col]:
        move_list.append([(self.row+self.direction,self.col)])
        if not self.board.pos_to_piece[self.row+2*self.direction][self.col]:
          move_list.append([(self.row+2*self.direction,self.col)])
    else:
      if not self.board.pos_to_piece[self.row+self.direction][self.col]:
        move_list.append([(self.row+self.direction,self.col)])
    poss_move = (self.row+self.direction,self.col+1)
    if self.board.OnBoard(poss_move) and \
       self.board.Take(self.color,poss_move[0],poss_move[1]):
      move_list.append([poss_move])
    poss_move = (self.row+self.direction,self.col-1)
    if self.board.OnBoard(poss_move) and \
       self.board.Take(self.color,poss_move[0],poss_move[1]):
      move_list.append([poss_move])

    poss_move = (self.row+self.direction,self.col+1)
    ep_move = (self.row,self.col+1)
    if self.board.OnBoard(poss_move) and \
       self.board.EnPassant(self.color,ep_move[0],ep_move[1]):
      move_list.append([poss_move])
    poss_move = (self.row+self.direction,self.col-1)
    ep_move = (self.row,self.col-1)
    if self.board.OnBoard(poss_move) and \
       self.board.EnPassant(self.color,ep_move[0],ep_move[1]):
      move_list.append([poss_move])
    return move_list

  def GetCheckMoveList(self):
    move_list = []
    poss_move = (self.row+self.direction,self.col+1)
    if self.board.OnBoard(poss_move):
      move_list.append([poss_move])
    poss_move = (self.row+self.direction,self.col-1)
    if self.board.OnBoard(poss_move):
      move_list.append([poss_move])
    return move_list

  def Affected(self,row,col):
    affected = [self]
    if self.board.pos_to_piece[row][col]:
      affected.append(self.board.pos_to_piece[row][col])
    elif abs(self.col-col) == 1 and \
      self.board.pos_to_piece[row][col] == None:
      affected.append(self.board.pos_to_piece[self.row][col])
    return affected

  def Move(self,row,col,Prom = Queen):
    if abs(self.row-row) == 2:
      self.en_passantable = True
    if abs(self.col-col) == 1 and \
       self.board.pos_to_piece[row][col] == None:
      taken = self.board.pos_to_piece[self.row][col]
      self.board.pos_to_piece[self.row][col] = None
      taken.alive = False
      taken.row = 0
      taken.col = 0
      if taken.color == 'W':
        del self.board.alive_white[self.board.alive_white.index(taken)]
      else:
        del self.board.alive_black[self.board.alive_black.index(taken)]

    self.board.UpdateBoard(self,row,col)
    self.row = row
    self.col = col
    if row == 8 or row == 1:
      NEW_PIECE = Prom(row,col,self.color,self.board)
      if self.color == 'W':
        self.board.all_white[self.board.all_white.index(self)] = NEW_PIECE
        self.board.alive_white[self.board.alive_white.index(self)] = NEW_PIECE
      else:
        self.board.all_black[self.board.all_black.index(self)] = NEW_PIECE
        self.board.alive_black[self.board.alive_black.index(self)] = NEW_PIECE
      self.board.pos_to_piece[row][col] = NEW_PIECE

  def Copy(self,kin=False):
    piece = Pawn(self.row,self.col,self.color,self.board)
    piece.home_row = self.home_row
    piece.direction = self.direction
    piece.en_passantable = self.en_passantable
    return piece

def InitBoard():
  BOARD = Board()
  for i in xrange(1,9):
    W_PAWN = Pawn(2,i,'W',BOARD)
    BOARD.Place(W_PAWN)
    B_PAWN = Pawn(7,i,'B',BOARD)
    BOARD.Place(B_PAWN)
  for i in xrange(2):
    W_BISHOP = Bishop(1,3+3*i,'W',BOARD)
    BOARD.Place(W_BISHOP)
    W_KNIGHT = Knight(1,2+5*i,'W',BOARD)
    BOARD.Place(W_KNIGHT)
    B_BISHOP = Bishop(8,3+3*i,'B',BOARD)
    BOARD.Place(B_BISHOP)
    B_KNIGHT = Knight(8,2+5*i,'B',BOARD)
    BOARD.Place(B_KNIGHT)
  W_LROOK = Rook(1,1,'W',BOARD)
  BOARD.Place(W_LROOK)
  W_RROOK = Rook(1,8,'W',BOARD)
  BOARD.Place(W_RROOK)
  B_LROOK = Rook(8,1,'B',BOARD)
  BOARD.Place(B_LROOK)
  B_RROOK = Rook(8,8,'B',BOARD)
  BOARD.Place(B_RROOK)
  W_QUEEN = Queen(1,4,'W',BOARD)
  BOARD.Place(W_QUEEN)
  B_QUEEN = Queen(8,4,'B',BOARD)
  BOARD.Place(B_QUEEN)
  W_KING = King(1,5,'W',BOARD,W_LROOK,W_RROOK)
  BOARD.Place(W_KING)
  B_KING = King(8,5,'B',BOARD,B_LROOK,B_RROOK)
  BOARD.Place(B_KING)
  BOARD.all_white.reverse()
  BOARD.all_black.reverse()
  BOARD.alive_white.reverse()
  BOARD.alive_black.reverse()
  return BOARD

def Game1():
  BOARD = Board()
  W_PAWN = Pawn(2,1,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,2,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,3,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,4,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,5,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,6,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,7,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,8,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_BISHOP = Bishop(1,3,'W',BOARD)
  BOARD.Place(W_BISHOP)
  W_BISHOP = Bishop(1,6,'W',BOARD)
  BOARD.Place(W_BISHOP)
  W_KNIGHT = Knight(1,2,'W',BOARD)
  BOARD.Place(W_KNIGHT)
  W_KNIGHT = Knight(1,7,'W',BOARD)
  BOARD.Place(W_KNIGHT)
  W_LROOK = Rook(1,1,'W',BOARD)
  BOARD.Place(W_LROOK)
  W_RROOK = Rook(1,8,'W',BOARD)
  BOARD.Place(W_RROOK)
  W_QUEEN = Queen(1,4,'W',BOARD)
  BOARD.Place(W_QUEEN)
  W_KING = King(1,5,'W',BOARD,W_LROOK,W_RROOK)
  BOARD.Place(W_KING)
  B_PAWN = Pawn(7,1,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,2,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,3,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,4,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,5,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,6,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,7,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,8,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_BISHOP = Bishop(8,3,'B',BOARD)
  BOARD.Place(B_BISHOP)
  B_BISHOP = Bishop(8,6,'B',BOARD)
  BOARD.Place(B_BISHOP)
  B_KNIGHT = Knight(8,2,'B',BOARD)
  BOARD.Place(B_KNIGHT)
  B_KNIGHT = Knight(8,7,'B',BOARD)
  BOARD.Place(B_KNIGHT)
  B_LROOK = Rook(8,1,'B',BOARD)
  BOARD.Place(B_LROOK)
  B_RROOK = Rook(8,8,'B',BOARD)
  BOARD.Place(B_RROOK)
  B_QUEEN = Queen(8,4,'B',BOARD)
  BOARD.Place(B_QUEEN)
  B_KING = King(8,5,'B',BOARD,B_LROOK,B_RROOK)
  BOARD.Place(B_KING)
  BOARD.all_white.reverse()
  BOARD.all_black.reverse()
  BOARD.alive_white.reverse()
  BOARD.alive_black.reverse()
  return BOARD

def Game2():
  BOARD = Board()
  W_PAWN = Pawn(2,1,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,2,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,3,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(4,4,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,5,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,6,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,7,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,8,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_BISHOP = Bishop(1,3,'W',BOARD)
  BOARD.Place(W_BISHOP)
  W_BISHOP = Bishop(1,6,'W',BOARD)
  BOARD.Place(W_BISHOP)
  W_KNIGHT = Knight(1,2,'W',BOARD)
  BOARD.Place(W_KNIGHT)
  W_KNIGHT = Knight(1,7,'W',BOARD)
  BOARD.Place(W_KNIGHT)
  W_LROOK = Rook(1,1,'W',BOARD)
  BOARD.Place(W_LROOK)
  W_RROOK = Rook(1,8,'W',BOARD)
  BOARD.Place(W_RROOK)
  W_QUEEN = Queen(1,4,'W',BOARD)
  BOARD.Place(W_QUEEN)
  W_KING = King(1,5,'W',BOARD,W_LROOK,W_RROOK)
  BOARD.Place(W_KING)
  B_PAWN = Pawn(7,1,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,2,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,3,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,4,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,5,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,6,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,7,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,8,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_BISHOP = Bishop(8,3,'B',BOARD)
  BOARD.Place(B_BISHOP)
  B_BISHOP = Bishop(8,6,'B',BOARD)
  BOARD.Place(B_BISHOP)
  B_KNIGHT = Knight(8,2,'B',BOARD)
  BOARD.Place(B_KNIGHT)
  B_KNIGHT = Knight(6,6,'B',BOARD)
  BOARD.Place(B_KNIGHT)
  B_LROOK = Rook(8,1,'B',BOARD)
  BOARD.Place(B_LROOK)
  B_RROOK = Rook(8,8,'B',BOARD)
  BOARD.Place(B_RROOK)
  B_QUEEN = Queen(8,4,'B',BOARD)
  BOARD.Place(B_QUEEN)
  B_KING = King(8,5,'B',BOARD,B_LROOK,B_RROOK)
  BOARD.Place(B_KING)
  BOARD.all_white.reverse()
  BOARD.all_black.reverse()
  BOARD.alive_white.reverse()
  BOARD.alive_black.reverse()
  return BOARD

def Game3():
  BOARD = Board()
  W_PAWN = Pawn(2,1,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,2,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,3,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,4,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(4,5,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,6,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,7,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,8,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_BISHOP = Bishop(1,3,'W',BOARD)
  BOARD.Place(W_BISHOP)
  W_BISHOP = Bishop(1,6,'W',BOARD)
  BOARD.Place(W_BISHOP)
  W_KNIGHT = Knight(1,2,'W',BOARD)
  BOARD.Place(W_KNIGHT)
  W_KNIGHT = Knight(1,7,'W',BOARD)
  BOARD.Place(W_KNIGHT)
  W_LROOK = Rook(1,1,'W',BOARD)
  BOARD.Place(W_LROOK)
  W_RROOK = Rook(1,8,'W',BOARD)
  BOARD.Place(W_RROOK)
  W_QUEEN = Queen(1,4,'W',BOARD)
  BOARD.Place(W_QUEEN)
  W_KING = King(1,5,'W',BOARD,W_LROOK,W_RROOK)
  BOARD.Place(W_KING)
  B_PAWN = Pawn(7,1,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,2,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(5,3,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,4,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,5,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,6,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,7,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,8,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_BISHOP = Bishop(8,3,'B',BOARD)
  BOARD.Place(B_BISHOP)
  B_BISHOP = Bishop(8,6,'B',BOARD)
  BOARD.Place(B_BISHOP)
  B_KNIGHT = Knight(8,2,'B',BOARD)
  BOARD.Place(B_KNIGHT)
  B_KNIGHT = Knight(8,7,'B',BOARD)
  BOARD.Place(B_KNIGHT)
  B_LROOK = Rook(8,1,'B',BOARD)
  BOARD.Place(B_LROOK)
  B_RROOK = Rook(8,8,'B',BOARD)
  BOARD.Place(B_RROOK)
  B_QUEEN = Queen(8,4,'B',BOARD)
  BOARD.Place(B_QUEEN)
  B_KING = King(8,5,'B',BOARD,B_LROOK,B_RROOK)
  BOARD.Place(B_KING)
  BOARD.all_white.reverse()
  BOARD.all_black.reverse()
  BOARD.alive_white.reverse()
  BOARD.alive_black.reverse()
  return BOARD

def Game4():
  BOARD = Board()
  W_PAWN = Pawn(2,1,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,2,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,3,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,4,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(4,5,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,6,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,7,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,8,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_BISHOP = Bishop(1,3,'W',BOARD)
  BOARD.Place(W_BISHOP)
  W_BISHOP = Bishop(1,6,'W',BOARD)
  BOARD.Place(W_BISHOP)
  W_KNIGHT = Knight(1,2,'W',BOARD)
  BOARD.Place(W_KNIGHT)
  W_KNIGHT = Knight(1,7,'W',BOARD)
  BOARD.Place(W_KNIGHT)
  W_LROOK = Rook(1,1,'W',BOARD)
  BOARD.Place(W_LROOK)
  W_RROOK = Rook(1,8,'W',BOARD)
  BOARD.Place(W_RROOK)
  W_QUEEN = Queen(1,4,'W',BOARD)
  BOARD.Place(W_QUEEN)
  W_KING = King(1,5,'W',BOARD,W_LROOK,W_RROOK)
  BOARD.Place(W_KING)
  B_PAWN = Pawn(7,1,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,2,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,3,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,4,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(5,5,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,6,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,7,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,8,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_BISHOP = Bishop(8,3,'B',BOARD)
  BOARD.Place(B_BISHOP)
  B_BISHOP = Bishop(8,6,'B',BOARD)
  BOARD.Place(B_BISHOP)
  B_KNIGHT = Knight(8,2,'B',BOARD)
  BOARD.Place(B_KNIGHT)
  B_KNIGHT = Knight(8,7,'B',BOARD)
  BOARD.Place(B_KNIGHT)
  B_LROOK = Rook(8,1,'B',BOARD)
  BOARD.Place(B_LROOK)
  B_RROOK = Rook(8,8,'B',BOARD)
  BOARD.Place(B_RROOK)
  B_QUEEN = Queen(8,4,'B',BOARD)
  BOARD.Place(B_QUEEN)
  B_KING = King(8,5,'B',BOARD,B_LROOK,B_RROOK)
  BOARD.Place(B_KING)
  BOARD.all_white.reverse()
  BOARD.all_black.reverse()
  BOARD.alive_white.reverse()
  BOARD.alive_black.reverse()
  return BOARD

def Game5():
  BOARD = Board()
  W_PAWN = Pawn(2,1,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,2,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,3,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(4,4,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,5,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,6,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,7,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,8,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_BISHOP = Bishop(1,3,'W',BOARD)
  BOARD.Place(W_BISHOP)
  W_BISHOP = Bishop(1,6,'W',BOARD)
  BOARD.Place(W_BISHOP)
  W_KNIGHT = Knight(1,2,'W',BOARD)
  BOARD.Place(W_KNIGHT)
  W_KNIGHT = Knight(1,7,'W',BOARD)
  BOARD.Place(W_KNIGHT)
  W_LROOK = Rook(1,1,'W',BOARD)
  BOARD.Place(W_LROOK)
  W_RROOK = Rook(1,8,'W',BOARD)
  BOARD.Place(W_RROOK)
  W_QUEEN = Queen(1,4,'W',BOARD)
  BOARD.Place(W_QUEEN)
  W_KING = King(1,5,'W',BOARD,W_LROOK,W_RROOK)
  BOARD.Place(W_KING)
  B_PAWN = Pawn(7,1,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,2,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,3,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(5,4,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,5,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,6,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,7,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,8,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_BISHOP = Bishop(8,3,'B',BOARD)
  BOARD.Place(B_BISHOP)
  B_BISHOP = Bishop(8,6,'B',BOARD)
  BOARD.Place(B_BISHOP)
  B_KNIGHT = Knight(8,2,'B',BOARD)
  BOARD.Place(B_KNIGHT)
  B_KNIGHT = Knight(8,7,'B',BOARD)
  BOARD.Place(B_KNIGHT)
  B_LROOK = Rook(8,1,'B',BOARD)
  BOARD.Place(B_LROOK)
  B_RROOK = Rook(8,8,'B',BOARD)
  BOARD.Place(B_RROOK)
  B_QUEEN = Queen(8,4,'B',BOARD)
  BOARD.Place(B_QUEEN)
  B_KING = King(8,5,'B',BOARD,B_LROOK,B_RROOK)
  BOARD.Place(B_KING)
  BOARD.all_white.reverse()
  BOARD.all_black.reverse()
  BOARD.alive_white.reverse()
  BOARD.alive_black.reverse()
  return BOARD

def Game6():
  BOARD = Board()
  W_PAWN = Pawn(2,1,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,2,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,3,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,4,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(4,5,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,6,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,7,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_PAWN = Pawn(2,8,'W',BOARD)
  BOARD.Place(W_PAWN)
  W_BISHOP = Bishop(1,3,'W',BOARD)
  BOARD.Place(W_BISHOP)
  W_BISHOP = Bishop(1,6,'W',BOARD)
  BOARD.Place(W_BISHOP)
  W_KNIGHT = Knight(1,2,'W',BOARD)
  BOARD.Place(W_KNIGHT)
  W_KNIGHT = Knight(1,7,'W',BOARD)
  BOARD.Place(W_KNIGHT)
  W_LROOK = Rook(1,1,'W',BOARD)
  BOARD.Place(W_LROOK)
  W_RROOK = Rook(1,8,'W',BOARD)
  BOARD.Place(W_RROOK)
  W_QUEEN = Queen(1,4,'W',BOARD)
  BOARD.Place(W_QUEEN)
  W_KING = King(1,5,'W',BOARD,W_LROOK,W_RROOK)
  BOARD.Place(W_KING)
  B_PAWN = Pawn(7,1,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,2,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,3,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,4,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(6,5,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,6,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,7,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_PAWN = Pawn(7,8,'B',BOARD)
  BOARD.Place(B_PAWN)
  B_BISHOP = Bishop(8,3,'B',BOARD)
  BOARD.Place(B_BISHOP)
  B_BISHOP = Bishop(8,6,'B',BOARD)
  BOARD.Place(B_BISHOP)
  B_KNIGHT = Knight(8,2,'B',BOARD)
  BOARD.Place(B_KNIGHT)
  B_KNIGHT = Knight(8,7,'B',BOARD)
  BOARD.Place(B_KNIGHT)
  B_LROOK = Rook(8,1,'B',BOARD)
  BOARD.Place(B_LROOK)
  B_RROOK = Rook(8,8,'B',BOARD)
  BOARD.Place(B_RROOK)
  B_QUEEN = Queen(8,4,'B',BOARD)
  BOARD.Place(B_QUEEN)
  B_KING = King(8,5,'B',BOARD,B_LROOK,B_RROOK)
  BOARD.Place(B_KING)
  BOARD.all_white.reverse()
  BOARD.all_black.reverse()
  BOARD.alive_white.reverse()
  BOARD.alive_black.reverse()
  return BOARD

if __name__ == '__main__':
  print InitBoard()

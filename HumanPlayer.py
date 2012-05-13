import ChessBoard

let_to_piece = {
          'P':ChessBoard.Pawn,
          'B':ChessBoard.Bishop,
          'R':ChessBoard.Rook,
          'N':ChessBoard.Knight,
          'Q':ChessBoard.Queen
           }

piece_to_let = {
                ChessBoard.Pawn: 'P',
                ChessBoard.Bishop: 'B',
                ChessBoard.Rook: 'R',
                ChessBoard.Knight: 'N',
                ChessBoard.Queen: 'Q',
               }

class Player():
  def __init__(self,pieces):
    self.color = pieces[0].color
    self.P1 = pieces[15]
    self.P2 = pieces[14]
    self.P3 = pieces[13]
    self.P4 = pieces[12]
    self.P5 = pieces[11]
    self.P6 = pieces[10]
    self.P7 = pieces[9]
    self.P8 = pieces[8]
    self.B1 = pieces[7]
    self.N1 = pieces[6]
    self.B2 = pieces[5]
    self.N2 = pieces[4]
    self.R1 = pieces[3]
    self.R2 = pieces[2]
    self.Q = pieces[1]
    self.K = pieces[0]
    self.di = {'P1':self.P1,
               'P2':self.P2,
               'P3':self.P3,
               'P4':self.P4,
               'P5':self.P5,
               'P6':self.P6,
               'P7':self.P7,
               'P8':self.P8,
               'B1':self.B1,
               'N1':self.N1,
               'B2':self.B2,
               'N2':self.N2,
               'R1':self.R1,
               'R2':self.R2,
               'Q1':self.Q,
               'K1':self.K,
               }
    self.next_val = {'P':9,
                      'B':3,
                      'N':3,
                      'R':3,
                      'Q':2}

  def UpdatePieceList(self,BOARD):
    if self.color == 'W':
      curr_pieces = BOARD.GetWhite()
    else:
      curr_pieces = BOARD.GetBlack()
    if not curr_pieces[-1] in self.di.values():
      new_piece = curr_pieces[-1]
      piece_let = piece_to_let[new_piece.__class__]
      piece_ind = str(self.next_val[piece_let])
      self.next_val[piece_let] += 1
      self.di[piece_let+piece_ind] = new_piece
      print "NEW PIECE IS", (piece_let+piece_ind)

  def GetMove(self,BOARD):
    self.UpdatePieceList(BOARD)

    print BOARD
    move = raw_input('Enter Move?')
    piece = self.di[move[:2]]
    col = ord(move[2])-ord('A')+1
    row = int(move[3])
    if len(move) > 4:
      return (piece, (row,col),let_to_piece[move[4]])
    else:
      return (piece, (row,col))

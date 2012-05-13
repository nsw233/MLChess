import sys
sys.path.append('../libsvm-3.12/python')
import ChessBoard
import svmutil

def Eval(board):
  PTP = board.GetPTP()
  WKingSafety = [] #Can castle
                  #Number of unoccupied neighboring vulnerable squares (0 to 8)
  BKingSafety = []
  WMaterial = [] #(score, 0) for each piece
  BMaterial = []
  WPieceActivity = [] #Number of threatened squares for each piece
  BPieceActivity = []
  WPawnStructure = [] #(0,1) in center square
                     #(0,1) Passed pawn
                     #(0,1) Part of pawn chain
                     #(-1,0) Base of 2 pawn chains
  BPawnStructure = []
  for w_piece, b_piece in zip(board.GetWhite(),board.GetBlack()):
    if w_piece.alive:
      WMaterial.append(w_piece.score)
    else:
      WMaterial.append(0)
    if b_piece.alive:
      BMaterial.append(b_piece.score)
    else:
      BMaterial.append(0)
    if w_piece.alive and b_piece.alive:
      WPieceActivity.append(.25*len(w_piece.MoveChoices()))
      BPieceActivity.append(.25*len(b_piece.MoveChoices()))
    else:
      WPieceActivity.append(0)
      BPieceActivity.append(0)
    if w_piece.alive and w_piece.__class__ == ChessBoard.Pawn and \
       b_piece.alive and b_piece.__class__ == ChessBoard.Pawn:
      if (w_piece.row == 4 or w_piece.row == 5) and \
         (w_piece.col == 4 or w_piece.col == 5):
        WPawnStructure.append(.5)
      else:
        WPawnStructure.append(0)
      for col in xrange(w_piece.col-1, w_piece.col+2):
        if col == 0 or col == 9:
          continue
        for row in xrange(w_piece.row+1,9,1):
          if PTP[row][col] and \
             PTP[row][col].color == 'B' and \
             PTP[row][col].__class__ == ChessBoard.Pawn:
            WPawnStructure.append(0)
            break
        if len(WPawnStructure)%4 == 2:
          break
      if len(WPawnStructure)%4 == 1:
        WPawnStructure.append(.5)
      num_base_pyr = 0
      num_top_pyr = 0
      if 0 < w_piece.row+1 < 9 and 0 < w_piece.col+1 < 9 and \
         PTP[w_piece.row+1][w_piece.col+1] and \
         PTP[w_piece.row+1][w_piece.col+1].color == 'W' and \
         PTP[w_piece.row+1][w_piece.col+1].__class__ == ChessBoard.Pawn:
        num_base_pyr += 1
      if 0 < w_piece.row-1 < 9 and 0 < w_piece.col+1 < 9 and \
         PTP[w_piece.row-1][w_piece.col+1] and \
         PTP[w_piece.row-1][w_piece.col+1].color == 'W' and \
         PTP[w_piece.row-1][w_piece.col+1].__class__ == ChessBoard.Pawn:
        num_base_pyr += 1
      if 0 < w_piece.row+1 < 9 and 0 < w_piece.col-1 < 9 and \
         PTP[w_piece.row+1][w_piece.col-1] and \
         PTP[w_piece.row+1][w_piece.col-1].color == 'W' and \
         PTP[w_piece.row+1][w_piece.col-1].__class__ == ChessBoard.Pawn:
        num_top_pyr += 1
      if 0 < w_piece.row-1 < 9 and 0 < w_piece.col-1 < 9 and \
         PTP[w_piece.row-1][w_piece.col-1] and \
         PTP[w_piece.row-1][w_piece.col-1].color == 'W' and \
         PTP[w_piece.row-1][w_piece.col-1].__class__ == ChessBoard.Pawn:
        num_top_pyr += 1
      WPawnStructure.append(.25*max(num_base_pyr,num_top_pyr))
      if num_base_pyr >= 2 + num_top_pyr:
        WPawnStructure.append(-1)
      else:
        WPawnStructure.append(0)
      if (b_piece.row == 4 or b_piece.row == 5) and \
         (b_piece.col == 4 or b_piece.col == 5):
        BPawnStructure.append(.5)
      else:
        BPawnStructure.append(0)
      for col in xrange(b_piece.col-1, b_piece.col+2):
        if col == 0 or col == 9:
          continue
        for row in xrange(b_piece.row-1,0,-1):
          if PTP[row][col] and \
             PTP[row][col].color == 'W' and \
             PTP[row][col].__class__ == ChessBoard.Pawn:
            BPawnStructure.append(0)
            break
        if len(BPawnStructure)%4 == 2:
          break
      if len(BPawnStructure)%4 == 1:
        BPawnStructure.append(.5)
      num_base_pyr = 0
      num_top_pyr = 0
      if 0 < b_piece.row+1 < 9 and 0 < b_piece.col+1 < 9 and \
         PTP[b_piece.row+1][b_piece.col+1] and \
         PTP[b_piece.row+1][b_piece.col+1].color == 'B' and \
         PTP[b_piece.row+1][b_piece.col+1].__class__ == ChessBoard.Pawn:
        num_base_pyr += 1
      if 0 < b_piece.row-1 < 9 and 0 < b_piece.col+1 < 9 and \
         PTP[b_piece.row-1][b_piece.col+1] and \
         PTP[b_piece.row-1][b_piece.col+1].color == 'B' and \
         PTP[b_piece.row-1][b_piece.col+1].__class__ == ChessBoard.Pawn:
        num_base_pyr += 1
      if 0 < b_piece.row+1 < 9 and 0 < b_piece.col-1 < 9 and \
         PTP[b_piece.row+1][b_piece.col-1] and \
         PTP[b_piece.row+1][b_piece.col-1].color == 'B' and \
         PTP[b_piece.row+1][b_piece.col-1].__class__ == ChessBoard.Pawn:
        num_top_pyr += 1
      if 0 < b_piece.row-1 < 9 and 0 < b_piece.col-1 < 9 and \
         PTP[b_piece.row-1][b_piece.col-1] and \
         PTP[b_piece.row-1][b_piece.col-1].color == 'B' and \
         PTP[b_piece.row-1][b_piece.col-1].__class__ == ChessBoard.Pawn:
        num_top_pyr += 1
      BPawnStructure.append(.25*max(num_base_pyr,num_top_pyr))
      if num_base_pyr >= 2 + num_top_pyr:
        BPawnStructure.append(-1)
      else:
        BPawnStructure.append(0)
    else:
      WPawnStructure.extend([0,0,0,0])
      BPawnStructure.extend([0,0,0,0])
    if w_piece.__class__ == ChessBoard.King:
      if w_piece.castle:
        WKingSafety.append(.5)
      else:
        WKingSafety.append(0)
      num_squares = 9
      for col in xrange(w_piece.col-1,w_piece.col+2):
        if col == 0 or col == 9:
          num_squares -= 3
          continue
        for row in xrange(w_piece.row-1,w_piece.row+2):
          if row == 0 or row == 9:
            num_squares -= 1
            continue
          if PTP[row][col] and \
             PTP[row][col].color == 'W':
            num_squares -= 1
      WKingSafety.append(.25*num_squares)
    if b_piece.__class__ == ChessBoard.King:
      if b_piece.castle:
        BKingSafety.append(.5)
      else:
        BKingSafety.append(0)
      num_squares = 9
      for col in xrange(b_piece.col-1,b_piece.col+2):
        if col == 0 or col == 9:
          num_squares -= 3
          continue
        for row in xrange(b_piece.row-1,b_piece.row+2):
          if row == 0 or row == 9:
            num_squares -= 1
            continue
          if PTP[row][col] and \
             PTP[row][col].color == 'B':
            num_squares -= 1
      BKingSafety.append(.25*num_squares)
  return WKingSafety, WMaterial, WPieceActivity, WPawnStructure[32:],\
         BKingSafety, BMaterial, BPieceActivity, BPawnStructure[32:]

m = svmutil.svm_load_model('CAMod/model1.txt')

def NoAggEval(board, color, num_moves):
  if num_moves == 0:
    dummy_piece = board.GetWhiteAlive()[0]
    if board.Check(dummy_piece, color,
                   (dummy_piece.row,dummy_piece.col)):
      if color == 'W':
        return -1000
      else:
        return 1000

    return 0
  w1,w2,w3,w4,b1,b2,b3,b4 = Eval(board)
  feats = []
  for li in [w1,w2,w3,w4,b1,b2,b3,b4]:
    feats.extend(li)
  u_a,u_b,val = svmutil.svm_predict([0],[feats],m)
  return 2*val[0][0]-1

def AggEval(board, color, num_moves):
  if num_moves == 0:
    dummy_piece = board.GetWhiteAlive()[0]
    if board.Check(dummy_piece, color,
                   (dummy_piece.row,dummy_piece.col)):
      if color == 'W':
        return -1000
      else:
        return 1000

    return 0
  w1,w2,w3,w4,b1,b2,b3,b4 = Eval(board)
  u_a,u_b,val = svmutil.svm_predict([0],[[sum(w1),sum(w2),sum(w3),sum(w4),sum(b1),sum(b2),sum(b3),sum(b4)]],m)
  return val[0][0]

def BaseEval(board, color, num_moves):
  if num_moves == 0:
    dummy_piece = board.GetWhiteAlive()[0]
    if board.Check(dummy_piece, color,
                   (dummy_piece.row,dummy_piece.col)):
      if color == 'W':
        return -1000
      else:
        return 1000
    return 0
  w1,w2,w3,w4,b1,b2,b3,b4 = Eval(board)
  w_score = sum(w1)+sum(w2)+sum(w3)+sum(w4)-(sum(b1)+sum(b2)+sum(b3)+sum(b4))
#  print sum(w1),sum(w2),sum(w3),sum(w4),sum(b1),sum(b2),sum(b3),sum(b4)

  return w_score

import SimuBoard
MAX_D = 2
#import random

colors = ['W','B']

def alphabeta(board_s, depth, alpha, beta, player, max_player,Eval,p_t):
  color = colors[player]
  move_list = SimuBoard.GetMoveList(board_s,player)
  best_move = None
  if depth == MAX_D -1:
    board_str = str(board_s)
    if board_str in p_t and p_t[board_str] == 2:
      return 0
  if depth == 0 or len(move_list) == 0:
    score = Eval(board_s, color, len(move_list))
#    print score
    if max_player == 1:
      return -1*score
    else:
      return score
  if player == max_player:
    for move in move_list:
      new_board = SimuBoard.SimuBoard(board_s)
      piece_dict = new_board.UpdateSimuBoard(move[0], move[1], move[2])
      old_alpha = alpha
      alpha = max(alpha, alphabeta(new_board, depth-1, alpha, beta, 1-player,
                                  max_player,Eval,p_t))
      #if depth == MAX_D:
      #  print move[0],move[1:]
      #print old_alpha, alpha
      if depth == MAX_D and old_alpha < alpha:# and \
        #(best_move == None or random.random() <= .95):
        best_move = move
      for new_piece, old_piece in piece_dict.items():
        if new_piece.color == 'W':
          piece_list = new_board.GetWhite()
        else:
          piece_list = new_board.GetBlack()
        if new_piece in piece_list:
          piece_list[piece_list.index(new_piece)] = old_piece
        else:
          if new_piece.__class__ == SimuBoard.ChessBoard.Pawn:
            poss_rep = None
            for piece in piece_list[8:]:
              if piece.__class__ != SimuBoard.ChessBoard.Pawn:
                poss_rep = piece
                break
            if poss_rep:
              piece_list[piece_list.index(poss_rep)] = old_piece
            else:
              piece_list[piece_list.index(new_piece)] = old_piece
          else:
            piece_list[piece_list.index(new_piece)] = old_piece
      board_s.RefreshPTP(new_board.pos_to_piece)
      board_s.RefreshAlive()
      if beta <= alpha:
        break
    if depth == MAX_D:
      return best_move
    return alpha
  else:
    for move in move_list:
      new_board = SimuBoard.SimuBoard(board_s)
      piece_dict = new_board.UpdateSimuBoard(move[0], move[1], move[2])
      beta = min(beta, alphabeta(new_board, depth-1, alpha, beta, 1-player,
                                 max_player,Eval,p_t))
      for new_piece, old_piece in piece_dict.items():
        if new_piece.color == 'W':
          piece_list = new_board.GetWhite()
        else:
          piece_list = new_board.GetBlack()
        if new_piece in piece_list:
          piece_list[piece_list.index(new_piece)] = old_piece
        else:
          if new_piece.__class__ == SimuBoard.ChessBoard.Pawn:
            poss_rep = None
            for piece in piece_list[8:]:
              if piece.__class__ != SimuBoard.ChessBoard.Pawn:
                poss_rep = piece
                break
            if poss_rep:
              piece_list[piece_list.index(poss_rep)] = old_piece
            else:
              piece_list[piece_list.index(new_piece)] = old_piece
          else:
            piece_list[piece_list.index(new_piece)] = old_piece
      board_s.RefreshPTP(new_board.pos_to_piece)
      board_s.RefreshAlive()
      if beta <= alpha:
        break
    return beta

#Still need to extract move from this...
'''
(* Initial call *)
alphabeta(origin, depth, -infinity, +infinity, MaxPlayer)'''

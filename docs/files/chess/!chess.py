from tkinter import *
import copy
board = dict()
coord = [0,92,184,276,368,460,552,644,9999999]
x_axis = ['a','b','c','d','e','f','g','h']
y_axis = ['8','7','6','5','4','3','2','1']
globalicon = ['']*64
globalselect = "none"
legal_moves = []
legal_captures = []
select_piece = False
root = Tk()
frame = Frame(root)
frame.pack()
canvas = Canvas(root, width = 800, height = 800)
canvas.pack()
globaldot = PhotoImage(file = "move_dot.png")
globaltarget = PhotoImage(file = "target.png")
globalcheck = PhotoImage(file = "check.png")
globalcastle = PhotoImage(file = "castle.png")
selectbox = PhotoImage(file = "selection_box.png")
globalturn = "white"
icon_garbage = []
global_trample_spaces = [] ##list of lists of spaces to an opponent king where inbetween stands only 1 opposing piece
global_trample_over_king = [] ###list of lists of spaces to opponent king undisturbed, and the empty spaces behind the king
global_trample_before_king = [] ##list of lists of spaces to opponent king
king_space = dict()
king_space["black"] = "none"
king_space["white"] = "none"
king_is_in_check = dict()
king_is_in_check["black"] = False
king_is_in_check["white"] = False
castle_left = "none"
castle_right = "none"
cannon_path_to_king = []
cannon_targeting_king = []
class square(object):
    def __init__(self,newline):
        self.current_tile = newline[1]
        self.diag_up_left = newline[2]
        self.up = newline[3]
        self.diag_up_right = newline[4]
        self.right = newline[5]
        self.diag_down_right = newline[6]
        self.down = newline[7]
        self.diag_down_left = newline[8]
        self.left = newline[9]
        self.occupying_piece = "none"
        self.x_coord = int(newline[10])
        self.y_coord = int(newline[11])

        
def move_diag_up_left(tile):
    return(board[tile].diag_up_left)
def move_up(tile):
    return(board[tile].up)
def move_diag_up_right(tile):
    return(board[tile].diag_up_right)
def move_right(tile):
    return(board[tile].right)
def move_diag_down_right(tile):
    return(board[tile].diag_down_right)
def move_down(tile):
    return(board[tile].down)
def move_diag_down_left(tile):
    return(board[tile].diag_down_left)
def move_left(tile):
    return(board[tile].left)
           
def move_castle(move_target):
    global canvas
    global globalselect
    global icon_garbage
    global global_trample_spaces
    global global_trample_over_king
    global global_trample_before_king
    global king_is_in_check
    canvas.delete("dot")
    if move_target == castle_left[1]:
        canvas.delete(castle_left[0])
        board[move_target].occupying_piece= board[king_space[globalturn]].occupying_piece
        board[move_target].occupying_piece.hasMoved = True
        board[king_space[globalturn]].occupying_piece = "none"
        iconimage = PhotoImage(file = board[move_target].occupying_piece.icon)
        icon_garbage.append(iconimage)
        canvas.create_image(board[move_target].x_coord,board[move_target].y_coord,image = icon_garbage[-1] ,tag = move_target)
        board[move_right(move_target)].occupying_piece = board[castle_left[0]].occupying_piece
        board[castle_left[0]].occupying_piece = "none"
        board[move_right(move_target)].occupying_piece.hasMoved = True
        iconimage = PhotoImage(file = board[move_right(move_target)].occupying_piece.icon)
        icon_garbage.append(iconimage)
        canvas.create_image(board[move_right(move_target)].x_coord,board[move_right(move_target)].y_coord,image = icon_garbage[-1] ,tag = move_right(move_target))
    elif move_target == castle_right[1]:
        canvas.delete(castle_right[0])
        board[move_target].occupying_piece= board[king_space[globalturn]].occupying_piece
        board[move_target].occupying_piece.hasMoved = True
        board[king_space[globalturn]].occupying_piece = "none"
        iconimage = PhotoImage(file = board[move_target].occupying_piece.icon)
        icon_garbage.append(iconimage)
        canvas.create_image(board[move_target].x_coord,board[move_target].y_coord,image = icon_garbage[-1] ,tag = move_target)
        board[move_left(move_target)].occupying_piece = board[castle_right[0]].occupying_piece
        board[castle_right[0]].occupying_piece = "none"
        board[move_left(move_target)].occupying_piece.hasMoved = True
        iconimage = PhotoImage(file = board[move_left(move_target)].occupying_piece.icon)
        icon_garbage.append(iconimage)
        canvas.create_image(board[move_left(move_target)].x_coord,board[move_left(move_target)].y_coord,image = icon_garbage[-1] ,tag = move_left(move_target))
    
    global_trample_spaces = []
    global_trample_over_king = []
    global_trample_before_king = []
    king_is_in_check[globalturn] = False
    canvas.delete(globalselect)
    canvas.delete("dot")

######################PIECE DEFINITIONS######################
              
class piece(object):
    def __init__(self,team):
        self.team = team
        self.hasMoved = False
    
class pawn(piece):
    def __init__(self,team):
        self.team = team
        self.hasMoved = False
        self.name = "pawn"
        self.canTrample = False
        self.canPromote = True
        if self.team == "white":
            self.icon = "pawn_white.png"
        elif self.team == "black":
            self.icon = "pawn_black.png"

    def move(self,tile):
        pawn_move(tile)
        
class bishop(piece):
    def __init__(self,team):
        self.team = team
        self.hasMoved = False
        self.name = "bishop"
        self.canTrample = True
        self.canPromote = False
        if self.team == "white":
            self.icon = "bishop_white.png"
        elif self.team == "black":
            self.icon = "bishop_black.png"

    def move(self,tile):
        bishop_move(tile)

    def trample(self,tile):
        bishop_trample(tile)
        
class knight(piece):
    def __init__(self,team):
        self.team = team
        self.hasMoved = False
        self.name = "knight"
        self.canTrample = False
        self.canPromote = False
        if self.team == "white":
            self.icon = "knight_white.png"
        elif self.team == "black":
            self.icon = "knight_black.png"

    def move(self,tile):
        knight_move(tile)
        
class rook(piece):
    def __init__(self,team):
        self.team = team
        self.hasMoved = False
        self.name = "rook"
        self.canTrample = True
        self.canPromote = False
        if self.team == "white":
            self.icon = "rook_white.png"
        elif self.team == "black":
            self.icon = "rook_black.png"
            
    def move(self,tile):
        rook_move(tile)
                            
    def trample(self,tile):
        rook_trample(tile)
            
class queen(piece):
    def __init__(self,team):
        self.team = team
        self.hasMoved = False
        self.name = "queen"
        self.canTrample = True
        self.canPromote = False
        if self.team == "white":
            self.icon = "queen_white.png"
        elif self.team == "black":
            self.icon = "queen_black.png"
    def move(self,tile):
        bishop_move(tile)
        rook_move(tile)
    def trample(self,tile):
        bishop_trample(tile)
        rook_trample(tile)
        
class king(piece):
    def __init__(self,team):
        self.team = team
        self.hasMoved = False
        self.name = "king"
        self.isInCheck = False
        self.canTrample = False
        self.canPromote = False
        if self.team == "white":
            self.icon = "king_white.png"
        elif self.team == "black":
            self.icon = "king_black.png"
    def move(self,tile):
        king_move(tile)
                   
class mann(piece):
    def __init__(self,team):
        self.team= team
        self.hasMoved = False
        self.name = "mann"
        self.canTrample = False
        self.canPromote = False
        if self.team == "white":
            self.icon = "mann_white.png"
        elif self.team == "black":
            self.icon = "mann_black.png"
    def move(self,tile):
        mann_move(tile)

class unicorn(piece):
    def __init__(self,team):
        self.team= team
        self.hasMoved = False
        self.name = "unicorn"
        self.canTrample = False
        self.canPromote = False
        if self.team == "white":
            self.icon = "unicorn_white.png"
        elif self.team == "black":
            self.icon = "unicorn_black.png"
    def move(self,tile):
        knight_move(tile,True)

class cannon(piece):
    def __init__(self,team):
        self.team= team
        self.hasMoved = False
        self.name = "cannon"
        self.canTrample = True
        self.canPromote = False
        if self.team == "white":
            self.icon = "cannon_white.png"
        elif self.team == "black":
            self.icon = "cannon_black.png"
    def move(self,tile):
        cannon_move(tile)
        

def check_for_promotion(tile):
    if board[tile].occupying_piece.team == "white":
        uptile = move_up(tile)
        if uptile == '0':
            promote(tile)
    if board[tile].occupying_piece.team == "black":
        downtile = move_down(tile)
        if downtile =='0':
            promote(tile)

def promote(tile):
    canvas.create_rectangle(184,322,552,414,fill= "#dbd3c7",tag = "promotion")
    if board[tile].occupying_piece.team == "white":
        icon = PhotoImage(file = "bishop_white.png")
        icon_garbage.append(icon)
        image1 = canvas.create_image(230,368,image = icon_garbage[-1],tags = ("promotion","image1"))
        canvas.tag_bind("image1",'<Button-1>',lambda e: actually_promote(tile,"bishop","white"))
        icon = PhotoImage(file = "knight_white.png")
        icon_garbage.append(icon)
        image2 = canvas.create_image(322,368,image = icon_garbage[-1],tag = ("promotion","image2"))
        canvas.tag_bind("image2",'<Button-1>',lambda e: actually_promote(tile,"knight","white"))
        icon = PhotoImage(file = "rook_white.png")
        icon_garbage.append(icon)
        image3 = canvas.create_image(414,368,image = icon_garbage[-1],tag = ("promotion","image3"))
        canvas.tag_bind("image3",'<Button-1>',lambda e:actually_promote(tile,"rook","white"))
        icon = PhotoImage(file = "queen_white.png")
        icon_garbage.append(icon)
        image4 = canvas.create_image(506,368,image = icon_garbage[-1],tag = ("promotion","image4"))
        canvas.tag_bind("image4",'<Button-1>',lambda e:actually_promote(tile,"queen","white"))
    if board[tile].occupying_piece.team == "black":
        icon = PhotoImage(file = "bishop_black.png")
        icon_garbage.append(icon)
        image1 = canvas.create_image(230,368,image = icon_garbage[-1],tag = ("promotion","image1"))
        canvas.tag_bind("image1",'<Button-1>',lambda e:actually_promote(tile,"bishop","black"))
        icon = PhotoImage(file = "knight_black.png")
        icon_garbage.append(icon)
        image2 = canvas.create_image(322,368,image = icon_garbage[-1],tag = ("promotion","image2"))
        canvas.tag_bind("image2",'<Button-1>',lambda e:actually_promote(tile,"knight","black"))
        icon = PhotoImage(file = "rook_black.png")
        icon_garbage.append(icon)
        image3 = canvas.create_image(414,368,image = icon_garbage[-1],tag = ("promotion","image3"))
        canvas.tag_bind("image3",'<Button-1>',lambda e:actually_promote(tile,"rook","black"))
        icon = PhotoImage(file = "queen_black.png")
        icon_garbage.append(icon)
        image4 = canvas.create_image(506,368,image = icon_garbage[-1],tag = ("promotion","image4"))
        canvas.tag_bind("image4",'<Button-1>',lambda e:actually_promote(tile,"queen","black"))

def actually_promote(tile,piece,team):
    canvas.delete(tile)
    canvas.delete("promotion")
    if piece == "knight":
        board[tile].occupying_piece = knight(team)
    elif piece == "bishop":
        board[tile].occupying_piece = bishop(team)
    elif piece == "rook":
        board[tile].occupying_piece = rook(team)
    elif piece == "queen":
        board[tile].occupying_piece = queen(team)
    icon = PhotoImage(file = board[tile].occupying_piece.icon)
    icon_garbage.append(icon)
    canvas.create_image(board[tile].x_coord,board[tile].y_coord,image = icon_garbage[-1],tag = tile)

def pawn_move(tile):
    global legal_moves
    global legal_captures
    if board[tile].occupying_piece.team == "white":
        uptile = move_up(tile)
        captureright = move_diag_up_right(tile)
        captureleft = move_diag_up_left(tile)
        if board[tile].occupying_piece.hasMoved == False:
            for i in range(0,2):
                if uptile != '0' and board[uptile].occupying_piece == "none":
                    legal_moves.append(uptile)
                    uptile = move_up(uptile)
        else:
            if uptile != '0' and board[uptile].occupying_piece == "none":                    
                    legal_moves.append(uptile)
                    uptile = move_up(uptile)
        if captureright != '0' and board[captureright].occupying_piece != "none" and board[captureright].occupying_piece.team != board[tile].occupying_piece.team:
            legal_captures.append(captureright)
        if captureleft != '0' and board[captureleft].occupying_piece != "none" and board[captureleft].occupying_piece.team != board[tile].occupying_piece.team:
            legal_captures.append(captureleft)
            
    if board[tile].occupying_piece.team == "black":
        downtile = move_down(tile)
        captureright = move_diag_down_right(tile)
        captureleft = move_diag_down_left(tile)
        if board[tile].occupying_piece.hasMoved == False:
            for i in range(0,2):
                if downtile != '0' and board[downtile].occupying_piece == "none":
                    legal_moves.append(downtile)
                    downtile = move_down(downtile)
        else:
            if downtile != '0' and board[downtile].occupying_piece == "none":
                    legal_moves.append(downtile)
                    downtile = move_down(downtile)
        if captureright != '0' and board[captureright].occupying_piece != "none" and board[captureright].occupying_piece.team != board[tile].occupying_piece.team:
            legal_captures.append(captureright)
        if captureleft != '0' and board[captureleft].occupying_piece != "none" and board[captureleft].occupying_piece.team != board[tile].occupying_piece.team:
            legal_captures.append(captureleft)
            
            
    for line in global_trample_spaces:
        if tile in line:
            legal_moves = list(set(line).intersection(legal_moves))
            legal_captures = list(set(line).intersection(legal_captures))
            
    if len(cannon_path_to_king) != 0:
        for line in cannon_path_to_king:
            for square in line:
                if square in legal_moves:
                    legal_moves.remove(square)
                if square in legal_captures:
                    legal_captures.remove(square)
            
    if king_is_in_check[board[tile].occupying_piece.team] == True: ##DO THIS before king
        is_involved_in_cannon = False
        if len(cannon_targeting_king)> 0:
            for line in cannon_targeting_king:
                if tile in line:
                    is_involved_in_cannon = True
                    legal_moves = list(set(line).intersection(legal_moves))
                    legal_captures = list(set(line).intersection(legal_captures))
                if line[-1] in legal_captures:
                    is_involved_in_cannon = True
                    legal_moves = []
                    legal_captures = line[-1]
        if is_involved_in_cannon == False:
            legal_moves = []
            legal_captures =[]
            
        if len(global_trample_before_king)+ len(cannon_targeting_king) > 1:
            legal_moves = []
            legal_captures = []
        elif len(global_trample_before_king) != 0:
            if len(legal_moves)!= 0 :
                for space in legal_moves:
                    if space not in global_trample_before_king[0]:
                        legal_moves.remove(space)
                for space in legal_moves: ##just do it twice
                    if space not in global_trample_before_king[0]:
                        legal_moves.remove(space)
                for space in legal_moves: ##just do it twice
                    if space not in global_trample_before_king[0]:
                        legal_moves.remove(space)
            if len(legal_captures)!= 0 :
                for space in legal_captures:
                    if space not in global_trample_before_king[0]:
                        legal_captures.remove(space)


                        

def bishop_move(tile):
    global legal_moves
    global legal_captures
    diag_up_lefttile = move_diag_up_left(tile)
    diag_up_righttile = move_diag_up_right(tile)
    diag_down_lefttile = move_diag_down_left(tile)
    diag_down_righttile = move_diag_down_right(tile)
    while diag_up_lefttile != "0" and board[diag_up_lefttile].occupying_piece == "none":
        legal_moves.append(diag_up_lefttile)
        diag_up_lefttile = move_diag_up_left(diag_up_lefttile)
    while diag_up_righttile != "0" and board[diag_up_righttile].occupying_piece == "none":
        legal_moves.append(diag_up_righttile)
        diag_up_righttile = move_diag_up_right(diag_up_righttile)
    while diag_down_lefttile != "0" and board[diag_down_lefttile].occupying_piece == "none":
        legal_moves.append(diag_down_lefttile)
        diag_down_lefttile = move_diag_down_left(diag_down_lefttile)
    while diag_down_righttile != "0" and board[diag_down_righttile].occupying_piece == "none":
        legal_moves.append(diag_down_righttile)
        diag_down_righttile = move_diag_down_right(diag_down_righttile)
    if diag_up_lefttile != "0" and board[diag_up_lefttile].occupying_piece != "none" and board[diag_up_lefttile].occupying_piece.team != board[tile].occupying_piece.team:
        legal_captures.append(diag_up_lefttile)
    if diag_up_righttile != "0" and board[diag_up_righttile].occupying_piece != "none" and board[diag_up_righttile].occupying_piece.team != board[tile].occupying_piece.team:
        legal_captures.append(diag_up_righttile)
    if diag_down_lefttile != "0" and board[diag_down_lefttile].occupying_piece != "none" and board[diag_down_lefttile].occupying_piece.team != board[tile].occupying_piece.team:
        legal_captures.append(diag_down_lefttile)
    if diag_down_righttile != "0" and board[diag_down_righttile].occupying_piece != "none" and board[diag_down_righttile].occupying_piece.team != board[tile].occupying_piece.team:
        legal_captures.append(diag_down_righttile)
        
            
    for line in global_trample_spaces:
        if tile in line:
            legal_moves = list(set(line).intersection(legal_moves))
            legal_captures = list(set(line).intersection(legal_captures))
            
    if len(cannon_path_to_king) != 0:
        for line in cannon_path_to_king:
            for square in line:
                if square in legal_moves:
                    legal_moves.remove(square)
                if square in legal_captures:
                    legal_captures.remove(square)
            
    if king_is_in_check[board[tile].occupying_piece.team] == True: ##DO THIS before king
        is_involved_in_cannon = False
        if len(cannon_targeting_king)> 0:
            for line in cannon_targeting_king:
                if tile in line:
                    is_involved_in_cannon = True
                    legal_moves = list(set(line).intersection(legal_moves))
                    legal_captures = list(set(line).intersection(legal_captures))
                if line[-1] in legal_captures:
                    is_involved_in_cannon = True
                    legal_moves = []
                    legal_captures = line[-1]
        if is_involved_in_cannon == False:
            legal_moves = []
            legal_captures =[]
            
        if len(global_trample_before_king)+ len(cannon_targeting_king) > 1:
            legal_moves = []
            legal_captures = []
        elif len(global_trample_before_king) != 0:
            if len(legal_moves)!= 0 :
                for space in legal_moves:
                    if space not in global_trample_before_king[0]:
                        legal_moves.remove(space)
                for space in legal_moves: ##just do it twice
                    if space not in global_trample_before_king[0]:
                        legal_moves.remove(space)
                for space in legal_moves: ##just do it twice
                    if space not in global_trample_before_king[0]:
                        legal_moves.remove(space)
            if len(legal_captures)!= 0 :
                for space in legal_captures:
                    if space not in global_trample_before_king[0]:
                        legal_captures.remove(space)


def bishop_trample(tile):
    global global_trample_spaces
    if board[tile].occupying_piece.team != globalturn:
        global global_trample_over_king
        global global_trample_before_king
    diag_up_lefttile = move_diag_up_left(tile)
    diag_up_righttile = move_diag_up_right(tile)
    diag_down_lefttile = move_diag_down_left(tile)
    diag_down_righttile = move_diag_down_right(tile)
    trample_spaces = []
    trample_over_king = []
    trample_spaces.append(tile)
    while diag_up_lefttile != "0" and board[diag_up_lefttile].occupying_piece == "none":
        trample_spaces.append(diag_up_lefttile)
        diag_up_lefttile = move_diag_up_left(diag_up_lefttile)
    if diag_up_lefttile != "0" and board[diag_up_lefttile].occupying_piece != "none" and board[diag_up_lefttile].occupying_piece.team != board[tile].occupying_piece.team:
        trample_spaces.append(diag_up_lefttile)
        if diag_up_lefttile == king_space[globalturn]:
            if trample_spaces not in global_trample_before_king:
                temp =  copy.deepcopy(trample_spaces) ####python works like this
                global_trample_before_king.append(temp)
            trample_over_king = trample_spaces
            while diag_up_lefttile != "0" and board[diag_up_lefttile].occupying_piece == "none":
                trample_over_king.append(diag_up_lefttile)
                diag_up_lefttile = move_diag_up_left(diag_up_lefttile)
            if trample_over_king not in global_trample_over_king:
                global_trample_over_king.append(trample_over_king)
        diag_up_lefttile = move_diag_up_left(diag_up_lefttile)
        while diag_up_lefttile != "0" and board[diag_up_lefttile].occupying_piece == "none":
            trample_spaces.append(diag_up_lefttile)
            diag_up_lefttile = move_diag_up_left(diag_up_lefttile)
        if diag_up_lefttile != "0" and diag_up_lefttile == king_space[globalturn]:
            if trample_spaces not in global_trample_spaces:
                global_trample_spaces.append(trample_spaces)
    trample_spaces = []
    while diag_up_righttile != "0" and board[diag_up_righttile].occupying_piece == "none":
        trample_spaces.append(diag_up_righttile)
        diag_up_righttile = move_diag_up_right(diag_up_righttile)
    if diag_up_righttile != "0" and board[diag_up_righttile].occupying_piece != "none" and board[diag_up_righttile].occupying_piece.team != board[tile].occupying_piece.team:
        trample_spaces.append(diag_up_righttile)
        if diag_up_righttile == king_space[globalturn]:
            if trample_spaces not in global_trample_before_king:
                temp =  copy.deepcopy(trample_spaces) ####python works like this
                global_trample_before_king.append(temp)
            trample_over_king = trample_spaces
            while diag_up_righttile != "0" and board[diag_up_righttile].occupying_piece == "none":
                trample_over_king.append(diag_up_righttile)
                diag_up_righttile = move_diag_up_right(diag_up_righttile)
            if trample_over_king not in global_trample_over_king:
                global_trample_over_king.append(trample_over_king)
        diag_up_righttile = move_diag_up_right(diag_up_righttile)
        while diag_up_righttile != "0" and board[diag_up_righttile].occupying_piece == "none":
            trample_spaces.append(diag_up_righttile)
            diag_up_righttile = move_diag_up_right(diag_up_righttile)
        if diag_up_righttile != "0" and diag_up_righttile == king_space[globalturn]:
            if trample_spaces not in global_trample_spaces:
                global_trample_spaces.append(trample_spaces)
    trample_spaces = []
    while diag_down_lefttile != "0" and board[diag_down_lefttile].occupying_piece == "none":
        trample_spaces.append(diag_down_lefttile)
        diag_down_lefttile = move_diag_down_left(diag_down_lefttile)
    if diag_down_lefttile != "0" and board[diag_down_lefttile].occupying_piece != "none" and board[diag_down_lefttile].occupying_piece.team != board[tile].occupying_piece.team:
        trample_spaces.append(diag_down_lefttile)
        if diag_down_lefttile == king_space[globalturn]:
            if trample_spaces not in global_trample_before_king:
                temp =  copy.deepcopy(trample_spaces) ####python works like this
                global_trample_before_king.append(temp)
            trample_over_king = trample_spaces
            while diag_down_lefttile != "0" and board[diag_down_lefttile].occupying_piece == "none":
                trample_over_king.append(diag_down_lefttile)
                diag_down_lefttile = move_diag_down_left(diag_down_lefttile)
            if trample_over_king not in global_trample_over_king:
                global_trample_over_king.append(trample_over_king)
        diag_down_lefttile = move_diag_down_left(diag_down_lefttile)
        while diag_down_lefttile != "0" and board[diag_down_lefttile].occupying_piece == "none":
            trample_spaces.append(diag_down_lefttile)
            diag_down_lefttile = move_diag_down_left(diag_down_lefttile)
        if diag_down_lefttile != "0" and diag_down_lefttile == king_space[globalturn]:
            if trample_spaces not in global_trample_spaces:
                global_trample_spaces.append(trample_spaces)
    trample_spaces = []
    while diag_down_righttile != "0" and board[diag_down_righttile].occupying_piece == "none":
        trample_spaces.append(diag_down_righttile)
        diag_down_righttile = move_diag_down_right(diag_down_righttile)
    if diag_down_righttile != "0" and board[diag_down_righttile].occupying_piece != "none" and board[diag_down_righttile].occupying_piece.team != board[tile].occupying_piece.team:
        trample_spaces.append(diag_down_righttile)
        if diag_down_righttile == king_space[globalturn]:
            if trample_spaces not in global_trample_before_king:
                temp =  copy.deepcopy(trample_spaces) ####python works like this
                global_trample_before_king.append(temp)
            trample_over_king = trample_spaces
            while diag_down_righttile != "0" and board[diag_down_righttile].occupying_piece == "none":
                trample_over_king.append(diag_down_righttile)
                diag_down_righttile = move_diag_down_right(diag_down_righttile)
            if trample_over_king not in global_trample_over_king:
                global_trample_over_king.append(trample_over_king)
        diag_down_righttile = move_diag_down_right(diag_down_righttile)
        while diag_down_righttile != "0" and board[diag_down_righttile].occupying_piece == "none":
            trample_spaces.append(diag_down_righttile)
            diag_down_righttile = move_diag_down_right(diag_down_righttile)
        if diag_down_righttile != "0" and diag_down_righttile == king_space[globalturn]:
            if trample_spaces not in global_trample_spaces:
                global_trample_spaces.append(trample_spaces)
    trample_spaces = []

def knight_move(tile,unicorn = False):
    global legal_moves
    global legal_captures
    global global_trample_before_king
    targets = []
    error_flag = False
    try:
        targets.append(move_left(move_up(move_up(tile))))
        this_tile = move_left(move_up(move_up(tile)))
        while unicorn == True and error_flag == False and this_tile != '0' and board[this_tile].occupying_piece == 'none':
            try:
                targets.append(move_left(move_up(move_up(this_tile))))
                this_tile = move_left(move_up(move_up(this_tile)))
            except KeyError:
                error_flag = True
    except KeyError:
        pass
    error_flag = False
    try:
        targets.append(move_right(move_up(move_up(tile))))
        this_tile = move_right(move_up(move_up(tile)))
        while unicorn == True and error_flag == False and this_tile != '0' and board[this_tile].occupying_piece == 'none':
            try:
                targets.append(move_right(move_up(move_up(this_tile))))
                this_tile = move_right(move_up(move_up(this_tile)))
            except KeyError:
                error_flag = True
    except KeyError:
        pass
    error_flag = False
    try:
        targets.append(move_up(move_right(move_right(tile))))
        this_tile = move_up(move_right(move_right(tile)))
        while unicorn == True and error_flag == False and this_tile != '0' and board[this_tile].occupying_piece == 'none':
            try:
                targets.append(move_up(move_right(move_right(this_tile))))
                this_tile = move_up(move_right(move_right(this_tile)))
            except KeyError:
                error_flag = True
    except KeyError:
        pass
    error_flag = False
    try:
        targets.append(move_down(move_right(move_right(tile))))
        this_tile = move_down(move_right(move_right(tile)))
        while unicorn == True and error_flag == False and this_tile != '0' and board[this_tile].occupying_piece == 'none':
            try:
                targets.append(move_down(move_right(move_right(this_tile))))
                this_tile = move_down(move_right(move_right(this_tile)))
            except KeyError:
                error_flag = True
    except KeyError:
        pass
    error_flag = False
    try:
        targets.append(move_left(move_down(move_down(tile))))
        this_tile = move_left(move_down(move_down(tile)))
        while unicorn == True and error_flag == False and this_tile != '0' and board[this_tile].occupying_piece == 'none':
            try:
                targets.append(move_left(move_down(move_down(this_tile))))
                this_tile = move_left(move_down(move_down(this_tile)))
            except KeyError:
                error_flag = True
    except KeyError:
        pass
    error_flag = False
    try:
        targets.append(move_right(move_down(move_down(tile))))
        this_tile = move_right(move_down(move_down(tile)))
        while unicorn == True and error_flag == False and this_tile != '0' and board[this_tile].occupying_piece == 'none':
            try:
                targets.append(move_right(move_down(move_down(this_tile))))
                this_tile = move_right(move_down(move_down(this_tile)))
            except KeyError:
                error_flag = True
    except KeyError:
        pass
    error_flag = False
    try:
        targets.append(move_up(move_left(move_left(tile))))
        this_tile = move_up(move_left(move_left(tile)))
        while unicorn == True and error_flag == False and this_tile != '0' and board[this_tile].occupying_piece == 'none':
            try:
                targets.append(move_up(move_left(move_left(this_tile))))
                this_tile = move_up(move_left(move_left(this_tile)))
            except KeyError:
                error_flag = True
    except KeyError:
        pass
    error_flag = False
    try:
        targets.append(move_down(move_left(move_left(tile))))
        this_tile = move_down(move_left(move_left(tile)))
        while unicorn == True and error_flag == False and this_tile != '0' and board[this_tile].occupying_piece == 'none':
            try:
                targets.append(move_down(move_left(move_left(this_tile))))
                this_tile = move_down(move_left(move_left(this_tile)))
            except KeyError:
                error_flag = True
    except KeyError:
        pass
    for stuff in targets:
        if stuff != '0':
            if board[stuff].occupying_piece != "none" and board[stuff].occupying_piece.team != board[tile].occupying_piece.team:
                if stuff not in legal_captures:
                    legal_captures.append(stuff)
                if board[stuff].occupying_piece.name == "king":
                    if tile not in global_trample_before_king:
                        global_trample_before_king.append(tile)
            elif board[stuff].occupying_piece == "none":
                if stuff not in legal_moves:
                    legal_moves.append(stuff)
            elif board[stuff].occupying_piece != "none" and board[stuff].occupying_piece == board[tile].occupying_piece.team:
                pass
            
            
    for line in global_trample_spaces:
        if tile in line:
            legal_moves = list(set(line).intersection(legal_moves))
            legal_captures = list(set(line).intersection(legal_captures))
            
    if len(cannon_path_to_king) != 0:
        for line in cannon_path_to_king:
            for square in line:
                if square in legal_moves:
                    legal_moves.remove(square)
                if square in legal_captures:
                    legal_captures.remove(square)
            
    if king_is_in_check[board[tile].occupying_piece.team] == True: ##DO THIS before king
        is_involved_in_cannon = False
        if len(cannon_targeting_king)> 0:
            for line in cannon_targeting_king:
                if tile in line:
                    is_involved_in_cannon = True
                    legal_moves = list(set(line).intersection(legal_moves))
                    legal_captures = list(set(line).intersection(legal_captures))
                if line[-1] in legal_captures:
                    is_involved_in_cannon = True
                    legal_moves = []
                    legal_captures = line[-1]
        if is_involved_in_cannon == False:
            legal_moves = []
            legal_captures =[]
            
        if len(global_trample_before_king)+ len(cannon_targeting_king) > 1:
            legal_moves = []
            legal_captures = []
        elif len(global_trample_before_king) != 0:
            if len(legal_moves)!= 0 :
                for space in legal_moves:
                    if space not in global_trample_before_king[0]:
                        legal_moves.remove(space)
                for space in legal_moves: ##just do it twice
                    if space not in global_trample_before_king[0]:
                        legal_moves.remove(space)
                for space in legal_moves: ##just do it twice
                    if space not in global_trample_before_king[0]:
                        legal_moves.remove(space)
            if len(legal_captures)!= 0 :
                for space in legal_captures:
                    if space not in global_trample_before_king[0]:
                        legal_captures.remove(space)



def rook_move(tile):
    global legal_moves
    global legal_captures
    lefttile = move_left(tile)
    righttile = move_right(tile)
    uptile = move_up(tile)
    downtile = move_down(tile)
    while lefttile != "0" and board[lefttile].occupying_piece == "none":
        legal_moves.append(lefttile)
        lefttile = move_left(lefttile)
    if lefttile != "0" and board[lefttile].occupying_piece != "none" and board[lefttile].occupying_piece.team != board[tile].occupying_piece.team:
        legal_captures.append(lefttile)
        lefttile = move_left(lefttile)                                   
    while righttile != "0" and board[righttile].occupying_piece == "none":
        legal_moves.append(righttile)
        righttile = move_right(righttile)
    while uptile != "0" and board[uptile].occupying_piece == "none":
        legal_moves.append(uptile)
        uptile = move_up(uptile)
    while downtile != "0" and board[downtile].occupying_piece == "none":
        legal_moves.append(downtile)
        downtile = move_down(downtile)
    if righttile != "0" and board[righttile].occupying_piece != "none" and board[righttile].occupying_piece.team != board[tile].occupying_piece.team:
        legal_captures.append(righttile)
    if uptile != "0" and board[uptile].occupying_piece != "none" and board[uptile].occupying_piece.team != board[tile].occupying_piece.team:
        legal_captures.append(uptile)
    if downtile != "0" and board[downtile].occupying_piece != "none" and board[downtile].occupying_piece.team != board[tile].occupying_piece.team:
        legal_captures.append(downtile)
        
            
    for line in global_trample_spaces:
        if tile in line:
            legal_moves = list(set(line).intersection(legal_moves))
            legal_captures = list(set(line).intersection(legal_captures))
            
    if len(cannon_path_to_king) != 0:
        for line in cannon_path_to_king:
            for square in line:
                if square in legal_moves:
                    legal_moves.remove(square)
                if square in legal_captures:
                    legal_captures.remove(square)
            
    if king_is_in_check[board[tile].occupying_piece.team] == True: ##DO THIS before king
        is_involved_in_cannon = False
        if len(cannon_targeting_king)> 0:
            for line in cannon_targeting_king:
                if tile in line:
                    is_involved_in_cannon = True
                    legal_moves = list(set(line).intersection(legal_moves))
                    legal_captures = list(set(line).intersection(legal_captures))
                if line[-1] in legal_captures:
                    is_involved_in_cannon = True
                    legal_moves = []
                    legal_captures = line[-1]
        if is_involved_in_cannon == False:
            legal_moves = []
            legal_captures =[]
            
        if len(global_trample_before_king)+ len(cannon_targeting_king) > 1:
            legal_moves = []
            legal_captures = []
        elif len(global_trample_before_king) != 0:
            if len(legal_moves)!= 0 :
                for space in legal_moves:
                    if space not in global_trample_before_king[0]:
                        legal_moves.remove(space)
                for space in legal_moves: ##just do it twice
                    if space not in global_trample_before_king[0]:
                        legal_moves.remove(space)
                for space in legal_moves: ##just do it twice
                    if space not in global_trample_before_king[0]:
                        legal_moves.remove(space)
            if len(legal_captures)!= 0 :
                for space in legal_captures:
                    if space not in global_trample_before_king[0]:
                        legal_captures.remove(space)

                        
def rook_trample(tile):
    global global_trample_spaces
    if board[tile].occupying_piece.team != globalturn:
        global global_trample_over_king
        global global_trample_before_king
    lefttile = move_left(tile)
    righttile = move_right(tile)
    uptile = move_up(tile)
    downtile = move_down(tile)
    trample_spaces = []
    trample_over_king = []
    trample_spaces.append(tile)
    while lefttile != "0" and board[lefttile].occupying_piece == "none":
        trample_spaces.append(lefttile)
        lefttile = move_left(lefttile)
    if lefttile != "0" and board[lefttile].occupying_piece != "none" and board[lefttile].occupying_piece.team != board[tile].occupying_piece.team:
        trample_spaces.append(lefttile)
        if lefttile == king_space[globalturn]:
            if trample_spaces not in global_trample_before_king:
                temp =  copy.deepcopy(trample_spaces) ####python works like this
                global_trample_before_king.append(temp)
            trample_over_king = trample_spaces
            while lefttile != "0" and board[lefttile].occupying_piece == "none":
                trample_over_king.append(lefttile)
                lefttile = move_left(lefttile)
            if trample_over_king not in global_trample_over_king:
                global_trample_over_king.append(trample_over_king)
        lefttile = move_left(lefttile)
        while lefttile != "0" and board[lefttile].occupying_piece == "none":
            trample_spaces.append(lefttile)
            lefttile = move_left(lefttile)
        if lefttile != "0" and lefttile == king_space[globalturn]:
            if trample_spaces not in global_trample_spaces:
                global_trample_spaces.append(trample_spaces)
    trample_spaces = []
    while righttile != "0" and board[righttile].occupying_piece == "none":
        trample_spaces.append(righttile)
        righttile = move_right(righttile)
    if righttile != "0" and board[righttile].occupying_piece != "none" and board[righttile].occupying_piece.team != board[tile].occupying_piece.team:
        trample_spaces.append(righttile)
        if righttile == king_space[globalturn]:
            if trample_spaces not in global_trample_before_king:
                temp =  copy.deepcopy(trample_spaces) ####python works like this
                global_trample_before_king.append(temp)
            trample_over_king = trample_spaces
            while righttile != "0" and board[righttile].occupying_piece == "none":
                trample_over_king.append(righttile)
                righttile = move_right(righttile)
            if trample_over_king not in global_trample_over_king:
                global_trample_over_king.append(trample_over_king)
        righttile = move_right(righttile)
        while righttile != "0" and board[righttile].occupying_piece == "none":
            trample_spaces.append(righttile)
            righttile = move_right(righttile)
        if righttile != "0" and righttile == king_space[globalturn]:
            if trample_spaces not in global_trample_spaces:
                global_trample_spaces.append(trample_spaces)
    trample_spaces = []
    while uptile != "0" and board[uptile].occupying_piece == "none":
        trample_spaces.append(uptile)
        uptile = move_up(uptile)
    if uptile != "0" and board[uptile].occupying_piece != "none" and board[uptile].occupying_piece.team != board[tile].occupying_piece.team:
        trample_spaces.append(uptile)
        if uptile == king_space[globalturn]:
            if trample_spaces not in global_trample_before_king:
                temp =  copy.deepcopy(trample_spaces) ####python works like this
                global_trample_before_king.append(temp)
            trample_over_king = trample_spaces
            while uptile != "0" and board[uptile].occupying_piece == "none":
                trample_over_king.append(uptile)
                uptile = move_up(uptile)
            if trample_over_king not in global_trample_over_king:
                global_trample_over_king.append(trample_over_king)
        uptile = move_up(uptile)
        while uptile != "0" and board[uptile].occupying_piece == "none":
            trample_spaces.append(uptile)
            uptile = move_up(uptile)
        if uptile != "0" and uptile == king_space[globalturn]:
            if trample_spaces not in global_trample_spaces:
                global_trample_spaces.append(trample_spaces)
    trample_spaces = []
    while downtile != "0" and board[downtile].occupying_piece == "none":
        trample_spaces.append(downtile)
        downtile = move_down(downtile)
    if downtile != "0" and board[downtile].occupying_piece != "none" and board[downtile].occupying_piece.team != board[tile].occupying_piece.team:
        trample_spaces.append(downtile)
        if downtile == king_space[globalturn]:
            if trample_spaces not in global_trample_before_king:
                temp =  copy.deepcopy(trample_spaces) ####python works like this
                global_trample_before_king.append(temp)
            trample_over_king = trample_spaces
            while downtile != "0" and board[downtile].occupying_piece == "none":
                trample_over_king.append(downtile)
                downtile = move_down(downtile)
            if trample_over_king not in global_trample_over_king:
                global_trample_over_king.append(trample_over_king)
        downtile = move_down(downtile)
        while downtile != "0" and board[downtile].occupying_piece == "none":
            trample_spaces.append(downtile)
            downtile = move_down(downtile)
        if downtile != "0" and downtile == king_space[globalturn]:
            if trample_spaces not in global_trample_spaces:
                global_trample_spaces.append(trample_spaces)
    trample_spaces = [] 

def king_move(tile):
    global legal_moves
    global legal_captures
    global castle_left
    global castle_right
    illegal_spaces = check_for_check(globalturn)
    lefttile = move_left(tile)
    righttile = move_right(tile)
    uptile = move_up(tile)
    downtile = move_down(tile)
    diag_up_lefttile = move_diag_up_left(tile)
    diag_up_righttile = move_diag_up_right(tile)
    diag_down_lefttile = move_diag_down_left(tile)
    diag_down_righttile = move_diag_down_right(tile)
    if lefttile != "0" and board[lefttile].occupying_piece != "none" and board[lefttile].occupying_piece.team != board[tile].occupying_piece.team :
        legal_captures.append(lefttile)
    elif lefttile != "0" and board[lefttile].occupying_piece == "none":
        legal_moves.append(lefttile)
    if righttile != "0" and board[righttile].occupying_piece != "none" and board[righttile].occupying_piece.team != board[tile].occupying_piece.team :
        legal_captures.append(righttile)
    elif righttile != "0" and board[righttile].occupying_piece == "none":
        legal_moves.append(righttile)
    if uptile != "0" and board[uptile].occupying_piece != "none" and board[uptile].occupying_piece.team != board[tile].occupying_piece.team:
        legal_captures.append(uptile)
    elif uptile != "0" and board[uptile].occupying_piece == "none":
        legal_moves.append(uptile)
    if downtile != "0" and board[downtile].occupying_piece != "none" and board[downtile].occupying_piece.team != board[tile].occupying_piece.team:
        legal_captures.append(downtile)
    elif downtile != "0" and board[downtile].occupying_piece == "none":
        legal_moves.append(downtile)
    if diag_up_lefttile != "0" and board[diag_up_lefttile].occupying_piece != "none" and board[diag_up_lefttile].occupying_piece.team != board[tile].occupying_piece.team:
        legal_captures.append(diag_up_lefttile)
    elif diag_up_lefttile != "0" and board[diag_up_lefttile].occupying_piece == "none":
        legal_moves.append(diag_up_lefttile)
    if diag_up_righttile != "0" and board[diag_up_righttile].occupying_piece != "none" and board[diag_up_righttile].occupying_piece.team != board[tile].occupying_piece.team:
        legal_captures.append(diag_up_righttile)
    elif diag_up_righttile != "0" and board[diag_up_righttile].occupying_piece == "none":
        legal_moves.append(diag_up_righttile)
    if diag_down_lefttile != "0" and board[diag_down_lefttile].occupying_piece != "none" and board[diag_down_lefttile].occupying_piece.team != board[tile].occupying_piece.team:
        legal_captures.append(diag_down_lefttile)
    elif diag_down_lefttile != "0" and board[diag_down_lefttile].occupying_piece == "none":
        legal_moves.append(diag_down_lefttile)
    if diag_down_righttile != "0" and board[diag_down_righttile].occupying_piece != "none" and board[diag_down_righttile].occupying_piece.team != board[tile].occupying_piece.team:
        legal_captures.append(diag_down_righttile)
    elif diag_down_righttile != "0" and board[diag_down_righttile].occupying_piece == "none":
        legal_moves.append(diag_down_righttile)


    if king_is_in_check[globalturn] == False and board[tile].occupying_piece.hasMoved == False:
        castle_lefttile = move_left(tile)
        castle_righttile = move_right(tile)
        left_castle = []
        right_castle = []
        while castle_lefttile != "0" and board[castle_lefttile].occupying_piece == "none" and castle_lefttile not in illegal_spaces:
            castle_lefttile = move_left(castle_lefttile)
        ###LONG LINES BELOW
        if castle_lefttile != "0" and board[castle_lefttile].occupying_piece != "none" and board[castle_lefttile].occupying_piece.name == "rook" and board[castle_lefttile].occupying_piece.team == board[tile].occupying_piece.team and board[castle_lefttile].occupying_piece.hasMoved == False:
            castle_left = [castle_lefttile,move_left(move_left(tile)),"left",tile]
        while castle_righttile != "0" and board[castle_righttile].occupying_piece == "none" and castle_righttile not in illegal_spaces:
            castle_righttile = move_right(castle_righttile)
        if castle_righttile != "0" and board[castle_righttile].occupying_piece != "none" and board[castle_righttile].occupying_piece.name == "rook" and board[castle_righttile].occupying_piece.team == board[tile].occupying_piece.team and board[castle_righttile].occupying_piece.hasMoved == False:
            castle_right = [castle_righttile,move_right(move_right(tile)),"right",tile]
            
    if king_is_in_check[globalturn] == True and len(cannon_targeting_king)>0:
        for line in cannon_targeting_king:
            for space in line:
                if space in legal_moves:
                    legal_moves.remove(space)
                     
    for space in illegal_spaces:
        try:
            legal_moves.remove(space)
        except ValueError:
            pass
        try:
            legal_captures.remove(space)
        except ValueError:
            pass
    for space in global_trample_over_king:
        for i in range(1,len(space)): ####the first space is the piece itself
            try:
                legal_moves.remove(space[i])
            except ValueError:
                pass
            try:
                legal_captures.remove(space[i])
            except ValueError:
                pass

def mann_move(tile):
    global legal_moves
    global legal_captures
    lefttile = move_left(tile)
    righttile = move_right(tile)
    uptile = move_up(tile)
    downtile = move_down(tile)
    diag_up_lefttile = move_diag_up_left(tile)
    diag_up_righttile = move_diag_up_right(tile)
    diag_down_lefttile = move_diag_down_left(tile)
    diag_down_righttile = move_diag_down_right(tile)
    if lefttile != "0" and board[lefttile].occupying_piece != "none" and board[lefttile].occupying_piece.team != board[tile].occupying_piece.team :
        legal_captures.append(lefttile)
    elif lefttile != "0" and board[lefttile].occupying_piece == "none":
        legal_moves.append(lefttile)
    if righttile != "0" and board[righttile].occupying_piece != "none" and board[righttile].occupying_piece.team != board[tile].occupying_piece.team :
        legal_captures.append(righttile)
    elif righttile != "0" and board[righttile].occupying_piece == "none":
        legal_moves.append(righttile)
    if uptile != "0" and board[uptile].occupying_piece != "none" and board[uptile].occupying_piece.team != board[tile].occupying_piece.team:
        legal_captures.append(uptile)
    elif uptile != "0" and board[uptile].occupying_piece == "none":
        legal_moves.append(uptile)
    if downtile != "0" and board[downtile].occupying_piece != "none" and board[downtile].occupying_piece.team != board[tile].occupying_piece.team:
        legal_captures.append(downtile)
    elif downtile != "0" and board[downtile].occupying_piece == "none":
        legal_moves.append(downtile)
    if diag_up_lefttile != "0" and board[diag_up_lefttile].occupying_piece != "none" and board[diag_up_lefttile].occupying_piece.team != board[tile].occupying_piece.team:
        legal_captures.append(diag_up_lefttile)
    elif diag_up_lefttile != "0" and board[diag_up_lefttile].occupying_piece == "none":
        legal_moves.append(diag_up_lefttile)
    if diag_up_righttile != "0" and board[diag_up_righttile].occupying_piece != "none" and board[diag_up_righttile].occupying_piece.team != board[tile].occupying_piece.team:
        legal_captures.append(diag_up_righttile)
    elif diag_up_righttile != "0" and board[diag_up_righttile].occupying_piece == "none":
        legal_moves.append(diag_up_righttile)
    if diag_down_lefttile != "0" and board[diag_down_lefttile].occupying_piece != "none" and board[diag_down_lefttile].occupying_piece.team != board[tile].occupying_piece.team:
        legal_captures.append(diag_down_lefttile)
    elif diag_down_lefttile != "0" and board[diag_down_lefttile].occupying_piece == "none":
        legal_moves.append(diag_down_lefttile)
    if diag_down_righttile != "0" and board[diag_down_righttile].occupying_piece != "none" and board[diag_down_righttile].occupying_piece.team != board[tile].occupying_piece.team:
        legal_captures.append(diag_down_righttile)
    elif diag_down_righttile != "0" and board[diag_down_righttile].occupying_piece == "none":
        legal_moves.append(diag_down_righttile)

            
    for line in global_trample_spaces:
        if tile in line:
            legal_moves = list(set(line).intersection(legal_moves))
            legal_captures = list(set(line).intersection(legal_captures))
            
    if len(cannon_path_to_king) != 0:
        for line in cannon_path_to_king:
            for square in line:
                if square in legal_moves:
                    legal_moves.remove(square)
                if square in legal_captures:
                    legal_captures.remove(square)
            
    if king_is_in_check[board[tile].occupying_piece.team] == True: ##DO THIS before king
        is_involved_in_cannon = False
        if len(cannon_targeting_king)> 0:
            for line in cannon_targeting_king:
                if tile in line:
                    is_involved_in_cannon = True
                    legal_moves = list(set(line).intersection(legal_moves))
                    legal_captures = list(set(line).intersection(legal_captures))
                if line[-1] in legal_captures:
                    is_involved_in_cannon = True
                    legal_moves = []
                    legal_captures = line[-1]
        if is_involved_in_cannon == False:
            legal_moves = []
            legal_captures =[]
            
        if len(global_trample_before_king)+ len(cannon_targeting_king) > 1:
            legal_moves = []
            legal_captures = []
        elif len(global_trample_before_king) != 0:
            if len(legal_moves)!= 0 :
                for space in legal_moves:
                    if space not in global_trample_before_king[0]:
                        legal_moves.remove(space)
                for space in legal_moves: ##just do it twice
                    if space not in global_trample_before_king[0]:
                        legal_moves.remove(space)
                for space in legal_moves: ##just do it twice
                    if space not in global_trample_before_king[0]:
                        legal_moves.remove(space)
            if len(legal_captures)!= 0 :
                for space in legal_captures:
                    if space not in global_trample_before_king[0]:
                        legal_captures.remove(space)

                        

def cannon_move(tile):
    global legal_moves
    global legal_captures
    lefttile = move_left(tile)
    righttile = move_right(tile)
    uptile = move_up(tile)
    downtile = move_down(tile)
    while lefttile != "0" and board[lefttile].occupying_piece == "none":
        legal_moves.append(lefttile)
        lefttile = move_left(lefttile)
    if lefttile != "0" and board[lefttile].occupying_piece != "none":
        lefttile = move_left(lefttile)
        while lefttile != "0" and board[lefttile].occupying_piece == "none":        
            lefttile = move_left(lefttile)
        if lefttile != "0" and board[lefttile].occupying_piece != "none" and board[lefttile].occupying_piece.team != board[tile].occupying_piece.team:
            legal_captures.append(lefttile)
    while righttile != "0" and board[righttile].occupying_piece == "none":
        legal_moves.append(righttile)
        righttile = move_right(righttile)
    if righttile != "0" and board[righttile].occupying_piece != "none":
        righttile = move_right(righttile)
        while righttile != "0" and board[righttile].occupying_piece == "none":        
            righttile = move_right(righttile)
        if righttile != "0" and board[righttile].occupying_piece != "none" and board[righttile].occupying_piece.team != board[tile].occupying_piece.team:
            legal_captures.append(righttile)
    while uptile != "0" and board[uptile].occupying_piece == "none":
        legal_moves.append(uptile)
        uptile = move_up(uptile)
    if uptile != "0" and board[uptile].occupying_piece != "none":
        uptile = move_up(uptile)
        while uptile != "0" and board[uptile].occupying_piece == "none":        
            uptile = move_up(uptile)
        if uptile != "0" and board[uptile].occupying_piece != "none" and board[uptile].occupying_piece.team != board[tile].occupying_piece.team:
            legal_captures.append(uptile)
    while downtile != "0" and board[downtile].occupying_piece == "none":
        legal_moves.append(downtile)
        downtile = move_down(downtile)
    if downtile != "0" and board[downtile].occupying_piece != "none":
        downtile = move_down(downtile)
        while downtile != "0" and board[downtile].occupying_piece == "none":        
            downtile = move_down(downtile)
        if downtile != "0" and board[downtile].occupying_piece != "none" and board[downtile].occupying_piece.team != board[tile].occupying_piece.team:
            legal_captures.append(downtile)
            
    for line in global_trample_spaces:
        if tile in line:
            legal_moves = list(set(line).intersection(legal_moves))
            legal_captures = list(set(line).intersection(legal_captures))
            
    if len(cannon_path_to_king) != 0:
        for line in cannon_path_to_king:
            for square in line:
                if square in legal_moves:
                    legal_moves.remove(square)
                if square in legal_captures:
                    legal_captures.remove(square)
            
    if king_is_in_check[board[tile].occupying_piece.team] == True: ##DO THIS before king
        is_involved_in_cannon = False
        if len(cannon_targeting_king)> 0:
            for line in cannon_targeting_king:
                if tile in line:
                    is_involved_in_cannon = True
                    legal_moves = list(set(line).intersection(legal_moves))
                    legal_captures = list(set(line).intersection(legal_captures))
                if line[-1] in legal_captures:
                    is_involved_in_cannon = True
                    legal_moves = []
                    legal_captures = line[-1]
        if is_involved_in_cannon == False:
            legal_moves = []
            legal_captures =[]
            
        if len(global_trample_before_king)+ len(cannon_targeting_king) > 1:
            legal_moves = []
            legal_captures = []
        elif len(global_trample_before_king) != 0:
            if len(legal_moves)!= 0 :
                for space in legal_moves:
                    if space not in global_trample_before_king[0]:
                        legal_moves.remove(space)
                for space in legal_moves: ##just do it twice
                    if space not in global_trample_before_king[0]:
                        legal_moves.remove(space)
                for space in legal_moves: ##just do it twice
                    if space not in global_trample_before_king[0]:
                        legal_moves.remove(space)
            if len(legal_captures)!= 0 :
                for space in legal_captures:
                    if space not in global_trample_before_king[0]:
                        legal_captures.remove(space)

                        
def cannon_trample(tile):
    global cannon_path_to_king
    global cannon_targeting_king
    lefttile = move_left(tile)
    righttile = move_right(tile)
    uptile = move_up(tile)
    downtile = move_down(tile)
    
    path_to_king = []
    if lefttile != '0':
        path_to_king.append(lefttile)
    while lefttile != "0" and board[lefttile].occupying_piece == "none":
        lefttile = move_left(lefttile)
        path_to_king.append(lefttile)
    if lefttile != "0" and board[lefttile].occupying_piece.name == "king" and board[lefttile].occupying_piece.team != board[tile].occupying_piece.team:
        temp =  copy.deepcopy(path_to_king) ##python is liddat
        if temp not in cannon_path_to_king:
            cannon_path_to_king.append(temp)
    else:
        if lefttile != "0" and board[lefttile].occupying_piece != "none":
            lefttile = move_left(lefttile)
            path_to_king.append(lefttile)
        while lefttile != "0" and board[lefttile].occupying_piece != "none":
            lefttile = move_left(lefttile)
            path_to_king.append(lefttile)
        if lefttile != "0" and board[lefttile].occupying_piece.name == "king" and board[lefttile].occupying_piece.team != board[tile].occupying_piece.team:
            path_to_king.append(tile)
            temp =  copy.deepcopy(path_to_king) ##python is liddat
            if temp not in cannon_targeting_king:
                cannon_targeting_king.append(temp)
                
    path_to_king = []
    if righttile != '0':
        path_to_king.append(righttile)    
    while righttile != "0" and board[righttile].occupying_piece == "none":
        righttile = move_right(righttile)
        path_to_king.append(righttile)
    if righttile != "0" and board[righttile].occupying_piece.name == "king" and board[righttile].occupying_piece.team != board[tile].occupying_piece.team:
        temp =  copy.deepcopy(path_to_king) ##python is liddat
        if temp not in cannon_path_to_king:
            cannon_path_to_king.append(temp)
    else:
        if righttile != "0" and board[righttile].occupying_piece != "none":
            righttile = move_right(righttile)
            path_to_king.append(righttile)
        while righttile != "0" and board[righttile].occupying_piece == "none":
            righttile = move_left(righttile)
            path_to_king.append(righttile)
        if righttile != "0" and board[righttile].occupying_piece.name == "king" and board[righttile].occupying_piece.team != board[tile].occupying_piece.team:
            path_to_king.append(tile)
            temp =  copy.deepcopy(path_to_king) ##python is liddat
            if temp not in cannon_targeting_king:
                cannon_targeting_king.append(temp)
                
    path_to_king = []
    if uptile != '0':
        path_to_king.append(uptile)
    while uptile != "0" and board[uptile].occupying_piece == "none":
        uptile = move_up(uptile)
        path_to_king.append(uptile)
    if uptile != "0" and board[uptile].occupying_piece.name == "king" and board[uptile].occupying_piece.team != board[tile].occupying_piece.team:
        temp =  copy.deepcopy(path_to_king) ##python is liddat
        if temp not in cannon_path_to_king:
            cannon_path_to_king.append(temp)
    else:
        if uptile != "0" and board[uptile].occupying_piece != "none":
            uptile = move_up(uptile)
            path_to_king.append(uptile)
        while uptile != "0" and board[uptile].occupying_piece == "none":
            uptile = move_up(uptile)
            path_to_king.append(uptile)
        if uptile != "0" and board[uptile].occupying_piece.name == "king" and board[uptile].occupying_piece.team != board[tile].occupying_piece.team:
            path_to_king.append(tile)
            temp =  copy.deepcopy(path_to_king) ##python is liddat
            if temp not in cannon_targeting_king:
                cannon_targeting_king.append(temp)
                
    path_to_king = []
    if downtile != '0':
        path_to_king.append(downtile)   
    while downtile != "0" and board[downtile].occupying_piece == "none":
        downtile = move_down(downtile)
        path_to_king.append(uptile)
    if downtile != "0" and board[downtile].occupying_piece == "king" and board[downtile].occupying_piece.team != board[tile].occupying_piece.team:
        temp =  copy.deepcopy(path_to_king) ##python is liddat
        if temp not in cannon_path_to_king:
            cannon_path_to_king.append(temp)
    else:
        if downtile != "0" and board[downtile].occupying_piece != "none":
            downtile = move_down(downtile)
            path_to_king.append(downtile)
        while downtile != "0" and board[downtile].occupying_piece == "none":
            downtile = move_down(downtile)
            path_to_king.append(uptile)
        if downtile != "0" and board[downtile].occupying_piece == "king" and board[downtile].occupying_piece.team != board[tile].occupying_piece.team:
            path_to_king.append(tile)
            temp =  copy.deepcopy(path_to_king) ##python is liddat
            if temp not in cannon_targeting_king:
                cannon_targeting_king.append(temp)
    

                
#############END OF PIECE DEFINITIONS######################
        
def get_board():
    data = open("board.dat",'r')
    newline = data.readline()
    while len(newline) != 0:
        if newline[0] == '|':
            newline = newline.strip("\n")
            newline = newline.split("|")
            board[newline[1]] = square(newline)
        newline = data.readline()
    data.close()
    
##    board["f1"].occupying_piece = king("white")
##    board["e8"].occupying_piece = king("black")
##    board["a1"].occupying_piece = cannon("white")
##    board["a4"].occupying_piece = cannon("black")
##    board["e4"].occupying_piece = cannon("black")
##    board["e2"].occupying_piece = cannon("white")
##    board["a8"].occupying_piece = pawn("black")

    board["a1"].occupying_piece = cannon("white")
    board["b1"].occupying_piece = knight("white")
    board["c1"].occupying_piece = bishop("white")
    board["d1"].occupying_piece = queen("white")
    board["e1"].occupying_piece = king("white")
    board["f1"].occupying_piece = bishop("white")
    board["g1"].occupying_piece = unicorn("white")
    board["h1"].occupying_piece = rook("white")
    board["a2"].occupying_piece = pawn("white")
    board["b2"].occupying_piece = mann("white")
    board["c2"].occupying_piece = pawn("white")
    board["d2"].occupying_piece = pawn("white")
    board["e2"].occupying_piece = pawn("white")
    board["f2"].occupying_piece = pawn("white")
    board["g2"].occupying_piece = mann("white")
    board["h2"].occupying_piece = pawn("white")
    board["a8"].occupying_piece = cannon("black")
    board["b8"].occupying_piece = knight("black")
    board["c8"].occupying_piece = bishop("black")
    board["d8"].occupying_piece = queen("black")
    board["e8"].occupying_piece = king("black")
    board["f8"].occupying_piece = bishop("black")
    board["g8"].occupying_piece = unicorn("black")
    board["h8"].occupying_piece = rook("black")
    board["a7"].occupying_piece = pawn("black")
    board["b7"].occupying_piece = mann("black")
    board["c7"].occupying_piece = pawn("black")
    board["d7"].occupying_piece = pawn("black")
    board["e7"].occupying_piece = pawn("black")
    board["f7"].occupying_piece = pawn("black")
    board["g7"].occupying_piece = mann("black")
    board["h7"].occupying_piece = pawn("black")

def check_for_endgame(team):
    global legal_moves
    global legal_captures
    temp_legal_moves = legal_moves
    temp_legal_captures = legal_captures
    legal_moves = []
    legal_captures = []
    for piece in board:
        if board[piece].occupying_piece != "none" and board[piece].occupying_piece.team == team:
            if board[piece].occupying_piece.name == "pawn":
                pawn_move(piece)
            elif board[piece].occupying_piece.name == "bishop":
                bishop_move(piece)
            elif board[piece].occupying_piece.name == "knight":
                knight_move(piece)
            elif board[piece].occupying_piece.name == "rook":
                rook_move(piece)
            elif board[piece].occupying_piece.name == "queen":
                rook_move(piece)
                bishop_move(piece)
            elif board[piece].occupying_piece.name == "king":
                king_move(piece)
            elif board[piece].occupying_piece.name == "unicorn":
                knight_move(piece,True)
            elif board[piece].occupying_piece.name == "cannon":
                cannon_move(piece)
    current_legal_moves = legal_moves
    current_legal_captures = legal_captures
    legal_moves = temp_legal_moves
    legal_captures = temp_legal_captures
    if len(current_legal_moves) == 0 and len(current_legal_captures) == 0:
        print("================A team has had it!!!=================")
        if king_is_in_check[team] == True:
            print("Team", team,"has lost!!!!!")
        elif king_is_in_check[team] == False:
            print("It's a stalemate!!!!")
        

    

def check_for_check(team = "none"):
    global legal_moves
    global legal_captures
    global canvas
    global global_trample_spaces
    global king_space
    global king_is_in_check
    temp_legal_moves = legal_moves
    temp_legal_captures = legal_captures
    legal_moves = []
    legal_captures = []
    white_legal_moves = []
    white_legal_captures = []
    black_legal_moves = []
    black_legal_captures = []
    for piece in board:
        if team != "white":        
            if board[piece].occupying_piece != "none" and board[piece].occupying_piece.team == "white":
                if board[piece].occupying_piece.name == "pawn":
                    pawn_move(piece)
                elif board[piece].occupying_piece.name == "bishop":
                    bishop_move(piece)
                    bishop_trample(piece)
                elif board[piece].occupying_piece.name == "knight":
                    knight_move(piece)
                elif board[piece].occupying_piece.name == "rook":
                    rook_move(piece)
                    rook_trample(piece)
                elif board[piece].occupying_piece.name == "queen":
                    rook_move(piece)
                    bishop_move(piece)
                    bishop_trample(piece)
                    rook_trample(piece)
                elif board[piece].occupying_piece.name == "mann":
                    mann_move(piece)
                elif board[piece].occupying_piece.name == "unicorn":
                    knight_move(piece,True)
                elif board[piece].occupying_piece.name == "cannon":
                    cannon_move(piece)
                    cannon_trample(piece)
        if board[piece].occupying_piece != "none" and board[piece].occupying_piece.name == "king"  and board[piece].occupying_piece.team == "white":
            whitekingspace = piece
    white_legal_moves = legal_moves
    white_legal_captures = legal_captures
    legal_moves = []
    legal_captures = []
    for piece in board:
        if team != "black":
            if board[piece].occupying_piece != "none" and board[piece].occupying_piece.team == "black":
                if board[piece].occupying_piece.name == "pawn":
                    pawn_move(piece)
                elif board[piece].occupying_piece.name == "bishop":
                    bishop_move(piece)
                    bishop_trample(piece)
                elif board[piece].occupying_piece.name == "knight":
                    knight_move(piece)
                elif board[piece].occupying_piece.name == "rook":
                    rook_move(piece)
                    rook_trample(piece)
                elif board[piece].occupying_piece.name == "queen":
                    rook_move(piece)
                    bishop_move(piece)
                    bishop_trample(piece)
                    rook_trample(piece)
                elif board[piece].occupying_piece.name == "mann":
                    mann_move(piece)
                elif board[piece].occupying_piece.name == "unicorn":
                    knight_move(piece,True)
                elif board[piece].occupying_piece.name == "cannon":
                    cannon_move(piece)
                    cannon_trample(piece)
        if board[piece].occupying_piece != "none" and board[piece].occupying_piece.name == "king" and board[piece].occupying_piece.team == "black":
            blackkingspace = piece
    black_legal_moves = legal_moves
    black_legal_captures = legal_captures
    legal_moves = []
    legal_captures = []
    if blackkingspace in white_legal_captures:
        canvas.create_image(board[blackkingspace].x_coord,board[blackkingspace].y_coord,image = globalcheck, tag = "check")
        king_is_in_check["black"] = True
    if whitekingspace in black_legal_captures:
        canvas.create_image(board[whitekingspace].x_coord,board[whitekingspace].y_coord,image = globalcheck, tag = "check")
        king_is_in_check["white"] = True
    legal_moves = temp_legal_moves
    legal_captures = temp_legal_captures
    black_legal_actions = black_legal_moves + black_legal_captures
    white_legal_actions = white_legal_moves + black_legal_captures
    if team == "white":
        return(black_legal_actions)
    if team == "black":
        return(white_legal_actions)
    king_space["black"] = blackkingspace
    king_space["white"] = whitekingspace


def make_move(tile):
    global canvas
    global globalselect
    global icon_garbage
    global global_trample_spaces
    global global_trample_over_king
    global global_trample_before_king
    global king_is_in_check
    global cannon_path_to_king
    global cannon_targeting_king
    canvas.delete("dot")
    canvas.delete(tile)
    board[tile].occupying_piece = board[globalselect].occupying_piece
    board[tile].occupying_piece.hasMoved = True
    iconimage = PhotoImage(file = board[globalselect].occupying_piece.icon)
    icon_garbage.append(iconimage)
    canvas.create_image(board[tile].x_coord,board[tile].y_coord,image = icon_garbage[-1] ,tag = tile)
    board[globalselect].occupying_piece = "none"
    global_trample_spaces = []
    global_trample_over_king = []
    global_trample_before_king = []
    cannon_path_to_king = []
    cannon_targeting_king = []
    king_is_in_check[globalturn] = False
    canvas.delete(globalselect)
    canvas.delete("dot")

def location(event):
    global globalselect
    global select_piece
    global legal_moves
    global legal_captures
    global canvas
    global globalturn
    global castle_left
    global castle_right
    print("Cannon path to king:",cannon_path_to_king)
    print("Cannon target: ", cannon_targeting_king)
    print("It is "+ globalturn +"'s turn to move.")
    check_for_check(globalturn)
    canvas.delete("selection")
    canvas.delete("dot")
    just_moved_flag = False
    for i in range(0,8):
        if coord[i] < event.x:
            x = i
        if coord[i] < event.y:
            y = i
    tile_clicked = x_axis[x] + y_axis[y]
    canvas.create_image(board[tile_clicked].x_coord,board[tile_clicked].y_coord, image = selectbox, tag  = "selection")
    if tile_clicked in legal_moves or tile_clicked in legal_captures:
        print("That was a legal move")
        make_move(tile_clicked)
        just_moved_flag = True
        canvas.delete("check")
    else:
        print("Move cancelled")
    if len(castle_left) != 0:
        if tile_clicked == castle_left[1]:  
            print("That was a legal castle")
            move_castle(tile_clicked)
            just_moved_flag = True
            canvas.delete("check")
    if len(castle_right) != 0:
        if tile_clicked == castle_right[1]:
            print("That was a legal castle")
            move_castle(tile_clicked)
            just_moved_flag = True
            canvas.delete("check")
    globalselect = tile_clicked   
    legal_moves = []
    legal_captures = []
    castle_left = []
    castle_right = []
    if board[tile_clicked].occupying_piece == "none":
        print("Tile clicked:", tile_clicked, "It is empty.")
        select_piece = False
    else:
        print("Tile clicked:", tile_clicked, "There is a", board[tile_clicked].occupying_piece.name, "here")
        select_piece = True
        if just_moved_flag == False:
            if board[tile_clicked].occupying_piece.team == globalturn:
                board[tile_clicked].occupying_piece.move(tile_clicked)                
                if len(castle_left) != 0:
                        canvas.create_image(board[castle_left[1]].x_coord,board[castle_left[1]].y_coord, image = globalcastle, tag = "dot")
                if len(castle_right) != 0:
                        canvas.create_image(board[castle_right[1]].x_coord,board[castle_right[1]].y_coord, image = globalcastle, tag = "dot")        
    if just_moved_flag == True:
        if globalturn == "black":
            globalturn = "white"
        elif globalturn == "white":
            globalturn = "black"
    if board[tile_clicked].occupying_piece != "none" and board[tile_clicked].occupying_piece.canPromote == True:
        check_for_promotion(tile_clicked)
    check_for_check()
    check_for_endgame(globalturn)
    print("It is "+ globalturn +"'s turn to move.")
    for space in legal_moves:
        canvas.create_image(board[space].x_coord,board[space].y_coord, image = globaldot, tag = "dot")
    for space in legal_captures:
        canvas.create_image(board[space].x_coord,board[space].y_coord, image = globaltarget, tag = "dot")

       

def create_board(): ##CENTER OF A TILE FROM CORNER IS 46 PIXELS
    global globalicon
    global canvas
    boardimg = PhotoImage(file = 'boardnumbered.png')
    canvas.create_image(0,0,image = boardimg,anchor="nw")
    canvas.bind('<Button-1>',location)
    i = 1
    for space in board:
        if board[space].occupying_piece != "none":
            iconimage = PhotoImage(file = board[space].occupying_piece.icon)
            globalicon[i] = iconimage
            piece = canvas.create_image(board[space].x_coord,board[space].y_coord,image = globalicon[i],tag = space)
            i +=1
    root.mainloop()

get_board()
create_board()

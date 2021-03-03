class GameState():
    def __init__(self):
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"],
        ]
        self.moveFunctions = {'p':self.getPawnMove,'R':self.getRookMove,'N':self.getKnightMove,'B':self.getBishopMove,'Q':self.getQueenMove,'K':self.getKingMove}
        self.WhiteToMove = True
        self.movelog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate= False
        self.staleMate= False
        self.empassantPossible = ()


    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol]=move.pieceMoved
        self.movelog.append(move)
        self.WhiteToMove = not self.WhiteToMove #swap players
        # update kings location
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)
        # pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0]+'Q'
        if move.isEmpassantMove:
            self.board[move.startRow][move.endCol]="--"
        # update EmpassantPossible variable
        if move.pieceMoved[1]=="p" and abs(move.startRow-move.endCol)==2:
            self.empassantPossible = ((move.startRow+move.endRow)//2, move.endCol)
        else:
            self.empassantPossible = ()

    def undoMove(self):
        if len(self.movelog)!=0:
            move=self.movelog.pop()
            self.board[move.startRow][move.startCol]=move.pieceMoved
            self.board[move.endRow][move.endCol]=move.pieceCaptured
            self.WhiteToMove = not self.WhiteToMove
            # update kings location
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
            if move.isEmpassantMove:
                self.board[move.endRow][move.endCol]="--"
                self.board[move.startRow][move.endCol]=move.pieceCaptured
                self.empassantPossible = (move.endRow,move.endCol)
            if move.pieceMoved[1]=="p" and abs(move.startRow-move.endRow)==2:
                self.empassantPossible = ()

    def getvalidMoves(self):
        tempEmpassantPossible=self.empassantPossible
        # get all the moves
        moves= self.getAllPossibleMoves()
        # for moves make the move
        for i in range(len(moves)-1,-1,-1):
            self.makeMove(moves[i])
        # generate opp moves for these moves
        # check if they attack the king
        # if attacking then invalid move
            self.WhiteToMove= not self.WhiteToMove
            if self.inCheck():
               moves.remove(moves[i])
            self.WhiteToMove = not self.WhiteToMove
            self.undoMove()
        if len(moves)==0:
            if self.inCheck():
                self.checkMate=True
            else:
                self.staleMate=True
        else:
            self.checkMate=False
            self.staleMate=False
        self.empassantPossible=tempEmpassantPossible
        return moves


    def inCheck(self):
        if self.WhiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0],self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def squareUnderAttack(self,r,c):
        self.WhiteToMove = not self.WhiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.WhiteToMove = not self.WhiteToMove
        for move in oppMoves:
            if move.endRow== r and move.endCol== c:
                return True
        return False


    def getAllPossibleMoves(self):
        moves=[]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn=self.board[r][c][0]
                if (turn == "w" and self.WhiteToMove) or (turn == "b" and not self.WhiteToMove):
                    piece=self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)
        return moves

    def getPawnMove(self,r,c,moves):
        if self.WhiteToMove:
            if self.board[r-1][c] == "--":
                moves.append(Move((r,c),(r-1,c),self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r,c),(r-2,c),self.board))
            if c-1>=0:
                if self.board[r-1][c-1][0]=="b":
                    moves.append(Move((r,c),(r-1,c-1),self.board))
                elif (r-1,c-1) == self.empassantPossible:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, isEmpassantMove=True))
            if c+1<=7:
                if self.board[r-1][c+1][0]=="b":
                    moves.append(Move((r,c),(r-1,c+1),self.board))
                elif (r-1,c+1) == self.empassantPossible:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, isEmpassantMove=True))

        else:
            if self.board[r+1][c] == "--":
                moves.append(Move((r,c),(r+1,c),self.board))
                if r==1 and self.board[r+2][c]=="--":
                    moves.append(Move((r,c),(r+2,c),self.board))
            if c-1>=0:
                if self.board[r+1][c-1][0]=="w":
                    moves.append(Move((r,c),(r+1,c-1),self.board))
                elif (r+1,c-1) == self.empassantPossible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, isEmpassantMove=True))
            if c+1<=7:
                if self.board[r+1][c+1][0]=="w":
                    moves.append(Move((r, c),(r+1,c+1),self.board))
                elif (r+1,c+1) == self.empassantPossible:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, isEmpassantMove=True))


    def getRookMove(self,r,c,moves):
        directions=((-1,0),(0,-1),(1,0),(0,1))
        enemyColor="b" if self.WhiteToMove else "w"
        for d in directions:
           for i in range(1,8):
               endRow=r+d[0]*i
               endCol=c+d[1]*i
               if 0<=endRow<8 and 0<=endCol<8:
                   endPiece=self.board[endRow][endCol]
                   if endPiece=="--":
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                   elif endPiece[0]==enemyColor:
                       moves.append(Move((r, c),(endRow, endCol),self.board))
                       break
                   else:
                       break
               else:
                   break


    def getKnightMove(self,r,c,moves):
        knightMoves=((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        allyColor = "w" if self.WhiteToMove else "b"
        for m in knightMoves:
            endRow=r+m[0]
            endCol=c+m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0]!= allyColor:
                    moves.append(Move((r,c),(endRow,endCol),self.board))


    def getBishopMove(self,r,c,moves):
        directions = ((-1,-1), (1, -1), (-1, 1), (1, 1))
        enemyColor = "b" if self.WhiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break


    def getQueenMove(self,r,c,moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1),(-1,-1), (1, -1), (-1, 1), (1, 1))
        enemyColor = "b" if self.WhiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break


    def getKingMove(self,r,c,moves):
        kingMoves=((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        allyColor = "w" if self.WhiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = r + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0]!= allyColor:
                    moves.append(Move((r,c),(endRow,endCol),self.board))


class Move():
    ranksToRows = {"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rowsToRanks = {v:k for (k,v) in ranksToRows.items()}
    filesToCols = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    colsToFiles = {v:k for (k,v) in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEmpassantMove=False):
        self.startRow=startSq[0]
        self.startCol=startSq[1]
        self.endRow=endSq[0]
        self.endCol=endSq[1]
        self.pieceMoved=board[self.startRow][self.startCol]
        self.pieceCaptured=board[self.endRow][self.endCol]
        self.isPawnPromotion = False
        self.isPawnPromotion =(self.pieceMoved == "wp" and self.endRow==0) or (self.pieceMoved == "bp" and self.endRow==7)
        self.isEmpassantMove=isEmpassantMove
        if self.isEmpassantMove:
            self.pieceCaptured="wp" if self.pieceMoved == "bp" else "bp"
        self.moveID= self.startRow*1000+self.startCol*100+self.endRow*10+self.endCol
        print(self.moveID)
    '''
    Overriding equals method
    '''
    def __eq__(self, other):
        if isinstance(other,Move):
            return self.moveID==other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol)+ self.getRankFile(self.endRow,self.endCol)

    def getRankFile(self,r,c):
        return self.colsToFiles[c]+self.rowsToRanks[r]
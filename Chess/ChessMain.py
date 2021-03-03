import pygame as p
from Chess import ChessEngine
WIDTH = HEIGHT = 512
DIMENSIONS = 8
SQ_SIZE = HEIGHT//DIMENSIONS
MAX_FPS = 15
IMAGES = {}
'''
loading images in global directory
'''
def loadImages():
  pieces=['wp','wR','wN','wB','wQ','wK','bp','bR','bN','bB','bQ','bK']
  for piece in pieces:
   IMAGES[piece]=p.transform.scale(p.image.load("images/"+piece+".png"),(SQ_SIZE,SQ_SIZE))


'''
main driver
'''

def main():
    p.init()
    screen=p.display.set_mode((WIDTH,HEIGHT))
    clock=p.time.Clock()
    screen.fill(p.Color("white"))

    gs=ChessEngine.GameState()
    validMoves=gs.getvalidMoves()
    animate=False
    moveMade= False
    loadImages()
    running=True
    sqSelected= () #tuple of selected squares
    playerClicks=[] #keep track of player clicks
    gameOver=False #for checkmate
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running=False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                   location = p.mouse.get_pos()
                   col = location[0]//SQ_SIZE
                   row = location[1]//SQ_SIZE
                   if sqSelected==(row,col):
                       sqSelected=()
                       playerClicks=[]
                   else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected)
                   if len(playerClicks)==2:
                       move=ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                       print(move.getChessNotation())

                       if move in validMoves:
                           gs.makeMove(move)
                           moveMade=True
                           animate=True
                           sqSelected = ()
                           playerClicks = []
                       else:
                           playerClicks=[sqSelected]
            elif e.type==p.KEYDOWN:
                if e.key==p.K_z:
                    gs.undoMove()
                    moveMade=True
                    animate=False
                elif e.key==p.K_r:
                    gs=ChessEngine.GameState()
                    validMoves=gs.getvalidMoves()
                    sqSelected=()
                    playerClicks=[]
                    moveMade=False
                    animate=False

        if moveMade:
            if animate:
               animateMove(gs.movelog[-1], screen, gs.board, clock)
            validMoves=gs.getvalidMoves()
            moveMade=False
            animate=False

        drawGameState(screen,gs,validMoves,sqSelected)
        if gs.checkMate:
            gameOver=True
            if gs.WhiteToMove:
                drawText(screen,"Black wins by Checkmate!!")
            else:
                drawText(screen, "White wins by Checkmate!!")
        elif gs.staleMate:
            drawText(screen,"Stalemate!!")

        clock.tick(MAX_FPS)
        p.display.flip()

def highlightSquares(screen,gs,validMoves,sqSelected):
    if sqSelected!= ():
        r,c = sqSelected
        if gs.board[r][c][0]==("w" if gs.WhiteToMove else "b"):
            s=p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s,(c*SQ_SIZE,r*SQ_SIZE))
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow== r and move.startCol == c:
                    screen.blit(s,(SQ_SIZE*move.endCol,move.endRow*SQ_SIZE))

def drawGameState(screen,gs,validMoves,sqSelected):
    drawBoard(screen)
    highlightSquares(screen,gs,validMoves,sqSelected)
    drawPieces(screen,gs.board)

def drawBoard(screen):
    global colors
    colors=[p.Color("white"), p.Color("grey")]
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            color=colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen,board):
        for r in range(DIMENSIONS):
            for c in range(DIMENSIONS):
                piece=board[r][c]
                if piece!="--":
                    screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                    
def animateMove(move, screen, board, clock):
    global colors
    coords = [] #list of rows and cols for animation
    dR= move.endRow - move.startRow
    dC= move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR)+abs(dC))*framesPerSquare
    for frame in range(frameCount+1):
        r,c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow+move.endCol)%2]
        endSquare = p.Rect(move.endCol*SQ_SIZE,move.endRow*SQ_SIZE,SQ_SIZE,SQ_SIZE)
        p.draw.rect(screen,color,endSquare)
        if move.pieceCaptured!="--":
            screen.blit(IMAGES[move.pieceCaptured],endSquare)
        screen.blit(IMAGES[move.pieceMoved],p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)
        
def drawText(screen,text):
    font=p.font.SysFont("Helvitca",32,True,False)
    textObject=font.render(text,0,p.Color('Black'))
    textLocation=p.Rect(0,0,WIDTH,HEIGHT).move(WIDTH/2 - textObject.get_width()/2,HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject,textLocation)


if __name__ == "__main__":
  main()

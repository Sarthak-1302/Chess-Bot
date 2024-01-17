import pygame as p
import chessEngine
import smartMoveFinder

WIDTH = HEIGHT = 512
DIMENSION  = 8 
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15
IMAGES  = {}


def loadImage():
    pieces = ['wp','wK','wN','wQ','wR','wB','bp','bK','bN','bQ','bR','bB']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Images/"+ piece + ".png"), (SQ_SIZE,SQ_SIZE))

def Main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessEngine.GameState()
    validMoves = gs.getvalidMoves()

    animate = False
    moveMade = False
    loadImage()
    running = True
    sqSelected= ()
    playerClick = []
    gameOver = False
    playerOne = False
    playerTwo = False
    while running:
        humanTurn =(gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in  p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row,col):
                        sqSelected = ()
                        playerClick = []    
                    else:
                        sqSelected = (row,col)
                        playerClick.append(sqSelected)
                    if len(playerClick) == 2:
                        move = chessEngine.Move(playerClick[0],playerClick[1],gs.board)
                        # print(move.getchessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClick = []
                        if not moveMade:
                            playerClick = [sqSelected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                if e.key == p.K_r:
                    gs = chessEngine.GameState()
                    validMoves = gs.getvalidMoves()
                    sqSelected =()
                    playerClick =[]
                    moveMade = False
                    animate = False
                    gameOver = False

        if not gameOver and not humanTurn:
            AImove =smartMoveFinder.findBestMoveMinMax(gs,validMoves)
            if AImove is None:
                AImove =smartMoveFinder.findRandomMove(validMoves)
            gs.makeMove(AImove)
            moveMade = True
            animate = True
        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1],screen,gs.board,clock)
            validMoves = gs.getvalidMoves()
            moveMade = False
            animate  =False
        drawGameState(screen,gs,validMoves,sqSelected)

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen,"Black wins by checkmate")
            else:
                drawText(screen,"white wins by checkmate")
        elif gs.staleMate:
            gameOver =True
            drawText(screen,"Stalemate")

        clock.tick(MAX_FPS)
        p.display.flip()

def drawText(screen,text):
    font =p.font.SysFont("monospace",32 ,True,False)
    textObject =font.render(text,0,p.Color("black"))
    textLocation = p.Rect(0,0,WIDTH,HEIGHT).move(WIDTH/2 - textObject.get_width()/2,HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject,textLocation)
    textObject = font.render(text,0,p.Color("black"))
    screen.blit(textObject,textLocation.move(2,2))

def highlightSquares(screen,gs,validMoves,sqSelected):
    if sqSelected !=():
        r,c =sqSelected
        if gs.board[r][c][0] == ("w" if gs.whiteToMove else "b"):
            s = p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s,  (c*SQ_SIZE,r*SQ_SIZE))
            s.fill(p.Color('brown'))
            for move in validMoves:
                if move.startRow == r and  move.startCol == c:
                    screen.blit(s,(move.endCol*SQ_SIZE,move.endRow*SQ_SIZE))

def animateMove(move,screen,board,clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare  =10
    frameCount =(abs(dR) +abs(dC) + framesPerSquare)
    for frame  in range(frameCount+1):
        r,c = (move.startRow+dR*frame/frameCount,move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen,board)
        color =colors[(move.endRow+move.endCol)%2]
        endSquare =p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE,SQ_SIZE,SQ_SIZE)
        p.draw.rect(screen,color,endSquare)

        if move.pieceCapture !="--":
            screen.blit(IMAGES[move.pieceCapture],endSquare)
        screen.blit(IMAGES[move.pieceMoved],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
        p.display.flip()
        clock.tick(60)
    


def drawGameState(screen , gs,validMoves,sqSelected):
    drawBoard(screen)
    drawPieces(screen, gs.board)
    highlightSquares(screen,gs,validMoves,sqSelected)


def drawBoard(screen):

    for row in range(DIMENSION):
        global colors
        colors = [p.Color("light gray"),p.Color("dark green")]
        for col in range(DIMENSION):
            if (row+col)%2 == 0:
                color = p.Color("light gray")
            else:
                color = p.Color("dark green")   
            p.draw.rect(screen,color,p.Rect(col*SQ_SIZE,row*SQ_SIZE,SQ_SIZE,SQ_SIZE))

def drawPieces(screen,board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if  piece!= "--":
                screen.blit(IMAGES[piece],p.Rect(col*SQ_SIZE,row*SQ_SIZE,SQ_SIZE,SQ_SIZE))



if __name__=="__main__":
    Main()
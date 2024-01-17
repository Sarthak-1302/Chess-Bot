import random

pieceScore = {"K":0 , "Q":10,"R":5,"B":3,"N":3,"p":1}
CHECKMATE =1000
STALEMATE =0
DEPTH = 4
def findRandomMove(validMoves):
    return validMoves[random.randint(0,len(validMoves)-1)]
def findBestMove(gs,validMoves):
    turn = 1 if gs.whiteToMove else -1
    maxScore = -CHECKMATE
    bestMove =None
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        if gs.checkMate:
            score =CHECKMATE
        elif gs.staleMate:
            score = STALEMATE

        score =turn * scoreMaterial(gs.board) 
        if score > maxScore:
            maxScore = score
            bestMove = playerMove
        gs.undoMove()
    return bestMove

def scoreMaterial(board):
    score =0
    for row in board:
        for square in row:
            if square[0]=='w':
                score+=pieceScore[square[1]]
            elif square[0]=='b':
                score-=pieceScore[square[1]]
    return score
def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.staleMate:
        return STALEMATE
    
    score =0
    for row in gs.board:
        for square in row:
            if square[0]=='w':
                score+=pieceScore[square[1]]
            elif square[0]=='b':
                score-=pieceScore[square[1]]
    return score
def findBestMoveMinMax(gs,validMoves):
    global nextMove
    nextMove =None
    random.shuffle(validMoves)
    findMoveAlphaBeta(gs,validMoves,DEPTH,-CHECKMATE,CHECKMATE,1 if gs.whiteToMove else -1)
    return nextMove


def findMoveAlphaBeta(gs,validMoves,depth,alpha,beta,turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier*scoreBoard(gs)
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves =gs.getvalidMoves()
        score = -findMoveAlphaBeta(gs,nextMoves,depth-1,-beta,-alpha,-turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove =move
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >=beta:
            break
    return maxScore

    
def findMoveMinMax(gs,validMoves,depth,whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)
    if whiteToMove:
        maxScore =-CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getvalidMoves()
            score = findMoveMinMax(gs,nextMoves,depth-1,False)
            if maxScore < score:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore =CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getvalidMoves()
            score = findMoveMinMax(gs,nextMoves,depth-1,True)
            if minScore > score:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore


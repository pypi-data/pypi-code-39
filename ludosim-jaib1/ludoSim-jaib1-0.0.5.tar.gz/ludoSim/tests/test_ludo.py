# This file contains unit and integration test functions for the ludoSim
# package

from ludoSim import *
import timeit

def test_roll():
    """ 
    Tests outcomes of a die roll given certain game states
    """
    b = Board()
    p = b._Board__players[0]
    # first test: move piece out of home base
    roll = 6
    
    # should be empty initially
    assert not(p._Player__activePieces) 

    # should be -1000 (indicates off board)
    assert p._Player__homePieces[-1]._Piece__boardPos == -1000
    
    p.makeMove(roll) # move piece out of home base 
    
    # check for update of board position and move count
    assert p._Player__activePieces[0]._Piece__boardPos == p._Player__startPos
    assert p._Player__activePieces[0]._Piece__moveCount == 1

def test_score():
    """
    Tests whether a score occurs when a player has a chance to move piece to 
    end of score arm
    """
    b = Board()
    p = b._Board__players[0]
    # get pieces onto board
    for piece in range(0, b._Board__numPieces):
        p._Player__activePieces.append(p._Player__homePieces.pop())
        # move that piece to the start position
        p._Player__activePieces[-1]._Piece__boardPos = p._Player__startPos
        # update that piece's move count
        p._Player__activePieces[-1]._Piece__moveCount = 1
        # update board's `__piecePosns`
        pID = p._Player__id
        pPiece = p._Player__activePieces[-1]._Piece__pieceID
        b._Board__piecePosns[str(pID)+str(pPiece)] = p._Player__startPos
    # `__homePieces` should now be empty
    assert not(p._Player__homePieces)
    # move one piece to score arm
    pz = p._Player__activePieces[-1]
    pz._Piece__boardPos = b._Board__boardSpaces
    pz._Piece__moveCount = b._Board__boardSpaces
    p.makeMove(6) # score the piece
    
    # check that the board position has been updated, that the right piece
    # scored, and that the score has been updated
    assert pz._Piece__boardPos == -1000
    assert pz._Piece__pieceID == 0
    assert p._Player__score == 1
    assert b._Board__scores[0] == 1
    assert p._Player__scorePieces != []
    
    # make sure moving past the score arm doesn't result in a score:
    
    # move piece to end of board and get cur score
    pz2 = p._Player__activePieces[-1]
    pz2._Piece__boardPos = b._Board__boardSpaces
    pz2._Piece__moveCount = b._Board__boardSpaces
    curScore = p._Player__score
    
    p.makeMove(3) # should move `pz` up 3 in the score Arm (to scoreArmPos == 2)
    assert pz2._Piece__scoreArmPos == 3
    curBoardPos = pz2._Piece__boardPos
    curMoveCount = pz2._Piece__moveCount
    assert curMoveCount > b._Board__boardSpaces
    assert b._Board__piecePosns['01'] and curBoardPos == -1000
    
    p.makeMove(4) # shouldn't result in a score nor move of `pz2`
    assert curScore == p._Player__score
    assert ((curBoardPos == pz2._Piece__boardPos) 
            and (curMoveCount == pz2._Piece__moveCount))
    p.makeMove(3) # should result in a score
    assert pz2._Piece__boardPos == -1000
    assert p._Player__score > curScore
    
def test_hit():
    """
    Tests what happens when one player's piece hits another player's piece
    """
    b = Board()
    p0 = b._Board__players[0]
    p1 = b._Board__players[1]
    # move one piece out for each player
    p0.makeMove(6)
    p1.makeMove(6)
    p0_pz = p0._Player__activePieces[0]
    p1_pz = p1._Player__activePieces[-1]
    # make sure pieces have moved out of home base for b's `__piecePosns`
    assert (b._Board__piecePosns['03'] and b._Board__piecePosns['13']) >= 0 
    distToMove = p1_pz._Piece__boardPos - p0_pz._Piece__boardPos
    while distToMove > 5:
        p0.makeMove(5)
        distToMove -= 5
    # make sure moves were properly registered
    assert b._Board__piecePosns['03'] == p0_pz._Piece__boardPos 
    numP1ActivePieces = len(p1._Player__activePieces)
    numP1HomePieces = len(p1._Player__homePieces)
    p0.makeMove(distToMove)
    # test that number of homePieces increases and activePieces decreases
    assert (numP1ActivePieces > len(p1._Player__activePieces)
            and numP1HomePieces < len(p1._Player__homePieces))
    assert p1_pz._Piece__boardPos == -1000
    assert p1_pz == p1._Player__homePieces[-1]
    
    # test that moving a piece onto the board at a board position an opponent's
    # piece occupies succesfully hits the opponent's piece:
    
    # move the piece that was just hit by p0 back onto the board to hit p0's
    # piece
    p1.makeMove(6)
    assert (p0_pz._Piece__boardPos == -1000 
            and len(p0._Player__homePieces) == 4 and not(p0._Player__activePieces))
    
    # test that the next piece to be moved out of home is the same piece that 
    # was just sent back home
    assert p1_pz._Piece__boardPos >= 0
    


def test_block():
    """
    Test what happens when one player has two pieces on the same square and
    another player's piece has the ability to move past that square
    """
    b = Board()
    p0 = b._Board__players[0]
    p1 = b._Board__players[1]
    # move one piece out for p0
    p0.makeMove(6)
    # move two pieces for p1 onto board
    for piece in range(0, 2):
        p1._Player__activePieces.append(p1._Player__homePieces.pop())
        # move that piece to the start position
        p1._Player__activePieces[-1]._Piece__boardPos = p1._Player__startPos
        # update that piece's move count
        p1._Player__activePieces[-1]._Piece__moveCount = 1
        # update board's `__piecePosns`
        p1ID = p1._Player__id
        p1Piece = p1._Player__activePieces[-1]._Piece__pieceID
        b._Board__piecePosns[str(p1ID)+str(p1Piece)] = p1._Player__startPos
        
    p0_pz = p0._Player__activePieces[0]
    p1_pz1 = p1._Player__activePieces[0]
    p1_pz2 = p1._Player__activePieces[1]
    # make sure p1's two pieces share the same position
    assert (b._Board__piecePosns['13'] == b._Board__piecePosns['12'] ==
            p1_pz1._Piece__boardPos == p1_pz2._Piece__boardPos)
    
    distToMove = p1_pz1._Piece__boardPos - p0_pz._Piece__boardPos
    while distToMove > 5:
        p0.makeMove(5)
        distToMove -= 5
        
    # make sure moves were properly registered
    curP0BoardPos = p0_pz._Piece__boardPos
    assert b._Board__piecePosns['03'] == p0_pz._Piece__boardPos 
    
    # test that move for p0 did not occur (could not pass block)
    p0.makeMove(distToMove)
    assert p0_pz._Piece__boardPos == curP0BoardPos
    p0.makeMove(distToMove+1)
    assert p0_pz._Piece__boardPos == curP0BoardPos

def test_playGame():
    """
    Test to make sure game runs to completion within a reasonable time, and
    that the declared winner is accurate
    """
    b = Board()
    # check running time
    tic = timeit.default_timer()
    b.playGame()
    toc = timeit.default_timer()
    
    # typically ~10000 function calls per game, which in total should take 
    # < 0.01 seconds, so we set `maxTime` threshold to 0.1 to be safe
    maxTime = 0.1
    assert (toc-tic) < maxTime 
    # make sure winner is player who's score == 4
    assert (b._Board__winner == b._Board__scores.index(4))
    
    # make sure winning player has only scorePieces (no activePieces or homePieces)
    winningPlayer = b._Board__players[(b._Board__winner)]
    assert (winningPlayer._Player__scorePieces 
            and not(winningPlayer._Player__homePieces)
            and not(winningPlayer._Player__activePieces))
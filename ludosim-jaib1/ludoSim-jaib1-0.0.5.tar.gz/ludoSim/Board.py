from ludoSim import * # import other classes in this package
from ludoSim.Player import Player
import random


class Board(): 
    """
    A class which represents a ludo board and runs the game of ludo.

    Notes for clarification:
    ------------------------
        - Terminology:
            - "home base": The area a player's pieces occupy at game start
            - "score base": The area a player's pieces occupy upon a score
            - "score arm": The area on the board leading directly to the score 
                base. A player's pieces cannot be hit when in this area.
            - "start position": The board space a player's piece occupies
                upon moving out of their home base.
            - "hit move": A move in which one player's piece hits another
                player's piece, moving the second player's piece back to that 
                player's home base
            - "block": a scenario in which one player has two pieces on the 
                same board position, which results in all opposing players' 
                pieces being unable to move to or past this board position.
                
        - Board Space Numbering: The start position of player0 is considered 
          space 0. 
    
    Rules:
    ------
        - If a 6 is rolled: 
            1) A player may move a piece out of their home base
            and onto the board. 
            2) The player rolls again.
        - "Hits": If a player's (e.g. player0) piece moves to the same board
        space another player's (e.g. player1) piece occupies (i.e. a player0 
        piece "hits" a player1 piece) the other player's (player1's) piece 
        moves back to their home base.
        - "Blocks": If a player's piece moves to a board space which another
        piece of the same player occupies, that space is now "blocked", and
        other players cannot move their pieces past that space.
    
    Run game:
    ---------
    Navigate to ludoSim's parent directory, launch python, and run the
    following commands:
        
    from ludoSim import *
    b = Board() # use optional input args to set the board however you'd like
    b.playGame()
    
    Attributes:
    -----------
        __numPlayers: The number of players in the game (must be an int between 
            1-4).
        __numPieces: The number of pieces each player has (must be an int >= 1).
        __players: Array of Player objects of length __numPlayers.
      	__piecePosns: Dict of piece positions ['PlayerID'+'PieceId':PiecePos] 
            of length __numPlayers * __numPieces.
        __startPosns: Numeric array with the start position for each player.
      	__scores: Numeric array of length numPlayers with the current score for 
            each player.
        __winner: A number representing the winning player (the playerID).
        __scoreArmSpaces: The number of spaces a player's piece needs to move
            once inside the score arm in order to score.
        __widthSpaces: The number of columns of length __scoreArmSpaces on each
            side of the board.
      	__boardSpaces: The total number of spaces on the board.
        __hits: Numeric array of length __numPlayers which holds the number of
          times each player hit another player's piece, where the index in the 
          array corresponds to the player ID.
        __rolls: Numeric array containing all the die rolls in the game.
        __playerTurns: Numeric array containing playerIDs, where the index in
            the array corresponds to the move number in the game.
    """
    
    # define and limit attributes:
    # we won't make them truly private (using `@property`), but will instead
    # make them hidden, using `__`
    __slots__ = ('__numPlayers', '__numPieces', '__players', '__piecePosns', 
                 '__startPosns', '__scores', '__winner', '__scoreArmSpaces', 
                 '__widthSpaces', '__boardSpaces', '__hits', '__rolls',
                 '__playerTurns')
    
    def __init__(self, numPlayers=2, numPieces=4, scoreArmSpaces=5, 
                 widthSpaces=3):
        """
        The constructor requires the number of players, number of pieces, 
        number of board spaces in the home arm, and number of board spaces
        between adjacent players. This function should be called directly by a
        user outside of this class.
        
        Parameters
        ----------
        numPlayers
        numPieces
        scoreArmSpaces
        widthSpaces
        
        Examples
        --------
        b = Board()
        
        b = Board(numPlayers=4)
        
        b = Board(4,5,8,4)      
        """
        
        self.__numPlayers = numPlayers 
        self.__numPieces = numPieces 
        # dict of piece positions: {"playerID""pieceNum": boardPos}
        self.__piecePosns = {str(player)+str(piece):-1000 
                                for player in range(0,numPlayers) 
                                for piece in range(0,numPieces)}
        self.__scores = [0 for i in range(0,numPlayers)] 
        self.__scoreArmSpaces = scoreArmSpaces 
        self.__widthSpaces = widthSpaces
        self.__boardSpaces = (scoreArmSpaces+1)*8 + (widthSpaces-2)*4
        # build `__startPositions` array
        self.__startPosns = [(i * (2*(scoreArmSpaces+1)+1)) 
                                for i in range(0,numPlayers)]
        # build `__players` array
        self.__players = [Player(self, i, self.__startPosns[i]) 
                         for i in range(0,numPlayers)]
        self.__winner = []
        self.__hits = [0, 0]
        self.__rolls = []
        self.__playerTurns = []
        
    def playGame(self):
        """
        Starts and runs the game of ludo. This function should be called
        directly by a user outside of this class.
        
        Examples
        --------
        b = Board()
        b.playGame()
        """
        turnNumber = 0

        while self.__winner == []:
            # roll die and record roll
            roll = random.randint(1,6)
            self.__rolls.append(roll)

            # player makes move
            playerTurn = turnNumber % self.__numPlayers
            self.__playerTurns.append(playerTurn)
            self.__players[playerTurn].makeMove(roll)
            if not(roll == 6):
                turnNumber +=1 
    
    def endGame(self):
        """
        Ends the game and declares a `winner` when a player has scored all of 
        their pieces. This function is called by a Player object when that
        player scores all of their pieces (see `Player/updateGame`)
        """
        self.__winner = self.__scores.index(self.__numPieces)  
        print('Game over. Player %s wins' % self.__winner)
        
        
class Piece():
    """
    A class which represents a player's piece in a ludo game. Instantiated and 
    used by `Player`.
    
    Attributes:
    -----------
        __playerID: The number ID of the player the piece belongs to.
        __pieceID: The number of the piece.
        __moveCount: The current number of spaces the piece has moved.
        __boardPos: The current board space the piece occupies.
        __scoreArmPos: The current score arm space the piece occupies.
    """
    
    # define and limit attributes:
    # we won't make them truly private (using `@property`), but will instead
    # make them hidden, using `__`
    __slots__ = ('__playerID', '__pieceID', '__moveCount', '__boardPos', 
                 '__scoreArmPos')
        
    def __init__(self, playerID, pieceID):
        """
        The constructor requires the id of the player the piece belongs to, and
        an id to distinguish it from the other player's pieces. This function 
        is called by `Player` upon the construction of `Player`.
        
        Parameters
        -----------
        playerID
        pieceID
        """
        
        self.__playerID = playerID
        self.__pieceID = pieceID
        self.__moveCount = -1000 # hacky placeholders for representing "off board"
        self.__boardPos = -1000
        self.__scoreArmPos = -1000
        
    def __iter__(self):
        """
        Generator function to use class as iterator.
        """
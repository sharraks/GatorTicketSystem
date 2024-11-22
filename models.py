import time

class User:
    """
    class to define a User node
    """
    def __init__(self, userID, priority) -> None:
        self.userID = userID
        self.priority = priority
        self.timeStamp = time.time() # to be used for resolving ties on basis of priority



class Booking:
    """
    Class to create a node for any booking done for reservation. It is a Red Black Tree node
    """
    def __init__(self, userID: int, seatID: int) -> None:
        self.userID = userID
        self.seatID = seatID
        self.left = None
        self.right = None
        self.parent = None
        self.color = 'R' # new node inserted are always Red in beginning
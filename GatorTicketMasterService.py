#add all required user defined libraries
import seats
from models import User
import waitlist
import reservations

class GatorTicketMaster():
    """
    Class to initialize the control services for the ticketing system. It has all the logic layer for the 10 functions required in the Problem Statement.
    """

    def __init__(self) -> None:
        """
        Initialise the ticketing service
        """
        self.eventInitialized = False #variable to save if the Initialize function has been called or not, as the reservations can't start if seats are available.
        self.seats = None
        self.waitlist = None
        self.reservations = reservations.RedBlackTree()

    def initialize(self,seatCount: int):
        """
        function to initailise the seats heap. Calls the MinHeapSeats constructor which creates a heap with nodes 1 to seatCount
        """
        if(self.eventInitialized == True):
            return "Seats already initialized. Please try to add seats"
        self.eventInitialized = True
        self.seats = seats.MinHeapSeats(seatCount)

        return f"{seatCount} Seats are made available for reservation"


    def available(self):
        """
        function to return the current size of the waitlist and the seats heaps.
        """
        #check if the seats heap has been initialised or not.
        if self.eventInitialized == False:
            return "Seats not initialized yet!!"
        else:
            availabel_seats = self.seats.size()
            waitlist_count = 0 if(self.waitlist == None) else self.waitlist.size()
            return f"Total Seats Available : {availabel_seats}, Waitlist : {waitlist_count}"

    def reserve(self,userID: int, userPriority: int):
        """
        function to book a seat for a user with its Id. If no seats are available then it add it to waitlist with the priority.
        """
        if(self.waitlist == None):
            self.waitlist = waitlist.MinHeapUser()
        
        newUser = User(userID,userPriority) #create a user node
        
        #check is seats available
        if(self.seats.size() == 0):
            self.waitlist.push(newUser) #push node to waitlist
            return f"User {userID} is added to the waiting list"
        else:
            #take the lowest seatID from heap and userID and pass to Red Black tree for insert
            seatID = self.seats.poll()
            self.reservations.addReservation(userID,seatID)
            return f"User {userID} reserved seat {seatID}"


    def cancel(self,seatID, userID):
        #check if seats initialised or not
        if(self.eventInitialized == False):
            return ["Event not initialized yet!!"]
        
        #check if a node with the userID is present in reservations or not
        data = self.reservations.search(self.reservations.root,userID)

        if(data == None):
            return [f"User {userID} has no reservation to cancel"]

        #reservation present but with different seatID
        elif(data.seatID != seatID):
            return [f"User {userID} has no reservation for seat {seatID} to cancel"]
        
        #waitlist is not empty so, cancel reservation and rebook for waitlist user.
        elif self.waitlist.size()!=0:
            self.reservations.deleteReservation(data)
            waitlist_user = self.waitlist.poll().userID
            self.reservations.addReservation(waitlist_user,seatID)
            return [f"User {userID} canceled their reservation",f"User {waitlist_user} reserved seat {seatID}"]
        
        #waitlist is empty so push to available seats heap
        elif self.waitlist.size() == 0:
            self.reservations.deleteReservation(data)
            self.seats.push(seatID)
            return [f"User {userID} canceled their reservation"]


    def exitWaitlist(self,userID):
        #if waitlist is empty or not initialise, no node to return
        if(self.waitlist == None or self.waitlist.size() == 0):
            return f"User {userID} is not in waitlist"
        
        else:
            #search and delete node from waitlist heap, if present
            check_delete = self.waitlist.remove(userID)
            if check_delete == False:
                return f"User {userID} is not in waitlist"
            else:
                return f"User {userID} is removed from the waiting list"

    def updatePriority(self,userID, userPriority):
        #if waitlist is empty or not initialise, no node to update
        if(self.waitlist == None or self.waitlist.size() == 0):
            return f"User {userID} priority is not updated"
        
        else:
            #search and update priority on node from waitlist heap, if present
            check_update = self.waitlist.updatePriority(userID, userPriority)
            if check_update == False:
                return f"User {userID} priority is not updated"
            else:
                return f"User {userID} priority has been updated to {userPriority}"

    def addSeats(self,count):
        #check if seats have been initialised or not, can't add seats if not initialise to begin with.
        if self.eventInitialized == False:
            return "Seats not initialized!!"
        
        else:
            output = []
            self.seats.resize(count) #add nodes to seats 
            output.append(f"Additional {count} Seats are made available for reservation")

            #for each available seat and user in waitlist book a reservation.
            if(self.waitlist is not None and self.waitlist.size() > 0):
                while(self.seats.isEmpty() == False and self.waitlist.size() > 0):
                    userObj = self.waitlist.poll()
                    output.append(self.reserve(userObj.userID, userObj.priority)) #collects output for individual operation
            
        return output

    def printReservations(self):
        #check if there is no reservation yet. Nothing to print.
        if(self.reservations.isEmpty() == "True"):
            return []
        
        bookings = []
        self.reservations.inorder(self.reservations.root,bookings=bookings) #traverse inorder of userID
        return sorted(bookings, key=lambda bookings: bookings[0]) #sort output in order of SeatID

    def releaseSeats(self,userID1, userID2):
        #check if there is no reservation yet. Nothing to remove.
        if(self.reservations.isEmpty() == True):
            return ["No reservations yet!!"]
        
        #check if event not initialised yet. Nothing to print.
        if(self.eventInitialized == False):
            return ["Seats not allocated yet!!"]
        
        result = []
        
        #Case 1: waitlist is not empty
        if(self.waitlist is not None and self.waitlist.size()>0):
            for i in range(userID1, userID2+1):
                booking = self.reservations.search(self.reservations.root,i)
                #case 1(a): node found in reservation red black tree
                if booking is not None:
                    seatID = booking.seatID
                    self.reservations.deleteReservation(booking) #delete node
                    self.seats.push(seatID) #add seats to available seats

                #case 1(b): node not in reservations. Check in waitlist and delete.
                else:
                    self.waitlist.remove(i)
            
            result.append(f"Reservations of the Users in the range [{userID1}, {userID2}] are released")
            
            #since waitlist is not empty, while seats lasts book all the available users in waitlist
            while(self.waitlist.size()>0 and self.seats.size()>0):
                waitlist_user = self.waitlist.poll().userID
                new_seat = self.seats.poll()
                self.reservations.addReservation(waitlist_user, new_seat)
                result.append(f"User {waitlist_user} reserved seat {new_seat}")

        #case 2: waitlist is empty
        else:
            for i in range(userID1, userID2+1):
                booking = self.reservations.search(self.reservations.root,i)
                #case 2(a):node present in reservations
                if booking is not None:
                    seatID = booking.seatID
                    self.reservations.deleteReservation(booking) #delete it
                    self.seats.push(seatID) #add seat to available seats

            result.append(f"Reservations/waitlist of the users in the range [{userID1}, {userID2}] have been released")

        return result
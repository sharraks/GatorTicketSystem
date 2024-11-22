# GatorTicketSystem

Problem Statement:
Gator Ticket Master is a seat booking service for Gator Events. Users utilize this service to secure a seat
for attendance at a gator event. The service is seeking to develop a software system that effectively
manages seat allocation and reservation management.
The service must adhere the following specific requirements for managing reservations:
• Every event commences with a specific initial number of seats, which can be increased in the
event of a high anticipated demand for the event.
• When a user attempts to reserve a seat for the event, the system prioritizes and assigns the seat with
the lowest number first from the available seats.
• Users have the option to withdraw their reservation, in which case the seat is reassigned to the user
selected from the waitlist. If the waitlist is empty, the reservation is deleted, and the seat number is
reintroduced into the list of unassigned seats.
• Users are assigned priorities (integer values), and the user with the highest priority is given
preference when assigning seats from the waitlist heap(e.g., User with priority 2 gets priority over
user with priority 1). Ties are resolved by considering the timestamp at which the reservation was
made (first-come, first-served basis).
• It is assumed that users will not attempt to reserve a seat twice.
• User priority can be modified once they enter the waitlist. We then update the waitlist with the
new priority while preserving the original timestamp data.
• If the event organizer finds out about any unusual booking activity from a group of users, they can
release the seats assigned to a range of user ID’s and make those seats available again. If any of
the users in the range are in waiting list, we remove the users from it.
Implement from scratch, a Red-Black tree to manage the reserved seat information. Each node in that
tree contains the following information: User ID (unique identifier of the user and is the Key for the Red-
Black Tree) and Seat ID (unique identifier of the seat). Implement from scratch, a priority-queue
mechanism using a Binary Min-Heap as a data structure to manage the waitlist in the event that there are
no seats currently unassigned. You should also implement a heap to keep track of the seat numbers that
are currently unassigned, to satisfy the 2nd requirement. Since, there can be a scenarios where a user
cancels his reservation and there is not waitlist, so the seat gets added back to the available seats. The system should support the following operations:
1. Initialize(seatCount) : Initialize the events with the specified number of seats, denoted as
“seatCount”. The seat numbers will be sequentially assigned as [1, 2, 3, …, seatCount] and added to
the list of unassigned seats .
2. Available() : Print the number of seats that are currently available for reservation and the length of
the waitlist.
3. Reserve(userID, userPriority): Allow a user to reserve the seat that is available from the
unassigned seat list and update the reserved seats tree. If no seats are currently available, create a
new entry in the waitlist heap as per the user’s priority and timestamp. Print out the seat number if a
seat is assigned. If the user is added to the waitlist Print out a message to the user stating that he is
added to the waitlist.
4. Cancel(seatID, userID): Reassign the seat to user from the waitlist heap. If the waitlist is empty,
delete the node and add it back to the available seats.
5. ExitWaitlist(userID): If the user is in the waiting list, remove him from the waiting list. If the user
is already assigned a seat prior to this, the user must use the cancel function to cancel his reservation
instead.
6. UpdatePriority(userID, userPriority): Modify the user priority only if he is in the waitlist heap.
Update the heap with this modification.
7. AddSeats(count): We add the new seat numbers to the available seat list. The new seat numbers
should follow the previously available range.
8. PrintReservations(): We print the information of all the assigned seats and the users they are
assigned to ordered by the seat Numbers.
9. ReleaseSeats(userID1, userID2): We release all the seats assigned to the users whose ID falls in
the range [userID1, userID2]. It is guaranteed that userID2 >= userID1. We even remove the users
from the waitlist if they are present there. The status of the change should be printed ordered by
userID’s in the range.
10. Quit(): Anything below this command in the input file will not be processed. The program
terminates either when the quit command is read by the system or when it reaches the end of the
input commands, which ever happens first.

Program Structure:
In my submission, there are six python files, namely:
-	gatorTicketMaster.py : this is the entry point for the program, takes the input from the cli argument and parse it to generate API calls to the service layer which has all the 10 functions required for the service. It parses the arguments as well for the function which require that. While switching between the function calls, it stores the output of individual function on new line of an output file.
-	gatorTicketMasterService.py : this file has all the 10 function and logic to use the underlying data structures to operate.
-	models.py : this file has the class definition for User node used for waitlisting using priority and insertion timestamp, and the Booking node which is used by the Red Black Tree to store, display, and delete the reservations.
-	seats.py : this file has the data structure for min binary heap for the allocation of available seats. It is a priority queue, and stores the lowest integer seat on top. Implementation is based on array or list in case of python.
-	waitlist.py : this file has the data structure for min binary heap for the waitlisting of user that try to make reservation but can’t due to unavailable seats. It is a priority queue, and stores the highest integer priority user on top, in case of ties on the basis of priority it stores the earlier timestamp as parent. Implementation is based on array or list in case of python
-	reservations.py : this file has the data structure implementation of a Red Black Tree. It uses the Booking nodes to maintain the BST. Contains the functions for insertion, search, deletion, rotation (to support insert and delete) and inorder traversal.
  

Running Process:
Unzip the folder if donloaded a zip file and/or else open a terminal from the root folder and run the program using command:
-	python3 gatorTicketMaster.py <filename>

<fileName> is the file which contains the sequence of operations to be performed on the service.

Example Testcase:
Initialize(4)
Available()
Reserve(8, 1)
Reserve(4, 3)
Reserve(5, 2)
Cancel(2, 4)
Reserve(1, 1)
Available()
PrintReservations()
Reserve(3, 1)
Reserve(2, 2)
Reserve(6, 3)
Available()
Cancel(1, 1)
Cancel(3, 5)
Available()
Reserve(11, 1)
Reserve(9, 2)
AddSeats(2)
Reserve(7, 2)
Cancel(1, 8)
Available()
ReleaseSeats(8, 10)
PrintReservations()
Quit()

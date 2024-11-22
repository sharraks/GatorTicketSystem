
class MinHeapSeats:
    """
    Class to create a min binary heap for available seats. Provides basic operations like push, poll/pop, peek, size, resize, isEmpty, heapifyUp & heapifyDown
    """
    heap = []  # start with an empty array
    max_seat = -1 # variable to store last highest seat ever pushed on the heap. Helpful for resizing.

    def __init__(self,size) -> None:
        """
        initializes heap with some specific size.
        """
        for i in range(0,size):
            self.push(i+1)

    def push(self, seat_id) -> None:
        """
        updates the value of max_seat encountered/pushed onto heap.
        add elements/seats to heap at last index, calls the heapifyUp function.
        """
        self.max_seat = seat_id if seat_id > self.max_seat else self.max_seat
        self.heap.append(seat_id)
        self.heapifyUp(len(self.heap) - 1)

    def poll(self) -> int:
        """
        pops the top most/ min element (integer) from the heap and returns it as well.
        If heap is empty returns -1.
        """
        if len(self.heap) > 0:
            root = self.heap[0]
            self.heap[0] = self.heap[-1] #exchange with the last element, heapify down handles the structure later.
            self.heap.pop() # after swapping, the last element is the min element or previous root.
            self.heapifyDown(0)
            return root
        
        return -1
    
    def peek(self) -> int:
        """
        returns the top/min element on heap
        """
        if len(self.heap) > 0:
            return self.heap[0]

        return -1
    
    def size(self):
        """
        returns current size of heap
        """
        return len(self.heap)
    
    def resize(self,new_seats: int) -> None:
        """
        reshape the heap by adding more seats starting from the max_seats+1 upto the count provided.
        """
        max = self.max_seat
        for i in range(max+1 , max + new_seats + 1):
            self.max_seat = i  # update the max_seat value for future calls to same function
            self.push(i)

    def isEmpty(self) -> bool:
        """
        return boolean value if the heap is empty or not.
        """
        return len(self.heap) == 0

    def heapifyUp(self, idx) -> None:
        """
        Performs the heapify opertaion on array from bottom to up, as new elements are added at the end of array.
        Compares the values with parent, swap if required and repeat the process.
        """
        while idx > 0:
            parent_index = (idx - 1) // 2
            if self.heap[parent_index] > self.heap[idx]:
                self.heap[parent_index], self.heap[idx] = self.heap[idx], self.heap[parent_index]
                idx = parent_index
            else:
                break

    def heapifyDown(self, idx) -> None:
        """
        Performs the heapify operation when top element is poped and swapped with the last element.
        Now the last element maybe the max element or not, is at root and compared with its left and right child at each level is swapped accordingly,
        and moves down to its correct position.
        """
        left_child = 2 * idx + 1
        right_child = 2 * idx + 2
        smallest = idx #assume the curr index is smallest

        if left_child < len(self.heap) and self.heap[left_child] < self.heap[smallest]:
            smallest = left_child
        if right_child < len(self.heap) and self.heap[right_child] < self.heap[smallest]:
            smallest = right_child
        if smallest != idx:
            # swap elements
            self.heap[smallest], self.heap[idx] = self.heap[idx], self.heap[smallest]
            #compare it recursively
            self.heapifyDown(smallest) 
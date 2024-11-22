from models import User

class MinHeapUser:
    """
    Class to create a min binary heap for user waitlist. Provides basic operations like push, poll/pop, size, isEmpty, heapifyUp & heapifyDown
    Also additional functionality to update any user priority and remove any specific user based on its id.
    """
    def __init__(self):
        self.heap = []  # start with an empty array

    def push(self, user: User):
        """
        Add a user node onto heap.
        """
        self.heap.append(user)
        self.heapifyUp(len(self.heap) - 1)

    def poll(self):
        """
        pops the top most/ min element (User Node) from the heap and returns it as well.
        If heap is empty returns None.
        """
        if len(self.heap) > 0:
            root = self.heap[0]
            self.heap[0] = self.heap[-1] #exchange with the last element, heapify down handles the structure later.
            self.heap.pop()  # after swapping, the last element is the min element or previous root.
            self.heapifyDown(0)
            return root
        return None

    def updatePriority(self, user_id, new_priority) -> bool:
        """
        function to update the priority for any specific user based on its userID
        """
        for i in range(len(self.heap)):
            if self.heap[i].userID == user_id:
                if self.heap[i].priority < new_priority:
                    self.heap[i].priority = new_priority
                    self.heapifyUp(i) #since priority is increased need to heapifyup the node again.
                else:
                    self.heap[i].priority = new_priority
                    self.heapifyDown(i) #since priority is decreased need to heapifydown the node again.
                
                return True
            
        return False

    def remove(self, user_id) -> bool:
        """
        function to remove any specific user based on userID from the waitlist/heap
        """
        for i in range(len(self.heap)):
            if self.heap[i].userID == user_id:
                self.heap[i] = self.heap[-1] #when matched found, swap with the last element.
                self.heap.pop() #pop the matched element from list
                self.heapifyDown(i) 
                return True
            
        return False
            

    def size(self) -> int:
        """
        returns current size of heap
        """
        return len(self.heap)

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
            if (self.heap[parent_index].priority < self.heap[idx].priority) or (self.heap[parent_index].priority == self.heap[idx].priority and (self.heap[parent_index].timeStamp - self.heap[idx].timeStamp > 0)):
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

        if (left_child < len(self.heap) and (self.heap[left_child].priority > self.heap[smallest].priority)) or (left_child < len(self.heap) and (self.heap[left_child].priority == self.heap[smallest].priority) and (self.heap[left_child].timeStamp - self.heap[smallest].timeStamp < 0)):
            smallest = left_child
        if (right_child < len(self.heap) and (self.heap[right_child].priority > self.heap[smallest].priority)) or (right_child < len(self.heap) and (self.heap[right_child].priority == self.heap[smallest].priority) and (self.heap[right_child].timeStamp - self.heap[smallest].timeStamp < 0)):
            smallest = right_child
        if smallest != idx:
            #swap elements
            self.heap[smallest], self.heap[idx] = self.heap[idx], self.heap[smallest]
             #compare it recursively
            self.heapifyDown(smallest)



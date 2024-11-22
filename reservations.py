from models import Booking

class RedBlackTree:
    def __init__(self) -> None:
        self.leaf = Booking(0, 0)  #node for null leaves
        self.leaf.color = 'B'  # leaves are always Black
        self.root = self.leaf


    def rotateLeft(self, x) -> None:
        """
        Perform a left rotation around node x.
        
        This operation changes the tree structure by rotating node x to the left.
        It is used to maintain the Red-Black Tree properties during insertion and deletion.
        """
        y = x.right
        x.right = y.left
        if y.left != self.leaf:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.leaf:
            self.root = y # If x is the root, y becomes the new root
        elif x == x.parent.left:
            x.parent.left = y # Make y the left child of x's parent
        else:
            x.parent.right = y  # Make y the right child of x's parent
        y.left = x
        x.parent = y


    def rotateRight(self, x) -> None:
        """
        Perform a right rotation around node x.
        
        This operation changes the tree structure by rotating node x to the right.
        It is used to maintain the Red-Black Tree properties during insertion and deletion.
        """
        y = x.left
        x.left = y.right
        if y.right != self.leaf:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == self.leaf:
            self.root = y  # If x is the root, y becomes the new root
        elif x == x.parent.right:
            x.parent.right = y  # Make y the right child of x's parent
        else:
            x.parent.left = y  # Make y the left child of x's parent
        y.right = x
        x.parent = y


    def search(self, node, user_id):
        """
        Search for a node with the given userID starting from the given node.
        
        This function performs a binary search in the tree. It returns the node 
        if found, or None if the userID does not exist in the tree.
        """
        if node == self.leaf:  
            return None
        elif node.userID == user_id: #match found
            return node
        elif user_id < node.userID:
            return self.search(node.left, user_id)
        else:
            return self.search(node.right, user_id)
        

    def addReservationHelper(self, k) -> None:
        """
        Fix any violations of Red-Black Tree properties after inserting a new node (k).
        
        This function ensures that the tree maintains its Red-Black properties
        after the insertion by performing rotations and recoloring as necessary.
        """
        while k != self.root and k.parent.color == "red":
            if k.parent == k.parent.parent.left:
                u = k.parent.parent.right  # uncle
                if u.color == "R":  # Case 1: Uncle is red
                    u.color = "B"
                    k.parent.color = "B"
                    k.parent.parent.color = "R"
                    k = k.parent.parent
                else: # Case 2: Uncle is black
                    if k == k.parent.right: # Case 2a: k is a right child
                        k = k.parent
                        self.rotateLeft(k)
                    k.parent.color = "B"  # Recolor parent to black
                    k.parent.parent.color = "R" # Recolor grandparent to red
                    self.rotateRight(k.parent.parent)
            else: # Parent is on the right side of the grandparent
                u = k.parent.parent.left #uncle
                if u.color == "R": # Case 1: Uncle is red
                    u.color = "B"
                    k.parent.color = "B"
                    k.parent.parent.color = "R"
                    k = k.parent.parent
                else:  # Case 2: Uncle is black
                    if k == k.parent.left:
                        k = k.parent
                        self.rotateRight(k)
                    k.parent.color = "B"
                    k.parent.parent.color = "R"
                    self.rotateLeft(k.parent.parent)
            if k == self.root: # If k is now the root, break the loop
                break
        self.root.color = "B" # Ensure the root is always black


    def addReservation(self, userID, seatID) -> None:
        """
        Insert a new reservation (node) into the Red-Black Tree.
        
        This function creates a new node for the reservation and inserts it into
        the tree while maintaining the Red-Black properties using the addReservationHelper.
        """
        node = Booking(userID, seatID) #create a new booking node, node is Red for insertion always by default.
        node.parent = None
        node.left = self.leaf
        node.right = self.leaf

        y = None
        x = self.root
        
        # Search for the correct spot in the Red-Black Tree for the new node
        while x != self.leaf:
            y = x  # Set the current node as the parent of the next node
            if node.userID < x.userID:
                x = x.left  # If the userID is smaller, move left in the tree
            else:
                x = x.right  # Otherwise, move right

        node.parent = y
        if y == None:
            self.root = node # If the tree was empty, the new node becomes the root
        elif node.userID < y.userID:
            y.left = node
        else:
            y.right = node

        # If the node's parent is None, we simply return because no balancing is needed (root node is black)
        if node.parent == None:
            node.color = "B"
            return

        if node.parent.parent == None:
            return

        # If the Red-Black Tree properties are violated (e.g., two consecutive red nodes), fix the tree
        self.addReservationHelper(node)


    def deleteReservationHelper(self, x):
        """
        Fix any violations of Red-Black Tree properties after deleting a node.
        
        This function ensures that the Red-Black properties are restored after deleting
        a node. It involves a series of rotations and recoloring to maintain the tree's balance.
        """
        while x != self.root and x.color == "B":
            if x == x.parent.left:
                sibling = x.parent.right
                if sibling.color == "R": # Case 1: Sibling is red
                    sibling.color = "B"
                    x.parent.color = "R"
                    self.rotateLeft(x.parent)
                    sibling = x.parent.right
                # Case 2: Sibling is black, and both children are black
                if sibling.left.color == "B" and sibling.right.color == "B":
                    sibling.color = "R"
                    x = x.parent
                else: # Case 3: Sibling's right child is black
                    if sibling.right.color == "B":
                        sibling.left.color = "B"
                        sibling.color = "R"
                        self.rotateRight(sibling)
                        sibling = x.parent.right
                    # Case 4: Sibling's right child is red
                    sibling.color = x.parent.color
                    x.parent.color = "B"
                    sibling.right.color = "B"
                    self.rotateLeft(x.parent)
                    x = self.root
            else: # If x is the right child of its parent (similar logic to the left side)
                sibling = x.parent.left
                if sibling.color == "R":
                    sibling.color = "B"
                    x.parent.color = "R"
                    self.rotateRight(x.parent)
                    sibling = x.parent.left
                if sibling.right.color == "B" and sibling.left.color == "B":
                    sibling.color = "R"
                    x = x.parent
                else:
                    if sibling.left.color == "B":
                        sibling.right.color = "B"
                        sibling.color = "R"
                        self.rotateLeft(sibling)
                        sibling = x.parent.left
                    sibling.color = x.parent.color
                    x.parent.color = "B"
                    sibling.left.color = "B"
                    self.rotateRight(x.parent)
                    x = self.root #move up to the root
        x.color = "B"  # Ensure x is black (if it is the root or any other black node)


    def maintainTreeChildren(self, node1, node2):
        """
        Adjust the parent-child relationships when a node is removed or replaced.
        
        This function ensures that after deletion or replacement of a node, 
        the tree structure is properly updated, especially the parent references.
        """
        if node1.parent == None:
            self.root = node2  # If node1 is the root, set the root to node2
            
        elif node1 == node1.parent.left:
            node1.parent.left = node2
        else:
            node1.parent.right = node2

        if node2 != self.leaf:
            node2.parent = node1.parent


    def inorderSuccessor(self, node):
        """
        Find the in-order successor of a given node.
        
        The in-order successor is the node that comes immediately after the given node
        in an in-order traversal of the tree. It is used in the delete operation to
        find the replacement for a deleted node.
        """
        while node.left != self.leaf: #keep on checking left nodes of the current node for next successor
            node = node.left
        return node
    

    def deleteReservation(self, node):
        """
        Delete a reservation (node) from the Red-Black Tree.
        
        This function deletes the node from the tree and ensures that the tree's Red-Black
        properties are maintained using rotations and color fixes.
        """
        y = node
        original_color = node.color # Save the original color of the node

        
        if node.left == self.leaf and node.right == self.leaf: # Case 1: Node has no children
            self.maintainTreeChildren(node, self.leaf)

        elif node.left == self.leaf: # Case 2: Node has one child (right child)
            x = node.right
            self.maintainTreeChildren(node, node.right)

        elif node.right == self.leaf: # Case 3: Node has one child (left child)
            x = node.left
            self.maintainTreeChildren(node, node.left)

        else: # Case 4: Node has two children
            y = self.inorderSuccessor(node.right) #find succesor
            original_color = y.color
            x = y.right
            
            if y.parent == node: # If the successor's parent is the node itself
                x.parent = y
            else:
                self.maintainTreeChildren(y, y.right) # Reassign the child pointers of y
                y.right = node.right
                y.right.parent = y

            self.maintainTreeChildren(node, y) # Replace node with its successor
            y.left = node.left
            y.left.parent = y
            y.color = node.color

        if original_color == "black": # If the node that was deleted was black, fix any violations
            self.deleteReservationHelper(x)


    def isEmpty(self):
        """
        Check if the Red-Black Tree is empty.
        
        Returns True if the tree is empty (i.e., the root is the sentinel leaf node),
        otherwise returns False.
        """
        if self.root == self.leaf:
            return True
        
        return False
    

    def inorder(self, root, bookings):
        """
        Perform an in-order traversal of the Red-Black Tree and store the booking information.
        
        This function appends the seatID and userID of each node to the bookings list.
        """
        if root != self.leaf:
            self.inorder(root.left,bookings)
            bookings.append([root.seatID, root.userID])
            self.inorder(root.right,bookings)


# if __name__ == "__main__":
#     rbt = RedBlackTree()
#     rbt.addReservation(1,1)
#     rbt.addReservation(2,2)
#     rbt.addReservation(3,3)
#     node1 = rbt.search(rbt.root, 3)
#     rbt.deleteReservation(node1)
#     rbt.addReservation(5,3)
#     rbt.addReservation(4,4)
#     rbt.addReservation(6,5)
#     rbt.addReservation(8,6)
#     rbt.addReservation(7,7)
#     node1 = rbt.search(rbt.root, 1)
#     print(node1.userID)
#     rbt.deleteReservation(node1)
#     node1 = rbt.search(rbt.root, 2)
#     print(node1.userID)
#     rbt.deleteReservation(node1)
#     print("Cop")
#     node1 = rbt.search(rbt.root, 3)
#     # print(node1.userID)
#     rbt.deleteReservation(node1)
#     node1 = rbt.search(rbt.root, 4)
#     print(node1.userID)
#     rbt.deleteReservation(node1)
#     # rbt.addReservation(5,6)
#     # rbt.addReservation(1,7)
#     # rbt.addReservation(9,10)
#     # rbt.addReservation(18,11)
#     bookings = []
#     rbt.inorder(rbt.root, bookings)
#     print(bookings)
#     # print(rbt.root.userID)
#     # print(rbt.root.parent)
#     # node1 = rbt.search(rbt.root, 3)
#     # # node2 = rbt.search(rbt.root, 9)
#     # rbt.deleteReservation(node1)
#     # # rbt.deleteReservation(node2)
#     # bookings = []
#     # rbt.inorder(rbt.root, bookings)
#     # print(bookings)
class User:
    def __init__(self, uuid, score):
        self.uuid = uuid
        self.score = score

    def __eq__(self, other):
        return self.score == other.score and self.uuid == other.uuid
    
    def __lt__(self, other):
        return self.score < other.score

    def __repr__(self):
        return f"User(id={self.uuid}, score={self.score})"


class Node:
    def __init__(self, user):
        self.user = user  # Store the user object
        self.left = None
        self.right = None
        self.center = [user]  # Store duplicates here
        self.height = 1


class Leaderboard:
    def __init__(self):
        self.root = None

        self.users = {}

        self.treesize = 0


    def insert(self, user: User):
        
        if user.uuid not in self.users:
            self.treesize += 1


        self.users[user.uuid] = user
        self.root = self._insert(self.root, user)

    
    def _insert(self, root, user):
        if not root:
            return Node(user)
        
        # Case for duplicate score (same score, different user)
        if user.score == root.user.score:
            root.center.append(user)  # Add to the center list
            return root
        
        # Standard AVL insertion logic
        if user < root.user:
            root.left = self._insert(root.left, user)
        else:
            root.right = self._insert(root.right, user)
        
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        return self.balance(root)

    def delete(self, user):
        self.root = self._delete(self.root, user)
    
    def _delete(self, root, user):
        if not root:
            return root
        
        if user < root.user:
            root.left = self._delete(root.left, user)
        elif user > root.user:
            root.right = self._delete(root.right, user)
        else:
            # Case 1: Node has duplicates in the center list
            if user in root.center:
                root.center.remove(user)  # Remove one occurrence of the user
                if root.center:  # If there are still duplicates, no further deletion is needed
                    return root
            
            # Case 2: No more duplicates, proceed with standard deletion
            if not root.left:
                return root.right
            elif not root.right:
                return root.left
            
            temp = self.get_min_value_node(root.right)
            root.user = temp.user
            root.center = temp.center  # Copy the center list
            root.right = self._delete(root.right, temp.user)
        
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        return self.balance(root)

    def balance(self, root):
        balance_factor = self.get_balance(root)
        if balance_factor > 1:
            if self.get_balance(root.left) < 0:
                root.left = self.rotate_left(root.left)
            return self.rotate_right(root)
        if balance_factor < -1:
            if self.get_balance(root.right) > 0:
                root.right = self.rotate_right(root.right)
            return self.rotate_left(root)
        return root

    def rotate_left(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def rotate_right(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def get_height(self, root):
        return root.height if root else 0

    def get_balance(self, root):
        return self.get_height(root.left) - self.get_height(root.right) if root else 0

    def get_min_value_node(self, root, acknowledge_center=False):
        while root.left:
            root = root.left
        if acknowledge_center:
            print(root.center)
            return root.center[-1]
        return root

    def get_max_value_node(self, root, acknowledge_center=False):
        while root.right:
            root = root.right
        if acknowledge_center:
            return root.center[0]
        return root

    def find_predecessor(self, user):
        current = self.root
        predecessor = None
        
        while current:
            if user < current.user:
                current = current.left
            elif user > current.user:
                predecessor = current
                current = current.right
            else:  # user == current.user
                    
                index_in_center = current.center.index(user)

                if index_in_center > 0:
                    predecessor = current.center[index_in_center - 1]
                else:
                    if current.left:
                        predecessor = self.get_max_value_node(current.left, acknowledge_center=True)
                break



                
        # # If we haven't found a predecessor yet, it means it's the first in its group
        # if predecessor and predecessor == user:
        #     predecessor = None

        if isinstance(predecessor, Node):
            predecessor = predecessor.center[-1]
        return predecessor

    # Find successor of the user object
    def find_successor(self, user):
        current = self.root
        successor = None
        
        while current:
            if user < current.user:
                successor = current
                current = current.left
            elif user > current.user:
                current = current.right
            else:  # user == current.user

                index_in_center = current.center.index(user)
                
                assert current.center[index_in_center] == user

                if index_in_center < len(current.center) - 1:
                    successor = current.center[index_in_center + 1]
                else:
                    if current.right:
                        successor = self.get_min_value_node(current.right, acknowledge_center=True)
                break
        

        if isinstance(successor, Node):
            successor = successor.center[0]
        return successor


    def inorder_traversal(self):
        return self._inorder_traversal(self.root)

    def _inorder_traversal(self, root):
        return self._inorder_traversal(root.left) + root.center + self._inorder_traversal(root.right) if root else []

    def adjacent(self, user: str | User):
        if isinstance(user, str):
            user = self.users[user]

        return self.find_predecessor(user), self.find_successor(user)
    
    def update(self, user: str | User, new_score: int):
        if isinstance(user, str):
            user = self.users[user]
        self.delete(user)
        user.score = new_score
        self.insert(user)

    def top_ten(self):
        result = []
        self._get_top_n(self.root, result, 10)
        return result

    def _get_top_n(self, node, result, n):
        if node and len(result) < n:
            self._get_top_n(node.right, result, n)
            if len(result) < n:
                # result.append(node.user)
                result.extend(node.center[::-1][:n - len(result)])
            self._get_top_n(node.left, result, n)

    def get_rank(self, user: str | User):
        if isinstance(user, str):
            user = self.users[user]
        return self.treesize - self._get_rank(self.root, user) + 1

    def _get_rank(self, node, user):
        if not node:
            return 0

        if user < node.user:
            return self._get_rank(node.left, user)
        
        left_size = self._get_size(node.left)
        if user == node.user:
            return left_size + 1  # Rank starts at 1 (not zero-indexed)

        return left_size + len(node.center) + self._get_rank(node.right, user)

    def _get_size(self, node):
        if not node:
            return 0
        return self._get_size(node.left) + self._get_size(node.right) + len(node.center)



if __name__ == "__main__":
    lb = Leaderboard()
    lb.insert(User("a", 10))
    lb.insert(User("b", 20))
    lb.insert(User("c", 30))
    lb.insert(User("d", 20))

    print(lb.top_ten())
    print(lb.get_rank("c"))
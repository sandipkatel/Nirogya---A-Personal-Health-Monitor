class AVLNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _rotate_right(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))

        return x

    def _rotate_left(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _insert(self, node, data):
        if not node:
            return AVLNode(data)
        
        if data< node.data:
            node.left = self._insert(node.left, data)
        else:
            node.right = self._insert(node.right, data)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        balance = self._get_balance(node)

        if balance > 1 and data < node.left.data:
            return self._rotate_right(node)

        if balance < -1 and data > node.right.data:
            return self._rotate_left(node)

        if balance > 1 and data > node.left.data:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        if balance < -1 and data < node.right.data:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def insert(self, data):
        self.root = self._insert(self.root, data)

    def _inorder_traversal(self, node, result):
        if node:
            self._inorder_traversal(node.left, result)
            result.append(node.data)
            self._inorder_traversal(node.right, result)

    def _inorder_traversal_search(self, node, term):
        if node == None or node.data[0] == term:
            return node.data
        elif term < node.data[0]:
            return self._inorder_traversal_search(node.left, term)
        else:
            return self._inorder_traversal_search(node.right, term)
        
    def get_data(self):
        result = []
        self._inorder_traversal(self.root, result)
        return result

    def search_data(self, data_index):
        return self._inorder_traversal_search(self.root, data_index)

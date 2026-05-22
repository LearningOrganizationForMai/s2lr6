class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def height(self, n):
        return n.height if n else 0

    def update(self, n):
        n.height = 1 + max(self.height(n.left), self.height(n.right))

    def balance(self, n):
        return self.height(n.left) - self.height(n.right)

    def rotate_right(self, y):
        x = y.left
        y.left = x.right
        x.right = y
        self.update(y)
        self.update(x)
        return x

    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        self.update(x)
        self.update(y)
        return y

    def insert(self, node, key):
        if not node:
            return AVLNode(key)
        if key < node.key:
            node.left = self.insert(node.left, key)
        elif key > node.key:
            node.right = self.insert(node.right, key)
        else:
            return node
        self.update(node)
        b = self.balance(node)
        if b > 1 and key < node.left.key:
            return self.rotate_right(node)
        if b < -1 and key > node.right.key:
            return self.rotate_left(node)
        if b > 1 and key > node.left.key:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if b < -1 and key < node.right.key:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        return node

    def min_node(self, node):
        while node.left:
            node = node.left
        return node

    def delete(self, node, key):
        if not node:
            return node
        if key < node.key:
            node.left = self.delete(node.left, key)
        elif key > node.key:
            node.right = self.delete(node.right, key)
        else:
            if not node.left:
                return node.right
            if not node.right:
                return node.left
            tmp = self.min_node(node.right)
            node.key = tmp.key
            node.right = self.delete(node.right, tmp.key)
        self.update(node)
        b = self.balance(node)
        if b > 1 and self.balance(node.left) >= 0:
            return self.rotate_right(node)
        if b > 1 and self.balance(node.left) < 0:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if b < -1 and self.balance(node.right) <= 0:
            return self.rotate_left(node)
        if b < -1 and self.balance(node.right) > 0:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        return node

    def inorder(self, node, res):
        if node:
            self.inorder(node.left, res)
            res.append(node.key)
            self.inorder(node.right, res)

class RBNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None
        self.red = True

class RBTree:
    def __init__(self):
        self.root = None

    def is_red(self, node):
        return node is not None and node.red

    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left:
            y.left.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def rotate_right(self, y):
        x = y.left
        y.left = x.right
        if x.right:
            x.right.parent = y
        x.parent = y.parent
        if not y.parent:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

    def insert_fix(self, node):
        while node != self.root and node.parent.red:
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if self.is_red(uncle):
                    node.parent.red = False
                    uncle.red = False
                    node.parent.parent.red = True
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.rotate_left(node)
                    node.parent.red = False
                    node.parent.parent.red = True
                    self.rotate_right(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if self.is_red(uncle):
                    node.parent.red = False
                    uncle.red = False
                    node.parent.parent.red = True
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.rotate_right(node)
                    node.parent.red = False
                    node.parent.parent.red = True
                    self.rotate_left(node.parent.parent)
        self.root.red = False

    def insert(self, key):
        node = RBNode(key)
        parent = None
        cur = self.root
        while cur:
            parent = cur
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                cur = cur.right
            else:
                return
        node.parent = parent
        if not parent:
            self.root = node
        elif key < parent.key:
            parent.left = node
        else:
            parent.right = node
        self.insert_fix(node)

    def transplant(self, u, v):
        if not u.parent:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    def find_min(self, node):
        while node.left:
            node = node.left
        return node

    def delete_fix(self, node):
        while node != self.root and not node.red:
            if node == node.parent.left:
                sib = node.parent.right
                if self.is_red(sib):
                    sib.red = False
                    node.parent.red = True
                    self.rotate_left(node.parent)
                    sib = node.parent.right
                if not self.is_red(sib.left) and not self.is_red(sib.right):
                    sib.red = True
                    node = node.parent
                else:
                    if not self.is_red(sib.right):
                        sib.left.red = False
                        sib.red = True
                        self.rotate_right(sib)
                        sib = node.parent.right
                    sib.red = node.parent.red
                    node.parent.red = False
                    sib.right.red = False
                    self.rotate_left(node.parent)
                    node = self.root
            else:
                sib = node.parent.left
                if self.is_red(sib):
                    sib.red = False
                    node.parent.red = True
                    self.rotate_right(node.parent)
                    sib = node.parent.left
                if not self.is_red(sib.right) and not self.is_red(sib.left):
                    sib.red = True
                    node = node.parent
                else:
                    if not self.is_red(sib.left):
                        sib.right.red = False
                        sib.red = True
                        self.rotate_left(sib)
                        sib = node.parent.left
                    sib.red = node.parent.red
                    node.parent.red = False
                    sib.left.red = False
                    self.rotate_right(node.parent)
                    node = self.root
        node.red = False

    def delete(self, key):
        node = self.root
        while node and node.key != key:
            if key < node.key:
                node = node.left
            else:
                node = node.right
        if not node:
            return
        y = node
        y_red = y.red
        if not node.left:
            x = node.right
            self.transplant(node, node.right)
        elif not node.right:
            x = node.left
            self.transplant(node, node.left)
        else:
            y = self.find_min(node.right)
            y_red = y.red
            x = y.right
            if y.parent == node:
                if x:
                    x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = node.right
                y.right.parent = y
            self.transplant(node, y)
            y.left = node.left
            y.left.parent = y
            y.red = node.red
        if not y_red and x:
            self.delete_fix(x)

    def inorder(self, node, res):
        if node:
            self.inorder(node.left, res)
            res.append(node.key)
            self.inorder(node.right, res)

print("AVL дерево")
avl = AVLTree()
root = None
for k in [10, 20, 30, 40, 50, 25]:
    root = avl.insert(root, k)
res1 = []
avl.inorder(root, res1)
print("Начальное дерево:", res1)
root = avl.delete(root, 30)
res2 = []
avl.inorder(root, res2)
print("Дерево после удаления 30:", res2)

print("Красно-черное дерево")
rb = RBTree()
for k in [10, 20, 30, 40, 50, 25]:
    rb.insert(k)
res3 = []
rb.inorder(rb.root, res3)
print("Начальное дерево", res3)
rb.delete(30)
res4 = []
rb.inorder(rb.root, res4)
print("Дерево после удаления 30", res4)

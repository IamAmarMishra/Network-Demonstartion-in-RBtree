class NilNode(object):
    def __init__(self):
        self.red = False

NIL = NilNode() 

class RBNode(object):
    def __init__(self,data):
        self.red = True
        self.parent = None
        self.data = data
        self.left = NIL
        self.right = NIL

class RedBlackTree(object):
    def __init__(self):
        self.root = None
        self.size =0
    def add(self,data,curr = None):
        self.size += 1
        new_node = RBNode(data)
        # Base Case - Nothing in the tree
        if self.root == None:
            new_node.red = False
            self.root = new_node
            return
        
        # Search to find the node's correct place
        currentNode = self.root
        while currentNode != NIL:
            potentialParent = currentNode
            if new_node.data < currentNode.data:
                currentNode = currentNode.left
            else:
                currentNode = currentNode.right
                
        # Assign parents and siblings to the new node
        new_node.parent = potentialParent
        if new_node.data < new_node.parent.data:
            new_node.parent.left = new_node
        else:
            new_node.parent.right = new_node
        self.fix_tree_after_add(new_node)

    def contains(self,data, curr=None):
        if curr == None:
            curr = self.root
        while curr != NIL and data != curr.data:
            if data < curr.data:
                curr = curr.left
            else:
                curr = curr.right
        return curr

    def fix_tree_after_add(self,new_node):
        #print("Tree is being fixed!")
        while new_node != self.root and new_node.parent.red == True:
            if new_node.parent == new_node.parent.parent.left:
                uncle = new_node.parent.parent.right
                if uncle.red:
                    # This is Case 1
                    new_node.parent.red = False
                    uncle.red = False
                    new_node.parent.parent.red = True
                    new_node = new_node.parent.parent
                else:
                    if new_node == new_node.parent.right:
                        # This is Case 2
                        new_node = new_node.parent
                        self.left_rotate(new_node)
                    # This is Case 3
                    new_node.parent.red = False
                    new_node.parent.parent.red = True
                    self.right_rotate(new_node.parent.parent)
            else:
                uncle = new_node.parent.parent.left
                if uncle.red:
                    # Case 1
                    new_node.parent.red = False
                    uncle.red = False
                    new_node.parent.parent.red = True
                    new_node = new_node.parent.parent
                else:
                    if new_node == new_node.parent.left:
                        # Case 2
                        new_node = new_node.parent
                        self.right_rotate(new_node)
                    # Case 3
                    new_node.parent.red = False
                    new_node.parent.parent.red = True
                    self.left_rotate(new_node.parent.parent)
        self.root.red = False



    def delete(self):
        pass
    
    def left_rotate(self,x):
        y = x.right
        x.right = y.left
        if y.left != NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        else:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self,x):
        y = x.left
        x.left = y.right
        # Turn sibling's left subtree into node's right subtree
        if y.right != NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        else:
            if x == x.parent.right:
                x.parent.right = y
            else:
                x.parent.left = y
        y.right = x
        x.parent = y

    def get_all_nodes(self):
        pass
    
    def is_red(self):
        return self.root != None and self.root.red == 1;
    
    def is_black(self):
        return self.root != None and self.root.black == 1;
    
def LevelOrder(root):
    levels = []
    levels.append([root.data])
    queue = [root]
    count = 2
    temp = 0
    arr = []
    level_node = {}
    level_node[root.data] = 0
    level = 1
    while queue != []:
        if temp == count:
            temp = 0
            count *= 2
            levels.append(arr)
            arr = []
            level += 1
        root = queue.pop(0)
        if root.left != NIL:
            queue.append(root.left)
            arr.append(root.left.data)
            level_node[root.left.data] = level
        if root.right != NIL:
            queue.append(root.right)
            arr.append(root.right.data)
            level_node[root.right.data] = level
        temp += 2
    if arr != []:
        levels.append(arr)
    return (levels,level_node)
    
        
def Display(root):
    if root != NIL:
        Display(root.left)
        print(root.data,end='\t')
        if root.parent is not None:
            print(root.parent.data,end='\t')
        else:
            print('root',end='\t')
        if root.left != NIL:
            print(root.left.data,end='\t\t')
        else:
            print('__',end='\t\t')
        if root.right != NIL:
            print(root.right.data,end='\t\t')
        else:
            print('__',end='\t\t')
        if root.red:
            print('RED')
        else:
            print('BLACK')
        Display(root.right)
        
def TracePath(root,key,return_type=True):
    path = []
    while root != NIL:
        if key < root.data:
            path.append(root.data)
            root = root.left
        elif key > root.data:
            path.append(root.data)
            root = root.right
        else:
            break
    if return_type:
        return path
    return root

if __name__ == "__main__":
    tree = RedBlackTree()
    print('Enter the values of nodes: ',end='')
    arr = list(map(int,input().split()))
    for i in arr:
        tree.add(i)
    print()
    print('The constructed RB tree is...')
    print('Node\tParent\tLeft Child\tRight Child\tColor')
    Display(tree.root)
    
    print()
    print('Nodes present at each levels are..')
    (levels,level_node) = LevelOrder(tree.root)
    for i in range(len(levels)):
        print(i,'->',levels[i])
    
    while True:
        print('\nEnter the value of crashed node or type any character to terminate: ',end='')
        try:
            key = int(input())
        except ValueError:
            print('Terminated')
            break
        level = level_node[key]
        if level == len(levels)-1:
            print('\nThe crashed node',key,'is prsent at last level and no remaining nodes below it.')
        else:
            print('\nThe crashed node',key,'is present at level',level,'and there are still',len(levels)-level-1,'levels below it.')
            node = TracePath(tree.root,key,False)
            nodes_at_level = levels[level+1]
            left_data = right_data = 0
            if node.left != NIL:
                left_data = node.left.data
            if node.right != NIL:
                right_data = node.right.data
            key = -999
            for i in nodes_at_level:
                if i != left_data and i != right_data:
                    key = i
                    break
            if key == -999:
                print('No possible path to reach level',level+1)
            else:
                print('The possible the path to reach level',level+1,'is...')
                path = TracePath(tree.root,key)
                for i in path:
                    print(i,end='-->')
                print(key)
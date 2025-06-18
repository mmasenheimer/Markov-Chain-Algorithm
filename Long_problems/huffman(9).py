'''
This program takes an input file based on a preorder
and inorder traversals of a tree and then constructs and uses the tree 
to decode an encoded sequence of values. The program then outputs the postorder
traversal of the tree along with the decoded sequence.
'''

class Tree:
    '''
    This class represents a tree of integer values as each node.

    The class defines methods for returning the value of a node,
    the left and right nodes, and also defines methods for
    inserting a new node at the right and the left.
    '''
    def __init__(self,value):
        '''
        The init method initializes a node and sets the left
        and right children to None.
        
        Parameters: value is an integer value.
        '''
        self._value = value
        self._left = None
        self._right = None

    def value(self):
        return self._value

    def left(self):
        return self._left

    def right(self):
        return self._right

    def insert_right(self, value):
        '''
        This method inserts a value in the right side of the tree.
        It does so by first checking if _right is None on the
        right side before adding the value (after creating a new node
        for it).
        
        Parameters: value is an integer value.
        '''
        if self._right == None:
            self._right = Tree(value)
            # Add new node if there is no right value
        else:
            current = Tree(value)
            current._right = self._right
            self._right = current
            # Otherwise add the node on the right

    def insert_left(self, value):
        '''
        This method inserts a value in the left side of the tree.
        It does so by first checking if _left is None on the
        right side before adding the value (after creating a new node
        for it).
        
        Parameters: value is an integer value.
        '''
        if self._left == None:
            self._left = Tree(value)
            # Add new node if there is no left value
        else:
            current = Tree(value)
            current._left = self._left
            self._left = current
            # Otherwise add the node on the left

def buildTree(preorder, inorder):
    '''
    This function takes the inorder and preorder traversal
    of the tree (from the input file), and contructs the tree
    using the above tree clas and recursion.
    
    Parameters: preorder is a list of the preorder traversal of the
    tree and inorder is a list of the inorder traversal of the tree.
    
    Returns: The root of the tree.
    '''
    if not preorder or not inorder:
        return None
        # Base case after traversing the in and pre lists
    
    root_val = preorder[0]
    root = Tree(root_val)
    # Create a node for the root (the first value in preorder traversal)

    root_index_in_inorder = inorder.index(root_val)
    # Find the index of the root in the inorder to contruct the tree

    left_subtree = buildTree(preorder[1:root_index_in_inorder+1], 
        inorder[:root_index_in_inorder])
    # Recursive call to build the left subtree
    
    right_subtree = buildTree(preorder[root_index_in_inorder+1:], 
        inorder[root_index_in_inorder+1:])
    # Recursive call to build the right subtree

    if left_subtree:
        root.insert_left(left_subtree._value)
        root._left = left_subtree
        # Insert the root node of the left subtree

    if right_subtree:
        root.insert_right(right_subtree._value)
        root._right = right_subtree
        # Insert the root node of the right subtree

    return root

def decode(root, values):
    '''
    This function takes in a tree and a list of encoded values. It
    iterates over every item in values, traversing left on the tree
    if the current item is a 0 and right if the item is a 1. It iterates
    until there are no more values in values, repeating the traversal when
    we hit a leaf node.
    
    Parameters: root is the root of a tree of integers, values is a list
    of 1s and 0s which show how to traverse the tree to decode the sequence.

    Returns: A string of the decoded value.
    '''
    current_node = root
    result = ''
    # Return the result in a string form

    for item in values:
        if item == 0:
            if current_node._left == None:
                return result
                # End traversal here if there is no left child
            current_node = current_node._left

        elif item == 1:
            if current_node._right == None:
                return result
                # End traversal here if there is no right child
            current_node = current_node._right

        else:
            return result
            # Otherwise return the result string
        
        if current_node._left == None and current_node._right == None:
            # Checks if the node is a leaf node and add to the final string
            result += str(current_node._value)
            current_node = root
            # Reset the node to the root for more traversal
    return result

def postorder(tree):
    '''
    This function takes in a tree and uses recursion to return a 
    string of the postorder traversal of the tree.

    Parameters: tree is a tree.

    Returns: A string of the postorder traversal of the nodes.
    '''
    if tree == None:
        return ''
        # Base case after going over the tree
    
    left_values = postorder(tree.left())
    right_values = postorder(tree.right())
    # Recursion on the left and rihgt side of the tree
    
    result = (left_values + ' ' + right_values).strip()
    return (result + ' ' + str(tree.value())).strip()
    # Adding the value to the string after recursion for postorder

def str_to_int(alist):
    '''
    This is a helper function intended to help convert items
    in a list to integers.
    
    Parameters: alist is a list of strings.
    
    Returns: A new list with integer indices.
    '''

    newlist = []

    for item in alist:
        newlist.append(int(item))
        # Converting to integers
    return newlist

def read_input():
    '''
    This function handles all of the function navigation and 
    inputs of the file. It takes a file input and opens it, formatting
    the pre and inoder traversals to be plugged into the tree
    builder function. It then decodes and prints out the decoded
    item and the postorder traversal of the tree.
    '''

    file = input("Input file: ")
    openfile = open(file, "r")
    
    newl = []

    for line in openfile:
        if " " in line.strip():
            # Checking if it is a traversal
            newl.append(str_to_int(line.strip().split(" ")))
        else:
            # Otherwise it must be the encoded item
            digits = []
            for digit in line.strip():
                digits.append(int(digit))
                # Splitting the big "number" into items in a list
            newl.append(digits)
    
    thetree = buildTree(newl[0], newl[1])
    tree_decoding = decode(thetree, newl[2])
    post_order_str = postorder(thetree)
    # Building the tree, decoding, and getting postorder

    openfile.close()
    print(post_order_str)
    print(tree_decoding)
    # Printing out the final values

def main():
    read_input()
main()
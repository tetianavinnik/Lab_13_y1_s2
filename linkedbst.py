"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
# from linkedqueue import LinkedQueue
from math import log
import random
import time


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)


    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node != None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)


    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)


    def left(self, position):
        """Return a Position representing p's left child.
        Return None if p does not have a left child.
        """
        if position.left:
            return position.left
        return None


    def right(self, position):
        """Return a Position representing p's right child.
        Return None if p does not have a right child.
        """
        if position.right:
            return position.right
        return None


    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None


    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)


    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None


    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None


    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None


    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""


        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)


    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0


    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1


    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            lift_max_in_left(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed


    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None


    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        return self.height1(self._root)


    def height1(self, top):
        '''
        Helper function
        :param top:
        :return:
        '''
        if self.is_leaf(top):
            return 0
        else:
            return 1 + max(self.height1(child) for child in self.children(top))


    def is_leaf(self, position):
        """
        Check if node is a leaf.
        """
        if position.left or position.right:
            return False
        return True


    def children(self, position):
        """
        Generate an iteration of Positions representing p's children.
        """
        if self.left(position) is not None:
            yield self.left(position)
        if self.right(position) is not None:
            yield self.right(position)


    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        nodes = self.num_of_nodes()
        height = self.height()
        return height < 2*log(nodes+1, 2) - 1


    def num_of_nodes(self):
        """
        Return number of nodes.
        """
        if not self.isEmpty():
            counter = 0
            for _ in self:
                counter += 1
            return counter
        return 0


    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        lst = list(self.inorder())
        return lst[lst.index(low):lst.index(high)+1]\
               if low in self and high in self else None


    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        def recursion(lst):
            while lst and lst[len(lst)//2] not in self:
                self.add(lst[len(lst)//2])
                recursion(lst[:len(lst)//2])
                recursion(lst[len(lst)//2+1:])

        if not self.isEmpty() and not self.is_balanced():
            lst = list(self.inorder())
            self.clear()
            recursion(lst)


    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        lst = list(self.inorder())
        if item in self:
            index = lst.index(item) + 1
            return lst[index] if index < len(lst) - 1 else None
        else:
            for i in lst:
                if i > item:
                    return i
        return None


    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        lst = list(self.inorder())
        if item in self:
            index = lst.index(item) - 1
            return lst[index] if index >= 0 else None
        else:
            for i in lst[::-1]:
                if i < item:
                    return i
        return None


    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        with open(path, 'r') as file:
            lst = file.read().split('\n')
            random_words = sorted([random.choice(lst) for _ in range(10000)])
            new_random = list(set(random_words))
            print('List search: ', self._list_search(random_words, new_random))

            tree = LinkedBST()
            for i in random_words:
                tree.new_add(i)
            print('Binary tree (ordered): ', self._bintree(tree, new_random))

            tree = LinkedBST(list(set(lst)))
            print('Binary tree (unordered): ', self._bintree(tree, new_random))

            tree.rebalance()
            print('Binary tree (rebalanced): ', self._bintree(tree, new_random))


    def _list_search(self, lst_of_words, lst_to_find):
        """
        List search.
        """
        start = time.time()
        for i in lst_to_find:
            _ = lst_of_words.index(i)
        finish = time.time()
        return finish - start


    def _bintree(self, tree, lst_to_find):
        """
        Binary tree search.
        """
        start = time.time()
        for i in lst_to_find:
            _ = tree.new_find(i)
        finish = time.time()
        return finish - start


    def new_add(self, item):
        """
        Add item to tree.
        """
        newnode = BSTNode(item)
        x = self._root
        y = None

        while (x != None):
            y = x
            if (item < x.data):
                x = x.left
            else:
                x = x.right
        if (y == None):
            self._root = newnode
        elif (item < y.data):
            y.left = newnode
        else:
            y.right = newnode
        self._size += 1


    def new_find(self, item):
        """
        Find elements in tree (without recursion).
        """
        node = self._root
        while node.data != item and node != None:
            if node.data > item:
                node = node.left
            elif node.data < item:
                node = node.right
        if node == None:
            return None
        return node.data

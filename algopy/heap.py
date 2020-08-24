# -*- coding: utf-8 -*-
"""
Heap for students (first year)
November 2017
@author: Nathalie

Heaps are represented using the hierarchical numbering
    H[1] contains the root
    if H[i] is the current node:
        H[2*i] contains its left child
        H[2*i+1] contains its right child
    H[0] is unused

Elements in heaps are pairs (value, elt) where 
    - value is used for the priority (numeral type)
    - elt can be of any type
"""

class Heap:
    def __init__(self):
        """Init heap."""

        self.elts = [None]
            

    def isempty(self):
        """Check whether heap is empty.

        Returns:
            bool: True if heap is empty, False otherwise.

        """
        return len(self.elts) == 1

    def push(self, x):
        """Add an element to the heap.

        Args:
            x (value, elt): pair to enqueue.

        Returns:
            Heap: The updated heap.

        """
        self.elts.append(x)
        i = len(self.elts)-1
        while (i > 1) and x[0] < self.elts[i//2][0]:
            (self.elts[i], self.elts[i//2]) = (self.elts[i//2], self.elts[i])
            i = i // 2
        return self
    
    def pop(self):
        """Remove and return first element from the heap.

        Returns:
            (num, any): Element from the queue.

        Raises:
            IndexError: If heap is empty.

        """
        e = self.elts[1]
        self.elts[1] = self.elts[len(self.elts)-1]
        self.elts.pop()
        n = len(self.elts)-1
        ok = False
        i = 1    
        while (i <= n // 2) and not ok:
            j = 2 * i
            if (j + 1 <= n) and (self.elts[j+1][0] < self.elts[j][0]):
                j = j + 1
            if self.elts[i][0] > self.elts[j][0]:
                (self.elts[i], self.elts[j]) = (self.elts[j], self.elts[i])
                i = j
            else:
                ok = True
        return e

"""
My implementation of a Min-Heap using an array (list).
I’m following the assignment rules:
- No imports
- No break/continue/pass
- Try to keep one return per method
- Explain everything with comments
"""

class MinHeap:
    def __init__(self):
        # I’m keeping two things:
        # _heap is the underlying list storing all values
        # _count tracks how many items are actually in the heap (logical size)
        self._heap = []
        self._count = 0

    # ----------- index helpers -----------
    # These functions let me find parent/child positions
    # based on where an element is in the list.

    def _left_child(self, parent_index):
        return 2 * parent_index + 1

    def _right_child(self, parent_index):
        return 2 * (parent_index + 1)

    def _parent(self, child_index):
        return (child_index - 1) // 2

    # ----------- swap helper -----------
    def _swap(self, i, j):
        # Swap two items inside the array if they’re not the same index
        if i != j:
            temp = self._heap[i]
            self._heap[i] = self._heap[j]
            self._heap[j] = temp

    # ----------- heap repair helpers -----------

    def _sift_up(self, index):
        # Used after inserting at the end.
        # If the new item is smaller than its parent, keep swapping upward.
        while index > 0 and self._heap[self._parent(index)] > self._heap[index]:
            p = self._parent(index)
            self._swap(p, index)
            index = p  # move up to parent

    def _sift_down(self, index):
        # Used after removing the root and moving last element to the top.
        # Compare the node with its children, and if it’s bigger than one,
        # swap it with the smaller child. Keep going until no fixes are needed.
        keep_checking = True
        while keep_checking:
            left = self._left_child(index)
            right = self._right_child(index)
            smallest = index

            if left < self._count and self._heap[left] < self._heap[smallest]:
                smallest = left
            if right < self._count and self._heap[right] < self._heap[smallest]:
                smallest = right

            if smallest != index:
                self._swap(index, smallest)
                index = smallest
                keep_checking = True
            else:
                # No violation found, stop here.
                keep_checking = False

    # ----------- public methods -----------

    def add(self, text):
        """
        Insert a new element.
        - Put it at the next available slot
        - Increase counter
        - Repair heap going upwards
        """
        if self._count == len(self._heap):
            # list is full, append at the end
            self._heap.append(text)
        else:
            # reuse slot if available
            self._heap[self._count] = text

        self._count += 1
        self._sift_up(self._count - 1)

    def remove(self):
        """
        Remove and return the smallest element (root).
        Steps:
        1. Save the root (smallest element).
        2. Move the last element to root.
        3. Physically pop the last element off the list.
        4. Decrease counter.
        5. Repair heap going down.
        """
        result = None
        if self._count > 0:
            result = self._heap[0]

            self._count -= 1  # shrink logical size

            if self._count > 0:
                last_value = self._heap[self._count]
                self._heap[0] = last_value

            # remove duplicate tail element
            self._heap.pop()

            if self._count > 0:
                self._sift_down(0)
        return result

    def peek(self):
        # Look at the smallest element without removing it.
        value = None
        if self._count > 0:
            value = self._heap[0]
        return value

    def size(self):
        # Just return how many items are in the heap.
        return self._count

    # ----------- helpers for me (not required) -----------

    def _heap_array_snapshot(self):
        # Show the internal heap as a tuple (for testing/debugging).
        return tuple(self._heap[:self._count])

    def _is_min_heap(self):
        # Quick check: is the heap property valid everywhere?
        i = 0
        ok = True
        while ok and i < self._count:
            left = self._left_child(i)
            right = self._right_child(i)
            if left < self._count and self._heap[i] > self._heap[left]:
                ok = False
            else:
                if right < self._count and self._heap[i] > self._heap[right]:
                    ok = False
            i += 1
        return ok


# --- quick sanity tests ---

h = MinHeap()

# Insert several strings out of order.
for word in ["pear", "apple", "banana", "apricot", "grape", "kiwi", "plum", "apple"]:
    h.add(word)

# Basic checks
assert h.size() == 8, "size should be 8 after 8 inserts"
assert h.peek() == "apple", "peek should be lexicographically smallest"
assert h._is_min_heap(), "heap property must hold after insertions"

# Remove all, verify non-decreasing order (ties allowed)
removed = []
while h.size() > 0:
    removed.append(h.remove())

expected = sorted(["pear", "apple", "banana", "apricot", "grape", "kiwi", "plum", "apple"])
assert removed == expected, "removed sequence should be sorted ascending"
assert h.size() == 0, "size should be 0 after all removes"
assert h.peek() is None, "peek on empty should be None"
assert h.remove() is None, "remove on empty should be None"

# Duplicates only
h2 = MinHeap()
for word in ["a", "a", "a"]:
    h2.add(word)
assert h2._is_min_heap()
assert h2.peek() == "a"
assert [h2.remove(), h2.remove(), h2.remove(), h2.remove()] == ["a", "a", "a", None]

# Already sorted inserts
h3 = MinHeap()
for word in ["ant", "bat", "cat", "dog", "eel"]:
    h3.add(word)
assert h3._is_min_heap()
assert h3.peek() == "ant"
assert [h3.remove(), h3.remove(), h3.remove(), h3.remove(), h3.remove()] == ["ant", "bat", "cat", "dog", "eel"]

"All tests passed!"
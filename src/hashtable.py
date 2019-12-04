from math import floor

# '''
# Linked List hash table key/value pair
# '''
class LinkedPair:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys
    """

    def __init__(self, capacity):
        self.capacity = capacity  # Number of buckets in the hash table
        self.original_allocation = capacity
        self.storage = [None] * capacity
        self.count = 0

    def _hash(self, key):
        """
        Hash an arbitrary key and return an integer.

        You may replace the Python hash with DJB2 as a stretch goal.
        """
        return hash(key)

    def _hash_djb2(self, key):
        """
        Hash an arbitrary key using DJB2 hash

        OPTIONAL STRETCH: Research and implement DJB2
        """
        hash_value = 5381

        for char in key:
            hash_value = ((hash_value << 5) + hash_value) ^ ord(char)  # hash * 33 ^ c

        return hash_value

    def _hash_mod(self, key):
        """
        Take an arbitrary key and return a valid integer index
        within the storage capacity of the hash table.
        """
        return self._hash_djb2(key) % self.capacity

    def _load_balance(self):
        """
        Assesses current table size and return if True iff it's time 
        for a resize.
        """
        return self.count / self.capacity

    def insert(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Fill this in.
        """

        target_index = self._hash_mod(key)

        if self.retrieve(key) is None:
            node = LinkedPair(key, value)
            if self.storage[target_index] is None:
                self.storage[target_index] = node
            else:
                _node = self.storage[target_index]
                while _node.next is not None:
                    _node = _node.next
                _node.next = node

            self.count += 1
            if self._load_balance() > 0.7:
                self.resize()
        else:
            _node = self.storage[target_index]
            while _node is not None:
                if _node.key == key:
                    _node.value = value
                    break
                _node = _node.next

    def remove(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Fill this in.
        """
        if self.retrieve(key) is None:
            print("NOT FOUND")
            return
        target_index = self._hash_mod(key)
        if self.storage[target_index].key == key:
            self.storage[target_index] = None
        else:
            prev_node = self.storage[target_index]
            curr_node = self.storage[target_index].next

            while curr_node is not None:
                if curr_node.key == key:
                    next_node = curr_node.next
                    prev_node.next = next_node
                    break
                prev_node = curr_node
                curr_node = curr_node.next

        self.count -= 1
        if self._load_balance() < 0.2:  # change this value?
            self.resize(0.5)

    def retrieve(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Fill this in.
        """
        node = self.storage[self._hash_mod(key)]
        while node is not None:
            if node.key == key:
                return node.value
            else:
                node = node.next
        return None

    def resize(self, factor=2):
        """
        Resizes the capacity of the hash table and rehash 
        all key/value pairs. Defaults to doubling size.

        Fill this in.
        """
        new_capacity = floor(self.capacity * factor)
        if new_capacity < self.original_allocation:
            return

        self.capacity = new_capacity
        old_storage = self.storage
        self.storage = [None] * self.capacity
        self.count = 0

        for old_node in old_storage:
            node = old_node
            while node is not None:
                self.insert(node.key, node.value)
                node = node.next


if __name__ == "__main__":
    ht = HashTable(2)

    ht.insert("line_1", "Tiny hash table")
    ht.insert("line_2", "Filled beyond capacity")
    ht.insert("line_3", "Linked list saves the day!")

    print("")

    # Test storing beyond capacity
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    # Test resizing
    old_capacity = len(ht.storage)
    ht.resize()
    new_capacity = len(ht.storage)

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    print("")

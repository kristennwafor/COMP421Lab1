class Block:
    def __init__(self):
        self.operations = []  # List to hold IR operations
        self.head = None
        self.tail = None

    def insert(self, op):
        if self.head is None:
            # If the list is empty, set head and tail to the new IR instruction
            self.head = self.tail = op
            self.tail.next = None
            self.head.prev = None
            self.operations.append(op)
        else:
            # Insert at the tail
            self.tail.next = op
            op.prev = self.tail
            self.tail = op
            self.tail.next = None
            self.operations.append(op)

    def print_ir(self):
        """Print the entire block of IR operations in a readable format."""
        for ir_op in self.operations:
            print(ir_op)

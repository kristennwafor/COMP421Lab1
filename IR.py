class IR:
    def __init__(self, opcode, lexeme, line_num, arg1=None, arg2=None, arg3=None):
        self.opcode = opcode
        self.line = line_num
        self.lexeme = lexeme
        self.next = None
        self.prev = None
        self.arg1 = [-1, -1, -1, -1]
        self.arg2 = [-1, -1, -1, -1]
        self.arg3 = [-1, -1, -1, -1]




        # Set arg1 (if it's a register like 'r1', extract the number)
        if arg1 is not None:
            if arg1[0] == 'r':
                self.arg1[1] = int(arg1[1:])  # Store the register number (e.g., r1 becomes 1)
            else:
                self.arg1[0] = int(arg1)  # Store constant if it's not a register

        # Set arg2
        if arg2 is not None:
            if arg2[0] == 'r':
                self.arg2[1] = int(arg2[1:])  # Store the register number (e.g., r2 becomes 2)
            else:
                self.arg2[0] = int(arg2)  # Store constant if it's not a register

        # Set arg3
        if arg3 is not None:
            if arg3[0] == 'r':
                self.arg3[1] = int(arg3[1:])  # Store the register number (e.g., r3 becomes 3)
            else:
                self.arg3[0] = int(arg3)  # Store constant if it's not a register

    def __str__(self):
        if self.lexeme == "loadI":
            return f"{self.lexeme} [ val {self.arg1[0]} ], [ ], [ sr{self.arg2[1]} ]"
        elif self.lexeme == "output":
            return f"{self.lexeme} [ val {self.arg1[0]} ], [ ], [ ]"
        # elif self.opcode == 0:
        #     return f"load or store [ vr{self.arg1[1]} ], [   ], [ vr{self.arg3[1]} ]"
        elif self.lexeme == "load" or self.lexeme == "store":
            return f"{self.lexeme} [ sr{self.arg1[1]} ], [ ], [ sr{self.arg2[1]} ]"
        elif self.lexeme == "nop":
            return f"{self.lexeme} [ ], [ ], [ ]"
        else:
            return f"{self.lexeme} [ sr{self.arg1[1]} ], [ sr{self.arg2[1]} ], [ sr{self.arg3[1]} ]"

    def __eq__(self, other):
        if isinstance(other, IR):
            return (self.opcode == other.opcode and
                    self.arg1 == other.arg1 and
                    self.arg2 == other.arg2 and
                    self.arg3 == other.arg3 and
                    self.line == other.line)
        return False

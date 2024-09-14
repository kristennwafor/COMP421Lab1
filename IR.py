class IR:
    # modify this to fix the line part
    def __init__(self, opcode, line_num, arg1=None, arg2=None, arg3=None):
        self.opcode = opcode
        self.line = line_num
        self.next = None
        self.prev = None
        self.arg1 = [-1, -1, -1, -1]
        self.arg2 = [-1, -1, -1, -1]
        self.arg3 = [-1, -1, -1, -1]

        # Set arg1
        if arg1 is not None:
            self.arg1[0] = int(arg1[1:]) if arg1[0] == 'r' else int(arg1)

        # Set arg2
        if arg2 is not None:
            self.arg2[0] = int(arg2[1:]) if arg2[0] == 'r' else int(arg2)

        # Set arg3
        if arg3 is not None:
            self.arg3[0] = int(arg3[1:]) if arg3[0] == 'r' else int(arg3)

    def parse_arg(self, arg):
        """
        Parse the argument to either a register, a numeric value, or a special keyword like 'CONST'.
        Returns a list in the format expected by IR (with -1s if no value is assigned).
        """
        if arg[0] == 'r':  # Register case
            return [int(arg[1:]), -1, -1, -1]
        elif arg.isdigit():  # Numeric case
            return [int(arg), -1, -1, -1]
        else:  # Handle special cases like 'CONST'
            return [-1, -1, -1, -1]  # Leave as default for special keywords

    def __str__(self):
        if self.opcode == "loadI":
            return f"{self.line}: {self.opcode} [ val{self.arg1[0]} ], [   ], [ vr{self.arg3[1]} ]"
        elif self.opcode == "output":
            return f"{self.line}: {self.opcode} [ val{self.arg1[0]} ], [   ], [   ]"
        elif self.opcode in ["load", "store"]:
            return f"{self.line}: {self.opcode} [ vr{self.arg1[1]} ], [   ], [ vr{self.arg3[1]} ]"
        elif self.opcode == "nop":
            return f"{self.line}: {self.opcode} [   ], [   ], [   ]"
        else:
            return f"{self.line}: {self.opcode} [ vr{self.arg1[1]} ], [ vr{self.arg2[1]} ], [ vr{self.arg3[1]} ]"

    def __eq__(self, other):
        if isinstance(other, IR):
            return (self.opcode == other.opcode and
                    self.arg1 == other.arg1 and
                    self.arg2 == other.arg2 and
                    self.arg3 == other.arg3 and
                    self.line== other.line)
        return False

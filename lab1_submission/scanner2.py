import sys
from utils import print_error

# TO DO: figure out what to return in report_error/skip to produce the right error message


# Declare global variables
filename = ""
line_num = 0
buffer = ""
curr_pos = 0

# Scanner Part of Speech (integer format)
MEMOP = 0
LOADI = 1
ARITHOP = 2
OUTPUT = 3
NOP = 4
CONSTANT = 5 # redo to be const
REGISTER = 6
COMMA = 7
INTO = 8
EOF = 9
EOL = 10

# These are the syntatic categories dictated by the needs of the scanner
token_type = [
    "MEMOP", "LOADI", "ARITHOP", "OUTPUT", "NOP", "CONST",
    "REG", "COMMA", "INTO", "ENDFILE", "NEWLINE"
]

keywords = {
    'load': MEMOP,
    'store': MEMOP,
    'loadI': LOADI,
    'add': ARITHOP,
    'sub': ARITHOP,
    'mult': ARITHOP,
    'lshift': ARITHOP,
    'rshift': ARITHOP,
    'output': OUTPUT,
    'nop': NOP
}

# Function to fill the buffer
#  TO DO: insert try catch into here
def fill_buffer(input_stream):
    global buffer, line_num
    # use read line to reach each line into the buffer
    buffer = input_stream.readline()
    line_num += 1

    return len(buffer)>0






# this function gets each character from the buffer so the scanner can operate incrementally
def get_char(input_stream):
    global curr_pos, buffer

    # if we've reached the end of the buffer
    if curr_pos >= len(buffer):
        # see if it's possible to refill the buffer
        if not fill_buffer(input_stream):
            return None
        # reset current position so the next character read will start from the beginning of the newly filled buffer
        curr_pos = 0

    curr_char = buffer[curr_pos]
    curr_pos += 1
    return curr_char


def go_back():
    global curr_pos
    if curr_pos > 0:
        curr_pos -= 1


#  this is used when we encounter an error as we don't need to process remaining characters in that line
def skip(input_stream, line_num, lexeme):
    # skip to the next line if we encounter an error on the current line
    print_error(f"ERROR {line_num}: \"{lexeme}\" is not a valid word.")

    while True:
        curr_char = get_char(input_stream)
        if curr_char == '\n' or curr_char is None:
            break

    if curr_char == '\n':
        #line_num += 1
        return (line_num, token_type[EOL], "\\n")
    return (line_num, token_type[EOF], "")


# this function handles and produces error tokens
def report_error(line_num, lexeme):
    return (line_num, "ERROR", lexeme)





# def scan(input_stream):
#     global curr_pos, buffer, line_num

#     lexeme = ""

#     # Read the first chunk (line) of the file into the buffer
#     if len(buffer) == 0:
#         fill_buffer(input_stream)


#     # Continue scanning until EOF
#     while True:
#         curr_char = get_char(input_stream)

#         # Handle End of File (EOF)
#         if curr_char is None:
#             if lexeme:
#                 if lexeme in keywords:
#                     return (line_num, keywords[lexeme], lexeme)
#                 elif lexeme.isdigit():
#                     return (line_num, CONSTANT, lexeme)
#                 else:
#                     return report_error(line_num, lexeme)
#             return (line_num, EOF, "")  # Return EOF token

#         # Handle newlines (don't skip, return the NEWLINE token)
#         if curr_char == '\n':
#             #line_num += 1
#             if lexeme:  # If there's an accumulated lexeme, return the token first
#                 if lexeme in keywords:
#                     return (line_num, keywords[lexeme], lexeme)
#                 elif lexeme.isdigit():
#                     return (line_num, CONSTANT, lexeme)
#                 else:
#                     return report_error(line_num, lexeme)



#             return (line_num, EOL, "\\n")

#         # Skip comments (//)
#         if curr_char == '/':
#             next_char = get_char(input_stream)
#             if next_char == '/':
#                 while curr_char != '\n' and curr_char is not None:
#                     curr_char = get_char(input_stream)
#                 #line_num += 1
#                 return (line_num, EOL, "\\n")
#             else:
#                 go_back()
#                 return skip(input_stream, line_num, lexeme)

#         # Process alphabetic characters (keywords or registers)
#         if curr_char.isalpha():
#             lexeme = curr_char
#             curr_char = get_char(input_stream)

#             # Handle registers (e.g., r1, r2, etc.)
#             if lexeme == 'r' and curr_char.isdigit():
#                 while curr_char.isdigit():
#                     lexeme += curr_char
#                     curr_char = get_char(input_stream)
#                 go_back()
#                 return (line_num, REGISTER, lexeme)

#             # Handle keywords (e.g., load, store, loadI)
#             while curr_char.isalpha():  # Collect the full keyword
#                 lexeme += curr_char
#                 curr_char = get_char(input_stream)


#             if lexeme == "load":
#                 if curr_char == 'I':  # Handle "loadI"
#                     lexeme += curr_char
#                     next_char = get_char(input_stream)
#                     if next_char in [' ', '\t', '\n']:  # Ensure it's followed by space, tab, or newline
#                         return (line_num, LOADI, lexeme)
#                     else:
#                         return report_error(line_num, lexeme)
#                 elif curr_char in [' ', '\t', '\n']:  # Handle regular "load"
#                     return (line_num, MEMOP, lexeme)
#                 else:
#                     return report_error(line_num, lexeme)


#             # Handle other keywords
#             if lexeme in keywords:
#                 return (line_num, keywords[lexeme], lexeme)
#             else:
#                 return skip(input_stream, line_num, lexeme)
#                 #return report_error(line_num, lexeme)

#         # Handle numeric constants
#         if curr_char.isdigit():
#             lexeme = curr_char  # Start accumulating the digits for the constant
#             while True:
#                 next_char = get_char(input_stream)
#                 if next_char is not None and next_char.isdigit():
#                     lexeme += next_char
#                 else:
#                     go_back()  # Go back if a non-digit character is found
#                     break
#             return (line_num, CONSTANT, lexeme)



#         # Handle operators (e.g., "=>")
#         if curr_char == '=':
#             next_char = get_char(input_stream)
#             if next_char == '>':
#                 return (line_num, INTO, "=>")
#             else:
#                 go_back()
#                 return skip(input_stream, line_num, lexeme)

#         # Handle commas
#         if curr_char == ',':
#             return (line_num, COMMA, ",")

#         # Handle whitespace (but don't skip without processing tokens)
#         if curr_char in [' ', '\t', '\r']:
#             if lexeme:  # If a token has been accumulated, return it before skipping whitespace
#                 if lexeme.isdigit():
#                     return (line_num, CONSTANT, lexeme)
#                 elif lexeme in keywords:
#                     return (line_num, keywords[lexeme], lexeme)
#                 else:
#                     return report_error(line_num, lexeme)
#             continue  # Skip the whitespace and continue


#         else:
#             return skip(input_stream, line_num, lexeme)







# 2nd take


def scan(input_stream):
    global curr_pos, buffer, line_num
    lexeme = ""

    # Read the first chunk (line) of the file into the buffer
    if len(buffer) == 0:
        fill_buffer(input_stream)

    while True:
        curr_char = get_char(input_stream)

        # Handle end of file
        if curr_char is None:
            return (line_num, EOF, "")

        # Handle newlines
        elif curr_char == '\n':
            return (line_num, EOL, "\\n")

        # Handle comments (//)
        elif curr_char == '/':
            next_char = get_char(input_stream)
            if next_char == '/':
                while curr_char != '\n' and curr_char is not None:
                    curr_char = get_char(input_stream)
                return (line_num, EOL, "\\n")
            else:
                go_back()
                return report_error(line_num, "/")

        # Process alphabetic characters one by one
        elif curr_char == 's':
            curr_char = get_char(input_stream)
            if curr_char == 't':
                curr_char = get_char(input_stream)
                if curr_char == 'o':
                    curr_char = get_char(input_stream)
                    if curr_char == 'r':
                        curr_char = get_char(input_stream)
                        if curr_char == 'e':
                            curr_char = get_char(input_stream)
                            if curr_char in [' ', '\t']:
                                return (line_num, MEMOP, "store")
                            else:
                                return report_error(line_num, "store")
                        else:
                            return report_error(line_num, "stor")
                    else:
                        return report_error(line_num, "sto")
                else:
                    return report_error(line_num, "st")

            elif curr_char == 'u':
                curr_char = get_char(input_stream)
                if curr_char == 'b':
                    curr_char = get_char(input_stream)
                    if curr_char in [' ', '\t']:
                        return (line_num, ARITHOP, "sub")
                    else:
                        return report_error(line_num, "sub")
                else:
                    return report_error(line_num, "su")
            else:
                return report_error(line_num, "s")



        # Handle keywords starting with 'l'
        elif curr_char == 'l':
            curr_char = get_char(input_stream)
            if curr_char == 's':
                curr_char = get_char(input_stream)
                if curr_char == 'h':
                    curr_char = get_char(input_stream)
                    if curr_char == 'i':
                        curr_char = get_char(input_stream)
                        if curr_char == 'f':
                            curr_char = get_char(input_stream)
                            if curr_char == 't':
                                curr_char = get_char(input_stream)
                                if curr_char in [' ', '\t']:
                                    return (line_num, ARITHOP, "lshift")
                                else:
                                    return report_error(line_num, "lshift")
                            else:
                                return report_error(line_num, "lshif")
                        else:
                            return report_error(line_num, "lshi")
                    else:
                        return report_error(line_num, "lsh")
                else:
                    return report_error(line_num, "ls")

            elif curr_char == 'o':
                curr_char = get_char(input_stream)
                if curr_char == 'a':
                    curr_char = get_char(input_stream)
                    if curr_char == 'd':
                        curr_char = get_char(input_stream)
                        if curr_char == 'I':
                            curr_char = get_char(input_stream)
                            if curr_char in [' ', '\t']:
                                return (line_num, LOADI, "loadI")
                            else:
                                return report_error(line_num, "loadI")
                        elif curr_char in [' ', '\t']:
                            return (line_num, MEMOP, "load")
                        else:
                            return report_error(line_num, "load-")
                    else:
                        return report_error(line_num, "loa")
                else:
                    return report_error(line_num, "lo")
            else:
                return report_error(line_num, "l")

        # Handle keywords starting with 'r'
        elif curr_char == 'r':
            curr_char = get_char(input_stream)
            if curr_char == 's':
                curr_char = get_char(input_stream)
                if curr_char == 'h':
                    curr_char = get_char(input_stream)
                    if curr_char == 'i':
                        curr_char = get_char(input_stream)
                        if curr_char == 'f':
                            curr_char = get_char(input_stream)
                            if curr_char == 't':
                                curr_char = get_char(input_stream)
                                if curr_char in [' ', '\t']:
                                    return (line_num, ARITHOP, "rshift")
                                else:
                                    return report_error(line_num, "rshift")
                            else:
                                return report_error(line_num, "rshif")
                        else:
                            return report_error(line_num, "rshi")
                    else:
                        return report_error(line_num, "rsh")
                else:
                    return report_error(line_num, "rs")

            # Handle registers (e.g., r1, r2, etc.)
            elif curr_char.isdigit():
                n = 0
                while curr_char.isdigit():
                    n = n * 10 + int(curr_char)
                    curr_char = get_char(input_stream)
                return (line_num, REGISTER, f"r{n}")
            else:
                return report_error(line_num, "r")

        # Handle keywords starting with 'm'
        elif curr_char == 'm':
            curr_char = get_char(input_stream)
            if curr_char == 'u':
                curr_char = get_char(input_stream)
                if curr_char == 'l':
                    curr_char = get_char(input_stream)
                    if curr_char == 't':
                        curr_char = get_char(input_stream)
                        if curr_char in [' ', '\t']:
                            return (line_num, ARITHOP, "mult")
                        else:
                            return report_error(line_num, "mult")
                    else:
                        return report_error(line_num, "mul")
                else:
                    return report_error(line_num, "mu")
            else:
                return report_error(line_num, "m")

        # Handle "add"
        elif curr_char == 'a':
            curr_char = get_char(input_stream)
            if curr_char == 'd':
                curr_char = get_char(input_stream)
                if curr_char == 'd':
                    curr_char = get_char(input_stream)
                    if curr_char in [' ', '\t', '\r', '\n']:  # Ensure it's followed by space, tab, or newline
                        return (line_num, ARITHOP, "add")
                    else:
                        return report_error(line_num, "add")
                else:
                    return report_error(line_num, "ad")
            else:
                return report_error(line_num, "a")

        elif curr_char == 'n':
            curr_char = get_char(input_stream)
            if curr_char == 'o':
                curr_char = get_char(input_stream)
                if curr_char == 'p':
                    curr_char = get_char(input_stream)
                    if curr_char in [' ', '\t', '\r', '\n']:  # Ensure it's followed by space, tab, or newline
                        return (line_num, NOP, "nop")
                    else:
                        return report_error(line_num, "nop")
                else:
                    return report_error(line_num, "no")
            else:
                return report_error(line_num, "n")

        # Handle "output"
        elif curr_char == 'o':
            curr_char = get_char(input_stream)
            if curr_char == 'u':
                curr_char = get_char(input_stream)
                if curr_char == 't':
                    curr_char = get_char(input_stream)
                    if curr_char == 'p':
                        curr_char = get_char(input_stream)
                        if curr_char == 'u':
                            curr_char = get_char(input_stream)
                            if curr_char == 't':
                                curr_char = get_char(input_stream)
                                if curr_char in [' ', '\t', '\r', '\n']:  # Ensure it's followed by space, tab, or newline
                                    return (line_num, OUTPUT, "output")
                                else:
                                    return report_error(line_num, "output")
                            else:
                                return report_error(line_num, "outpu")
                        else:
                            return report_error(line_num, "outp")
                    else:
                        return report_error(line_num, "out")
                else:
                    return report_error(line_num, "ou")
            else:
                return report_error(line_num, "o")

        # Handle "=>"
        elif curr_char == '=':
            next_char = get_char(input_stream)
            if next_char == '>':
                return (line_num, INTO, "=>")
            else:
                return report_error(line_num, "=")

        # Handle constants (e.g., numbers)
        # Handle constants (e.g., numbers)
        elif curr_char.isdigit():
            n = 0
            # Collect all digits of the number
            while curr_char.isdigit():
                n = n * 10 + int(curr_char)
                curr_char = get_char(input_stream)

            # Now, after processing the constant, check for the next possible tokens
            if curr_char == ',':  # If it's a comma
                return (line_num, COMMA, ",")
            elif curr_char == '=':  # If it's part of "=>"
                next_char = get_char(input_stream)
                if next_char == '>':
                    return (line_num, INTO, "=>")
                else:
                    go_back()  # Rollback to handle any other cases
                    return (line_num, CONSTANT, str(n)) # to do: check if this is correct
            elif curr_char in [' ', '\t', '\r', '\n']:  # Whitespace or end of token
                return (line_num, CONSTANT, str(n))
            else:
                return report_error(line_num, f"Unexpected char '{curr_char}' after constant")

        # Handle operators (e.g., "=>")
        elif curr_char == '=':
            next_char = get_char(input_stream)
            if next_char == '>':
                return (line_num, INTO, "=>")
            else:
                go_back()
                return report_error(line_num, "=")

        # Handle commas
        elif curr_char == ',':
            return (line_num, COMMA, ",")

        # Skip whitespace (but return tokens before skipping)
        elif curr_char in [' ', '\t', '\r']:
            continue  # Skip the whitespace and continue

        # Return an error for unexpected characters
        else:
            return report_error(line_num, f"Unexpected char '{curr_char}'")
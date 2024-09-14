# Scanner Code


# TO DO: double check how im printing errors -stderr
# Office Hours:
# - for some reason, my first line always starts at line num = 2 instead of 1
# - im not getting the end of file token being printed out for some reason
# make sure all error statements print standard error including stuff like Errr 10: "word" is not a valid word


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

    # Check if the buffer is empty, indicating EOF
    # if buffer == '':  # Empty string means EOF
    #     return (line_num, token_type[EOF], "")  # Return EOF token



    # else: # nothing was read so buffer is empty
    #     return False
    return len(buffer)>0






# this function gets each character from the buffer so the scanner can operate incrementally
def get_char(input_stream):
    global curr_pos, buffer

    # if we've reached the end of the buffer
    if curr_pos >= len(buffer):
        # see if it's possible to refill the buffer
        # if fill_buffer(input_stream) == False:
        #     return None
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
    print(f"ERROR {line_num}: \"{lexeme}\" is not a valid word.")

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





def scan(input_stream):
    global curr_pos, buffer, line_num

    lexeme = ""

    # Read the first chunk (line) of the file into the buffer
    if len(buffer) == 0:
        fill_buffer(input_stream)




    # Continue scanning until EOF
    while True:
        curr_char = get_char(input_stream)

        # Handle End of File (EOF)
        if curr_char is None:
            if lexeme:
                if lexeme in keywords:
                    return (line_num, token_type[keywords[lexeme]], lexeme)
                elif lexeme.isdigit():
                    return (line_num, token_type[CONSTANT], lexeme)
                else:
                    return report_error(line_num, lexeme)
            return (line_num, token_type[EOF], "")  # Return EOF token

        # Handle newlines (don't skip, return the NEWLINE token)
        if curr_char == '\n':
            #line_num += 1
            if lexeme:  # If there's an accumulated lexeme, return the token first
                if lexeme in keywords:
                    return (line_num, token_type[keywords[lexeme]], lexeme)
                elif lexeme.isdigit():
                    return (line_num, token_type[CONSTANT], lexeme)
                else:
                    return report_error(line_num, lexeme)


            return (line_num, token_type[EOL], "\\n")

        # Skip comments (//)
        if curr_char == '/':
            next_char = get_char(input_stream)
            if next_char == '/':
                while curr_char != '\n' and curr_char is not None:
                    curr_char = get_char(input_stream)
                #line_num += 1
                return (line_num, token_type[EOL], "\\n")
            else:
                go_back()
                print("skip in the comment case")
                return skip(input_stream, line_num, lexeme)

        # Process alphabetic characters (keywords or registers)
        if curr_char.isalpha():
            lexeme = curr_char
            curr_char = get_char(input_stream)

            # Handle registers (e.g., r1, r2, etc.)
            if lexeme == 'r' and curr_char.isdigit():
                while curr_char.isdigit():
                    lexeme += curr_char
                    curr_char = get_char(input_stream)
                go_back()
                return (line_num, token_type[REGISTER], lexeme)

            # Handle keywords (e.g., load, store, loadI)
            while curr_char.isalpha():  # Collect the full keyword
                lexeme += curr_char
                curr_char = get_char(input_stream)

            # to do: clarify with keith if this method of comparing opcodes or keywords is valid

            if lexeme == "load":
                if curr_char == 'I':  # Handle "loadI"
                    lexeme += curr_char
                    next_char = get_char(input_stream)
                    if next_char in [' ', '\t', '\n']:  # Ensure it's followed by space, tab, or newline
                        return (line_num, token_type[LOADI], lexeme)
                    else:
                        return report_error(line_num, lexeme)
                elif curr_char in [' ', '\t', '\n']:  # Handle regular "load"
                    return (line_num, token_type[MEMOP], lexeme)
                else:
                    return report_error(line_num, lexeme)


            # Handle other keywords
            if lexeme in keywords:
                return (line_num, token_type[keywords[lexeme]], lexeme)
            else:
                return skip(input_stream, line_num, lexeme)
                #return report_error(line_num, lexeme)

        # Handle numeric constants
        if curr_char.isdigit():
            lexeme = curr_char  # Start accumulating the digits for the constant
            while True:
                next_char = get_char(input_stream)
                if next_char is not None and next_char.isdigit():
                    lexeme += next_char
                else:
                    go_back()  # Go back if a non-digit character is found
                    break
            return (line_num, token_type[CONSTANT], lexeme)



        # Handle operators (e.g., "=>")
        if curr_char == '=':
            next_char = get_char(input_stream)
            if next_char == '>':
                return (line_num, token_type[INTO], "=>")
            else:
                go_back()
                print("skip in the => case")
                return skip(input_stream, line_num, lexeme)

        # Handle commas
        if curr_char == ',':
            return (line_num, token_type[COMMA], ",")

        # Handle whitespace (but don't skip without processing tokens)
        if curr_char in [' ', '\t', '\r']:
            if lexeme:  # If a token has been accumulated, return it before skipping whitespace
                if lexeme.isdigit():
                    return (line_num, token_type[CONSTANT], lexeme)
                elif lexeme in keywords:
                    return (line_num, token_type[keywords[lexeme]], lexeme)
                else:
                    return report_error(line_num, lexeme)
            continue  # Skip the whitespace and continue


        else:
            #print("skip at the very end")
            return skip(input_stream, line_num, lexeme)

import sys
from scanner2 import  *
from IR import IR
from block import Block

# To DO: figure out what to return in the parser if anythign
# what is supposed to happen if the parser receives a newline token first?
# for some reason, when it hits the break, it doesnt go through anything else
# something in the parser should be using ints rather than strings


# for error on line 10, im getting "" instead and it's printing out the whole lexeme instead of just the char

tokens = []  # List of tokens (to be filled by scanning)
token_category = None
error_count = 0
num_ops = 0

# two way dictionary

# initialize a block
# sequence of IR operations that are executed in order,
block = Block()


# double check this
# def parse_error(missing, context):
#     print(f"ERROR {context['line_num']}: Missing {missing} in {context['lexeme']}.")
#     # skip to a new line

#     # Skip tokens until a NEWLINE is encountered
#     token_category = None
#     while token_category != 'NEWLINE' and token_category != 'ENDFILE':
#         token_data = scan(input_stream)
#         token_category = token_data[1]  # Update the token_category

#     global error_count
#     error_count += 1

def parse_error(missing, line_num, lexeme, opcode, input_stream):
    print(f"ERROR {line_num}: Missing {missing} in {opcode}.")
    # skip to a new line

    # Skip tokens until a NEWLINE or ENDFILE is encountered
    token_category = None
    while token_category != 'NEWLINE' and token_category != 'ENDFILE':
        token_data = scan(input_stream)
        token_category = token_data[1]  # Update the token_category

    global error_count
    error_count += 1




def next_token(input_stream):
    """Retrieve the next token by calling the scan function."""
    global line_num, token_category, lexeme

    token_data = scan(input_stream)
    line_num, token_category, lexeme = token_data

    if token_data is None:
        print("Error: scan() returned None.")
        return

    if len(token_data) != 3:
        print(f"Error: scan() returned unexpected data: {token_data}.")
        return

   # print(f"Updated: line_num={line_num}, token_category={token_category}, lexeme={lexeme}")
    # token category is of type string
    return token_data


def parse(input_stream):
    """Main parsing loop."""
    global token_category, error_count, num_ops
    errors_found = False

    next_token(input_stream)
    # everytime u build a token, have the category be an intgeer
    #print(f"Initial token: {token_category}, {lexeme}")


    while token_category != 'ENDFILE':

        #if token_category == MEMOP

        # have something for converting categories

        if token_category == "MEMOP":
            finish_memop(input_stream)
        elif token_category == "LOADI":
            print("Calling finish_loadi()")
            finish_loadi(input_stream)
        elif token_category == "ARITHOP":
            print("Calling finish_arithop()")
            finish_arithop(input_stream)
        elif token_category == "OUTPUT":
            print("Calling finish_output()")
            finish_output(input_stream)
        elif token_category == "NOP":
            print("Calling finish_nop()")
            finish_nop(input_stream)
        elif token_category == 'ERROR':
            errors_found = True
            print(f"ERROR {line_num}: \"{lexeme}\" is not a valid word.")
            while token_category != 'NEWLINE' and token_category != 'ENDFILE':
                next_token(input_stream)
            next_token(input_stream)  # Move to the first token of the next line
            continue
        else:
            #print("test")
            #continue
            pass

            # handle default case here


        #print("right before we hit next token")
        #print(token_category)
        #print(lexeme)
        # Fetch the next token
        next_token(input_stream)
        # it's not reaching here for some reason

        #print(f"Next token: {token_category}, {lexeme}")

        # if errors_found:
        #     print("Parse found errors.")
        # else:
        #     print(f"Parse succeeded. Processed {num_ops} operations.")

        # figure out later where to return error count and num opps here
    return error_count, num_ops




def finish_arithop(input_stream):
    print(f"Processing ARITHOP: {token_category}")
    op_token = token_category
    next_token(input_stream)

    if token_category != 'REG':
        #parse_error("first source register", op_token)
        parse_error("first source register", line_num, lexeme, op_token, input_stream)
        return

    arg1 = lexeme

    next_token(input_stream)
    if token_category != 'COMMA':
        #parse_error("comma", op_token)
        parse_error("comma", line_num, lexeme, op_token, input_stream)
        return

    next_token(input_stream)
    if token_category != 'REG':
        #parse_error("second source register", op_token)
        parse_error("second source register", line_num, lexeme, op_token, input_stream)
        return

    arg2 = lexeme

    next_token(input_stream)
    if token_category != 'INTO':
        #parse_error("into", op_token)
        parse_error("into", line_num, lexeme, op_token, input_stream)
        return

    next_token(input_stream)
    if token_category != 'REG':
        #parse_error("target register", op_token)
        parse_error("target register", line_num, lexeme, op_token, input_stream)
        return

    arg3 = lexeme

    next_token(input_stream)
    if token_category == 'NEWLINE':
        ir_operation = IR(op_token, line_num, arg1, arg2, arg3)
        block.insert(ir_operation)
        global num_ops
        num_ops += 1
    else:
        #parse_error("newline", op_token)
        parse_error("newline", line_num, lexeme, op_token, input_stream)


def finish_memop(input_stream):
    print(f"Processing MEMOP: {token_category}")
    op_token = token_category
    global num_ops

    next_token(input_stream)

    if token_category != 'REG':
        #parse_error("source register", op_token)
        parse_error("source register", line_num, lexeme, op_token, input_stream)
        return

    arg1 = lexeme

    next_token(input_stream)
    if token_category != 'INTO':
        #parse_error("into", op_token)
        parse_error("into", line_num, lexeme, op_token, input_stream)
        return

    next_token(input_stream)

    if token_category != 'REG':
        #parse_error("target register", op_token)
        parse_error("target register", line_num, lexeme, op_token, input_stream)
        return

    arg2 = lexeme

    next_token(input_stream)

    if token_category == 'NEWLINE':
        ir_operation = IR(op_token, line_num, arg1, arg2)
        block.insert(ir_operation)
        num_ops += 1
    else:
        #parse_error("newline", op_token)
        parse_error("newline", line_num, lexeme, op_token, input_stream)


def finish_loadi(input_stream):
    #print(f"Processing LOADI: {token_category}")
    op_token = token_category
    next_token(input_stream)

    if token_category != 'CONST':
        #parse_error("constant", op_token)
        parse_error("constant", line_num, lexeme, op_token, input_stream)
        return

    arg1 = lexeme

    next_token(input_stream)
    if token_category != 'INTO':
        #parse_error("into", op_token)
        parse_error("into", line_num, lexeme, op_token, input_stream)
        return

    next_token(input_stream)

    if token_category != 'REG':
        #parse_error("target register", op_token)
        parse_error("into", line_num, lexeme, op_token, input_stream)
        return

    arg2 = lexeme

    next_token(input_stream)

    if token_category == 'NEWLINE':
        ir_operation = IR(op_token, line_num, arg1, arg2)
        block.insert(ir_operation)
        global num_ops
        num_ops += 1
    else:
        #parse_error("newline", op_token)
        parse_error("newline", line_num, lexeme, op_token, input_stream)


def finish_nop(input_stream):
    print(f"Processing NOP: {token_category}")
    op_token = token_category
    next_token(input_stream)

    if token_category == 'NEWLINE':
        ir_operation = IR(op_token, line_num)
        block.insert(ir_operation)
        global num_ops
        num_ops += 1
    else:
        #parse_error("newline", op_token)
        parse_error("newline", line_num, lexeme, op_token, input_stream)


def finish_output(input_stream):
    print(f"Processing OUTPUT: {token_category}")
    op_token = token_category
    next_token(input_stream)

    if token_category != 'CONST':
        #parse_error("constant", op_token)
        parse_error("constant", line_num, lexeme, op_token, input_stream)
        return

    arg1 = lexeme

    next_token(input_stream)

    if token_category == 'NEWLINE':
        ir_operation = IR(op_token, line_num, arg1)
        block.insert(ir_operation)
        global num_ops
        num_ops += 1
    else:
        #parse_error("newline", op_token)
        parse_error("constant", line_num, lexeme, op_token, input_stream)




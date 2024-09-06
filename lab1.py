import sys

# Function to display help information
def display_help():
    print("Usage: 412fe [options] <file>")
    print("Options:")
    print("  -h              Display help")
    print("  -s <file>       Scan the input file and output tokens")
    print("  -p <file>       Parse the input file and check for syntax errors")
    print("  -r <file>       Parse the input file and output the intermediate representation")

# Function to print error messages to stderr
def print_error(message):
    print(message, file=sys.stderr)

#  keeps track of the flag priorities
flag_priority = [False, False, False, False] # ['-h', '-r', '-p', '-s']

# sample argv
# "412fe -s <filename>"

def main():

    # error checking if there's more than one flag
    # error if there's not enough arguments (just lab1.py)
    # error if there's no filename
    # if no flag is given, p is the default flag to use
    # if the file doesnt exist - try catch?
    # error if it cant read the input file


    filename = ""

    args = sys.argv[1:]

    # Error check: if less than 2 arguments are passed
    if len(args) < 2:
        print_error("Error: No file or flag provided.")
        display_help()
        return


    for arg in args:
        # Check if the argument is a flag (starts with '-')
        if arg.startswith('-'):
            # Check for specific flags
            if 'h' in arg:
                flag_list[0] = True  # -h flag
                # run h flag handler
            elif 's' in arg:
                flag_list[1] = True  # -s flag
            elif 'p' in arg:
                flag_list[2] = True  # -p flag
            elif 'r' in arg:
                flag_list[3] = True  # -r flag
            # not a valid flag
            else:
                print_error(f"Error: Unrecognized flag '{arg}'.")
                display_help()
                return

        else:
            # If it's not a flag, it must be the file name
            if file_name == "":
                file_name = arg


                lab1.py -a filename




# this will read in command line arguments
def main():
    # error check if there's not enough arguments (less than 2)

    # error check for incorrect or incompatible command line parameters

    # store the first command line argument passed by in the user

    # conditionals depending on what it is

    # if it's h

    # if it's s

    # if it's p

    # if it's r



# Entry point of the script
if __name__ == "__main__":
    main()
    # debugging
    print("Flags: ", flag_list)
    print("File name: ", file_name)

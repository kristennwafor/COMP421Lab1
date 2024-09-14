import sys
from scanner2 import *
from parser import *

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
flag_list = [False, False, False, False] # ['-h', '-r', '-p', '-s']

# sample argv
# "412fe -s <filename>"

def main():

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
            elif 'r' in arg:
                flag_list[1] = True  # -r flag
            elif 'p' in arg:
                flag_list[2] = True  # -p flag
            elif 's' in arg:
                flag_list[3] = True  # -s flag
            # not a valid flag
            else:
                print_error(f"Error: Unrecognized flag '{arg}'.")
                display_help()
                return

        else:
            # If it's not a flag, it must be the file name
            if filename == "":
                filename = arg
            else:
                print_error("Error: Multiple filenames provided.")
                display_help()
                return

    # If no file name is provided
    if filename == "":
        print_error("Error: No file provided.")
        display_help()
        return

    # If no flag is given, assume -p (parse) by default
    if not any(flag_list[1:]):  # If -, -p, -r flags are not set
        flag_list[2] = True  # Set -p as default

    # Process file with the appropriate handler

    if flag_list[0]: # -h flag handler (display help message)
        display_help()



    elif flag_list[1]:  # -r flag handler (IR output)
        print(f"Building intermediate representation for file: {filename}")
        try:
            with open(filename, 'r') as file:
                error_count, num_operations = parse(file)


                if error_count:
                    print("\nDue to errors, run terminates")
                else:
                    # build the IR
                    print(f"Parse succeeded. Processed {num_operations} operations.")

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"Error: {str(e)}")


    elif flag_list[2]:  # -p flag handler (parse)
        print(f"Parsing file: {filename}")
        try:
            with open(filename, 'r') as file:
                error_count, num_operations = parse(file)

                if error_count:
                    print("Parse found errors.")
                else:
                    print(f"Parse succeeded. Processed {num_operations} operations.")

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"Error: {str(e)}")


    elif flag_list[3]:  # -s flag handler (scan)
        print(f"Scanning file: {filename}")
        try:
            with open(filename, 'r') as file:
                while True:
                    token = scan(file)
                    line_num, token_category, lexeme = token

                    # If we encounter EOF, break out of the loop
                    if token_category == token_type[EOF]:
                        break

                    # Handle errors
                    if token_category == "ERROR":
                        # TO DO: double check if i should print the error or return to standard error
                        print(f"ERROR {line_num}: \"{lexeme}\" is not a valid word.")
                        print_error(f"ERROR {line_num}: \"{lexeme}\" is not a valid word.")
                    else:
                        # Print valid tokens
                        # convert integer to string for token category before next line
                        print(f"{line_num}: < {token_category}, \"{lexeme}\" >")
                #token_category = "ENDFILE"
                print(f"{line_num}: < ENDFILE, \"\" >")
        # manually create EOF token here
        #print()
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"Error: {str(e)}")





    # Debugging output
    print("Flags: ", flag_list)
    print("File name: ", filename)




# Entry point of the script
if __name__ == "__main__":
    main()

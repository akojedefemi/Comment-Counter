# Author: Mark Ezema
# This script helps automate checks on when the code is merged into the build pipeline.

# Define quote_check() function takes in the line and target char as input and returns True if target char is not inbetween quotation marks
def quote_check(line, c_comment):
    quote_char = chr(34)    # Set quote_char to '"'
    in_quote = False    # True when within a quote
    comment_seen = False    # True when Target char found and not within quote

    for ch in line:
        if in_quote is False and ch == c_comment:
            comment_seen = True
        if ch == quote_char:
            in_quote = not in_quote

    return comment_seen

# Define quote_check_multiple() function takes in the line and target string as input and returns True if target char is not inbetween quotation marks
def quote_check_multiple(line, find):
    quote_char = chr(34)    # Set quote_char to '"'
    index = line.find(quote_char)   # Set index to index of quote_char
    if line.find(quote_char, index + 1) < line.find(find):
        return True # Return True if target char comes before second quotation mark
    return False

# Define automate_checks() function takes in the filepath to the program file as input and prints out the required outputs
def automate_checks(thefilepath):

    # Open the file in default read mode
    fileHandler = open(thefilepath)

    # Get list of all lines in file
    listOfLines = fileHandler.readlines()

    # Count the number of lines in the program file by getting the length of the list of all lines
    # This approach works well for reasonably sized files so I am assuming the file is of a reasonable size
    count = len(listOfLines)

    totalCommentLineCount = 0   # Initializes the Total # of comment lines
    totalBlockCommentLineCount = 0  # Initializes the Total # of block line comments
    block_mode = False   # Initializes the boolean value for if we are in a multi-line comment
    toDoCount = 0   # Initializes the Total # of TO-DO’s
    singleCommentLineCount = 0  # Initializes the Total # of single line comments
    block_line_total = 0  # Initializes the Total # of comment lines within block comments
    tracker = 0     # Initializes an integer value to count comments within a multi-line comment
    quote_char = '"'

    # Check if its a python file
    if thefilepath[-1] == "y":

        # Iterate through the list of lines
        for line in listOfLines:

            # Remove all white space from the beginning (left trimming)
            lineWithoutWhitespace = line.lstrip()

            # Check if line contains #
            if lineWithoutWhitespace.startswith("#") or lineWithoutWhitespace.find("#") != -1:

                # If the line contains TODO and isn't enclosed in quotation marks, increment Total # of TODO’s
                if lineWithoutWhitespace.find("TODO") != -1:
                    if lineWithoutWhitespace.find(quote_char) == -1:
                        toDoCount += 1
                    elif quote_check_multiple(lineWithoutWhitespace, "TODO"):
                        toDoCount += 1

                # If the line starts with # and isn't enclosed in quotation marks, increment Total # of comment lines
                if lineWithoutWhitespace.startswith("#"):
                    totalCommentLineCount += 1
                else:
                    # If the line does not starts with # and isn't enclosed in quotation marks, increment Total # of comment lines
                    # If the line does not starts with # and isn't enclosed in quotation marks, increment Total # of single line comments
                    # Assuming block comments in python always starts with # after left trimming
                    if lineWithoutWhitespace.find(quote_char) == -1:
                        totalCommentLineCount += 1
                        singleCommentLineCount += 1
                        tracker = 0

                        # If in multi-line mode, disable multi-line mode and increment Total # of block line comments
                        if block_mode is True:
                            totalBlockCommentLineCount += 1
                            block_mode = False
                            tracker = 0
                    elif quote_check(lineWithoutWhitespace, "#"):
                        totalCommentLineCount += 1
                        singleCommentLineCount += 1
                        tracker = 0

                        # If in multi-line mode, disable multi-line mode and increment Total # of block line comments
                        if block_mode is True:
                            totalBlockCommentLineCount += 1
                            block_mode = False
                            tracker = 0

                # If the line starts with #, increment tracker
                if lineWithoutWhitespace.startswith("#"):
                    tracker += 1

                # If the line starts with # and tracker == 2, increment Total # of comment lines within block comments and activate multi-line mode
                if tracker == 2 and lineWithoutWhitespace.startswith("#"):
                    block_line_total += 1   # Increment for the first line of the block comment
                    block_mode = True

                # increment Total # of comment lines within block comments if in multi-line mode
                if block_mode is True:
                    block_line_total += 1

            # Assuming block comments in python always starts with # after left trimming
            # If line doesnt start with #, Check if in multi-line mode
            elif not lineWithoutWhitespace.startswith("#"):
                if tracker == 1:
                    singleCommentLineCount += 1 # Increment Total # of single line comments if not in multiline mode but has seen 1 #
                    tracker = 0  # Reset tracker

                # if in multi-line mode, increment Total # of block line comments, disable multi-line mode, reset tracker
                if block_mode is True:
                    totalBlockCommentLineCount += 1
                    block_mode = False
                    tracker = 0

    # For Java, Javascript, C
    else:
        # Iterate through the list of lines
        for line in listOfLines:

            # Remove all white space from the beginning (left trimming)
            lineWithoutWhitespace = line.lstrip()

            # Check if line contains /* or */ or // or *
            if lineWithoutWhitespace.find("/*") != -1 or lineWithoutWhitespace.find("*/") != -1 or lineWithoutWhitespace.startswith("*") or lineWithoutWhitespace.find("//") != -1:

                # If it isn't enclosed in quotation marks, increment Total # of comment lines
                if lineWithoutWhitespace.find(quote_char) == -1:
                    totalCommentLineCount += 1
                elif quote_check_multiple(lineWithoutWhitespace, "//"):
                    totalCommentLineCount += 1

                # If the line contains // and isn't enclosed in quotation marks, increment Total # of single line comments
                if lineWithoutWhitespace.find("//") != -1:
                    if lineWithoutWhitespace.find(quote_char) == -1:
                        singleCommentLineCount += 1
                    elif quote_check_multiple(lineWithoutWhitespace, "//"):
                        singleCommentLineCount += 1

                    # If the line contains TODO and isn't enclosed in quotation marks, increment Total # of TODO’s
                    if lineWithoutWhitespace.find("TODO") != -1:
                        if lineWithoutWhitespace.find(quote_char) == -1:
                            toDoCount += 1
                        elif quote_check_multiple(lineWithoutWhitespace, "TODO"):
                            toDoCount += 1

                # If the line contains /* and isn't enclosed in quotation marks, activate multi-line mode
                if lineWithoutWhitespace.find("/*") != -1:
                    if lineWithoutWhitespace.find(quote_char) == -1:
                        block_mode = True
                    elif quote_check_multiple(lineWithoutWhitespace, "/*"):
                        block_mode = True

                # increment Total # of comment lines within block comments if in multi-line mode
                if block_mode is True:
                    block_line_total += 1

                # If the line contains */, is in multi-line mode and isn't enclosed in quotation marks, deactivate multi-line mode
                if lineWithoutWhitespace.find("*/") != -1 and block_mode:
                    if lineWithoutWhitespace.find(quote_char) == -1:
                        block_mode = False
                        totalBlockCommentLineCount += 1  # Increment Total # of block line comments
                    elif quote_check_multiple(lineWithoutWhitespace, "*/"):
                        block_mode = False
                        totalBlockCommentLineCount += 1

    # Close file
    fileHandler.close()

    print("Total # of lines: ", count)
    print("Total # of comment lines: ", totalCommentLineCount)
    print("Total # of single line comments: ", singleCommentLineCount)
    print("Total # of comment lines within block comments: ", block_line_total)
    print("Total # of block line comments: ", totalBlockCommentLineCount)
    print("Total # of TODO’s: ", toDoCount)

automate_checks("/Users/chukaezema/PycharmProjects/CapitalOne/test.py")

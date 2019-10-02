# CapitalOne-Technical-Assessment
# This script helps automate checks on when the code is merged into the build pipeline.

#Assumptions: 
- """triple quotes""" is not a multiline comment in python instead its a docstring.
- Program file is written in Python, Java, Javascript or C
- Input come in form of a filepath

# the define automate_checks() function takes in the filepath to the program file as input and returns the following outputs:
# Total # of lines
# Total # of comment lines
# Total # of single line comments
# Total # of comment lines within block comments
# Total # of block line comments
# Total # of TODO’s

# It makes use of two helper functions quote_check() and quote_check_multiple() which takes in the line and target char as input and returns True if target char is not inbetween quotes and takes in the line and target string as input and returns True if target char is not inbetween quotes respectively.

# We begin by opening the file in the default read mode. We the get list of all lines in file and count the number of lines in the program file by getting the length of the list of all lines.
# This approach works well for reasonably sized files so I am assuming the file is of a reasonable size.

# We then check if its a Python, Javascript, C or Java file.
# We iterate through the list of lines and remove all white space from the beginning (left trimming) and perform the necessary checks.

# We then close file to manage resources

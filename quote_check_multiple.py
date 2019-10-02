# Define quote_check_multiple() function takes in the line and target string as input and returns True if target char is not inbetween quotation marks
def quote_check_multiple(line, find):
    quote_char = chr(34)    # Set quote_char to '"'
    index = line.find(quote_char)   # Set index to index of quote_char
    if line.find(quote_char, index + 1) < line.find(find):
        return True # Return True if target char comes before second quotation mark
    return False
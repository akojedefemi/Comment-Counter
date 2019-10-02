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


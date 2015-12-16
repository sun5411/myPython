#/usr/bin/python
# -*- coding: utf-8 -*-

# Deal with the input strings
class Buffer(object):
    def __init__(self,data):
        self.data = data
        self.offset = 0

    # Extract one character where locate with offset
    def peek(self):
        if self.offset >= len(self.data):
            return None
        return self.data[self.offset]

    # Locate move back one after the character extracted
    def advance(self):
        self.offset += 1

# Generate the Token lists
class Token(object):
    def consume(self,buffer):
        pass


# Int type token
class IntToken(Token):
    # Get the strings until the string isn't Int number
    def consume(self,buffer):
        accum = ""
        while True:
            ch = buffer.peek()
            if ch is None or ch not in "0123456789":
                break
            else:
                accum += ch
                buffer.advance()
        # return the int number if read content isn't null, otherwith return None
        if accum != "":
            return ("int",int(accum))
        else:
            return None

# Operation type (+,-)
class OperatorToken(Token):
    def consume(self,buffer):
        ch = buffer.peek()
        if ch is not None and ch in "+-":
            buffer.advance()
            return ("ope",ch)
        return None
# Expression of binary tree node
class Node(object):
    pass

# Int Node
class IntNode(Node):
        def __init__(self,value):
            self.value = value
# operation Node (+ or -)
class BinaryOpNode(Node):
    def __init__(self,kind):
        self.kind = kind
        self.left = None
        self.right = None

# Get the Int number and operator Token from strings
def tokenize(string):
    buffer = Buffer(string)
    tk_int = IntToken()
    tk_op = OperatorToken()
    tokens = []

    while buffer.peek():
        token = None
        for tk in (tk_int,tk_op):
            token = tk.consume(buffer)
            if token:
                tokens.append(token)
                break
        # It indicate input error if no identifiable token
        if not token:
            raise ValueError("Error in syntax")
    return tokens

# Generate the expression binary tree from the Token list
def parse(tokens):
    if tokens[0][0] != 'int':
        raise ValueError("Must start with one int number")
    # Get tokens[0], and it's a int Token
    node = IntNode(tokens[0][1])
    nbo = None
    last = tokens[0][0]
    # Get Tokens from the second Token with for cycle
    for token in tokens[1:]:
        # Will be error if the adjacent 2 same types
        if token[0] == last:
            raise ValueError("Error in syntax")
        last = token[0]
        # If Token is operator, save it as opnode, and save the last int as left node
        if token[0] == 'ope':
            nbo = BinaryOpNode(token[1])
            nbo.left = node
        # If Token is Int,save it as right Node 
        if token[0] == 'int':
            nbo.right = IntNode(token[1])
            node = nbo
    return node

# Calculate the binary tree value, with recursive method
def calculate(nbo):
    #If it's the binary tree with left Node, then calculate the left Node value firstly
    if isinstance(nbo.left,BinaryOpNode):
        leftval = calculate(nbo.left)
    else:
        leftval = nbo.left.value
    # Doing plus or reduce calculate base on the operator Node
    if nbo.kind == '-':
        return leftval - nbo.right.value
    elif nbo.kind == '+':
        return leftval + nbo.right.value
    else:
        return ValueError("Wrong operator")

#Judge If the input is Int
def evaluate(node):
    # Return the value directly if the expression only one Int
    if isinstance(node,IntNode):
        return node.value
    else:
        return calculate(node)

#Main process, input / output
if __name__ == "__main__":
    input = raw_input("Input :")
    # Get the Token list from input strings
    tokens = tokenize(input)
    # Generate the expression tree from Token list
    node = parse(tokens)
    print("Result:"+str(evaluate(node)))

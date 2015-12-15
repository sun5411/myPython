
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

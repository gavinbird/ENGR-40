# audiocom library: Source and sink functions
import common_srcsink as common
import Image
from graphs import *
import binascii
import random



class Source:
    def __init__(self, monotone, filename=None):
        # The initialization procedure of source object
        self.monotone = monotone
        self.fname = filename
        print 'Source: '

    def process(self):
            # Form the databits, from the filename 
            if self.fname is not None:
                if self.fname.endswith('.png') or self.fname.endswith('.PNG'):
                    #A Assume it's an image
                    databits = self.bits_from_image(filename)
                    payload = databits + self.get_header(os.path.getsize(filename)*8, "image")
                else:           
                    # Assume it's text 
                    databits = self.text2bits(filename)   
                    payload = databits + self.get_header(os.path.getsize(filename)*8, "text")                
            else:               
                # Send monotone (the payload is all 1s for 
                # monotone bits)   
                databits = [1]*monotone
                payload = databits + self.get_header(monotone, "monotone")

            return payload, databits

    def text2bits(self, filename):
        # Given a text file, convert to bits
        f = open(filename)
        s = s.read()
        bits = int(s, 2)
        return bits

    def bits_from_image(self, filename):
        # Given an image, convert to bits
        f = Image.open(filename)
        return f.bits

    def get_header(self, payload_length, srctype): 
        # Given the payload length and the type of source 
        # (image, text, monotone), form the header
        header = bin(x)
        if srctype == "image":
            header = "00" + header
        else if srctype = "text":
            header = "01" + header
        else if srctype = "monotone":
            header = "10" + header
        return header

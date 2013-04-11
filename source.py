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
                    databits = self.bits_from_image(self.fname)
                    payload = self.get_header(len(databits), "image") + databits
                else:           
                    # Assume it's text 
                    databits = self.text2bits(self.fname)   

                    payload = self.get_header(len(databits), "text") + databits         
            else:               
                # Send monotone (the payload is all 1s for 
                # monotone bits)
                databits = [1]*self.monotone   
                payload = self.get_header(self.monotone, "monotone") + databits
            print len(payload)
            return numpy.array(payload), numpy.array(databits)

    def text2bits(self, filename):
        # Given a text file, convert to bits
        f = open(filename)
        s = f.read()
        bits = []
        bitstring = bin(reduce(lambda x, y: 256*x+y, (ord(c) for c in s), 0))
        bitstring = bitstring[2:]
        for bit in bitstring:
            bits.append(int(bit))
        return bits

    def bits_from_image(self, filename):
        # Given an image, convert to bits
        im = Image.open(filename)
        pix = im.load()
        bits = []
        for x in range(im.size[0]):
            for y in range(im.size[1]):
                newbits1 = bin(pix[x,y][0])
                newbits1 = newbits1[2:]
                while(len(newbits1) < 8):
                    newbits1 = "0" + newbits1
                newbits2 = bin(pix[x,y][1])
                newbits2 = newbits2[2:]
                while(len(newbits2) < 8):
                    newbits2 = "0" + newbits2
                for bit in newbits1:
                    bits.append(int(bit))
                for bit in newbits2:
                    bits.append(int(bit))
        return bits

    def get_header(self, payload_length, srctype): 
        # Given the payload length and the type of source 
        # (image, text, monotone), form the header
        src = []
        if srctype == "image":
            src.append(0)
            src.append(0)
        elif srctype == "text":
            src.append(0)
            src.append(1)
        elif srctype == "monotone":
            src.append(1)
            src.append(0)
        length = self.convertToBinaryList(payload_length)
        while(len(src) + len(length) < 32): #makes length of header consistent
            src.append(0)
        return src + length

    def convertToBinaryList(self, x):
        if x <= 0: return [0]
        bit = []
        while x:
            bit.append(x % 2)
            x >>= 1
        return bit[::-1]

# audiocom library: Source and sink functions
import common_srcsink
import Image
from graphs import *
import binascii
import random
import StringIO

class Sink:
    def __init__(self):
        # no initialization required for sink 
        print 'Sink:'

    def process(self, recd_bits):
        # Process the recd_bits to form the original transmitted
        # file. 
        # Here recd_bits is the array of bits that was 
        # passed on from the receiver. You can assume, that this 
        # array starts with the header bits (the preamble has 
        # been detected and removed). However, the length of 
        # this array could be arbitrary. Make sure you truncate 
        # it (based on the payload length as mentioned in 
        # header) before converting into a file.
        
        # If its an image, save it as "rcd-image.png"
        # If its a text, just print out the text
        
        dataType, payloadLength = self.read_header(recd_bits[0:32])
        payloadEnd = 32 + payloadLength
        recd_payload = recd_bits[32:payloadEnd]
        if(dataType == "00"):
            self.image_from_bits(recd_payload, "rcd-image.png")
        elif(dataType == "01"):
            print self.bits2text(recd_payload)
        elif(dataType == "10"):
            print "Received monotone"

        # Return the received payload for comparison purposes
        return recd_bits

    def bits2text(self, recd_bits):
        # Convert the received payload to text (string)
        bits = "0b"
        for bit in recd_bits:
            bits += str(bit)
        n = int(bits, 2)
        text = binascii.unhexlify('%x' % n)
        return text

    def image_from_bits(self, bits, filename):
        # Convert the received payload to an image and save it
        # No return value required .
        size = 32, 32
        imageString = "0b"
        for bit in bits:
            imageString += str(bit)
        n = int(imageString, 2)
        imageText = binascii.unhexlify('%x' % n)
        buff = StringIO.StringIO(imageText)
        buff.seek(0)
        im = Image.open(buff)
        im.save(filename)
        pass 

    def read_header(self, header_bits): 
        # Given the header bits, compute the payload length
        # and source type (compatible with get_header on source)
        srctype = str(header_bits[0]) + str(header_bits[1])
        header_bits = header_bits[2:]
        payload_length = ""
        for bit in header_bits:
            payload_length += str(bit) 
        payload_length = int(payload_length, 2)
        print '\tRecd header: ', header_bits
        print '\tLength from header: ', payload_length
        print '\tSource type: ', srctype
        return srctype, payload_length
import numpy
import math
import operator

# Methods common to both the transmitter and receiver.
def hamming(s1,s2):
    # Given two binary vectors s1 and s2 (possibly of different 
    # lengths), first truncate the longer vector (to equalize 
    # the vector lengths) and then find the hamming distance
    # between the two. Also compute the bit error rate  .
    # BER = (# bits in error)/(# total bits )
    hamming_d = 0
    shorter = len(s1)
    len2 = len(s2)
    if len2 < shorter:
    	shorter = len2
    for i in range(shorter):
    	if s2[i] != s1[i]:
    		hamming_d += 1
    ber = hamming_d / shorter
    return hamming_d, ber

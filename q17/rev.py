#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Auth0r : afang
# nice day mua! :P
# desc:

#lambs:
wait = lambda x: raw_input(x)

# imports
import struct 
import ctypes
import gmpy2

const = 0x4E65534532303138 #NeSE2018

binary = open("./barely_reversible", "rb")
content = binary.read()
binary.close()
const_array = []


def showlong(var):

    if var>=0:
        return var
    else:
        return 0x10000000000000000 + var

def tosigned_long(var):

    return ctypes.c_long(var).value

def getint(var):

    offset = (8 + var & 0x3ff) * 4
    return struct.unpack('<i', content[offset:offset+4])[0]

for i in range(0,8):

    #1
    for j in range(0,8):

        const += 1

    #2
    for l in range(0,10):

        for m in range(0,4):

            const += 1

    if i == 7: #not last
        const_array.append(tosigned_long(const))
        break
    t1 = getint(const)
    t2 = getint(const+2)
    t3 = getint(const*2)
    t4 = getint(const*3)
    t5 = getint(const+13)
    const += tosigned_long(t5 ^ (t3 * t4 ^ (t1+t2<<32))) 
    #after each iteration.
    const_array.append(tosigned_long(const))

#for x in const_array:
#
#    print hex(showlong(x))

start_input = [] #input is 8*8

fp = open("./barely_reversible", "rb")
fp.seek(0x1da0)
content2 = fp.read(64)
#start_input = list(content2)
start_input = ['T', 'F', '\x12', '^', '~', 'h', ':', '\x0b', '\x0f', '\x1b', 'A', '~', '>', '\x17', '\x02', '\x08', 'B', 'H', '%', '?', 'D', '\x11', ';', 'd', 'e', '\n', 'F', '\r', ' ', 'A', '\x12', '<', '|', '\r', 'S', '}', '"', 'O', 'F', 'U', ':', 'V', "'", 'O', '#', '}', ']', 'q', "'", '\x1b', '\x14', ',', '\x01', '\x0b', '\x00', '\r', '\x1c', 'Z', '<', 'L', 'a', 'f', '\x19', '\x18']
#round1 
print start_input
temp_var2 = [0] * 8
temp_var  = [0] * 8

#before final solve, we need to solve calc2 first.

def sov_calc2(retval , cval):

    temp1 = tosigned_long(retval + 0xC40BF11DDFCD22E)
    t1 = getint(cval)
    t2 = getint(cval + 2)
    t3 = getint(cval * 2)
    t4 = getint(cval * 3)
    t5 = getint(cval + 13)
    v5 = tosigned_long(t5 ^ (t3 * t4 ^ (t1+t2<<32)))
    temp2 = tosigned_long(v5 * 0x59D39E717F7) & 0xffffffffffffff #large
    t1 = tosigned_long(tosigned_long(temp1 - temp2) % (1<<56)) & 0xffffffffffffff
    t2 = gmpy2.invert(0x35E55F10E61, (1<<56))
    v6 = tosigned_long(t1 * t2) & 0xffffffffffffff 
    cval_high = cval & 0xff00000000000000
    v6 = v6 | cval_high 
    print "v6: " + hex(v6)

    #print hex(showlong(v6))
    #raw_input("show v6")
    xor= 0

    temp1 = v6>>56 & 0xff #head
    temp2 = v6>>48 & 0xff 
    temp3 = v6>>40 & 0xff 
    temp4 = v6>>32 & 0xff 
    temp5 = v6>>24 & 0xff
    temp6 = v6>>16 & 0xff 
    temp7 = v6>>8  & 0xff 
    temp8 = v6 & 0xff
    g1 = temp1 
    g2 = g1 ^ temp2
    g3 = g1 ^ g2 ^ temp3 
    g4 = g1 ^ g2 ^ g3 ^ temp4 
    g5 = g1 ^ g2 ^ g3 ^ g4 ^ temp5 
    g6 = g1 ^ g2 ^ g3 ^ g4 ^ g5 ^temp6 
    g7 = g1 ^ g2 ^ g3 ^ g4 ^ g5 ^ g6 ^ temp7
    g8 = g1 ^ g2 ^ g3 ^ g4 ^ g5 ^ g6 ^ g7 ^ temp8
    xor= g1<<56 | g2 << 48 | g3 << 40 | g4 << 32 | g5 << 24 | g6 << 16 | g7 << 8 | g8
    
    res1 = tosigned_long(tosigned_long(xor) ^ tosigned_long(cval))
    s2 = tosigned_long(res1 + 0xC40BF11DDFCD22E)
    s3 = 0x59D39E717F7 * tosigned_long(cval)
    s4 = (s2 - s3) % (1<<56)
    s5 = gmpy2.invert(0x35E55F10E61, (1<<56))
    s6 = tosigned_long(s4 * tosigned_long(s5)) & 0xffffffffffffff
    return s6
    

#solve temp_var2 first.
t = []
for n in range(0,8):

    for o in range(0,8):

        index = 8*(o^n) + o
        char = ord(start_input[index])
        shift = o*7
        temp_var2[n] = temp_var2[n] | (char<<shift)


conster = const_array[-1] - 4
for l in range(0,10):

    for m in range(0,4):
 
        temp = sov_calc2(temp_var2[2*m+1], temp_var2[2*m])
        print "res1: " + hex(showlong(temp))
        print "conster: " + hex(showlong(conster))
        former = sov_calc2(temp, conster)
        print hex(former)
        temp_var2[2*m+1]= temp_var2[2*m] 
        temp_var2[2*m] = former
        conster += 1
    conster -= 8

#after round! 
conster -= 4

for x in range(0,8):

    print hex(conster)
    temp_var[x] = sov_calc2(temp_var2[x], conster)
    conster += 1

for j in range(0,8):

    start_input[j*8+0] = chr((temp_var[j] & (0x7f<<28)) >> 28)
    start_input[j*8+1] = chr((temp_var[j] & (0x7f<<35)) >> 35)
    start_input[j*8+2] = chr((temp_var[j] & (0x7f<<42)) >> 42)
    start_input[j*8+3] = chr((temp_var[j] & (0x7f<<49)) >> 49)
    start_input[j*8+4] = chr((temp_var[j] & (0x7f)))
    start_input[j*8+5] = chr((temp_var[j] & (0x7f<<7)) >> 7)
    start_input[j*8+6] = chr((temp_var[j] & (0x7f<<14)) >> 14)
    start_input[j*8+7] = chr((temp_var[j] & (0x7f<<21)) >> 21)

print ''.join(start_input)


from binaryfang import *
import struct
import ctypes

our_input = "a" * 8 + "b" * 8 + "c" * 8 + "d" * 8 + "e" * 8 + "f" * 8 + "g" * 8 + "h" * 7 + "\x00"
our_output = list(our_input)
print our_input
temp_var  = [1] * 8
temp_var2 = [1] * 8

conster = 0x4E65534532303138 #NeSE2018

binary = open("./barely_reversible", "rb")
content = binary.read()

def showlong(var):

    if  var >= 0:
        val = var
    else:
        val = 0x10000000000000000 + var 
    return val

def tounsigned_long(var):

    return ctypes.c_ulong(var).value

def tounsigned_short(var):

    return ctypes.c_ushort(var).value

def tosigned_short(var):

    return ctypes.c_short(var).value

def tosigned_long(var):

    return ctypes.c_long(var).value

def tosigned_int(var):

    return ctypes.c_int(var).value

def tosigned_int8(var):

    return ctypes.c_int8(var).value

def tounsigned_int(var):

    return ctypes.c_uint(var).value


def shifting_inner(input_byte4):

    #given the promise each byte is unsigned.
    c1 = tosigned_int8(ord(input_byte4[2]))
    c2 = tosigned_int8(ord(input_byte4[0]))
    c3 = tosigned_int8(ord(input_byte4[1]))
    c4 = tosigned_int8(ord(input_byte4[3]))
    t1 = tosigned_int(c1 << 14)
    t2 = tosigned_int(c2)
    t3 = tosigned_int(c3 << 7)
    t4 = tosigned_int(c4 << 21)
    t5 = (t1 | t2 | t3 | t4)
    return tosigned_long(t5)


def shifting_outer(input_byte8):

    first4 = input_byte8[:4]
    second4= input_byte8[4:]
    v1 = tosigned_long(shifting_inner(first4) << 28)
    v2 = shifting_inner(second4) 
    return tosigned_long(v1 | v2)

def process_1(var1, var2):

    t1 = tosigned_long(0x59D39E717F7 * var2) 
    t2 = tosigned_long(0x35E55F10E61 * var1)
    t3 = tosigned_long(t1 + t2 - 0xC40BF11DDFCD22E) 

    return tosigned_long(t3 & 0xffffffffffffff)

def process_2(var1, var2):

    t1 = tosigned_long(var1)
    t2 = tosigned_long(var2)
    return tosigned_long(t1  ^ t2)

def rdtsc_retaddr_calc(var1):

    par1 = tosigned_short(var1)
    offset = (0x8 + par1 & 0x3ff) * 4
    temp_bytes = content[offset:offset+4]
    return temp_bytes



def calc(var1):
    
    v1 = rdtsc_retaddr_calc(var1) #1
    v1_= struct.unpack('<i' , v1)[0]
    par1 = tounsigned_short(var1)
    temp = rdtsc_retaddr_calc(par1 + 2) #2
    temp_= struct.unpack('<Q', temp + "\x00" * 4)[0]
    v2 = v1_ + temp_ 
    v2_= tosigned_int(v2)
    v2__ = tosigned_long(v2_)
    v2___= v2__ << 32
    v2____ = tosigned_long(v2___)
    v3 = rdtsc_retaddr_calc(par1 * 2)
    v3_= struct.unpack('<i', v3)[0]
    v3__ = tosigned_long(v3_)
    v4 = rdtsc_retaddr_calc(3 * par1)
    v4_= struct.unpack('<i', v4)[0]
    v4_temp = tosigned_long(v4_ * v3__)
    v4__= tosigned_long(v4_temp ^ v2____)
    ret = rdtsc_retaddr_calc(par1 + 13)
    ret_= struct.unpack('<i', ret)[0]
    ret_= ret_ ^ v4__
    return tosigned_long(ret_)
    
    

def rdtsc_calc(var1, const = 0x5f5e100):

    par1 = tounsigned_int(var1)
    return calc(par1) 


def alot_xor(var1):

    par1 = tounsigned_long(var1)
    t1 = (par1 >> 48) ^ (par1 >> 40) ^ (par1 >> 32) ^ (par1 >> 24) ^ par1 ^ (par1 >> 8) ^ (par1 >> 16) ^ (par1 >> 56)
    return tounsigned_long(t1)

def calc2(stack_var1, var, debug = 0):

    #stack_var1 is a 8byte variable,so do var.
    res1 = process_1(stack_var1, var)
    print hex(showlong(res1))
    #if debug == 0:
    #    print "res1: " + hex(res1)
    #    print "calc2_1: " + hex(stack_var1) + " calc2_2: " + hex(var)
    #    raw_input("inside calc2")
    xor  = process_2(res1, var)
    print hex(showlong(xor))
    v5   = rdtsc_calc(var)
    print hex(showlong(v5))
    v6   = tosigned_long(alot_xor(xor))
    print hex(showlong(v6))
    ret  = process_1(v6,v5)
    print hex(showlong(ret))
    return tosigned_long(ret)

def algorithm(our_input):

    global conster
    ccc = 0
    for i in range(0,8):

        if i != 0:
            our_input = ""
            for char in our_output:
                our_input += char
            print len(our_output)
        # counter1 = rdtsc()
        for j in range(0,8):
            
            shift_opnum = our_input[j*8 : j*8 + 8]
            temp_var[j] = (shifting_outer(shift_opnum))
            #debuuuuug






        for k in range(0,8):
        #problem here! 

            temp_var2[k] = (calc2(temp_var[k], conster, debug=i))
            conster += 1

       
        for l in range(0,10):
            
            for m in range(0,4):

                v2 = temp_var2[2 * m + 1]
                print "calc2_1 : "
                print "para1   : "  + hex(showlong(temp_var2[2*m]))
                print "para2   : "  + hex(showlong(conster))
                v3 = calc2(temp_var2[2*m], conster)
                print "result calc2_1 : " + hex(showlong(v3))
                temp_var2[2*m] = v2

                print "calc2_2 : "
                print "para1 : " + hex(showlong(v3))
                print "para2 : " + hex(showlong(v2))
                temp_var2[2*m + 1] = calc2(v3,v2)
                
                print "result calc2_2 : " + hex(showlong(temp_var2[2*m + 1]))
                raw_input('wait')
                conster += 1
        for n in range(0,8):
            
            for ii in range(0,8):

                shifter= 7 * ii
                temper = temp_var2[n] >> shifter 
                reser  = temper & 0x7f
                indexer= 8*(ii^n) + ii 
                our_output[indexer] = chr(reser)

                ccc += 1
                print "input: " + hex(reser) + " at " + str(indexer) + " seq: " + str(ccc)
        temptemp = rdtsc_calc(conster)
        conster += temptemp


algorithm(our_input)

print len(our_output)
print our_output

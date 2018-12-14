from binaryfang import *
import struct
import ctypes

our_input = "a" * 8 + "b" * 8 + "c" * 8 + "d" * 8 + "e" * 8 + "f" * 8 + "g" * 8 + "h" * 7 + "\x00"
print our_input
temp_var  = [1] * 8
temp_var2 = [1] * 8

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

def getint(var1):

    offset = (8 + var1 & 0x3ff) * 4
    temp_bytes = content[offset:offset+4]
    return struct.unpack('<i', temp_bytes)[0]

def calc2(stack_var1, var):

    xor  =  tosigned_long(
            tosigned_long(0x59D39E717F7 * var) + \
            tosigned_long(0x35E55F10E61 * stack_var1) - \
            0xC40BF11DDFCD22E & \
            0xffffffffffffff ^\
            var)
    t1 = getint(var)
    t2 = getint(var + 2)
    t3 = getint(var * 2)
    t4 = getint(var * 3)
    t5 = getint(var + 13)
    v5 = tosigned_long(t5 ^ tosigned_long(t3 * t4 ^ tosigned_long(t1 + t2<<32)))

    v6 = 0
    for i in range(8):
        
        v6 ^= (tounsigned_long(xor)>>(i*8))

    ret  = tosigned_long(0x59D39E717F7 * v5) + \
           tosigned_long(0x35E55F10E61 * v6) - \
           0xC40BF11DDFCD22E & \
           0xffffffffffffff

    return tosigned_long(ret)

def algorithm(our_input):

    const = 0x4E65534532303138 #NeSE2018
    our_output = list(our_input)

    for i in range(0,8):

        for j in range(0,8):
            
            temp_var[j] = tosigned_long( 
            (
             (ord(our_output[j*8+0])       | \
              ord(our_output[j*8+1]) << 7  | \
              ord(our_output[j*8+2]) << 14 | \
              ord(our_output[j*8+3]) << 21)
              << 28) | \
             (ord(our_output[j*8+4])       | \
              ord(our_output[j*8+5]) << 7  | \
              ord(our_output[j*8+6]) << 14 | \
              ord(our_output[j*8+7]) << 21)
            )

        for k in range(0,8):

            temp_var2[k] = (calc2(temp_var[k], const))
            const += 1

        for l in range(0,10):
            
            for m in range(0,4):

                v3 = calc2(temp_var2[2*m], const)
                temp_var2[2*m] = temp_var2[2*m+1]
                temp_var2[2*m + 1] = calc2(calc2(temp_var2[2*m],const),temp_var2[2*m+1])
                const += 1
        for n in range(0,8):
            for o in range(0,8):
                our_output[8*(o^n)+o] = chr(temp_var2[n]>>(o*7)&0x7f)

        t1 = getint(const)
        t2 = getint(const + 2)
        t3 = getint(const * 2)
        t4 = getint(const * 3)
        t5 = getint(const + 13)
        const += tosigned_long(t5 ^ tosigned_long(t3 * t4 ^ tosigned_long(t1 + t2<<32)))
    return our_output

finalize = algorithm(our_input)

#show out
gogo = 0
showout = ""
for char in finalize: 
    gogo += 1
    showout += char 
    if gogo == 8:
        print showout[::-1].encode("hex")
        showout = ""
        gogo = 0


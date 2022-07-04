"""
Name: Wong Cheok Foong
Std ID: 29801028
"""
import sys
import random
import math

def convert_binary(number):
    binary = ""
    while number > 0:
        binary += str(number%2)
        number >>= 1
    binary = binary[::-1] #flip it to make it prepend
    return binary

def modular_exponentiation(integer,power,mod):
    binary_power = convert_binary(power)
    result = 1
    remainder = 0
    
    index = len(binary_power) - 1
    for i in range(len(binary_power)):
        if i == 0:
            remainder = integer % mod
        else:
            remainder = (remainder**2) % mod

        #index-i because it starts from right end
        if binary_power[index-i] == "1":
            result = (result * remainder) % mod

    return result

def miller_rabin(n ,k):
    if n == 2:
        return True
    elif n % 2 == 0:
        return False
    
    s = 0
    t = n-1
    while t % 2 == 0:
        s = s + 1
        t = t//2

    for i in range(k):
        a = random.randint(2,n-1)
        if modular_exponentiation(a,n-1,n) != 1:
            return False
        j = 1
        x = (2**j) * t
        y = (2**(j-1)) * t
        rem1 = modular_exponentiation(a,x,n)
        rem2 = modular_exponentiation(a,y,n)
        for j in range(1, s+1):            
            if rem1 == 1 and (rem2 != 1 and rem2 != n-1):
                return False

            if j != s:
                rem2 = rem1
                rem1 = modular_exponentiation(rem1,2,n)

    return True

def twin_prime(m):
    start = 2**(m-1)
    end = 2**m-1
    output = None
    
    while True:
        n = random.randint(start,end)
        min_k = 64
        prob = 1/math.log(n)
        k= max(min_k, math.ceil(1/prob))
        is_prime = miller_rabin(n,k)

        if is_prime == True:
            a = n - 2
            b = n + 2
            if miller_rabin(a,k) == True:
                if n > a:
                    output = (a,n)
                else:
                    output = (n,a)
                break

            elif miller_rabin(b,k) == True:
                if n > b:
                    output = (b,n)
                else:
                    output = (n,b)
                break
                
    # create txt file for output
    file = open("output_twin_prime.txt", "w")
    file.write(str(output[0]) + "\n")
    file.write(str(output[1]))
    file.close
    return output

#print(miller_rabin(3,64))
#print(twin_prime(20))

if __name__ == "__main__":

    argument_00 =sys.argv[0]

    argument_01 = sys.argv[1]

    twin_prime(argument_01)

import sympy
import eulerlib
import math
import random
from sympy.abc import x



    
def millerRabin(n, maxRuns):

    iterations = 0
    while iterations < maxRuns:
        a = random.randint(1, n -1)
        s = 0
        val = n - 1
        while val % 2 != 0:
            s = s + 1
            val = val / 2
        
        if (mrCheckComposite(a, val, n, s)):
            return False
        
        iterations = iterations + 1

    return True


def mrCheckComposite(a, d, n, s):
    if pow(a, d) % n == 1:
        return False

    for r in range(0, s):
        if (pow(a, pow(2, r) * d) % n == -1 ):
            return False

    return True



def testPrime(n, maxRuns = 7):

    if millerRabin(n, maxRuns) == False:
        #print('Miller-rabin round composite')
        return False
    
    print('Miller-rabin found', n, 'as probably prime with probability', 
          "{0:.5f}".format(1 - pow(.25, maxRuns)))

    ####################################################################
    ##### comment out this return statement to continue running AKS ####
    ####################################################################
    return True

    print('Miller-rabin found', n, 'as probably prime, verifying with AKS')

    if type(n) is not int:
        # throw exception
        return;

    # test perfrect power
    if (checkPerfectPower(n)):
        #print('perfect power')
        return False;
    
    r = calculateR(n)

    if checkStep3(r, n):
        #print('step 3')
        return False
    
    if (n <= r):
        #print('n smaller than r = ', r)
        return True

    
    target = math.floor(math.sqrt(eulerlib.Divisors().phi(r)) * 
                        math.log(n, 2))

    a = 2
    while (a <= target):
        if (not checkPolyRemainder(a, n, r)):
            #print('check poly')
            return False

        a = a + 1

    #print('end')
    return True

#sympy.abc.
def checkPolyRemainder(a, n, r):
    val1 = sympy.rem( (x + a)**n, x**r - 1, modulus=n)
    val2 = sympy.rem( (x**n + a), x**r - 1, modulus=n)
    if (val1 != val2):
        return False
        
    return True


def checkStep3(r, n):
    a = 2
    while a <= min(r, n-1):
        if (n%a == 0):
            return True
        a = a + 1

    return False



def GCD(a, b):
    result = eulerlib.numtheory.gcd(a,b)
    return result

def calculateR(n):
    r = 1;
    multOrd = 0
    target = math.pow (math.log(n, 2) , 2)

    while(multOrd <= target):
        r = r + 1
        while GCD(r, n) != 1:
            r = r + 1
        #print("calling getMult with",r)
        multOrd = getMult(r, n)

    return r
    

def getMult(r, n):

    k = 1
    while (True):
        #print("k = ", k)
        result = pow(n, k) % r
        #print("result = ", result, "r = ", r)

        if  result == 1:
            return k
        k = k + 1



def checkPerfectPower(n):
    result = 0;
    sqrtN = math.sqrt(n)
    a = 2
    b = 2

    while (a < sqrtN):
        while (result < n):
            result = math.pow(a, b)
            if result == n:
                return True
            b = b + 1
        a = a + 1
        b = 2

    return False
    

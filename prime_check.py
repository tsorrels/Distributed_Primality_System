import prime_test

def main():

    primes = [23, 24, 25, 29, 31, 37, 41, 43, 228, 229, 231,233, 349, 541, 1009]

    
    # test getMultiplicitiveOrder
    prime_test.getMult(7,4) 
    prime_test.getMult(3,4) 
    #print("Checkin prime_test.calcualteR")
    #print("GCD of 2 and 4 ",  prime_test.GCD(2, 4))
    prime_test.calculateR(4)



    for prime in primes:
        if (prime_test.testPrime(prime)):
            print(prime, "is prime")
        else:
            print(prime, "is not prime")
            

if __name__ == "__main__":
    main()

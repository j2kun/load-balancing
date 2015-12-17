import math
import random


def decompose(n):
   exponentOfTwo = 0
 
   while n % 2 == 0:
      n = int(n / 2)
      exponentOfTwo += 1
 
   return exponentOfTwo, n
 
def isWitness(possibleWitness, p, exponent, remainder):
   possibleWitness = pow(possibleWitness, remainder, p)
 
   if possibleWitness == 1 or possibleWitness == p - 1:
      return False
 
   for _ in range(exponent):
      possibleWitness = pow(possibleWitness, 2, p)
 
      if possibleWitness == p - 1:
         return False
 
   return True
 
def probablyPrime(p, accuracy=1000):
   if p == 2 or p == 3: return True
   if p < 2: return False
 
   numTries = 0
   exponent, remainder = decompose(p - 1)
 
   for _ in range(accuracy):
      possibleWitness = random.randint(2, p - 2)
      if isWitness(possibleWitness, p, exponent, remainder):
         return False
 
   return True

def randomPrime(pMin, pMax):
   numBits = int(math.ceil(math.log2(pMax)))
   p = 1
   while not (pMin < p < pMax) or not probablyPrime(p):
      p = random.getrandbits(numBits)

   return p


class UniversalHashFamily(object):
   def __init__(self, universeSize, primeBounds=None):
      self.universeSize = universeSize
   
      if primeBounds is not None:
         pMin, pMax = primeBounds
         if pMin > pMax:
            raise Exception("Empty prime bounds")
         if pMax < 2*pMin:
            print("Warning, there might not exist any primes in the given range %r" % ((pMin, pMax)))

         self.p = randomPrime(pMin, pMax)
      else:
         self.p = randomPrime(1<<32, 1<<33) # a 32 bit prime.

   def draw(self):
      a = random.randint(1, self.p-1)
      b = random.randint(0, self.p-1)

      return lambda x: ((a*x + b) % self.p) % self.m

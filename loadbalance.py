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
   def __init__(self, numBins, primeBounds=None):
      self.numBins = numBins
   
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

      return lambda x: ((a*x + b) % self.p) % self.numBins


class ChoiceHashFamily(object):
   def __init__(self, hashFamily, queryBinSize, numChoices=2):
      self.queryBinSize = queryBinSize
      self.hashFamily = hashFamily
      self.numChoices = numChoices
   
   def draw(self):
      hashes = [self.hashFamily.draw() for _ in range(self.numChoices)]
      
      def h(x):
         indices = [h(x) for h in hashes]
         counts = [self.queryBinSize(i) for i in indices]
         count, index = min([(c, i) for (c, i) in zip(counts, indices)])
         return index

      return h


if __name__ == "__main__":
   # test the load balancer
   m = 100000
   n = 100

   H = UniversalHashFamily(numBins=n, primeBounds=[n, 2*n])
   
   results = []
   for simulation in range(100):
      bins = [0] * n
      h = H.draw()
      for i in range(m):
         bins[h(i)] += 1
      results.append(max(bins))

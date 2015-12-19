from loadbalance import *


def testInputs(n, m, inputs, hashFunction=None):
   if hashFunction is None:
      H = UniversalHashFamily(numBins=n, primeBounds=[n, 2*n])
      hashFunction = H.draw()
   
   bins = [0] * n
   for i in inputs:
      bins[hashFunction(i)] += 1

   return bins


def simulateMany(n, m, numTrials=100):
   results = [0] * numTrials

   for i in range(numTrials):
      bins = testInputs(n, m, range(m))

   results.append(max(bins))

   return results


def getBadInputs():
   m = 100000
   n = 100

   H = UniversalHashFamily(numBins=n, primeBounds=[n, 2*n])
   h = H.draw()
   badInputs = [i for i in range(m) if h(i) == 9]

   return badInputs


def test2Choices(inputs):
   m = 100000
   n = 100
   numTrials = 100

   print("expected value is %r" % (1+(m-1)/n,))

   results = []

   for _ in range(numTrials):
      bins = [0] * n
      binSize = lambda i: bins[i]

      G = UniversalHashFamily(numBins=n, primeBounds=[n, 2*n])
      H = ChoiceHashFamily(G, binSize, numChoices=2)
      h = H.draw()

      for i in inputs:
         bins[h(i)] += 1
      
      results.append(max(bins))

   return bins, results



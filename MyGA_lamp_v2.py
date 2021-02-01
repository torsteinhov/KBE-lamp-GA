import random
import math

class MyGA_lamp:

    def __init__(self, popsize, generations, mutProb, point, legLength):
        self.popsize = popsize 
        self.generations = generations
        self.mutProb = mutProb
        self.point = point
        self.winner = []

        self.data = []
        for i in range(0, self.popsize):
            lamp = []

            topLength = random.randint(legLength, legLength+100)
            lamp.append(topLength)

            point_1 = [0,0,topLength]
            point_2 = [random.randint(-100,100), random.randint(-100,100), random.randint(0, topLength)]

            lamp.append(point_1)
            lamp.append(point_2)

            self.data.append(lamp)
        self.currGeneration = self.data

    #generates vector based on point2-point1 for each axis
    def generateVector(self, x, y):
        v = []
        for i in range(len(x)):
            v.append(y[i] - x[i])
        return v

    #makes it a unit vector
    def normalize(self, x):
        normalizedVector = [x[i] / self.norm(x) for i in range(len(x))]
        return normalizedVector

    #takes two coordinate vectors and returns a number
    def dotProduct(self, x, y):
        product = sum([x[i] * y[i] for i in range(len(x))])
        return product

    #gives the ordinary length
    def norm(self, x):
        var = math.sqrt(self.dotProduct(x, x))
        return var

    #calculates the angle between vector1 and vector2
    def angle(self,vector1,vector2):
        angle = math.acos(self.dotProduct(vector1,vector2) / (self.norm(vector1) * self.norm(vector2)))
        return angle

    def crossover(self, parentX, parentY):
        # Define crossover "masks" - it is problem specific, depends on the string length.
        # Select feasbile "paths" for crossover - having common point(s) on the path

        mask_head = random.randint(30,40)
        mask_tail = 3
        childX = []
        childY = []
        
        #appends the leg height to each of the children
        childX.append(parentX[0])
        childY.append(parentY[0])

        #initiates the origin points for the children
        childX_point = []
        childY_point = []

        childX_point.append((parentX[2][1]))
        childY_point.append((parentY[2][1]))

        #conducts the crossover, makes a hybrid between the two parents
        for i in range(2):
            childX_point.append((parentX[2][i] & mask_head) + (parentY[2][i] & mask_tail))
            childY_point.append((parentY[2][i] & mask_head) + (parentX[2][i] & mask_tail))

        #adds the points to the children
        childX.append(parentX[1])
        childY.append(parentY[1])
        childX.append(childX_point)
        childY.append(childY_point)

        #print("Child 1: ", childX, "Child 2: " , childY)

        #initiates a table with all the fitnessvalues for each element
        fitnessTable = [self.fitness(parentX), self.fitness(parentY), self.fitness(childX), self.fitness(childY)]

        #sort the fitnesstable in ascending order, where lower score equals better fitness
        fitnessTable.sort()

        crossoverFinished = []

        #iterates through the fitnesstable to chech if it correlates with the fitness to any of the elements, if so => add to the result
        for i in range(2):
            if fitnessTable[i] == self.fitness(parentX):
                crossoverFinished.append(parentX)
                continue
            elif fitnessTable[i] == self.fitness(parentY):
                crossoverFinished.append(parentY)
                continue
            elif fitnessTable[i] == self.fitness(childX):
                crossoverFinished.append(childX)
                continue
            elif fitnessTable[i] == self.fitness(childY):
                crossoverFinished.append(childY)
                continue

        #returns the two elements with best fitness out of parent1, parent2, child1 and child2 after the crossover is finished.
        print("crossover: ", crossoverFinished[0], crossoverFinished[1])
        return crossoverFinished[0], crossoverFinished[1]

    def fitness(self, individual):
        #generates vector between hood and the goal
        vectorXY = self.generateVector(self.point, individual[1])
        #makes it a unit vector
        vXY = self.normalize(vectorXY)

        #generates vector between current point and the goal
        vectorHood = self.generateVector(individual[2], individual[1])
        #makes it a unit vector
        vHood = self.normalize(vectorHood)

        score = math.degrees(self.angle(vXY, vHood))
        return score

    def selection(self, currGeneration, fitnessResults):
        # Makes a mating pool where individuals with good fitness is given a higher chance to be picked
        # Select feasible parents for crossover.
        mating_pool = []
        
        for i in range(len(fitnessResults)):

            if fitnessResults[i] < 5:
                for j in range(21):
                    #print("a")
                    mating_pool.append(currGeneration[i])
            elif (10 > fitnessResults[i] and fitnessResults[i] >= 5):
                for j in range(11):
                    #print("b")
                    mating_pool.append(currGeneration[i])
            elif (30 > fitnessResults[i] and fitnessResults[i] >= 10):
                for j in range(6):
                    #print("c")
                    mating_pool.append(currGeneration[i])
            else:
                mating_pool.append(currGeneration[i])
        
        theBest = fitnessResults.index(min(fitnessResults))

        chosen1 = random.randint(0,len(mating_pool))
        chosen2 = random.randint(0,len(mating_pool))
        chosen3 = random.randint(0,len(mating_pool))

        chosen = []
        print("Best: ", self.fitness(currGeneration[theBest]))
        
        # picks out individuals if the mating pool is very small
        if len(mating_pool) < 4:
            return (mating_pool[0], mating_pool[1])

        #checks if the random numbers generated are alike
        if chosen1 != chosen2:
            #print("Selection: ", [mating_pool[chosen1], mating_pool[chosen3]])
            #adds the best couples to the chosens, with a random where a good one is more likely to be picked
            chosen.append((mating_pool[chosen1], mating_pool[chosen2]))
            chosen.append((currGeneration[theBest], mating_pool[chosen1]))
            chosen.append((currGeneration[theBest], mating_pool[chosen2]))
        else:
            #adds the best couples to the chosens, with a random where a good one is more likely to be picked
            chosen.append((mating_pool[chosen1], mating_pool[chosen3]))
            chosen.append((currGeneration[theBest], mating_pool[chosen1]))
            chosen.append((currGeneration[theBest], mating_pool[chosen3]))
            
        print(chosen)
        return chosen
    # Mutation function example
    # mutProb is given as an integer representing a percent (%)
    def mutate(self, population, mutProb):
        
        #iterates through the whole population and gives each element in the individual a mutProb(%) chance
        #to be replaced with a new random int between -100 and 100, this is also customizable
        for i in population:
            var = random.randint(0,mutProb*100)
            x_or_y = random.randint(0,1)
            if var == 1:
                i[2][x_or_y] = random.randint(-100,100)

        return

    def run(self):
        # Execute the algorithm
        nextGeneration = self.data  # To populate as the next generation, in the beginning is set to data
        fitnessResults = []  # An empty array to store fitness results.
        # Iterating via the # of generations defined.
        for i in range(1, self.generations):
            currGeneration = nextGeneration.copy()  # Important to copy to create a new instance of the array object
            nextGeneration.clear()
            # Fitness evaluation for the current generation
            for individual in currGeneration:
                fitnessResults.append(self.fitness(individual))
            # Select the fittest parents for crossover
            selected = self.selection(currGeneration, fitnessResults)

            nextGeneration = []

            # Make the crossover
            for select in selected:
                child1, child2 = self.crossover(select[0], select[1])  # Taking two selected parents to generate two children
                if child1 not in nextGeneration:
                    nextGeneration.append(child1)
                if child2 not in nextGeneration:
                    nextGeneration.append(child2)
            
            print("NG: ", nextGeneration)
            
            # Mutation check before next iteration
            self.mutate(nextGeneration, self.mutProb)
            
            # Clearing fitnessResults
            fitnessResults.clear()

            if len(nextGeneration) == 1:
                break

        print("nextGeneration: ", nextGeneration)
        
        #adds the fitnessresults for each individual in the nextGeneration
        for individual in nextGeneration:
            fitnessResults.append(self.fitness(individual))
        #print(fitnessResults)
        self.winner = nextGeneration[fitnessResults.index(min(fitnessResults))]
        #return [self.nextGeneration[0][0], self.normalize(self.generateVector(self.nextGeneration[0][1], self.nextGeneration[0][2]))]
        #print(self.fitness(nextGeneration[0]))
        return self.winner
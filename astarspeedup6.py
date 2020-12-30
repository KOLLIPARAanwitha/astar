import sys; args = sys.argv[1:]
# Anwitha Kollipara, Period 4
import time;

startTime = time.time()

def getDimensions(puzzle):
    myVal = len(puzzle)
    if myVal ** 0.5 == int(myVal ** 0.5): return (int(myVal ** 0.5), int(myVal ** 0.5))
    possibilities = set()
    for i in range(0, myVal):
        for j in range(0, myVal):
            if i * j == myVal:
                possibilities.add((i, j))
    lowestDiff = myVal
    optimalDim = ()
    for p in possibilities:
        if abs(p[0] - p[1]) < lowestDiff:
            lowestDiff = abs(p[0] - p[1])
            optimalDim = (p[0], p[1])
    return (optimalDim)


def manhattan(puzzle, goal, gWIDTH):
    sum = 0
    for i in puzzle:
        if i == '_':
            continue
        sum += abs(puzzle.index(i) % gWIDTH - goal.index(i) % gWIDTH)
        sum += abs(puzzle.index(i) // gWIDTH - goal.index(i) // gWIDTH)
    return sum

def solve(puzzle, goal, width):
    if puzzle==goal: return 0
    if isImpossible(puzzle, goal, gWIDTH, gHEIGHT): return -1
    md = manhattan(puzzle, goal, width)
    bucketDict, closedSet = {}, {}
    bucketDict[md]=[(md, 0, puzzle, puzzle.find('_'), -1)]
    whichBucketKey, whichItemInBucket = md, 0
    while whichBucketKey<md**2+1:
        if whichItemInBucket>=len(bucketDict[whichBucketKey]):
            whichItemInBucket=0
            whichBucketKey+=1
            while whichBucketKey not in bucketDict: whichBucketKey+=1
        pzlTuple = bucketDict[whichBucketKey][whichItemInBucket]
        whichItemInBucket+=1
        pzl, level, uPosition, gpuPosition, f = pzlTuple[2], pzlTuple[1], pzlTuple[3], pzlTuple[4], pzlTuple[0]

        if pzl in closedSet: continue
        closedSet[pzl]=level
        priorPosition = uPosition
        p = [*pzl]

        for nextPosition in lookupTable[uPosition]:
            if nextPosition == gpuPosition: continue
            # letter = p[nextPosition]
            # goalUPosition, pzlUPosition = goal.index(letter), pzl.index(letter)
            p[priorPosition], p[uPosition], p[nextPosition], priorPosition = \
                p[uPosition], p[nextPosition], p[priorPosition], nextPosition
            neighbor = ''.join(p)
            letter = neighbor[uPosition]
            if neighbor == goal: return level+1
            if neighbor in closedSet: continue
            goalUPosition, pzlUPosition = goal.index(letter), pzl.index(letter)
            neighborUPosition = neighbor.index(letter)
            neighDist = abs(neighborUPosition % gWIDTH - goalUPosition % gWIDTH)+ abs(neighborUPosition // gWIDTH - goalUPosition // gWIDTH)
            pzlDist = abs(pzlUPosition % gWIDTH - goalUPosition % gWIDTH)+ abs(pzlUPosition // gWIDTH - goalUPosition // gWIDTH)
            if neighDist>pzlDist: newEstimate = level + 1 + f - level + 1
            else: newEstimate = level + 1 + f - level - 1
            if newEstimate in bucketDict: bucketDict[newEstimate].append((newEstimate, level+1, neighbor, nextPosition, uPosition))
            else: bucketDict[newEstimate]=[(newEstimate, level+1, neighbor, nextPosition, uPosition)]
    return -1

def isImpossible(puzzle, goalstate, gWIDTH, gHEIGHT):
    inversionCount = sum(
        puzzle.find(c) > puzzle.find(d) for i, c in enumerate(goalstate) for d in goalstate[i + 1:] if {'_'} - {c, d})
    if gWIDTH % 2:
        return inversionCount % 2
    return (inversionCount + puzzle.find('_') // gWIDTH + goalstate.find('_') // gWIDTH) % 2


lstPzls = open(args[0], 'r').read().replace('.', '_').replace('0', '_').splitlines()
goalstate = lstPzls[0]
dim = getDimensions(goalstate)
gWIDTH, gHEIGHT = dim[0], dim[1]
# currPuzzle = "BECDIAFG_JKHMNOL"
# lookupTable = [
#        ({u + gWIDTH, u - gWIDTH, u - (u % gWIDTH > 0), u + ((u + 1) % gWIDTH > 0)} & {*range(len(currPuzzle))}) - {u}
#        for u in range(len(currPuzzle))]
#
# print(solve(currPuzzle, "ABCDEFGHIJKLMNO_", 4))

for currPuzzle in lstPzls:
    startT = time.time()
    lookupTable = [
        ({u + gWIDTH, u - gWIDTH, u - (u % gWIDTH > 0), u + ((u + 1) % gWIDTH > 0)} & {*range(len(currPuzzle))}) - {u}
        for u in range(len(currPuzzle))]
    print(lookupTable)
    print(f'{currPuzzle} solved in {solve(currPuzzle, goalstate, gWIDTH)} steps in {time.time() - startT} seconds')

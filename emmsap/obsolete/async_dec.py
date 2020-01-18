import multiprocessing
from functools import wraps
from itertools import repeat
try:
    from itertools import izip
except ImportError:  # Python 3 built-in zip already returns iterable
    izip = zip
from math import ceil

def _func_star_many(func_items_args):
    """Equivalent to:
       func = func_item_args[0]
       items = func_item_args[1]
       args = func_item_args[2:]
       return func(items[0],items[1],...,args[0],args[1],...)
    """
    return func_items_args[0](*list(func_items_args[1]) + func_items_args[2])

def _func_star_single(func_item_args):
    """Equivalent to:
       func = func_item_args[0]
       item = func_item_args[1]
       args = func_item_args[2:]
       return func(item,args[0],args[1],...)
    """
    return func_item_args[0](*[func_item_args[1]] + func_item_args[2])


def runFuncAsync(func, iterableFull, *args, **kwargs):
    leaveOut = 1
    chunksize = kwargs.get("chunksize", 1)

    poolSize = multiprocessing.cpu_count() # @UndefinedVariable
    if poolSize > 2:
        poolSize = poolSize - leaveOut
#    res = pool.imap(func, tupleArgs)
    timeouts = 0
    eventsProcessed = 0
    summaryOutput = []
    maxTimeout = 99999


    iterationSize = kwargs.get('iterationsize', poolSize * 2)
    iterationChunkNum = int(ceil(len(iterableFull) / float(iterationSize)))

    for itchunkNum in range(iterationChunkNum):
        continueIt = True
        itchunkStart = iterationSize * itchunkNum
        itchunkEnd = itchunkStart + iterationSize
        if (itchunkEnd > len(iterableFull)):
            itchunkEnd = len(iterableFull)
        iterable = iterableFull[itchunkStart:itchunkEnd]
        print(iterable, itchunkStart, itchunkEnd)
        pool = multiprocessing.Pool(processes=poolSize) # @UndefinedVariable
        izipOutput = izip(repeat(func), iterable, repeat(list(args)))
        #for z in izipOutput:
        #    print(z)
        res = pool.imap(_func_star_many, izipOutput,
                          chunksize)

        while continueIt is True:
            try:
                newResult = res.next(timeout=1)
                if timeouts >= 5:
                    print("")
                timeouts = 0
                eventsProcessed += 1
                summaryOutput.append(newResult)
            except multiprocessing.TimeoutError: # @UndefinedVariable
                timeouts += 1
                if timeouts == 5 and eventsProcessed > 0:
                    pass
                elif timeouts == 5:
                    pass
                if timeouts % 5 == 0:
                    print(str(timeouts) + " ", end="")
                if timeouts > maxTimeout and eventsProcessed > 0:
                    print("\nToo many delays, giving up...")
                    continueIt = False
                    pool.close()
                    exit()
            except StopIteration:
                continueIt = False
                pool.close()
                pool.join()
            except Exception as excp:
                eventsProcessed += 1
                summaryOutput.append(excp)
    return summaryOutput


def mockWrapDec(func):
    @wraps(func)
    def callMock(argTuple):
        return func(*argTuple)
    return callMock

def testMock(i, j):
    from time import sleep
    from random import randint
    print("starting")
    sleep(randint(1, 3))
    print("waking from sleep")
    return (i, j, randint(1, 200))

if __name__ == '__main__':
    #from music21.ext.parmap import starmap
    argList = []
    for i in range(10):
        t = (i, "hi")
        argList.append(t)
    x = runFuncAsync(testMock, argList)
    print("xxxxxxxxxxxxxxxxx")
    print(x)

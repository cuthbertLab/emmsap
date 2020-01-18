# -*- coding: utf-8 -*-
'''
Make a subset of the EMMSAP files to give to Dmitri T.
'''
from emmsap import files
import random
import shutil


def main():
    outDirectory = '/Users/Cuthbert/Desktop/dtOut'
    allFiles = files.allFiles()
    sampleFiles = random.sample(allFiles, 400)
    outSample = []
    for f in sampleFiles:
        if 'Fallows' not in f:
            outSample.append(f)
    outSample.sort()
    for f in outSample:
        inFile = files.emmsapDir + '/' + f
        outFile = outDirectory + '/' + f
        print(inFile, '->', outFile)
        shutil.copy2(inFile, outFile)


if __name__ == '__main__':
    main()

from emmsap import files

def main(numMeasures, skew=5, allowDouble=True, allowHalf=True):
    for f in files.FileIterator():
        p = f.parts[0]
        countM = len(p.getElementsByClass('Measure'))
        if numMeasures - skew < countM < numMeasures + skew:
            print(f.filePath, countM)
        if allowDouble:
            if (numMeasures - skew) * 2 < countM < (numMeasures + skew) * 2:
                print(f.filePath, countM, '**Double')
        if allowHalf:
            if (numMeasures - skew) / 2 < countM < (numMeasures + skew) / 2:
                print(f.filePath, countM, '**Half')


if __name__ == '__main__':
    main(220)

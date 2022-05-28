from pprint import pprint
from emmsap import mysqlEM
import itertools
import pickle

class TransProb:
    def __init__(self):
        self.db = mysqlEM.EMMSAPMysql()
        self.twoGrams = []
    
    def one(self, intervalList):
        if intervalList[0] > 1:
            qBase = '[0-9]'
        else:
            qBase = ''

        qSuffix = ''.join([str(i) for i in intervalList])
        q = qBase + qSuffix
        queryFull = f'''SELECT count(DISTINCT(fn)) FROM intervals 
                    WHERE intervalsNoUnisons LIKE "%{qSuffix}%"'''
        if qBase:
            queryFull += f'AND intervalsNoUnisons REGEXP "{q}"'
            
        self.db.cursor.execute(queryFull)
        return list(self.db.cursor)[0][0]
        
    def twoGramGenerate(self):
        self.twoGrams = []
        for i in range(-9, 10):
            if i in (-1, 0, 1):
                continue         
            thisRow = []
            for j in range(-9, 10):
                if j in (-1, 0, 1):
                    continue         
                thisRow.append(self.one([i, j]))
            self.twoGrams.append(thisRow)
        return self.twoGrams

    def nGramGenerate(self, n=3):
        try: 
            with open('transitionGram' + str(n - 1) + '.p', 'rb') as fh:
                d = pickle.load(fh)
        except Exception as e:
            print(e)
            d = {}
            
        possibilities = (-9, -8, -7, -6, -5, -4, -3, -2,
                         2, 3, 4, 5, 6, 7, 8, 9)
        for index, tup in enumerate(itertools.product(possibilities, repeat=n)):
            if n > 1 and d[tup[:-1]] == 0:
                d[tup] = 0
            else:
                d[tup] = self.one(tup)

            if index % 100 == 0:
                print(index, tup, d[tup])
                    
        with open('transitionGram' + str(n) + '.p', 'wb') as fh:
            pickle.dump(d, fh)

        return d
        
if __name__ == '__main__':
    with open('transitionGram4.p', 'rb') as fh:
        d = pickle.load(fh)
    
    for k, v in d.items():
        #if v == 1:
        #    print(str(k) + ' ++ ')
        if len(k) > 3 and v > 200:
            print(str(k) + ' -- ' + str(v))
    
#     tp = TransProb()
#     x = tp.nGramGenerate(4)
#     pprint(x)
#     
#     
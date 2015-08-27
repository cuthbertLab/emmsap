#from Levenshtein import ratio as lvRatio
from Levenshtein import distance

st1 = 'hello my friend'
st2 = 'goodbye friends'
st3 = 'hello my doggie'

print(distance(st1, st2))
print(distance(st2, st3))
print(distance(st1, st3))

for i in range(len(st1)):
    print(i, distance(st1[0:i], st2[0:i]) + distance(st1[i:], st2[i:]), end='')
    print(distance(st1[0:i], st3[0:i]) + distance(st1[i:], st3[i:]))
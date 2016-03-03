x=['a','b','c','d','e','f']
primeros=[]
segundos=[]
final=[]
for i in range(len(x)):
    if i%2 is not 0:
        primeros.append(x[i])
    else:
        segundos.append(x[i])
final.append(primeros)
final.append(segundos)


print(primeros)
print(segundos)

print(final)

        
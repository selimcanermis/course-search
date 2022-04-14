a = 5
b = 5.5
c = "&5,55"

print(a)
print(b)
print(c)


print(type(a))
print(type(b))
print(type(c))

c = c[1:]
c = c.replace(',','.')
print(c)
print(type(c))

list = [0,1,2,3,4,5,6,7,8,9]
print(list[:-1])
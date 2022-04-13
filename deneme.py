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
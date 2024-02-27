def listToString(list):
    str1 = ""
    return (str1.join(list))
print(list("123456789ABCDEF "))
print(listToString(list("123456789ABCDEF ")))
print(list(listToString(list("123456789ABCDEF "))))
print(listToString(list("123456789ABCDEF ")))

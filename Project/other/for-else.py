li = [ i for i in range(10)]
li[5]={"hi":"lol"}
cmp = {"hi":"lol"}
for i in li:
    if i == cmp:
        print("find")
        break
else:
    print("Not found")

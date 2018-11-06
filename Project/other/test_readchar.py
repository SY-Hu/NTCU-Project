import readchar

print("Start test readchar.")
for i in range(100):
    key = readchar.readkey()
    print(key)
    
    if key == 'q' or key == 'Q':
        break

print("Readchar test end. ")

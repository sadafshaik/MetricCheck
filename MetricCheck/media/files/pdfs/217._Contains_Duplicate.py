def duplicates(A):
    return len(set(A)) != len(A)


A = [1,2,2,3,4]
print(duplicates(A))

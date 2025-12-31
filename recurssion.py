def recurssion(n):
    if n <= 1:
        return n
    else:
        return recurssion(n - 1) + recurssion(n - 2)
print(recurssion(3))
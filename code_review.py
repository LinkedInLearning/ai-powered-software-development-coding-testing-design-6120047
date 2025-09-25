# Example 1
def calc(x,y,o):
    if o == "+":
        return x+y
    if o == "-":
        return x-y
    if o == "*":
        return x*y
    if o == "/":
        return x/y
print(calc(10,5,"+"))
print(calc(10,5,"/"))


# Example 2
numbers = [1,2,3,4,5]
squares = []
for i in range(len(numbers)):
    squares.append(numbers[i]**2)
print(squares)
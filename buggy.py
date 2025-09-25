# Example 1
def add_item(item, container=[]):
    container.append(item)
    return container

print(add_item("apple"))
print(add_item("banana"))


# Example 2
a = 0.1 + 0.2
if a == 0.3:
    print("Equal")
else:
    print("Not equal")
# Example 1
def add_item(item, container=None):
    if container is None:
        container = []
    container.append(item)
    return container

print(add_item("apple")) # ["apple"]
print(add_item("banana")) # ["banana"]


# Example 2
import math

a = 0.1 + 0.2
if math.isclose(a, 0.3):
    print("Equal")
else:
    print("Not equal")
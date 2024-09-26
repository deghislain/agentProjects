from typing import TypeAlias

Vector: TypeAlias = list[str]

def process_vector(vector: Vector) -> None:
    if type(vector) == Vector:
        print("The object is a list")
    for item in vector:
        print(item)

# Valid usage
my_vector = '["apple", "banana", "cherry"]'
process_vector(my_vector)

